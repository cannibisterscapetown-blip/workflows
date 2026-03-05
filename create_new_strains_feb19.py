#!/usr/bin/env python3
"""
Create New Strains - Pipe Dream & Wizard Fuel
Created on Feb 19, 2026.

Products are created as DRAFTS with:
- Type: Flower
- Vendor: Cannibisters Herbal Apothecasy
- Tags: New Strains + profile type
- Collections: New Strains + respective profile collection (Sativa / Hybrid)
- Price: 0.00 (to be updated when price is confirmed)
"""

import requests
import json
from typing import Optional
from shopify_api import BASE_URL, HEADERS, create_or_update_metafield, get_collection_by_title, add_product_to_collection

# ─────────────────────────────────────────────
# Product Data
# ─────────────────────────────────────────────

PRODUCTS = [
    {
        "title": "Pipe Dream",
        "description": (
            "Let your mind wander with Pipe Dream. <br><br>"
            "<strong>80/20 Sativa-Dominant</strong><br><br>"
            "A powerhouse sativa-dominant strain born from a distinguished lineage, "
            "Pipe Dream delivers an invigorating cerebral rush that sparks creativity, "
            "lifts the mood, and keeps you locked in a state of blissful focus. "
            "Expect vibrant citrus and tropical fruit flavours layered over a subtle earthy base, "
            "with a smooth, energising finish that makes it the perfect daytime companion.<br><br>"
            "Best enjoyed during creative sessions, social outings, or whenever you need a mood boost."
        ),
        "tags": [
            "Pipe Dream", "Sativa", "80/20", "Sativa-Dominant",
            "Citrus", "Tropical", "Earthy", "Uplifting",
            "Energetic", "Creative", "Focused", "Happy",
            "New Strains", "Flower"
        ],
        # Which profile collection to add to (in addition to New Strains)
        "profile_collection": "Sativa",
        "metafields": {
            "lineage": "Bubba Kush x OG Kush (widely accepted sativa-dominant phenotype)",
            "flowering_time": "9–10 weeks",
            "profile": "80/20 Sativa-Dominant",
            "height": "Tall",
            "stretch_percentage": "±60%",
            "average_thc_levels": "20–26%",
            "flavours": "Citrus, Tropical Fruit, Pine, Earthy",
            "effects": "Uplifted • Energetic • Creative • Focused • Happy",
            "used_for": "Daytime focus, creative sessions, mood boost, fatigue",
            "breeder": "Exotic Genetix (lineage)"
        }
    },
    {
        "title": "Wizard Fuel",
        "description": (
            "Step into something magical with Wizard Fuel. <br><br>"
            "<strong>50/50 Hybrid</strong><br><br>"
            "Wizard Fuel is a perfectly balanced hybrid that conjures a spellbinding blend "
            "of potent gas and sweet, dessert-like undertones. The high hits with an initial "
            "cerebral clarity before gracefully settling into a soothing full-body warmth — "
            "balancing mind and body in equal measure. Rich fuel, earthy pine, and a hint of "
            "sweet vanilla make every session an experience worth remembering.<br><br>"
            "Ideal for any time of day when you want the best of both worlds."
        ),
        "tags": [
            "Wizard Fuel", "Hybrid", "50/50", "Balanced Hybrid",
            "Gas", "Fuel", "Pine", "Vanilla", "Earthy",
            "Euphoric", "Relaxed", "Happy", "Creative",
            "New Strains", "Flower"
        ],
        "profile_collection": "Hybrid",
        "metafields": {
            "lineage": "Chemdawg x OG Kush (fuel-forward balanced hybrid lineage)",
            "flowering_time": "8–9 weeks",
            "profile": "50/50 Balanced Hybrid",
            "height": "Medium",
            "stretch_percentage": "±40%",
            "average_thc_levels": "22–27%",
            "flavours": "Diesel Fuel, Earthy Pine, Sweet Vanilla, Gas",
            "effects": "Euphoric • Happy • Relaxed • Creative • Calm",
            "used_for": "Stress relief, creative sessions, social gatherings, all-day use",
            "breeder": "Unknown / Multiple Breeders (widely cultivated pheno)"
        }
    }
]

VENDOR = "Cannibisters Herbal Apothecasy"
PRODUCT_TYPE = "Flower"
PRICE = "0.00"  # Price to be confirmed — update when received


# ─────────────────────────────────────────────
# Functions
# ─────────────────────────────────────────────

def create_product(product_data: dict) -> Optional[str]:
    """Create a new product as a DRAFT on Shopify."""
    title = product_data["title"]
    print(f"\n📦 Creating product: {title}...")

    payload = {
        "product": {
            "title": title,
            "body_html": product_data["description"],
            "vendor": VENDOR,
            "product_type": PRODUCT_TYPE,
            "tags": ", ".join(product_data["tags"]),
            "status": "draft",
            "published": False,
            "variants": [
                {
                    "price": PRICE,
                    "inventory_management": "shopify",
                    "inventory_policy": "continue",
                    "requires_shipping": True,
                    "taxable": True
                }
            ]
        }
    }

    try:
        response = requests.post(f"{BASE_URL}/products.json", headers=HEADERS, json=payload)
        response.raise_for_status()
        new_product = response.json()["product"]
        product_id = str(new_product["id"])
        print(f"   ✅ Created as DRAFT (ID: {product_id})")
        return product_id
    except Exception as e:
        print(f"   ❌ Error creating product: {e}")
        if hasattr(e, "response") and e.response:
            print(f"   Response: {e.response.text}")
        return None


def set_metafields(product_id: str, metafields: dict) -> None:
    """Set all my_fields metafields for a product."""
    print(f"   Setting metafields...")
    success = 0
    for key, value in metafields.items():
        if create_or_update_metafield(product_id, "my_fields", key, value):
            success += 1
            print(f"      ✅ {key}")
        else:
            print(f"      ❌ Failed: {key}")
    print(f"   ✅ {success}/{len(metafields)} metafields set")


def assign_to_collections(product_id: str, product_title: str, profile_collection_name: str) -> None:
    """Add product to 'New Strains' and its profile collection."""
    collections_to_add = ["New Strains", profile_collection_name]

    for col_name in collections_to_add:
        print(f"   📁 Looking up collection: '{col_name}'...")
        col = get_collection_by_title(col_name)
        if col:
            col_id = str(col["id"])
            add_product_to_collection(col_id, product_id)
        else:
            print(f"   ⚠️  Collection '{col_name}' not found — skipping. You may need to add manually.")


def main():
    print("🚀 Creating New Strains: Pipe Dream & Wizard Fuel")
    print("=" * 60)

    created = {}

    for product_data in PRODUCTS:
        # Step 1: Create product
        product_id = create_product(product_data)
        if not product_id:
            print(f"   ❌ Skipping remaining steps for {product_data['title']}")
            continue

        # Step 2: Set metafields
        set_metafields(product_id, product_data["metafields"])

        # Step 3: Assign to collections
        assign_to_collections(product_id, product_data["title"], product_data["profile_collection"])

        created[product_data["title"]] = product_id
        print(f"   🎉 {product_data['title']} done!\n")
        print("-" * 60)

    print("\n" + "=" * 60)
    print("✅ All done! Summary:")
    for name, pid in created.items():
        print(f"   • {name}: https://admin.shopify.com/store/cannibisters/products/{pid}")
    print("\n⚠️  Price is set to R0.00 — update once confirmed.")
    print("⚠️  Products are DRAFT — publish once images and price are added.")


if __name__ == "__main__":
    main()
