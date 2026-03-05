#!/usr/bin/env python3
import sys
import shopify_api

print("🚀 Script starting...", flush=True)

try:
    print("🔍 Fetching latest products (Active)...", flush=True)
    products = shopify_api.list_products(limit=10, status='active')
    print(f"✅ Found {len(products)} active products.", flush=True)
    
    print("🔍 Fetching latest products (Draft)...", flush=True)
    drafts = shopify_api.list_products(limit=10, status='draft')
    print(f"✅ Found {len(drafts)} draft products.", flush=True)
    
    all_products = products + drafts
    # Sort by created_at descending if available
    all_products.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    print(f"\nScanning {len(all_products)} recent products for 'Joint'...", flush=True)
    
    count = 0
    for p in all_products:
        title = p.get('title', 'Unknown Title')
        pid = p.get('id', 'Unknown ID')
        print(f"Checking: {title} ({pid})", flush=True)
        
        if 'joint' in title.lower():
            count += 1
            print(f"\n🎯 MATCH FOUND [{count}]", flush=True)
            print(f"ID: {pid}", flush=True)
            print(f"Title: {title}", flush=True)
            print(f"Status: {p.get('status', 'Unknown')}", flush=True)
            print(f"Created: {p.get('created_at', 'Unknown')}", flush=True)
            desc_preview = p.get('body_html', '') or ''
            print(f"Description (HTML): {desc_preview[:100]}...", flush=True)
            print(f"Tags: {p.get('tags', [])}", flush=True)
            print("-" * 40, flush=True)
            
            if count >= 5: break

except Exception as e:
    print(f"❌ ERROR: {e}", file=sys.stderr, flush=True)
    import traceback
    traceback.print_exc()

print("🏁 Script finished.", flush=True)
