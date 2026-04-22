"""
Performance reporting for Cannibisters Google Ads.

Produces a plain-text report covering the full membership conversion funnel:
  Impressions → Clicks → Sign-ups (conversions) → Cost per sign-up

Metrics reported at campaign, ad group, keyword, and ad level.
"""

from datetime import datetime
from typing import Optional
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

from .config import CUSTOMER_ID, MICROS_PER_ZAR
from .auth import clean_customer_id, handle_google_ads_exception


def _search(client, customer_id, query):
    ga = client.get_service("GoogleAdsService")
    try:
        resp = ga.search_stream(customer_id=customer_id, query=query)
        for batch in resp:
            yield from batch.results
    except GoogleAdsException as ex:
        handle_google_ads_exception(ex)


def _pct(numerator, denominator) -> str:
    if not denominator:
        return "N/A"
    return f"{numerator / denominator * 100:.1f}%"


def _zar(micros) -> str:
    return f"R{micros / MICROS_PER_ZAR:.2f}"


def report_campaigns(client: GoogleAdsClient, customer_id: str, date_range: str):
    print(f"\n{'='*70}")
    print(f"CAMPAIGNS — {date_range}")
    print(f"{'='*70}")

    query = f"""
        SELECT
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type,
            metrics.impressions,
            metrics.clicks,
            metrics.ctr,
            metrics.average_cpc,
            metrics.cost_micros,
            metrics.conversions,
            metrics.cost_per_conversion,
            metrics.search_impression_share
        FROM campaign
        WHERE campaign.status != 'REMOVED'
            AND segments.date DURING {date_range}
        ORDER BY metrics.cost_micros DESC
    """

    total_spend = 0
    total_conversions = 0

    print(f"\n  {'Campaign':<40} {'Status':<8} {'Impr':>8} {'Clicks':>7} "
          f"{'CTR':>6} {'Spend':>8} {'Conv':>5} {'CPA':>8}")
    print("  " + "-" * 100)

    for row in _search(client, customer_id, query):
        m = row.metrics
        c = row.campaign
        spend = m.cost_micros / MICROS_PER_ZAR
        cpa = (m.cost_per_conversion / MICROS_PER_ZAR) if m.conversions > 0 else 0
        total_spend += spend
        total_conversions += m.conversions

        share = f"{m.search_impression_share*100:.0f}%" if m.search_impression_share else "N/A"

        print(f"  {c.name[:38]:<40} {c.status.name[:6]:<8} "
              f"{m.impressions:>8,} {m.clicks:>7,} "
              f"{m.ctr*100:>5.1f}% R{spend:>7.0f} "
              f"{m.conversions:>5.0f} {'R'+str(int(cpa)) if cpa else 'N/A':>8}")

    print("  " + "-" * 100)
    print(f"  {'TOTAL':<50} {'':>8} {'':>7} {'':>6} R{total_spend:>7.0f} "
          f"{total_conversions:>5.0f}")


def report_keywords(client: GoogleAdsClient, customer_id: str, date_range: str):
    print(f"\n{'='*70}")
    print(f"TOP KEYWORDS — {date_range}")
    print(f"{'='*70}")

    query = f"""
        SELECT
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type,
            ad_group_criterion.quality_info.quality_score,
            campaign.name,
            metrics.impressions,
            metrics.clicks,
            metrics.ctr,
            metrics.average_cpc,
            metrics.cost_micros,
            metrics.conversions
        FROM keyword_view
        WHERE ad_group_criterion.status != 'REMOVED'
            AND ad_group_criterion.type = 'KEYWORD'
            AND metrics.impressions > 0
            AND segments.date DURING {date_range}
        ORDER BY metrics.cost_micros DESC
        LIMIT 25
    """

    print(f"\n  {'Keyword':<38} {'Match':<8} {'QS':<4} {'Impr':>7} "
          f"{'CTR':>6} {'CPC':>7} {'Conv':>5}")
    print("  " + "-" * 85)

    for row in _search(client, customer_id, query):
        m = row.metrics
        kw = row.ad_group_criterion
        qs = kw.quality_info.quality_score or '-'

        print(f"  {kw.keyword.text[:36]:<38} {kw.keyword.match_type.name[:6]:<8} "
              f"{str(qs):<4} {m.impressions:>7,} "
              f"{m.ctr*100:>5.1f}% {_zar(m.average_cpc):>7} {m.conversions:>5.0f}")


