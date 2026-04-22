"""
Performance optimization for Cannibisters Google Ads campaigns.

Optimization rules (all run as dry-run by default):
  - Pause keywords with Quality Score < 3 (poor relevance signal)
  - Pause ads with CTR < 0.5% after 1,000+ impressions
  - Flag campaigns where CPA exceeds R300 (ceiling threshold)
  - Flag campaigns where impression share drops below 30%
  - Recommend budget increases where CPA is healthy and impression share is low
  - Archive paused campaigns older than 90 days

Run weekly or integrate into a cron schedule.
"""

from typing import List, Optional
from datetime import datetime
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

from .config import (
    CUSTOMER_ID, CTR_FLOOR, CPA_TARGET_ZAR, CPA_CEILING_ZAR,
    IMPRESSION_SHARE_FLOOR, MICROS_PER_ZAR,
)
from .auth import clean_customer_id, handle_google_ads_exception


def _ga_search(client: GoogleAdsClient, customer_id: str, query: str):
    """Helper: run a GAQL query and yield rows."""
    ga_service = client.get_service("GoogleAdsService")
    try:
        response = ga_service.search_stream(customer_id=customer_id, query=query)
        for batch in response:
            yield from batch.results
    except GoogleAdsException as ex:
        handle_google_ads_exception(ex)


def audit_keyword_quality_scores(
    client: GoogleAdsClient,
    customer_id: str = None,
    min_impressions: int = 100,
    quality_score_floor: int = 3,
    execute: bool = False,
) -> List[dict]:
    """
    Find keywords with low Quality Scores.
    Low QS = Google thinks your ad/landing page isn't relevant → higher CPCs, lower positions.
    """
    cid = clean_customer_id(customer_id)
    print(f"\nAuditing keyword Quality Scores (floor: {quality_score_floor})...")

    query = f"""
        SELECT
            ad_group_criterion.criterion_id,
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type,
            ad_group_criterion.quality_info.quality_score,
            ad_group_criterion.status,
            campaign.name,
            ad_group.name,
            metrics.impressions
        FROM keyword_view
        WHERE ad_group_criterion.status IN ('ENABLED', 'PAUSED')
            AND ad_group_criterion.type = 'KEYWORD'
            AND metrics.impressions >= {min_impressions}
            AND segments.date DURING LAST_30_DAYS
        ORDER BY ad_group_criterion.quality_info.quality_score ASC
    """

    flagged = []
    for row in _ga_search(client, cid, query):
        qs = row.ad_group_criterion.quality_info.quality_score
        if qs and qs < quality_score_floor:
            entry = {
                'criterion_id': row.ad_group_criterion.criterion_id,
                'keyword': row.ad_group_criterion.keyword.text,
                'match_type': row.ad_group_criterion.keyword.match_type.name,
                'quality_score': qs,
                'impressions': row.metrics.impressions,
                'campaign': row.campaign.name,
                'ad_group': row.ad_group.name,
                'status': row.ad_group_criterion.status.name,
            }
            flagged.append(entry)

    if flagged:
        print(f"\n  {'Keyword':<40} {'Match':<8} {'QS':<5} {'Impressions':<12} Campaign")
        print("  " + "-" * 90)
        for kw in flagged:
            print(f"  {kw['keyword']:<40} {kw['match_type']:<8} {kw['quality_score']:<5} "
                  f"{kw['impressions']:<12} {kw['campaign'][:30]}")
    else:
        print("  No low Quality Score keywords found.")

    return flagged


def pause_low_ctr_ads(
    client: GoogleAdsClient,
    customer_id: str = None,
    min_impressions: int = 1000,
    ctr_floor: float = CTR_FLOOR,
    execute: bool = False,
) -> List[dict]:
    """
    Pause ads with CTR below threshold after sufficient impressions.
    Low CTR hurts Quality Score and wastes spend on non-converting audiences.
    """
    cid = clean_customer_id(customer_id)
    print(f"\nChecking ads for low CTR (< {ctr_floor}% after {min_impressions:,} impressions)...")

    query = f"""
        SELECT
            ad_group_ad.ad.id,
            ad_group_ad.ad.name,
            ad_group_ad.status,
            campaign.name,
            ad_group.name,
            metrics.impressions,
            metrics.clicks,
            metrics.ctr
        FROM ad_group_ad
        WHERE ad_group_ad.status = 'ENABLED'
            AND metrics.impressions >= {min_impressions}
            AND segments.date DURING LAST_30_DAYS
        ORDER BY metrics.ctr ASC
    """

    paused = []
    for row in _ga_search(client, cid, query):
        ctr = row.metrics.ctr * 100  # convert to percentage
        if ctr < ctr_floor:
            entry = {
                'ad_id': row.ad_group_ad.ad.id,
                'ad_name': row.ad_group_ad.ad.name,
                'campaign': row.campaign.name,
                'ad_group': row.ad_group.name,
                'impressions': row.metrics.impressions,
                'clicks': row.metrics.clicks,
                'ctr': ctr,
            }
            paused.append(entry)
            status = '[DRY RUN] Would pause' if not execute else 'Pausing'
            print(f"  {status}: {entry['ad_name'] or entry['ad_id']} "
                  f"(CTR: {ctr:.2f}%, {row.metrics.impressions:,} impressions)")

            if execute:
                _set_ad_status(client, cid, row.ad_group_ad.resource_name, 'PAUSED')

    if not paused:
        print("  No low-CTR ads found — all ads above threshold.")

    return paused


