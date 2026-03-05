#!/usr/bin/env python3
"""
Update Black Cat strain on Shopify
"""

import subprocess
import sys

product = {
    "id": "9019110293716",
    "name": "Black Cat",
    "metafields_file": "black_cat_metafields.json",
    "tags": "New Strains, Indica, Relaxed, Sedative, Sour Fruit, Diesel, Gas",
    "description": "<p><strong>Black Cat</strong> is a potent indica-dominant hybrid born from the cross of Black Rose and Cheetah Piss. It delivers a heavy, sedative high that melts away tension and induces deep relaxation. Expect a bold profile of sour fruit and diesel with skunky undertones, making it the perfect choice for a peaceful evening and restorative sleep.</p><ul><li><strong>Lineage:</strong> Black Rose x Cheetah Piss</li><li><strong>Effects:</strong> Relaxed, Sedative, Euphoric</li></ul>"
}

print(f"🚀 Updating {product['name']} (ID: {product['id']})...")

cmd = [
    "python3", "update_product.py",
    "--product-id", product["id"],
    "--description", product["description"],
    "--tags", product["tags"],
    "--metafields", product["metafields_file"],
    "--yes"
]

try:
    subprocess.run(cmd, check=True)
    print(f"✅ Successfully updated {product['name']}")
except subprocess.CalledProcessError as e:
    print(f"❌ Failed to update {product['name']}: {e}")
    sys.exit(1)
