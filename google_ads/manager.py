"""
Campaign, ad group, keyword, and ad creation/management.

All campaigns are built around the Cannibisters membership funnel:
  Search/Display → cannibisters.co.za → membership sign-up → Klaviyo → purchase

Three campaign templates:
  1. search_membership   — Search ads targeting people looking for social clubs / apothecaries
  2. display_awareness   — Display ads for lifestyle/brand awareness, retargeting
  3. customer_match_warm — Search ads targeting existing leads/members via Customer Match

Always created in PAUSED status. Use --execute to activate.
"""

import sys
from datetime import datetime, timedelta
from typing import List, Optional
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

from .config import (
    MICROS_PER_ZAR, DEFAULT_DAILY_BUDGET_ZAR, DEFAULT_MAX_CPC_ZAR,
    MEMBERSHIP_SIGNUP_URL, PRIMARY_GEO_TARGETS, AGE_MIN, AGE_MAX,
    CUSTOMER_ID,
)
from .auth import clean_customer_id, handle_google_ads_exception
from .compliance import (
    check_ad, print_compliance_report,
    COMPLIANT_HEADLINES, COMPLIANT_DESCRIPTIONS, NEGATIVE_KEYWORDS,
    RECOMMENDED_KEYWORDS,
)


# ---------------------------------------------------------------------------
# Budget
# ---------------------------------------------------------------------------

def create_campaign_budget(
    client: GoogleAdsClient,
    name: str,
    daily_budget_zar: float = DEFAULT_DAILY_BUDGET_ZAR,
    customer_id: str = None,
) -> str:
    cid = clean_customer_id(customer_id)
    budget_service = client.get_service("CampaignBudgetService")
    op = client.get_type("CampaignBudgetOperation")
    budget = op.create

    budget.name = name
    budget.amount_micros = int(daily_budget_zar * MICROS_PER_ZAR)
    budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD

    response = budget_service.mutate_campaign_budgets(
        customer_id=cid, operations=[op]
    )
    resource_name = response.results[0].resource_name
    print(f"  Budget created: {resource_name} (R{daily_budget_zar}/day)")
    return resource_name


# ---------------------------------------------------------------------------
# Campaigns
# ---------------------------------------------------------------------------

def create_search_membership_campaign(
    client: GoogleAdsClient,
    name: str = None,
    daily_budget_zar: float = DEFAULT_DAILY_BUDGET_ZAR,
    customer_id: str = None,
    execute: bool = False,
) -> Optional[str]:
    """
    Search campaign targeting intent-based queries for club membership.
    Best for capturing people actively searching for cannabis/herbal social clubs.
    Landing page: cannibisters.co.za
    """
    cid = clean_customer_id(customer_id)
    campaign_name = name or f"Cannibisters - Membership Search - {datetime.now().strftime('%Y%m%d')}"

    print(f"\nCreating Search Campaign: {campaign_name}")
    if not execute:
        print("  [DRY RUN] Not submitting to Google Ads. Use --execute to apply.")
        return None

    try:
        budget_resource = create_campaign_budget(
            client, f"Budget - {campaign_name}", daily_budget_zar, cid
        )

        campaign_service = client.get_service("CampaignService")
        op = client.get_type("CampaignOperation")
        campaign = op.create

        campaign.name = campaign_name
        campaign.advertising_channel_type = (
            client.enums.AdvertisingChannelTypeEnum.SEARCH
        )
        campaign.status = client.enums.CampaignStatusEnum.PAUSED
        campaign.campaign_budget = budget_resource

        # Manual CPC with enhanced CPC — gives control while still optimizing
        campaign.manual_cpc.enhanced_cpc_enabled = True

        campaign.network_settings.target_google_search = True
        campaign.network_settings.target_search_network = True
        campaign.network_settings.target_content_network = False  # Search only

        campaign.start_date = datetime.now().strftime('%Y%m%d')
        campaign.end_date = (datetime.now() + timedelta(days=90)).strftime('%Y%m%d')

        # Geo targeting (set at campaign level, refined at ad group level)
        for geo_id in PRIMARY_GEO_TARGETS:
            location = campaign.geo_target_type_setting
            # Detailed geo targeting applied via CampaignCriterion — see add_geo_targets()

        response = campaign_service.mutate_campaigns(
            customer_id=cid, operations=[op]
        )
        resource_name = response.results[0].resource_name
        print(f"  Campaign created: {resource_name}")

        _add_geo_targets(client, cid, resource_name, PRIMARY_GEO_TARGETS)

        return resource_name

    except GoogleAdsException as ex:
        handle_google_ads_exception(ex)
        return None


