import os
import requests
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
INSTAGRAM_ID = '17841459113832751'
API_VERSION = 'v24.0'

if not ACCESS_TOKEN:
    print("No Token")
    exit(1)

def check_ig_direct():
    print(f"Checking IG ID: {INSTAGRAM_ID}")
    url = f"https://graph.facebook.com/{API_VERSION}/{INSTAGRAM_ID}"
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'id,username,name,ig_id'
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    print(f"Response: {data}")

if __name__ == "__main__":
    check_ig_direct()
