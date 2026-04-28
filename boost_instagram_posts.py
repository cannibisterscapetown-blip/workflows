import os
import sys
import time
import requests
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative

load_dotenv()

ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
AD_ACCOUNT_ID = os.getenv('META_AD_ACCOUNT_ID')
PAGE_ID = os.getenv('META_PAGE_ID')
INSTAGRAM_ACCOUNT_ID = os.getenv('META_INSTAGRAM_ACCOUNT_ID')
API_VERSION = 'v21.0'

DAILY_BUDGET_CENTS = 20000  # R200/day
BOOST_DURATION_DAYS = 7

TOP_SA_CITIES = [
    {'latitude': -33.9249, 'longitude': 18.4241, 'radius': 30, 'distance_unit': 'kilometer', 'name': 'Cape Town'},
    {'latitude': -26.2041, 'longitude': 28.0473, 'radius': 30, 'distance_unit': 'kilometer', 'name': 'Johannesburg'},
    {'latitude': -25.7479, 'longitude': 28.2293, 'radius': 30, 'distance_unit': 'kilometer', 'name': 'Pretoria'},
    {'latitude': -29.8587, 'longitude': 31.0218, 'radius': 30, 'distance_unit': 'kilometer', 'name': 'Durban'},
    {'latitude': -26.2677, 'longitude': 27.8585, 'radius': 20, 'distance_unit': 'kilometer', 'name': 'Soweto'},
]


def validate_env():
    missing = [v for v in ['META_ACCESS_TOKEN', 'META_AD_ACCOUNT_ID', 'META_PAGE_ID', 'META_INSTAGRAM_ACCOUNT_ID']
               if not os.getenv(v)]
    if missing:
        print(f"Error: Missing environment variables: {', '.join(missing)}")
        sys.exit(1)


def get_recent_posts(count=3):
    """Fetch the most recent Instagram posts."""
    url = f"https://graph.facebook.com/{API_VERSION}/{INSTAGRAM_ACCOUNT_ID}/media"
    params = {
        'access_token': ACCESS_TOKEN,
        'limit': count,
        'fields': 'id,caption,permalink,media_type,timestamp',
    }
    resp = requests.get(url, params=params)
    data = resp.json()

    if 'error' in data:
        print(f"Error fetching posts: {data['error']['message']}")
        sys.exit(1)

    posts = data.get('data', [])
    if not posts:
        print("No Instagram posts found.")
        sys.exit(1)

    return posts


def get_ad_account():
    account_id = AD_ACCOUNT_ID if AD_ACCOUNT_ID.startswith('act_') else f'act_{AD_ACCOUNT_ID}'
    return AdAccount(account_id)


def create_campaign(account, post_index):
    """Create an engagement campaign for a boosted post."""
    params = {
        'name': f'Boosted IG Post #{post_index} - {time.strftime("%Y-%m-%d")}',
        'objective': 'OUTCOME_ENGAGEMENT',
        'status': 'PAUSED',
        'special_ad_categories': [],
    }
    campaign = account.create_campaign(params=params)
    campaign_id = campaign['id']
    print(f"  Created campaign: {campaign_id}")
    return campaign_id


def create_ad_set(account, campaign_id, post_index):
    """Create an ad set with SA city targeting and R200/day budget."""
    start_time = int(time.time()) + 600  # 10 minutes from now
    end_time = start_time + (BOOST_DURATION_DAYS * 24 * 60 * 60)

    params = {
        'name': f'Ad Set - Post #{post_index} - 7 Days - R200/day',
        'campaign_id': campaign_id,
        'daily_budget': DAILY_BUDGET_CENTS,
        'billing_event': 'IMPRESSIONS',
        'optimization_goal': 'POST_ENGAGEMENT',
        'bid_strategy': 'LOWEST_COST_WITHOUT_CAP',
        'targeting': {
            'geo_locations': {'custom_locations': TOP_SA_CITIES},
            'age_min': 18,
            'age_max': 40,
        },
        'start_time': start_time,
        'end_time': end_time,
        'status': 'PAUSED',
    }
    ad_set = account.create_ad_set(params=params)
    ad_set_id = ad_set['id']
    print(f"  Created ad set: {ad_set_id}")
    return ad_set_id


def create_ad_creative(account, instagram_media_id, post_index):
    """Create an ad creative from an existing Instagram post."""
    params = {
        'name': f'Creative - IG Post #{post_index} - {instagram_media_id}',
        'instagram_actor_id': INSTAGRAM_ACCOUNT_ID,
        'source_instagram_media_id': instagram_media_id,
    }
    creative = account.create_ad_creative(params=params)
    creative_id = creative['id']
    print(f"  Created creative: {creative_id}")
    return creative_id


def create_ad(account, ad_set_id, creative_id, post_index):
    """Create the ad."""
    params = {
        'name': f'Boosted Post Ad #{post_index}',
        'adset_id': ad_set_id,
        'creative': {'creative_id': creative_id},
        'status': 'PAUSED',
    }
    ad = account.create_ad(params=params)
    ad_id = ad['id']
    print(f"  Created ad: {ad_id}")
    return ad_id


def boost_post(account, post, index):
    """Run the full boost flow for a single Instagram post."""
    post_id = post['id']
    caption = post.get('caption', '')[:80].replace('\n', ' ')
    permalink = post.get('permalink', 'N/A')
    timestamp = post.get('timestamp', 'N/A')

    print(f"\n--- Post #{index}: {post_id} ---")
    print(f"  Posted: {timestamp}")
    print(f"  Link: {permalink}")
    print(f"  Caption: {caption}...")

    campaign_id = create_campaign(account, index)
    ad_set_id = create_ad_set(account, campaign_id, index)
    creative_id = create_ad_creative(account, post_id, index)
    ad_id = create_ad(account, ad_set_id, creative_id, index)

    return {
        'post_id': post_id,
        'permalink': permalink,
        'campaign_id': campaign_id,
        'ad_set_id': ad_set_id,
        'creative_id': creative_id,
        'ad_id': ad_id,
    }


def main():
    validate_env()
    FacebookAdsApi.init(access_token=ACCESS_TOKEN)
    account = get_ad_account()

    print("Fetching 3 most recent Instagram posts...")
    posts = get_recent_posts(count=3)
    print(f"Found {len(posts)} post(s) to boost.\n")

    results = []
    for i, post in enumerate(posts, start=1):
        try:
            result = boost_post(account, post, i)
            results.append(result)
        except Exception as e:
            print(f"  ERROR boosting post #{i} ({post.get('id')}): {e}")

    print("\n" + "=" * 60)
    print("BOOST SUMMARY")
    print("=" * 60)
    print(f"Budget: R{DAILY_BUDGET_CENTS / 100:.0f}/day per post x {BOOST_DURATION_DAYS} days")
    print(f"Targeting: Cape Town, Johannesburg, Pretoria, Durban, Soweto | Ages 18-40")
    print(f"Status: PAUSED — review in Ads Manager and activate when ready\n")

    for r in results:
        print(f"Post:     {r['permalink']}")
        print(f"Campaign: {r['campaign_id']}  |  Ad: {r['ad_id']}")
        print()

    print(f"Total max spend if activated: R{len(results) * (DAILY_BUDGET_CENTS / 100) * BOOST_DURATION_DAYS:.0f} over {BOOST_DURATION_DAYS} days")


if __name__ == '__main__':
    main()
