import shopify_api

def find_draft_joints():
    print("🔍 Searching for draft products with 'Joint' or 'joints' tag or title...")
    drafts = shopify_api.list_products(limit=50, status='draft')
    
    matches = []
    for p in drafts:
        title = p.get('title', '').lower()
        tags = [t.lower() for t in (p.get('tags') or [])]
        if 'joint' in title or 'moonstick' in title or 'joint' in tags or 'joints' in tags:
            matches.append(p)
    
    print(f"\nFound {len(matches)} matching drafts:")
    for p in matches:
        print(f"\nID: {p['id']}")
        print(f"Title: {p['title']}")
        print(f"Tags: {p.get('tags')}")
        print(f"Body: {p.get('body_html', '')}")
        print("-" * 30)

if __name__ == "__main__":
    find_draft_joints()
