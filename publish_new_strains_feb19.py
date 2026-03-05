#!/usr/bin/env python3
"""
Set price (R190) and publish Pipe Dream & Wizard Fuel to all sales channels.
Created Feb 19, 2026.
"""

from shopify_api import graphql_query, update_product_price

PRICE = 190.00

PRODUCTS = {
    "9078149382356": "Pipe Dream",
    "9078149415124": "Wizard Fuel",
}

# Sales channels to publish to (all channels)
CHANNELS = [
    "gid://shopify/Publication/80986341588",  # Online Store
    "gid://shopify/Publication/80986374356",  # Facebook & Instagram
    "gid://shopify/Publication/86118662356",  # Facebook & Instagram
    "gid://shopify/Publication/86118695124",  # Facebook & Instagram
    "gid://shopify/Publication/92670623956",  # Facebook & Instagram
    "gid://shopify/Publication/80986407124",  # Google & YouTube
    "gid://shopify/Publication/80986439892",  # Buy Button
    "gid://shopify/Publication/81254809812",  # Point of Sale
    "gid://shopify/Publication/83172589780",  # Point of Sale
    "gid://shopify/Publication/126995890388", # Snapchat Ads
    "gid://shopify/Publication/181273952468", # Canni Agent
]

MUTATION = """
mutation publishablePublish($id: ID!, $input: [PublicationInput!]!) {
  publishablePublish(id: $id, input: $input) {
    publishable {
      publishedOnCurrentPublication
    }
    userErrors {
      field
      message
    }
  }
}
"""

def main():
    print("🚀 Publishing Pipe Dream & Wizard Fuel to Online Store + POS")
    print("=" * 60)

    for pid, name in PRODUCTS.items():
        gid = f"gid://shopify/Product/{pid}"

        # Step 1: Set price to R190
        print(f"\n💰 Setting price for {name}...")
        if update_product_price(pid, PRICE):
            print(f"   ✅ Price set to R{PRICE:.0f}")
        else:
            print(f"   ❌ Failed to set price")

        # Step 2: Publish to all channels
        print(f"📢 Publishing {name} to all channels...")
        variables = {
            "id": gid,
            "input": [{"publicationId": ch} for ch in CHANNELS],
        }
        result = graphql_query(MUTATION, variables)
        data = (result.get("data") or {}).get("publishablePublish") or {}
        errors = data.get("userErrors", [])

        if errors:
            print(f"   ❌ Errors:")
            for e in errors:
                print(f"      • {e['field']}: {e['message']}")
        else:
            print(f"   ✅ {name} is now live on Online Store + Point of Sale")

    print("\n" + "=" * 60)
    print("✅ Done! Both products published.")
    print("   • Pipe Dream  → https://admin.shopify.com/store/cannibisters/products/9078149382356")
    print("   • Wizard Fuel → https://admin.shopify.com/store/cannibisters/products/9078149415124")
    print("\n⚠️  Remember to update prices and add photos when ready.")


if __name__ == "__main__":
    main()
