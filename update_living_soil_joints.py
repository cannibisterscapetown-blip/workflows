#!/usr/bin/env python3
"""
Update 5 New Living Soil Joints with premium descriptions and SEO tags.
"""

from shopify_api import get_product, update_product_description, create_or_update_metafield
import json

JOINT_DATA = {
    "9029349179604": {
        "name": "Bruce Banner",
        "lineage": "OG Kush x Strawberry Diesel",
        "profile": "60/40 Sativa-Dominant Hybrid",
        "flavours": "Sweet strawberry, earthy diesel, floral pine",
        "effects": "Euphoric • Uplifted • Creative • Relaxed • Energetic",
        "used_for": "Creative projects, daytime energy, mood enhancement, stress relief",
        "extra_desc": "Expect a powerful, monster-strength experience that balances cerebral euphoria with a gentle body relaxation, perfect for sparking inspiration."
    },
    "9029349638356": {
        "name": "Cherry Lime Reserve",
        "lineage": "Cherry Pie x Lime Skunk",
        "profile": "50/50 Balanced Hybrid",
        "flavours": "Tart cherry, zesty lime, sweet berry, citrus gas",
        "effects": "Balanced • Happy • Focused • Social • Tingly",
        "used_for": "Social gatherings, afternoon focus, anxiety relief, any-time use",
        "extra_desc": "A vibrant and zesty hybrid that offers a refreshingly balanced high, blending bright citrus notes with a calming, focused mental state."
    },
    "9029350129876": {
        "name": "Chimax",
        "lineage": "Indo-Kush Pheno-selection (Living Soil Elite)",
        "profile": "60/40 Indica-Dominant Hybrid",
        "flavours": "Tropical fruit, earthy musk, sweet spice, citrus undertones",
        "effects": "Relaxed • Euphoric • Dreamy • Calm • Sociable",
        "used_for": "Evening social sessions, stress relief, mild pain management, winding down",
        "extra_desc": "Grown in nutrient-rich living soil, Chimax delivers a smooth, terpene-heavy smoke that transitions from a physical calm to a dreamy mental ease."
    },
    "9029349015764": {
        "name": "Ghost Of Leroy",
        "lineage": "Ghost OG x Rare Dankness #1",
        "profile": "70/30 Indica-Dominant Hybrid",
        "flavours": "Lemony citrus, skunky earth, pungent fuel, herbal pine",
        "effects": "Ghostly Relaxed • Tingly • Giggly • Heavy Body • Happy",
        "used_for": "Deep relaxation, sleep support, chronic pain, late-night movie sessions",
        "extra_desc": "A hauntingly potent indica that wraps you in a thick blanket of relaxation, starting with a heady citrus buzz before settling into a blissful body stone."
    },
    "9029349900500": {
        "name": "Miami Blu",
        "lineage": "Miami Heat x Blue Dream (Select Pheno)",
        "profile": "80/20 Sativa-Dominant Hybrid",
        "flavours": "Tropical berry, sweet cream, citrus zest, floral breeze",
        "effects": "Energetic • Vivacious • Uplifted • Clear-headed • Motivated",
        "used_for": "Morning motivation, outdoor activities, creative flow, social buzz",
        "extra_desc": "Bring the energy of South Beach to your session with this vibrant sativa, offering a surge of clear-headed motivation and sweet, sun-soaked berry flavors."
    }
}

def update_joint(product_id, data):
    print(f"\n📦 Processing: {data['name']} (ID: {product_id})")
    
    # 1. Fetch current product to get existing description
    product = get_product(product_id)
    if not product:
        print(f"   ❌ Could not fetch product {product_id}")
        return
    
    old_body = product.get('body_html', '')
    
    # 2. Construct new description (append style)
    # Preservation rule: "Please dont remove the text that is currently in the descriptions, just add to it in a new line."
    new_desc = f"{old_body}<br><strong>{data['name']} Joint - Living Soil</strong><br>{data['extra_desc']}"
    
    tags = product.get('tags', '').split(', ')
    if "New Strains" not in tags: tags.append("New Strains")
    if "joints" not in tags: tags.append("joints")
    if "Living Soil" not in tags: tags.append("Living Soil")
    
    if update_product_description(product_id, new_desc, tags):
        print("   ✅ Description & Tags updated")
    else:
        print("   ❌ Failed to update Description & Tags")
        
    # 3. Update Metafields (my_fields)
    print("   Updating metafields...")
    mf_map = {
        "lineage": data['lineage'],
        "profile": data['profile'],
        "flavours": data['flavours'],
        "effects": data['effects'],
        "used_for": data['used_for']
    }
    
    success_count = 0
    for key, val in mf_map.items():
        if create_or_update_metafield(product_id, "my_fields", key, val):
            success_count += 1
            
    print(f"   ✅ {success_count}/5 metafields updated")
    
    # 4. Update SEO Meta Tags
    print("   Updating SEO Meta Tags...")
    seo_title = f"{data['name']} Joint | Living Soil Preroll | Cannibisters"
    seo_desc = f"Premium {data['name']} Living Soil Preroll. {data['profile']} with {data['flavours']} notes. {data['effects']} effects. Shop Cannibisters."[:158]
    
    if create_or_update_metafield(product_id, "global", "title_tag", seo_title):
        print(f"      ✅ SEO Title set")
    if create_or_update_metafield(product_id, "global", "description_tag", seo_desc):
        print(f"      ✅ SEO Description set")

def main():
    print("🚀 Starting bulk update for 5 Living Soil Joints...")
    print("=" * 60)
    
    for pid, data in JOINT_DATA.items():
        update_joint(pid, data)
        print("-" * 40)
        
    print("\n" + "=" * 60)
    print("🎉 Bulk update complete!")

if __name__ == "__main__":
    main()