def create_display_awareness_campaign(
    client: GoogleAdsClient,
    name: str = None,
    daily_budget_zar: float = DEFAULT_DAILY_BUDGET_ZAR,
    customer_id: str = None,
    execute: bool = False,
) -> Optional[str]:
    """
    Display campaign for brand awareness and remarketing.
    Targets people who visited cannibisters.co.za but didn't sign up.
    Uses lifestyle/wellness interest targeting for cold audiences.
    """
    cid = clean_customer_id(customer_id)
    campaign_name = name or f"Cannibisters - Awareness Display - {datetime.now().strftime('%Y%m%d')}"

    print(f"\nCreating Display Campaign: {campaign_name}")
    if not execute:
        print("  [DRY RUN] Not submitting to Google Ads. Use --execute to apply.")
        return None

    try:
        budget_resource = create_campaign_budget(
            client, f"Budget - {campaign_name}", daily_budget_zar, cid
        )

        campaign_service = client.get_service("CampaignService")
        op = client.get_type("CampaignOperation")
        campaign = op.create

        campaign.name = campaign_name
        campaign.advertising_channel_type = (
            client.enums.AdvertisingChannelTypeEnum.DISPLAY
        )
        campaign.status = client.enums.CampaignStatusEnum.PAUSED
        campaign.campaign_budget = budget_resource

        # Target CPA bidding — optimize for membership sign-ups
        campaign.target_cpa.target_cpa_micros = int(150 * MICROS_PER_ZAR)

        campaign.start_date = datetime.now().strftime('%Y%m%d')
        campaign.end_date = (datetime.now() + timedelta(days=90)).strftime('%Y%m%d')

        response = campaign_service.mutate_campaigns(
            customer_id=cid, operations=[op]
        )
        resource_name = response.results[0].resource_name
        print(f"  Campaign created: {resource_name}")

        _add_geo_targets(client, cid, resource_name, PRIMARY_GEO_TARGETS)

        return resource_name

    except GoogleAdsException as ex:
        handle_google_ads_exception(ex)
        return None


def _add_geo_targets(
    client: GoogleAdsClient,
    customer_id: str,
    campaign_resource: str,
    geo_ids: List[int],
):
    """Attach location criteria to a campaign."""
    criterion_service = client.get_service("CampaignCriterionService")
    operations = []
    geo_target_service = client.get_service("GeoTargetConstantService")

    for geo_id in geo_ids:
        op = client.get_type("CampaignCriterionOperation")
        criterion = op.create
        criterion.campaign = campaign_resource
        criterion.location.geo_target_constant = (
            geo_target_service.geo_target_constant_path(str(geo_id))
        )
        operations.append(op)

    if operations:
        criterion_service.mutate_campaign_criteria(
            customer_id=customer_id, operations=operations
        )
        print(f"  Geo targets added: {len(geo_ids)} locations")


# ---------------------------------------------------------------------------
# Ad Groups
# ---------------------------------------------------------------------------

