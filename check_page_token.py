import os
import requests
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
API_VERSION = 'v21.0'

if not ACCESS_TOKEN:
    print("No Token")
    exit(1)

def check_me():
    url = f"https://graph.facebook.com/{API_VERSION}/me"
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'id,name,instagram_business_account'
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    print(f"ME: {data}")

if __name__ == "__main__":
    check_me()
