import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
INSTAGRAM_ID = os.getenv('META_INSTAGRAM_ACCOUNT_ID')
API_VERSION = 'v21.0' # Use a recent version

if not ACCESS_TOKEN or not INSTAGRAM_ID:
    print("Missing credentials.")
    sys.exit(1)

url = f"https://graph.facebook.com/{API_VERSION}/{INSTAGRAM_ID}/media"
params = {
    'access_token': ACCESS_TOKEN,
    'limit': 1,
    'fields': 'id,caption,permalink,media_type,timestamp'
}

try:
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'error' in data:
        print(f"API Error: {data['error']['message']}")
        sys.exit(1)
        
    if 'data' in data and len(data['data']) > 0:
        latest = data['data'][0]
        print(f"LATEST_POST_ID:{latest['id']}")
        print(f"Caption: {latest.get('caption', '')[:100]}...")
        print(f"Link: {latest.get('permalink')}")
    else:
        print("No media found.")

except Exception as e:
    print(f"Request failed: {e}")
