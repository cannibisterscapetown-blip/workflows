#!/usr/bin/env python3
"""
Update Chocolope - Cannibisters Limited Collection product on Shopify.
"""

from shopify_api import update_product_description, create_or_update_metafield, upload_product_image
import os

PRODUCT_ID = "9029351997652"

# Premium description in Martine's style
DESCRIPTION = """Chocolope is a legendary sativa-dominant classic that pays homage to the beloved Chocolate strains of the 1980s. By crossing Chocolate Thai with Cannalope Haze, breeders created a masterpiece that balances nostalgic, rich cocoa aromas with modern sativa vigor. This strain is celebrated for its clear-headed, energetic buzz that fuels creativity and keeps you motivated throughout the day."""

TAGS = ["New Strains", "Limited Collection", "Flower", "Sativa", "Chocolope", "Creative", "Energizing"]

METAFIELDS = {
    "lineage": "Chocolate Thai x Cannalope Haze (nostalgic sativa classic)",
    "flowering_time": "9–10 weeks",
    "profile": "95/5 Sativa-Dominant Hybrid",
    "height": "Tall",
    "stretch_percentage": "±60%",
    "average_thc_levels": "18–22%",
    "flavours": "Roasted coffee, dark cocoa, sweet haze, earthy spice",
    "effects": "Creative • Energetic • Uplifted • Happy • Focused",
    "used_for": "Daytime productivity, creative focus, social energy, morning motivation"
}

def main():
    print(f"🚀 Updating Chocolope - Cannibisters Limited Collection (ID: {PRODUCT_ID})...")
    print("=" * 60)
    
    # 1. Update Description and Tags
    # Prepend Profile text directly in bold to match Martine's style
    profile_text = METAFIELDS['profile']
    full_description = f"<strong>{profile_text}</strong><br><br>{DESCRIPTION}"
    
    desc_success = update_product_description(PRODUCT_ID, full_description, TAGS)
    if desc_success:
        print(f"   ✅ Description & Tags updated")
    else:
        print(f"   ❌ Failed to update Description & Tags")
        
    # 2. Update Metafields
    print(f"   Updating metafields...")
    mf_success_count = 0
    for key, value in METAFIELDS.items():
        if create_or_update_metafield(PRODUCT_ID, "my_fields", key, value):
            mf_success_count += 1
        else:
            print(f"      ❌ Failed on {key}")
            
    print(f"   ✅ {mf_success_count}/{len(METAFIELDS)} metafields updated")

    # 3. Upload Image if found
    image_path = "Chocolope .png"
    if os.path.exists(image_path):
        print(f"\n📸 Found image: {image_path}. Uploading...")
        if upload_product_image(PRODUCT_ID, image_path):
             print(f"   ✅ Successfully uploaded {image_path}")
        else:
             print(f"   ❌ Failed to upload {image_path}")
    else:
        print(f"\n⚠️  Image '{image_path}' not found in root directory.")

    print("\n" + "=" * 60)
    print("🎉 Update process finished!")

if __name__ == "__main__":
    main()
