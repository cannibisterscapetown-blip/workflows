import shopify_api
from datetime import datetime, timedelta

def find_recent():
    print("🔍 Fetching recent drafts...")
    drafts = shopify_api.list_products(limit=50, status='draft')
    
    print(f"\nScanning {len(drafts)} drafts for 'Joint' or 'Moonstick'...")
    for p in drafts:
        title = p.get('title', '').lower()
        if 'joint' in title or 'moonstick' in title:
            print(f"\nID: {p['id']}")
            print(f"Title: {p['title']}")
            print(f"Created: {p['created_at']}")
            print(f"Tags: {p.get('tags')}")
            print(f"Body: {p.get('body_html', '')}")

if __name__ == "__main__":
    find_recent()