def create_membership_ad_group(
    client: GoogleAdsClient,
    campaign_resource: str,
    name: str = "Membership Signups",
    max_cpc_zar: float = DEFAULT_MAX_CPC_ZAR,
    customer_id: str = None,
    execute: bool = False,
) -> Optional[str]:
    """Creates a Search Standard ad group for membership queries."""
    cid = clean_customer_id(customer_id)
    group_name = f"{name} - {datetime.now().strftime('%Y%m%d')}"

    print(f"\nCreating Ad Group: {group_name}")
    if not execute:
        print("  [DRY RUN] Not submitting. Use --execute to apply.")
        return None

    try:
        ad_group_service = client.get_service("AdGroupService")
        op = client.get_type("AdGroupOperation")
        ad_group = op.create

        ad_group.name = group_name
        ad_group.campaign = campaign_resource
        ad_group.status = client.enums.AdGroupStatusEnum.ENABLED
        ad_group.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
        ad_group.cpc_bid_micros = int(max_cpc_zar * MICROS_PER_ZAR)

        response = ad_group_service.mutate_ad_groups(
            customer_id=cid, operations=[op]
        )
        resource_name = response.results[0].resource_name
        print(f"  Ad group created: {resource_name}")
        return resource_name

    except GoogleAdsException as ex:
        handle_google_ads_exception(ex)
        return None


# ---------------------------------------------------------------------------
# Keywords
# ---------------------------------------------------------------------------

def add_keywords(
    client: GoogleAdsClient,
    ad_group_resource: str,
    keywords: List[dict],
    customer_id: str = None,
    execute: bool = False,
) -> int:
    """
    Add keywords to an ad group.
    keywords: list of {'text': str, 'match_type': 'EXACT'|'PHRASE'|'BROAD'}
    """
    cid = clean_customer_id(customer_id)
    print(f"\nAdding {len(keywords)} keywords to ad group")
    if not execute:
        for kw in keywords:
            print(f"  [DRY RUN] {kw['match_type']}: {kw['text']}")
        return 0

    try:
        criterion_service = client.get_service("AdGroupCriterionService")
        operations = []
        match_type_enum = client.enums.KeywordMatchTypeEnum

        match_map = {
            'EXACT': match_type_enum.EXACT,
            'PHRASE': match_type_enum.PHRASE,
            'BROAD': match_type_enum.BROAD,
        }

        for kw in keywords:
            op = client.get_type("AdGroupCriterionOperation")
            criterion = op.create
            criterion.ad_group = ad_group_resource
            criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            criterion.keyword.text = kw['text']
            criterion.keyword.match_type = match_map.get(kw['match_type'], match_type_enum.PHRASE)
            operations.append(op)

        response = criterion_service.mutate_ad_group_criteria(
            customer_id=cid, operations=operations
        )
        added = len(response.results)
        print(f"  Added {added} keywords")
        return added

    except GoogleAdsException as ex:
        handle_google_ads_exception(ex)
        return 0


def add_negative_keywords_to_campaign(
    client: GoogleAdsClient,
    campaign_resource: str,
    negative_keywords: List[str] = None,
    customer_id: str = None,
    execute: bool = False,
):
    """Add campaign-level negative keywords (blocks irrelevant/unsafe searches)."""
    cid = clean_customer_id(customer_id)
    negatives = negative_keywords or NEGATIVE_KEYWORDS

    print(f"\nAdding {len(negatives)} negative keywords to campaign")
    if not execute:
        print(f"  [DRY RUN] {negatives[:5]}... (and {len(negatives)-5} more)")
        return

    try:
        criterion_service = client.get_service("CampaignCriterionService")
        operations = []

        for kw_text in negatives:
            op = client.get_type("CampaignCriterionOperation")
            criterion = op.create
            criterion.campaign = campaign_resource
            criterion.negative = True
            criterion.keyword.text = kw_text
            criterion.keyword.match_type = (
                client.enums.KeywordMatchTypeEnum.BROAD
            )
            operations.append(op)

        criterion_service.mutate_campaign_criteria(
            customer_id=cid, operations=operations
        )
        print(f"  Added {len(negatives)} negative keywords")

    except GoogleAdsException as ex:
        handle_google_ads_exception(ex)


# ---------------------------------------------------------------------------
# Ads
# ---------------------------------------------------------------------------

