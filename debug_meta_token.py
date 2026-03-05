import os
import sys
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi

load_dotenv()

ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
INSTAGRAM_ID = os.getenv('META_INSTAGRAM_ACCOUNT_ID')

if not ACCESS_TOKEN:
    print("No Token")
    sys.exit(1)

FacebookAdsApi.init(access_token=ACCESS_TOKEN)
api = FacebookAdsApi.get_default_api()

print("--- DEBUG INFO ---")
try:
    # 1. Who am I?
    me = api.call('GET', 'me', params={'fields': 'id,name,permissions'})
    data = me.json()
    print(f"ME: Name={data.get('name')}, ID={data.get('id')}")
    # print(f"Permissions: {data.get('permissions')}") # Might be verbose

    # 2. Try to access the IG User directly
    print(f"\nTargeting IG User: {INSTAGRAM_ID}")
    try:
        resp = api.call('GET', f'{INSTAGRAM_ID}', params={'fields': 'id,username,name'})
        print(f"IG User Found: {resp.json()}")
        
        # 3. Get Media
        print("\nFetching Media...")
        media_resp = api.call('GET', f'{INSTAGRAM_ID}/media', params={'limit': 1, 'fields': 'id,caption,permalink'})
        data = media_resp.json()
        if 'data' in data and len(data['data']) > 0:
            post = data['data'][0]
            print(f"LATEST_POST_ID:{post['id']}")
            print(f"Caption: {post.get('caption')}")
        else:
            print("No media found (empty data).")

    except Exception as e:
        print(f"Failed to access IG User: {e}")

except Exception as e:
    print(f"General API Error: {e}")
