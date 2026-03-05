import os
import sys
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adcreative import AdCreative

load_dotenv()
ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
AD_ACCOUNT_ID = os.getenv('META_AD_ACCOUNT_ID')
INSTAGRAM_ID = '17841459113832751'
POST_ID = '18121880863493356'

FacebookAdsApi.init(access_token=ACCESS_TOKEN)

account = AdAccount('act_' + AD_ACCOUNT_ID)

print(f"Testing Creative Creation on Account {AD_ACCOUNT_ID}")
print(f"Post: {POST_ID}")
print(f"Actor: {INSTAGRAM_ID}")

params = {
    'name': 'Test Creative Debug',
    'object_story_id': POST_ID,
    'instagram_actor_id': INSTAGRAM_ID
}

try:
    creative = account.create_ad_creative(params=params)
    print(f"SUCCESS: Created Creative {creative['id']}")
except Exception as e:
    print(f"FAILED: {e}")