def report_search_terms(client: GoogleAdsClient, customer_id: str, date_range: str):
    """Show actual search queries that triggered ads — critical for negative keyword discovery."""
    print(f"\n{'='*70}")
    print(f"SEARCH TERMS REPORT — {date_range}")
    print(f"{'='*70}")
    print("  Use this to find irrelevant queries to add as negative keywords.")

    query = f"""
        SELECT
            search_term_view.search_term,
            search_term_view.status,
            campaign.name,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions
        FROM search_term_view
        WHERE segments.date DURING {date_range}
            AND metrics.impressions > 5
        ORDER BY metrics.impressions DESC
        LIMIT 50
    """

    print(f"\n  {'Search Term':<45} {'Impr':>7} {'Clicks':>7} {'Spend':>8} {'Conv':>5}")
    print("  " + "-" * 80)

    for row in _search(client, customer_id, query):
        m = row.metrics
        st = row.search_term_view
        flag = " [NEGATIVE?]" if m.conversions == 0 and m.cost_micros / MICROS_PER_ZAR > 20 else ""

        print(f"  {st.search_term[:43]:<45} {m.impressions:>7,} {m.clicks:>7,} "
              f"{_zar(m.cost_micros):>8} {m.conversions:>5.0f}{flag}")


def report_ads(client: GoogleAdsClient, customer_id: str, date_range: str):
    print(f"\n{'='*70}")
    print(f"ADS PERFORMANCE — {date_range}")
    print(f"{'='*70}")

    query = f"""
        SELECT
            ad_group_ad.ad.id,
            ad_group_ad.ad.responsive_search_ad.headlines,
            ad_group_ad.status,
            campaign.name,
            ad_group.name,
            metrics.impressions,
            metrics.clicks,
            metrics.ctr,
            metrics.cost_micros,
            metrics.conversions
        FROM ad_group_ad
        WHERE ad_group_ad.status != 'REMOVED'
            AND metrics.impressions > 0
            AND segments.date DURING {date_range}
        ORDER BY metrics.cost_micros DESC
        LIMIT 20
    """

    for row in _search(client, customer_id, query):
        m = row.metrics
        ad = row.ad_group_ad

        headlines = ad.ad.responsive_search_ad.headlines
        headline_texts = [h.text for h in headlines[:3]] if headlines else ['(no headlines)']

        print(f"\n  Ad ID: {ad.ad.id} | Status: {ad.status.name}")
        print(f"  Campaign: {row.campaign.name}")
        print(f"  Headlines: {' | '.join(headline_texts)}")
        print(f"  Impressions: {m.impressions:,} | Clicks: {m.clicks:,} | "
              f"CTR: {m.ctr*100:.2f}% | Spend: {_zar(m.cost_micros)} | Conv: {m.conversions:.0f}")


def generate_full_report(
    client: GoogleAdsClient,
    customer_id: str = None,
    date_range: str = "LAST_30_DAYS",
):
    """Full performance report across all levels."""
    cid = clean_customer_id(customer_id)

    print(f"\n{'#'*70}")
    print(f"CANNIBISTERS GOOGLE ADS PERFORMANCE REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Period: {date_range.replace('_', ' ').title()}")
    print(f"Funnel: Search/Display → co.za → Membership → Klaviyo → Purchase")
    print(f"{'#'*70}")

    report_campaigns(client, cid, date_range)
    report_keywords(client, cid, date_range)
    report_search_terms(client, cid, date_range)
    report_ads(client, cid, date_range)

    print(f"\n{'#'*70}")
    print("END OF REPORT")
    print(f"{'#'*70}")
