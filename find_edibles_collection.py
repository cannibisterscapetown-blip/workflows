#!/usr/bin/env python3
import shopify_api

def find_edibles_collection():
    print("🔍 Searching for 'Edibles' collection...")
    collections = shopify_api.list_collections()
    
    for collection in collections:
        if 'edible' in collection['title'].lower():
            print(f"Found: {collection['title']}")
            print(f"ID: {collection['id']}")
            print(f"Handle: {collection.get('handle')}")
            print("-" * 30)

if __name__ == "__main__":
    find_edibles_collection()
