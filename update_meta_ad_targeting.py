import os
import sys
import argparse
import time
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad

load_dotenv()

ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
AD_ACCOUNT_ID = os.getenv('META_AD_ACCOUNT_ID')

# Budget split
CT_SHARE = 0.55
OTHER_SHARE = 0.45

CAPE_TOWN = [
    {'latitude': -33.9249, 'longitude': 18.4241, 'radius': 40, 'distance_unit': 'kilometer', 'name': 'Cape Town'},
]

OTHER_CITIES = [
    {'latitude': -26.2041, 'longitude': 28.0473, 'radius': 30, 'distance_unit': 'kilometer', 'name': 'Johannesburg'},
    {'latitude': -25.7479, 'longitude': 28.2293, 'radius': 30, 'distance_unit': 'kilometer', 'name': 'Pretoria'},
    {'latitude': -29.8587, 'longitude': 31.0218, 'radius': 30, 'distance_unit': 'kilometer', 'name': 'Durban'},
    {'latitude': -26.2677, 'longitude': 27.8585, 'radius': 20, 'distance_unit': 'kilometer', 'name': 'Soweto'},
]


def initialize_api():
    if not ACCESS_TOKEN:
        print("Error: META_ACCESS_TOKEN not found.")
        sys.exit(1)
    if not AD_ACCOUNT_ID:
        print("Error: META_AD_ACCOUNT_ID not found.")
        sys.exit(1)
    FacebookAdsApi.init(access_token=ACCESS_TOKEN)


def get_ad_account():
    account_id = AD_ACCOUNT_ID
    if not account_id.startswith('act_'):
        account_id = 'act_' + account_id
    return AdAccount(account_id)


def fetch_active_ad_sets(account):
    """Fetch all currently active ad sets."""
    ad_sets = account.get_ad_sets(
        fields=[
            AdSet.Field.id,
            AdSet.Field.name,
            AdSet.Field.status,
            AdSet.Field.campaign_id,
            AdSet.Field.daily_budget,
            AdSet.Field.lifetime_budget,
            AdSet.Field.optimization_goal,
            AdSet.Field.billing_event,
            AdSet.Field.bid_strategy,
            AdSet.Field.start_time,
            AdSet.Field.end_time,
            AdSet.Field.targeting,
        ],
        params={'effective_status': ['ACTIVE']},
    )
    return list(ad_sets)


def get_ads_for_ad_set(ad_set_id):
    """Fetch ads belonging to a given ad set."""
    ad_set = AdSet(ad_set_id)
    ads = ad_set.get_ads(fields=[Ad.Field.id, Ad.Field.name, Ad.Field.creative])
    return list(ads)


def create_replacement_ad_set(account, original, name, locations, daily_budget_cents, dry_run):
    """Create a new ad set based on the original, with updated targeting and budget."""
    params = {
        'name': name,
        'campaign_id': original['campaign_id'],
        'daily_budget': daily_budget_cents,
        'billing_event': original.get('billing_event', 'IMPRESSIONS'),
        'optimization_goal': original.get('optimization_goal', 'POST_ENGAGEMENT'),
        'bid_strategy': original.get('bid_strategy', 'LOWEST_COST_WITHOUT_CAP'),
        'targeting': {
            'geo_locations': {'custom_locations': locations},
            'age_min': 18,
            'age_max': 40,
        },
        'status': 'ACTIVE',
    }

    # Preserve end time if set
    if original.get('end_time'):
        params['end_time'] = original['end_time']

    # Start slightly in the future
    params['start_time'] = int(time.time()) + 60

    if dry_run:
        print(f"    [DRY RUN] Would create ad set: '{name}' | Budget: R{daily_budget_cents / 100:.0f}/day")
        return None

    new_ad_set = account.create_ad_set(params=params)
    print(f"    Created ad set '{name}': {new_ad_set['id']}")
    return new_ad_set['id']


