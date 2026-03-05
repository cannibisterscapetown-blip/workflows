#!/usr/bin/env python3
"""
Update Bucket Hat product description and tags
"""

from shopify_api import update_product_description, get_product

product_id = "9010347278548"

# Description inspired by Joint Holder but tailored for Bucket Hat
description = """<div>
<p><span>The </span><span>Cannibisters Bucket Hat</span><span> combines street style with premium comfort. </span><span>Featuring the iconic Cannibisters branding, this durable and stylish hat is perfect for sunny days or adding a laid-back vibe to your outfit. A must-have accessory for true Cannibisters fans who want to represent in style.</span></p>
</div>"""

tags = ["Accessories", "Apparel", "Hat", "Merchandise", "Cannibisters Gear", "Summer"]

print(f"🚀 Updating Bucket Hat (ID: {product_id})...")
print("="*80)

# 1. Update Description and Tags
if update_product_description(product_id, description, tags):
    print("✅ Description and tags updated successfully")
else:
    print("❌ Failed to update description and tags")

# 2. Verify update
print("\n🔍 Verifying update...")
updated_product = get_product(product_id)
if updated_product:
    print(f"   Current Tags: {updated_product.get('tags')}")
    print(f"   Description length: {len(updated_product.get('body_html', ''))} chars")
else:
    print("❌ Could not retrieve updated product for verification")

print("\n" + "="*80)
print("🏁 Update process finished!")
