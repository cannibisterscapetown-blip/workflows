import os
import requests
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
AD_ACCOUNT_ID = os.getenv('META_AD_ACCOUNT_ID')
API_VERSION = 'v24.0' # Use latest

if not ACCESS_TOKEN:
    print("No Token")
    exit(1)

def check_ad_account_assets():
    print(f"Checking Ad Account: {AD_ACCOUNT_ID}")
    # Try different edges to see connected IG accounts
    edges = ['instagram_accounts', 'connected_instagram_accounts'] 
    
    for edge in edges:
        url = f"https://graph.facebook.com/{API_VERSION}/act_{AD_ACCOUNT_ID}/{edge}"
        params = {'access_token': ACCESS_TOKEN, 'fields': 'id,username'}
        resp = requests.get(url, params=params)
        print(f"--- Edge: {edge} ---")
        print(resp.json())

if __name__ == "__main__":
    check_ad_account_assets()
