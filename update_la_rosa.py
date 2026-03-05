#!/usr/bin/env python3
"""
Update LA Rosa (Martine New Strain)
Created on Feb 09, 2026.
"""

from shopify_api import update_product_description, create_or_update_metafield, get_product

# Product Data Configuration
PRODUCTS = {
    "9068135481556": { # LA Rosa
        "title": "LA Rosa",
        "description": "Experience the exotic allure of LA Rosa. <br><br><strong>50/50 Hybrid</strong><br><br>This perfectly balanced strain combines sweet floral notes with earthy undertones and a hint of citrus. LA Rosa delivers a smooth, uplifting high that promotes creativity and relaxation in equal measure, making it ideal for any time of day.<br><br>A versatile strain that adapts to your needs.",
        "tags": ["LA Rosa", "Hybrid", "50/50", "Floral", "Sweet", "Earthy", "Citrus", "Euphoric", "Happy", "Creative", "Relaxed", "Limited Collection", "New Strains", "Cannibisters Limited Collection"],
        "metafields": {
            "lineage": "LA Confidential x Unknown Sativa",
            "flowering_time": "8-9 Weeks",
            "profile": "50/50 Hybrid",
            "height": "Medium",
            "stretch_percentage": "Medium (150%)",
            "average_thc_levels": "18-22%",
            "flavours": "Sweet Floral, Earthy, Citrus, Pine",
            "effects": "Euphoric • Happy • Creative • Relaxed",
            "used_for": "Stress, anxiety, depression, pain relief",
            "breeder": "Unknown"
        }
    }
}

def main():
    print("🚀 Updating LA Rosa (Feb 09)...")
    print("=" * 60)

    for pid, data in PRODUCTS.items():
        print(f"\n📦 Processing {data['title']} (ID: {pid})...")
        
        # Verify product exists
        product = get_product(pid)
        if not product:
            print(f"   ❌ Product not found! Skipping...")
            continue
            
        # 1. Update Description and Tags
        full_description = data['description']
        
        print(f"   Updating Description & Tags...")
        if update_product_description(pid, full_description, data['tags']):
             print(f"   ✅ Description & Tags updated")
        else:
             print(f"   ❌ Failed to update Description & Tags")
             
        # 2. Update Metafields
        print(f"   Updating metafields...")
        mf_success_count = 0
        for key, value in data['metafields'].items():
            if create_or_update_metafield(pid, "my_fields", key, value):
                mf_success_count += 1
                print(f"      ✅ Set {key}")
            else:
                print(f"      ❌ Failed on {key}")
        print(f"   ✅ {mf_success_count}/{len(data['metafields'])} metafields updated")

    print("\n" + "=" * 60)
    print("🎉 All updates finished!")

if __name__ == "__main__":
    main()
