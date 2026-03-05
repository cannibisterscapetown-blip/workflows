#!/usr/bin/env python3
"""
Optimize Chocolope SEO and Descriptions on Shopify.
"""

from shopify_api import update_product_description, create_or_update_metafield

PRODUCT_ID = "9029351997652"

# Refined premium description
DESCRIPTION = """
Chocolope is a legendary sativa-dominant classic that pays homage to the beloved Chocolate strains of the 1980s. By crossing Chocolate Thai with Cannalope Haze, breeders created a masterpiece that balances nostalgic, rich cocoa aromas with modern sativa vigor. 

This elite cultivar is celebrated for its clear-headed, energetic buzz that fuels creativity and keeps you motivated throughout the day. With its unique profile of roasted coffee and dark cocoa, Chocolope offers a smooth and inspired journey for the discerning connoisseur.
"""

# SEO Meta Tags
SEO_TITLE = "Chocolope | Cannibisters Limited Collection | Sativa Flower"
SEO_DESCRIPTION = "Experience the nostalgia of Chocolope, a 95/5 sativa classic from the Cannibisters Limited Collection. Rich cocoa notes with clear-headed creative energy. Shop now."

TAGS = ["New Strains", "Limited Collection", "Flower", "Sativa", "Chocolope", "Creative", "Energizing", "Cocoa", "Coffee"]

def main():
    print(f"🚀 Optimizing SEO and Description for Chocolope (ID: {PRODUCT_ID})...")
    print("=" * 60)
    
    # 1. Update Description and Tags
    profile_text = "95/5 Sativa-Dominant Hybrid"
    full_description = f"<strong>{profile_text}</strong><br><br>{DESCRIPTION.strip()}"
    
    desc_success = update_product_description(PRODUCT_ID, full_description, TAGS)
    if desc_success:
        print(f"   ✅ Description & Tags updated")
    else:
        print(f"   ❌ Failed to update Description & Tags")
        
    # 2. Update SEO Meta Tags (metafields)
    print(f"   Updating SEO Meta Tags...")
    
    # Title Tag
    if create_or_update_metafield(PRODUCT_ID, "global", "title_tag", SEO_TITLE):
        print(f"      ✅ SEO Title Tag set: {SEO_TITLE}")
    else:
        print(f"      ❌ Failed to set SEO Title Tag")
        
    # Description Tag
    if create_or_update_metafield(PRODUCT_ID, "global", "description_tag", SEO_DESCRIPTION):
        print(f"      ✅ SEO Meta Description set")
    else:
        print(f"      ❌ Failed to set SEO Meta Description")

    print("\n" + "=" * 60)
    print("🎉 SEO Optimization complete!")

if __name__ == "__main__":
    main()