def copy_ads_to_ad_set(ads, new_ad_set_id, label, dry_run):
    """Re-create each ad from the original ad set into the new ad set."""
    for ad in ads:
        creative_id = ad.get('creative', {}).get('id')
        if not creative_id:
            print(f"    Warning: Ad {ad['id']} has no creative, skipping.")
            continue

        if dry_run:
            print(f"    [DRY RUN] Would copy ad '{ad.get('name')}' -> {label}")
            continue

        new_ad = AdSet(new_ad_set_id).get_api().call(
            'POST',
            f'/act_{AD_ACCOUNT_ID}/ads',
            params={
                'name': ad.get('name', 'Boosted Post Ad'),
                'adset_id': new_ad_set_id,
                'creative': {'creative_id': creative_id},
                'status': 'ACTIVE',
            }
        )
        print(f"    Copied ad '{ad.get('name')}' -> {label} (new ad id: {new_ad['id']})")


def pause_ad_set(ad_set_id, name, dry_run):
    if dry_run:
        print(f"    [DRY RUN] Would pause original ad set: '{name}' ({ad_set_id})")
        return
    ad_set = AdSet(ad_set_id)
    ad_set.api_update(params={'status': 'PAUSED'})
    print(f"    Paused original ad set: '{name}' ({ad_set_id})")


def main():
    parser = argparse.ArgumentParser(description='Update live Meta ad sets with city-focused targeting')
    parser.add_argument('--dry-run', action='store_true', default=True,
                        help='Preview changes without applying them (default: True)')
    parser.add_argument('--apply', action='store_true',
                        help='Actually apply the changes to live campaigns')
    args = parser.parse_args()

    dry_run = not args.apply
    if dry_run:
        print("=" * 60)
        print("DRY RUN MODE — no changes will be made to live campaigns.")
        print("Run with --apply to execute for real.")
        print("=" * 60)
    else:
        print("=" * 60)
        print("LIVE MODE — changes will be applied to your active campaigns.")
        print("=" * 60)

    initialize_api()
    account = get_ad_account()

    print("\nFetching active ad sets...")
    active_ad_sets = fetch_active_ad_sets(account)

    if not active_ad_sets:
        print("No active ad sets found.")
        return

    print(f"Found {len(active_ad_sets)} active ad set(s).\n")

    for ad_set in active_ad_sets:
        ad_set_id = ad_set['id']
        name = ad_set.get('name', 'Unnamed')
        daily_budget = ad_set.get('daily_budget')

        if not daily_budget:
            print(f"Skipping '{name}' — uses lifetime budget (manual split needed).")
            continue

        total_cents = int(daily_budget)
        ct_cents = round(total_cents * CT_SHARE / 100) * 100   # round to nearest rand
        other_cents = total_cents - ct_cents

        print(f"Ad Set: '{name}' ({ad_set_id})")
        print(f"  Current budget: R{total_cents / 100:.0f}/day")
        print(f"  -> Cape Town (55%): R{ct_cents / 100:.0f}/day")
        print(f"  -> Other cities (45%): R{other_cents / 100:.0f}/day")

        # Fetch the ads inside this ad set so we can copy their creatives
        ads = get_ads_for_ad_set(ad_set_id)
        print(f"  Ads to copy: {len(ads)}")

        # Create Cape Town ad set
        ct_ad_set_id = create_replacement_ad_set(
            account, ad_set,
            name=f"{name} — Cape Town",
            locations=CAPE_TOWN,
            daily_budget_cents=ct_cents,
            dry_run=dry_run,
        )

        # Create Other Cities ad set
        other_ad_set_id = create_replacement_ad_set(
            account, ad_set,
            name=f"{name} — JHB/PTA/DBN/Soweto",
            locations=OTHER_CITIES,
            daily_budget_cents=other_cents,
            dry_run=dry_run,
        )

        # Copy ads into new ad sets
        if ct_ad_set_id:
            copy_ads_to_ad_set(ads, ct_ad_set_id, 'Cape Town', dry_run)
        if other_ad_set_id:
            copy_ads_to_ad_set(ads, other_ad_set_id, 'JHB/PTA/DBN/Soweto', dry_run)

        # Pause the original broad ad set
        pause_ad_set(ad_set_id, name, dry_run)

        print()

    print("Done.")
    if dry_run:
        print("\nRun with --apply to make these changes live.")


if __name__ == '__main__':
    main()
