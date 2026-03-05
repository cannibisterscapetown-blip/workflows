#!/usr/bin/env python3
"""
Add Metafields to Sodaze Products
Created on Feb 09, 2026.
"""

from shopify_api import create_or_update_metafield

# Product Data with Metafields
PRODUCTS = {
    "9068414009556": {  # Blueberry Lemonade Soda
        "title": "Sodaze Blueberry Lemonade Soda",
        "metafields": {
            "thc_content": "30mg",
            "volume": "250ml",
            "ingredients": "Real fruit, Natural flavours, Cannabis extract",
            "product_type": "Infused Beverage",
            "flavours": "Blueberry, Lemon, Sweet",
            "effects": "Relaxed • Happy • Euphoric",
            "used_for": "Relaxation, social enjoyment, stress relief",
            "preservative_free": "Yes",
            "artificial_colourants": "No"
        }
    },
    "9068414107860": {  # Lemon Meringue Soda
        "title": "Sodaze Lemon Meringue Soda",
        "metafields": {
            "thc_content": "30mg",
            "volume": "250ml",
            "ingredients": "Real fruit, Natural flavours, Cannabis extract",
            "product_type": "Infused Beverage",
            "flavours": "Lemon, Meringue, Sweet, Citrus",
            "effects": "Relaxed • Happy • Euphoric",
            "used_for": "Relaxation, social enjoyment, stress relief",
            "preservative_free": "Yes",
            "artificial_colourants": "No"
        }
    },
    "9068414173396": {  # Orange Creme Soda
        "title": "Sodaze Orange Creme Soda",
        "metafields": {
            "thc_content": "30mg",
            "volume": "250ml",
            "ingredients": "Real fruit, Natural flavours, Cannabis extract",
            "product_type": "Infused Beverage",
            "flavours": "Orange, Cream, Sweet, Citrus",
            "effects": "Relaxed • Happy • Euphoric",
            "used_for": "Relaxation, social enjoyment, stress relief",
            "preservative_free": "Yes",
            "artificial_colourants": "No"
        }
    }
}

def main():
    print("🚀 Adding Metafields to Sodaze Products...")
    print("=" * 60)
    
    for pid, data in PRODUCTS.items():
        print(f"\n📦 Processing {data['title']} (ID: {pid})...")
        print(f"   Updating metafields...")
        
        mf_success_count = 0
        for key, value in data['metafields'].items():
            if create_or_update_metafield(pid, "my_fields", key, value):
                mf_success_count += 1
                print(f"      ✅ Set {key}")
            else:
                print(f"      ❌ Failed on {key}")
        
        print(f"   ✅ {mf_success_count}/{len(data['metafields'])} metafields updated")
        print("-" * 40)

    print("\n" + "=" * 60)
    print("🎉 All metafields updated!")

if __name__ == "__main__":
    main()