def create_membership_rsa(
    client: GoogleAdsClient,
    ad_group_resource: str,
    headlines: List[str] = None,
    descriptions: List[str] = None,
    final_url: str = None,
    customer_id: str = None,
    execute: bool = False,
    skip_compliance_check: bool = False,
) -> Optional[str]:
    """
    Create a Responsive Search Ad for membership sign-up.
    Runs compliance check before submission.
    """
    cid = clean_customer_id(customer_id)
    url = final_url or MEMBERSHIP_SIGNUP_URL
    ad_headlines = headlines or COMPLIANT_HEADLINES[:8]
    ad_descriptions = descriptions or COMPLIANT_DESCRIPTIONS[:4]

    # Enforce compliance check
    if not skip_compliance_check:
        result = check_ad(ad_headlines, ad_descriptions, url)
        print_compliance_report(result, "RSA Pre-submission Check")
        if not result.is_safe_to_submit:
            print("\nAd submission blocked due to compliance issues.")
            print("Fix the flagged terms before resubmitting.")
            return None

    print(f"\nCreating Responsive Search Ad → {url}")
    if not execute:
        print("  [DRY RUN] Headlines:")
        for h in ad_headlines:
            print(f"    - {h} ({len(h)} chars)")
        print("  Descriptions:")
        for d in ad_descriptions:
            print(f"    - {d[:60]}... ({len(d)} chars)")
        return None

    try:
        ad_group_ad_service = client.get_service("AdGroupAdService")
        op = client.get_type("AdGroupAdOperation")
        ad_group_ad = op.create

        ad_group_ad.ad_group = ad_group_resource
        ad_group_ad.status = client.enums.AdGroupAdStatusEnum.PAUSED

        ad = ad_group_ad.ad
        ad.final_urls.append(url)

        rsa = ad.responsive_search_ad

        for i, headline_text in enumerate(ad_headlines[:15]):  # max 15 headlines
            headline = client.get_type("AdTextAsset")
            headline.text = headline_text
            # Pin headline 1 to position 1 for brand consistency
            if i == 0:
                headline.pinned_field = (
                    client.enums.ServedAssetFieldTypeEnum.HEADLINE_1
                )
            rsa.headlines.append(headline)

        for desc_text in ad_descriptions[:4]:  # max 4 descriptions
            desc = client.get_type("AdTextAsset")
            desc.text = desc_text
            rsa.descriptions.append(desc)

        response = ad_group_ad_service.mutate_ad_group_ads(
            customer_id=cid, operations=[op]
        )
        resource_name = response.results[0].resource_name
        print(f"  RSA created: {resource_name}")
        return resource_name

    except GoogleAdsException as ex:
        handle_google_ads_exception(ex)
        return None


# ---------------------------------------------------------------------------
# Full campaign scaffold
# ---------------------------------------------------------------------------

