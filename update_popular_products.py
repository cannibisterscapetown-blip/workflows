#!/usr/bin/env python3
# Updates Popular Products section in Klaviyo campaign template
# Products: Superberry Crush, Backwood Natural Cigar leaf, Blueberry Gary
import requests, os

KLAVIYO_API_KEY = os.environ.get('KLAVIYO_API_KEY', 'pk_bbe3e99a1e058ba1b45decc3d66d9575ac')
MSG_ID = '01KKV9756FFVM81A7BR2VQTXG8'
HEADERS = {
    'Authorization': f'Klaviyo-API-Key {KLAVIYO_API_KEY}',
    'revision': '2024-10-15',
    'Content-Type': 'application/json',
}

resp = requests.get(f'https://a.klaviyo.com/api/campaign-messages/{MSG_ID}/template/', headers=HEADERS)
html = resp.json()['data']['attributes']['html']
editor_type = resp.json()['data']['attributes'].get('editor_type', 'CODE')

# Products: super-berry-crush, backwood-natural-cigar-papers (sale), blueberry-muffin
