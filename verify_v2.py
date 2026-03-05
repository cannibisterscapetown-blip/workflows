import shopify_api
import sys

pids = ["9072664772820", "8944913187028", "8822549676244", "8829780754644"]

print("🔍 FINAL VERIFICATION REPORT", flush=True)
print("="*40, flush=True)

for pid in pids:
    p = shopify_api.get_product(pid)
    if not p:
        print(f"❌ {pid} NOT FOUND", flush=True)
        continue
    
    print(f"\nProduct: {p['title']} ({p['id']})", flush=True)
    tags = p.get('tags', '')
    has_meta = "Yes" if p.get('metafields') else "No"
    img_count = len(p.get('images', []))
    
    print(f"   Tags: {tags}", flush=True)
    print(f"   Metafields Loaded: {has_meta}", flush=True)
    print(f"   Images: {img_count}", flush=True)
    if img_count > 0:
        print(f"   Cover Image Position 1: {p['images'][0]['src'][:80]}...", flush=True)
    
    # Check for profile in description
    if "<strong>" in (p.get('body_html', '') or ''):
        print("   ✅ Profile (bold) found in description", flush=True)
    else:
        print("   ⚠️ Profile NOT found in description!", flush=True)

print("\n"+"="*40, flush=True)
