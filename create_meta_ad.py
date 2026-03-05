import os
import sys
import argparse
import time
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative

# Load environment variables
load_dotenv()

# Configuration from .env
ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
AD_ACCOUNT_ID = os.getenv('META_AD_ACCOUNT_ID')
PAGE_ID = os.getenv('META_PAGE_ID')
INSTAGRAM_ACCOUNT_ID = os.getenv('META_INSTAGRAM_ACCOUNT_ID') # Optional depending on setup

def initialize_api():
    """Initializes the Facebook Ads API."""
    if not ACCESS_TOKEN:
        print("Error: META_ACCESS_TOKEN not found in environment variables.")
        sys.exit(1)
    if not AD_ACCOUNT_ID:
        print("Error: META_AD_ACCOUNT_ID not found in environment variables.")
        sys.exit(1)
        
    FacebookAdsApi.init(access_token=ACCESS_TOKEN)

def get_ad_account():
    """Returns the Ad Account object."""
    account_id = AD_ACCOUNT_ID
    if not account_id.startswith('act_'):
        account_id = 'act_' + account_id
    return AdAccount(account_id)

def create_campaign(account):
    """Creates a campaign for engagement."""
    params = {
        'name': 'Boosted Instagram Post Workflow',
        'objective': 'OUTCOME_ENGAGEMENT',
        'status': 'PAUSED', # Start paused for safety
        'special_ad_categories': [],
        'is_adset_budget_sharing_enabled': False,
    }
    campaign = account.create_campaign(params=params)
    print(f"Created Campaign: {campaign['id']}")
    return campaign['id']

def create_ad_set(account, campaign_id):
    """Creates an ad set targeting broad audience for now."""
    # Start time slightly in the future
    start_time = int(time.time()) + 60*10 
    end_time = start_time + (7 * 24 * 60 * 60) # 7 days
    
    params = {
        'name': 'Ad Set - 7 Days Boost - R200/day',
        'campaign_id': campaign_id,
        'daily_budget': 20000, # 200 ZAR in cents (assuming currency is ZAR)
        'billing_event': 'IMPRESSIONS',
        'optimization_goal': 'POST_ENGAGEMENT',
        'bid_strategy': 'LOWEST_COST_WITHOUT_CAP',
        'targeting': {
            'geo_locations': {
                'countries': ['ZA'], # South Africa
            },
            'age_min': 18,
            'age_max': 65,
             # We can add more specific targeting here later
        },
        'start_time': start_time,
        'end_time': end_time,
        'status': 'PAUSED', 
    }
    ad_set = account.create_ad_set(params=params)
    print(f"Created Ad Set: {ad_set['id']}")
    return ad_set['id']

def create_ad_creative(account, instagram_post_id):
    """Creates an ad creative using the Instagram post."""
    # Ideally, we should fetch the object_story_id or similar.
    # For boosting an IG post, we often use the object_story_id which is typically page_id_post_id
    # However, for IG, it depends.
    # Let's assume we are passing the Instagram Media ID.
    
    params = {
        'name': f'Creative for Post {instagram_post_id}',
        'object_story_id': instagram_post_id, # This might need to be resolved to page_id_post_id or similar depending on the input
        'instagram_actor_id': PAGE_ID
    }
    
    # Note: creating creative for existing post might differ slightly based on if it's an IG or FB post.
    # For IG post passed as ID, we might need to verify if it's usable as object_story_id directly or via effective_object_story_id
    
    creative = account.create_ad_creative(params=params)
    print(f"Created Creative: {creative['id']}")
    return creative['id']

def create_ad(account, ad_set_id, creative_id):
    """Creates the ad."""
    params = {
        'name': 'Boosted Post Ad',
        'adset_id': ad_set_id,
        'creative': {'creative_id': creative_id},
        'status': 'PAUSED',
    }
    ad = account.create_ad(params=params)
    print(f"Created Ad: {ad['id']}")
    return ad['id']

def main():
    parser = argparse.ArgumentParser(description='Create Meta Ad for Instagram Post')
    parser.add_argument('--post_id', required=True, help='The Instagram Post ID to boost')
    args = parser.parse_args()
    
    initialize_api()
    account = get_ad_account()
    
    # 1. Create Campaign (or use existing if we wanted to be smarter, but let's create new for now as per simple workflow)
    campaign_id = create_campaign(account)
    
    # 2. Create Ad Set
    ad_set_id = create_ad_set(account, campaign_id)
    
    # 3. Create Creative
    try:
        creative_id = create_ad_creative(account, args.post_id)
        
        # 4. Create Ad
        ad_id = create_ad(account, ad_set_id, creative_id)
        print(f"Successfully created Ad Campaign! Ad ID: {ad_id}")
        
    except Exception as e:
        print(f"Error creating creative or ad: {e}")
        # Cleanup if possible?
        sys.exit(1)

if __name__ == '__main__':
    main()
