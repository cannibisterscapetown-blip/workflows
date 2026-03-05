
import shopify_api

product_id = "9071245623508"

# 1. Update Description
description = """
<p><strong>Canni Ltd Collection Joints Special x3</strong></p>
<p>Experience the finest from our exclusive Limited Collection with this special bundle offer! Choose any 3 of our premium Canni Ltd Collection joints.</p>
<p>Select from our current Limited Collection strains, including:</p>
<ul>
    <li>Astro Grape</li>
    <li>Chocolope</li>
    <li>Grandpa's Endgame</li>
    <li>Mad Ghost</li>
    <li>Purple Panda</li>
    <li>Sour Diesel D</li>
    <li>Supercheese</li>
</ul>
<p>Each joint is expertly rolled with our top-tier, indoor-grown flower, providing a luxurious smoking experience unique to our Limited Collection.</p>
<p><em>Note: Strain availability may vary. Please specify your choices in the order notes.</em></p>
"""

tags = [
    "Joints",
    "Bundle",
    "Special",
    "Limited Collection",
    "New Strains"
]

print(f"Updating description and tags for product {product_id}...")
shopify_api.update_product_description(product_id, description, tags)

# 2. Update Metafields
# Since this is a bundle, we use generic/descriptive values
metafields = {
    "my_fields": {
        "strain_type": "Hybrid",  # Defaulting to Hybrid as it's a mix
        "effects": "Various",
        "flavor": "Various",
        "lineage": "Cannibisters Limited Collection Strains",
        "thc_content": "High",
        "flowering_time": "N/A"
    }
}

print(f"Updating metafields for product {product_id}...")
shopify_api.update_product_metafields(product_id, metafields)

print("Done.")
