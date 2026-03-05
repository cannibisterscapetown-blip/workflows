#!/usr/bin/env python3
"""
Update SuperCheese Preroll Joint - Living Soil with premium description and SEO tags.
"""

from shopify_api import get_product, update_product_description, create_or_update_metafield

PRODUCT_ID = "9029354684628"

DATA = {
    "name": "SuperCheese",
    "lineage": "Indo-Kush x Elite Cheese selection (Living Soil)",
    "profile": "80/20 Indica-Dominant Hybrid",
    "flavours": "Pungent cheese, creamy musk, earthy skunk, sweet funk",
    "effects": "Deeply Relaxed • Euphoric • Calm • Sleepy • Happy",
    "used_for": "Late-night relaxation, stress relief, physical comfort, sleep support",
    "extra_desc": "A heavy-hitting indica classic, SuperCheese is renowned for its intense, pungent aroma and deep, physical relaxation. Grown in nutrient-rich living soil, this joint delivers a smooth, savory smoke that melts away tension and leaves you in a state of blissful calm."
}

def main():
    print(f"🚀 Processing: {DATA['name']} (ID: {PRODUCT_ID})")
    print("=" * 60)
    
    # 1. Fetch current product to get existing description
    product = get_product(PRODUCT_ID)
    if not product:
        print(f"   ❌ Could not fetch product {PRODUCT_ID}")
        return
    
    old_body = product.get('body_html', '')
    
    # 2. Construct new description (append style)
    new_desc = f"{old_body}<br><strong>{DATA['name']} Joint - Living Soil</strong><br>{DATA['extra_desc']}"
    
    tags = product.get('tags', '').split(', ')
    tags_to_add = ["joints", "New Strains", "Living Soil", "Indica", "SuperCheese"]
    for t in tags_to_add:
        if t not in tags:
            tags.append(t)
    
    if update_product_description(PRODUCT_ID, new_desc, tags):
        print("   ✅ Description & Tags updated")
    else:
        print("   ❌ Failed to update Description & Tags")
        
    # 3. Update Metafields (my_fields)
    print("   Updating metafields...")
    mf_map = {
        "lineage": DATA['lineage'],
        "profile": DATA['profile'],
        "flavours": DATA['flavours'],
        "effects": DATA['effects'],
        "used_for": DATA['used_for']
    }
    
    success_count = 0
    for key, val in mf_map.items():
        if create_or_update_metafield(PRODUCT_ID, "my_fields", key, val):
            success_count += 1
            
    print(f"   ✅ {success_count}/5 metafields updated")
    
    # 4. Update SEO Meta Tags
    print("   Updating SEO Meta Tags...")
    seo_title = f"{DATA['name']} Joint | Living Soil Preroll | Cannibisters"
    seo_desc = f"Premium {DATA['name']} Living Soil Preroll. {DATA['profile']} with {DATA['flavours']} notes. {DATA['effects']} effects. Shop Cannibisters."[:158]
    
    if create_or_update_metafield(PRODUCT_ID, "global", "title_tag", seo_title):
        print(f"      ✅ SEO Title set")
    if create_or_update_metafield(PRODUCT_ID, "global", "description_tag", seo_desc):
        print(f"      ✅ SEO Description set")

    print("\n" + "=" * 60)
    print("🎉 Update complete!")

if __name__ == "__main__":
    main()
