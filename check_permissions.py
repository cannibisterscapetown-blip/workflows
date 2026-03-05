import os
import requests
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
API_VERSION = 'v21.0'

if not ACCESS_TOKEN:
    print("No Token")
    exit(1)

def check_debug_token():
    # Calling debug_token to see scopes and granularity
    # Need APP ID and APP SECRET usually, but let's try 'me/permissions'
    url = f"https://graph.facebook.com/{API_VERSION}/me/permissions"
    params = {'access_token': ACCESS_TOKEN}
    resp = requests.get(url, params=params)
    data = resp.json()
    if 'data' in data:
        print("Permissions:")
        for perm in data['data']:
            print(f"- {perm['permission']} ({perm['status']})")
    else:
        print(f"Error checking permissions: {data}")

def get_ad_accounts():
    url = f"https://graph.facebook.com/{API_VERSION}/me/adaccounts"
    params = {'access_token': ACCESS_TOKEN, 'fields': 'name,account_id'}
    resp = requests.get(url, params=params)
    data = resp.json()
    if 'data' in data:
        print(f"\nFound {len(data['data'])} Ad Accounts:")
        for acc in data['data']:
            print(f"- {acc['name']} (ID: {acc['account_id']})")
    else:
        print(f"\nError fetching ad accounts: {data}")

def get_pages():
    url = f"https://graph.facebook.com/{API_VERSION}/me/accounts"
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'name,id,instagram_business_account,access_token'
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    if 'data' in data:
        print(f"Found {len(data['data'])} Pages:")
        for page in data['data']:
            print(f"- Page: {page['name']} (ID: {page['id']})")
            
            # Try to get IG account using PAGE token
            page_token = page.get('access_token')
            if page_token:
                p_url = f"https://graph.facebook.com/{API_VERSION}/{page['id']}"
                p_params = {
                    'access_token': page_token,
                    'fields': 'instagram_business_account'
                }
                p_resp = requests.get(p_url, params=p_params)
                p_data = p_resp.json()
                if 'instagram_business_account' in p_data:
                    ig = p_data['instagram_business_account']
                    print(f"  -> [PageToken] Connected IG: {ig.get('id')}")
                else:
                    print(f"  -> [PageToken] No IG connection found. Resp: {p_data}")
            else:
                 if 'instagram_business_account' in page:
                    ig = page['instagram_business_account']
                    print(f"  -> Connected Instagram Business Account: ID {ig.get('id')}")
                 else:
                    print("  -> No Connected Instagram Business Account")
    else:
        print(f"Error fetching pages: {data}")

if __name__ == "__main__":
    check_debug_token()
    get_ad_accounts()
    print("")
    get_pages()
