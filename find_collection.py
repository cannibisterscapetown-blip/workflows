#!/usr/bin/env python3
"""
Find Collection ID by title.
"""

from shopify_api import BASE_URL, HEADERS
import requests
import json

def find_collection(search_term):
    print(f"🔍 Searching for collection: '{search_term}'...")
    
    # Check Custom Collections
    url = f"{BASE_URL}/custom_collections.json?limit=250"
    while url:
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code != 200:
            print(f"Error fetching custom collections: {resp.status_code}")
            break
            
        data = resp.json()
        for c in data.get('custom_collections', []):
            if search_term.lower() in c['handle'].lower() or search_term.lower() in c['title'].lower():
                print(f"FOUND (Custom): {c['id']} | {c['title']} | Handle: {c['handle']}")
                
        link = resp.headers.get('Link')
        url = None
        if link and 'rel="next"' in link:
            url = link.split(';')[0].strip('< >')

    # Check Smart Collections
    url = f"{BASE_URL}/smart_collections.json?limit=250"
    while url:
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code != 200:
            print(f"Error fetching smart collections: {resp.status_code}")
            break
            
        data = resp.json()
        for c in data.get('smart_collections', []):
            if search_term.lower() in c['handle'].lower() or search_term.lower() in c['title'].lower():
                print(f"FOUND (Smart): {c['id']} | {c['title']} | Handle: {c['handle']}")

        link = resp.headers.get('Link')
        url = None
        if link and 'rel="next"' in link:
            url = link.split(';')[0].strip('< >')

if __name__ == "__main__":
    find_collection("coffee-beverages-snacks")