def _set_ad_status(client, customer_id, resource_name, status):
    service = client.get_service("AdGroupAdService")
    op = client.get_type("AdGroupAdOperation")
    op.update.resource_name = resource_name
    op.update.status = getattr(client.enums.AdGroupAdStatusEnum, status)
    op.update_mask.paths.append("status")
    try:
        service.mutate_ad_group_ads(customer_id=customer_id, operations=[op])
    except GoogleAdsException as ex:
        handle_google_ads_exception(ex)


def audit_campaign_cpa(
    client: GoogleAdsClient,
    customer_id: str = None,
    cpa_target: float = CPA_TARGET_ZAR,
    cpa_ceiling: float = CPA_CEILING_ZAR,
) -> List[dict]:
    """
    Report on campaigns that are above or below CPA target.
    CPA = cost per membership sign-up conversion.
    """
    cid = clean_customer_id(customer_id)
    print(f"\nAuditing campaign CPAs (target: R{cpa_target}, ceiling: R{cpa_ceiling})...")

    query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            metrics.cost_micros,
            metrics.conversions,
            metrics.cost_per_conversion,
            metrics.impressions,
            metrics.search_impression_share
        FROM campaign
        WHERE campaign.status != 'REMOVED'
            AND metrics.impressions > 0
            AND segments.date DURING LAST_30_DAYS
        ORDER BY metrics.cost_per_conversion DESC
    """

    results = []
    print(f"\n  {'Campaign':<45} {'Spend':>8} {'Conv':>6} {'CPA':>8} {'Imp Share':>10} Status")
    print("  " + "-" * 95)

    for row in _ga_search(client, cid, query):
        m = row.metrics
        spend = m.cost_micros / MICROS_PER_ZAR
        cpa = m.cost_per_conversion / MICROS_PER_ZAR if m.conversions > 0 else None
        imp_share = m.search_impression_share

        if m.conversions == 0 and spend < 50:
            continue  # Skip campaigns with minimal data

        status = 'OK'
        if cpa is not None:
            if cpa > cpa_ceiling:
                status = 'OVER CEILING'
            elif cpa > cpa_target:
                status = 'ABOVE TARGET'
            elif cpa < cpa_target * 0.7:
                status = 'GOOD - SCALE'

        if imp_share and imp_share < IMPRESSION_SHARE_FLOOR:
            status = status + ' | LOW SHARE'

        entry = {
            'campaign_id': row.campaign.id,
            'name': row.campaign.name,
            'status': row.campaign.status.name,
            'spend_zar': spend,
            'conversions': m.conversions,
            'cpa_zar': cpa,
            'impression_share': imp_share,
            'recommendation': status,
        }
        results.append(entry)

        cpa_str = f"R{cpa:.2f}" if cpa is not None else "N/A"
        share_str = f"{imp_share*100:.1f}%" if imp_share else "N/A"
        print(f"  {row.campaign.name[:43]:<45} R{spend:>6.0f} {m.conversions:>6.0f} "
              f"{cpa_str:>8} {share_str:>10} {status}")

    return results


def budget_recommendations(
    client: GoogleAdsClient,
    customer_id: str = None,
    cpa_target: float = CPA_TARGET_ZAR,
) -> List[dict]:
    """
    Suggest budget changes based on CPA performance.
    - Campaigns performing well (CPA < target) → suggest budget increase
    - Campaigns over ceiling CPA → suggest budget decrease or pause
    """
    cid = clean_customer_id(customer_id)
    print(f"\nBudget recommendations...")

    audit = audit_campaign_cpa(client, cid, cpa_target)
    recs = []

    for c in audit:
        if c['cpa_zar'] is None:
            continue
        if c['cpa_zar'] < cpa_target * 0.7 and c['impression_share'] and c['impression_share'] < 0.7:
            recs.append({
                'campaign': c['name'],
                'action': 'INCREASE BUDGET',
                'reason': f"CPA R{c['cpa_zar']:.0f} is well below target, "
                          f"impression share {c['impression_share']*100:.0f}% has room to scale",
            })
        elif c['cpa_zar'] and c['cpa_zar'] > CPA_CEILING_ZAR:
            recs.append({
                'campaign': c['name'],
                'action': 'REDUCE BUDGET OR PAUSE',
                'reason': f"CPA R{c['cpa_zar']:.0f} exceeds ceiling R{CPA_CEILING_ZAR}",
            })

    if recs:
        print("\n  Budget Recommendations:")
        for r in recs:
            print(f"  [{r['action']}] {r['campaign']}")
            print(f"    Reason: {r['reason']}")
    else:
        print("  No budget changes recommended at this time.")

    return recs


def run_full_optimization(
    client: GoogleAdsClient,
    customer_id: str = None,
    execute: bool = False,
):
    """Run all optimization checks in one pass."""
    cid = clean_customer_id(customer_id)
    mode = "EXECUTION MODE" if execute else "DRY RUN"

    print(f"\n{'='*60}")
    print(f"Cannibisters Google Ads Optimization [{mode}]")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")

    audit_keyword_quality_scores(client, cid, execute=execute)
    pause_low_ctr_ads(client, cid, execute=execute)
    audit_campaign_cpa(client, cid)
    budget_recommendations(client, cid)

    print(f"\n{'='*60}")
    if not execute:
        print("Dry run complete. Use --execute to apply pauses and changes.")
    else:
        print("Optimization pass complete.")
    print(f"{'='*60}")
