#!/usr/bin/env python3
"""
Update Animal Tsunami, Astro Grape, and Afghan Kush products on Shopify.
Created on Feb 12, 2026.
"""
from shopify_api import update_product_description, create_or_update_metafield, get_product
import sys

PRODUCTS = {
    "9072664772820": { # Animal Tsunami Joint
        "title": "Animal Tsunami Joint",
        "description": "Animal Tsunami is an indica-dominant powerhouse born from crossing Animal Cookies and Caramel Tsunami. It offers an intensely sweet and earthy flavor profile with heavy, blissful euphoria that settles into deep physical relaxation. Perfect for managing stress and tension after a long day.",
        "tags": ["Joint", "Pre-roll", "Indica", "Indica-Dominant", "70/30", "Relaxed", "Euphoric", "Happy", "Sweet", "Earthy", "Animal Cookies", "Caramel Tsunami", "New Strains"],
        "metafields": {
            "lineage": "Animal Cookies x Caramel Tsunami",
            "profile": "70/30 Indica-Dominant Hybrid",
            "flavours": "Sweet, earthy, caramel, herbal",
            "effects": "Relaxed • Euphoric • Happy • Calm",
            "used_for": "Evening relaxation, stress relief, pain management",
            "breeder": "Premium Genetics"
        }
    },
    "8944913187028": { # Animal Tsunami - Rosin Moonstick
        "title": "Animal Tsunami - Rosin Moonstick",
        "description": "Animal Tsunami is an indica-dominant powerhouse born from crossing Animal Cookies and Caramel Tsunami. This handcrafted Moonstick combines flower, rosin, and kief to deliver an intensely sweet and earthy experience with heavy, blissful euphoria. Perfect for connoisseur-level evening relaxation.",
        "tags": ["Moonstick", "Rosin", "Indica", "Indica-Dominant", "70/30", "Relaxed", "Euphoric", "Happy", "Sweet", "Earthy", "Cannabis Connoisseur"],
        "metafields": {
            "lineage": "Animal Cookies x Caramel Tsunami",
            "profile": "70/30 Indica-Dominant Hybrid",
            "flavours": "Sweet, earthy, caramel, rich hash notes",
            "effects": "Relaxed • Euphoric • Happy • Deeply Sedative",
            "used_for": "Premium evening relaxation, high-potency effects",
            "breeder": "Cannibisters Artisanal"
        }
    },
    "8822549676244": { # Astro Grape - Rosin Moonstick
        "title": "Astro Grape - Rosin Moonstick",
        "description": "Astro Grape delivers juicy grape flavors paired with dreamy calming effects in a potent handcrafted Moonstick. Crafted with premium rosin and kief, this indica-dominant hybrid provides smooth evening vibes and floaty feels—ideal for true cannabis connoisseurs seeking flavor and deep physical ease.",
        "tags": ["Moonstick", "Rosin", "Indica", "Indica-Dominant", "60/40", "Grape", "Calm", "Dreamy", "Euphoric", "Evening", "Fruity"],
        "metafields": {
            "lineage": "Grape Pie x Planet Dosi influence",
            "profile": "60/40 Indica-Dominant Hybrid",
            "flavours": "Juicy grape, sweet fruit, earthy undertones",
            "effects": "Calm • Dreamy • Euphoric • Floaty",
            "used_for": "Evening vibes, flavor chasing, relaxation",
            "breeder": "Cannibisters Artisanal"
        }
    },
    "8829780754644": { # Afghan Kush Moonstick
        "title": "Afghan Kush Moonstick",
        "description": "Afghan Kush is a legendary 100% Indica landrace strain from the Hindu Kush mountain range. This Moonstick offers rich, hashy flavor and heavy physical relaxation. Known for its potent sedative properties, it's the ultimate choice for deep rest and natural relief.",
        "tags": ["Moonstick", "Hashy", "Indica", "Pure Indica", "Sedative", "Relaxed", "Earthy", "Heavy", "Classic"],
        "metafields": {
            "lineage": "Landrace Afghan Indica",
            "profile": "100% Pure Indica",
            "flavours": "Hashy, earthy, spicy, woody",
            "effects": "Sedative • Relaxed • Sleepy • Heavy",
            "used_for": "Deep rest, chronic pain, insomnia relief",
            "breeder": "Ancestral Landrace"
        }
    }
}

def main():
    print("🚀 Updating Martine's New Joints & Moonsticks...")
    print("=" * 60)

    for pid, data in PRODUCTS.items():
        print(f"\n📦 Processing {data['title']} (ID: {pid})...")
        
        # Verify product exists
        product = get_product(pid)
        if not product:
            print(f"   ❌ Product not found! Skipping...")
            continue
            
        profile_text = data['metafields'].get('profile', '')
        # Ensure we keep the profile bolded at the top as per Cannibisters style
        full_description = f"<strong>{profile_text}</strong><br><br>{data['description'].strip()}"
        
        print(f"   Updating Description & Tags...")
        if update_product_description(pid, full_description, data['tags']):
             print(f"   ✅ Description & Tags updated")
        else:
             print(f"   ❌ Failed to update Description & Tags")
             
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