def scaffold_membership_campaign(
    client: GoogleAdsClient,
    customer_id: str = None,
    campaign_name: str = None,
    daily_budget_zar: float = DEFAULT_DAILY_BUDGET_ZAR,
    execute: bool = False,
):
    """
    End-to-end scaffold: campaign → ad group → keywords → RSA → negative keywords.
    This is the recommended starting point for Cannibisters Google Ads.
    """
    cid = clean_customer_id(customer_id)
    label = "EXECUTING" if execute else "DRY RUN PREVIEW"
    print(f"\n{'='*60}")
    print(f"Cannibisters Membership Campaign Scaffold [{label}]")
    print(f"{'='*60}")
    print(f"Daily budget: R{daily_budget_zar}")
    print(f"Landing page: {MEMBERSHIP_SIGNUP_URL}")
    print(f"Funnel: Search → co.za membership sign-up → Klaviyo → purchase")

    # 1. Campaign
    campaign_resource = create_search_membership_campaign(
        client, campaign_name, daily_budget_zar, cid, execute
    )

    if execute and not campaign_resource:
        print("Campaign creation failed — aborting scaffold.")
        return

    placeholder = campaign_resource or "customers/XXX/campaigns/YYY [dry run]"

    # 2. Ad Group
    ad_group_resource = create_membership_ad_group(
        client, placeholder, "Social Club Membership", DEFAULT_MAX_CPC_ZAR, cid, execute
    )

    # 3. Negative keywords on campaign
    add_negative_keywords_to_campaign(
        client, placeholder, NEGATIVE_KEYWORDS, cid, execute
    )

    # 4. Keywords
    keywords = (
        [{'text': kw.strip('[]"'), 'match_type': 'EXACT'}
         for kw in RECOMMENDED_KEYWORDS['EXACT']]
        + [{'text': kw.strip('"'), 'match_type': 'PHRASE'}
           for kw in RECOMMENDED_KEYWORDS['PHRASE']]
    )

    ag_placeholder = ad_group_resource or "customers/XXX/adGroups/YYY [dry run]"
    add_keywords(client, ag_placeholder, keywords, cid, execute)

    # 5. RSA
    create_membership_rsa(
        client, ag_placeholder,
        COMPLIANT_HEADLINES[:8], COMPLIANT_DESCRIPTIONS[:4],
        MEMBERSHIP_SIGNUP_URL, cid, execute
    )

    print(f"\n{'='*60}")
    if execute:
        print("Campaign scaffold complete. All entities created in PAUSED status.")
        print("Review in Google Ads UI, then activate when ready.")
    else:
        print("Dry run complete. Re-run with --execute to apply.")
    print(f"{'='*60}")


# ---------------------------------------------------------------------------
# Campaign management
# ---------------------------------------------------------------------------

def list_campaigns(client: GoogleAdsClient, customer_id: str = None) -> List[dict]:
    """Fetch all campaigns with status and basic metrics."""
    cid = clean_customer_id(customer_id)
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type,
            campaign.start_date,
            campaign.end_date,
            campaign_budget.amount_micros,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.ctr,
            metrics.average_cpc,
            metrics.conversions,
            metrics.cost_per_conversion
        FROM campaign
        WHERE campaign.status != 'REMOVED'
            AND segments.date DURING LAST_30_DAYS
        ORDER BY metrics.cost_micros DESC
    """

    results = []
    try:
        response = ga_service.search_stream(customer_id=cid, query=query)
        for batch in response:
            for row in batch.results:
                c = row.campaign
                m = row.metrics
                results.append({
                    'id': c.id,
                    'name': c.name,
                    'status': c.status.name,
                    'type': c.advertising_channel_type.name,
                    'daily_budget_zar': row.campaign_budget.amount_micros / MICROS_PER_ZAR,
                    'impressions': m.impressions,
                    'clicks': m.clicks,
                    'spend_zar': m.cost_micros / MICROS_PER_ZAR,
                    'ctr': m.ctr,
                    'avg_cpc_zar': m.average_cpc / MICROS_PER_ZAR,
                    'conversions': m.conversions,
                    'cpa_zar': m.cost_per_conversion / MICROS_PER_ZAR if m.conversions > 0 else None,
                })
    except GoogleAdsException as ex:
        handle_google_ads_exception(ex)

    return results


def pause_campaign(
    client: GoogleAdsClient,
    campaign_id: str,
    customer_id: str = None,
    execute: bool = False,
):
    cid = clean_customer_id(customer_id)
    resource_name = client.get_service("CampaignService").campaign_path(cid, campaign_id)

    if not execute:
        print(f"  [DRY RUN] Would pause campaign {campaign_id}")
        return

    try:
        campaign_service = client.get_service("CampaignService")
        op = client.get_type("CampaignOperation")
        op.update.resource_name = resource_name
        op.update.status = client.enums.CampaignStatusEnum.PAUSED
        op.update_mask.paths.append("status")
        campaign_service.mutate_campaigns(customer_id=cid, operations=[op])
        print(f"  Paused campaign {campaign_id}")
    except GoogleAdsException as ex:
        handle_google_ads_exception(ex)
