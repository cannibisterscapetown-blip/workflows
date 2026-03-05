# Cannibisters Shopify Integration - Usage Guide

## Overview

This guide explains how to use the Shopify API integration to manage products for Cannibisters.

## Available Tools

### 1. Python Scripts (Recommended when Python is available)

#### `shopify_api.py`
Core API module with functions for product management.

**Test connection:**
```bash
python3 shopify_api.py
```

#### `list_products.py`
List and search for products.

**Examples:**
```bash
# List all active products
python3 list_products.py

# Search for a specific strain
python3 list_products.py --search "Purple Punch"

# List draft products
python3 list_products.py --status draft

# Export to JSON
python3 list_products.py --json > products.json
```

#### `update_product.py`
Update product descriptions, tags, and metafields.

**Examples:**
```bash
# Show current product info
python3 update_product.py --product-name "Ready Whip" --show-current

# Update product with metafields
python3 update_product.py --product-id 123456 \
  --description "New description" \
  --tags "Indica, Relaxing, Evening" \
  --metafields metafields.json

# Update by name (will search)
python3 update_product.py --product-name "Purple Punch" \
  --metafields purple_punch_metafields.json
```

### 2. Shell Scripts (Alternative when Python has issues)

#### `list_products.sh`
List products using curl.

**Examples:**
```bash
# List all active products
./list_products.sh

# List draft products
./list_products.sh --status draft

# Save to file
./list_products.sh --output products.json
```

### 3. Direct curl Commands

**Get shop info:**
```bash
curl -X GET "https://cannibisters.myshopify.com/admin/api/2024-01/shop.json" \
  -H "X-Shopify-Access-Token: YOUR_SHOPIFY_ACCESS_TOKEN"
```

**List products:**
```bash
curl -X GET "https://cannibisters.myshopify.com/admin/api/2024-01/products.json?limit=10" \
  -H "X-Shopify-Access-Token: YOUR_SHOPIFY_ACCESS_TOKEN"
```

**Get product details:**
```bash
curl -X GET "https://cannibisters.myshopify.com/admin/api/2024-01/products/PRODUCT_ID.json" \
  -H "X-Shopify-Access-Token: YOUR_SHOPIFY_ACCESS_TOKEN"
```

**Get product metafields:**
```bash
curl -X GET "https://cannibisters.myshopify.com/admin/api/2024-01/products/PRODUCT_ID/metafields.json" \
  -H "X-Shopify-Access-Token: YOUR_SHOPIFY_ACCESS_TOKEN"
```

**Update product description:**
```bash
curl -X PUT "https://cannibisters.myshopify.com/admin/api/2024-01/products/PRODUCT_ID.json" \
  -H "X-Shopify-Access-Token: YOUR_SHOPIFY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product": {
      "id": PRODUCT_ID,
      "body_html": "<p>Your description here</p>",
      "tags": "tag1, tag2, tag3"
    }
  }'
```

**Create/Update metafield:**
```bash
curl -X POST "https://cannibisters.myshopify.com/admin/api/2024-01/products/PRODUCT_ID/metafields.json" \
  -H "X-Shopify-Access-Token: YOUR_SHOPIFY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "metafield": {
      "namespace": "custom",
      "key": "lineage",
      "value": "Ice Cream Cake x Whipped Cream",
      "type": "single_line_text_field"
    }
  }'
```

## Metafield JSON Format

Create a JSON file with your metafields:

**Example: `ready_whip_metafields.json`**
```json
{
  "lineage": "Ice Cream Cake x Whipped Cream (dessert-gas hybrid lineage; widely accepted cut)",
  "flowering_time": "8–9 weeks",
  "profile": "70/30 Indica-Dominant Hybrid",
  "height": "Medium",
  "stretch_percentage": "±35%",
  "average_thc_levels": "22–27%",
  "flavours": "Whipped cream, vanilla frosting, sugary dough, light gas",
  "effects": "Relaxed • Euphoric • Warm body buzz • Happy • Dreamy",
  "breeder": "Exotic Genetix (commonly credited lineage source)",
  "used_for": "Evening relaxation, dessert-flavour sessions, mellow creative flow",
  "plant_characteristics": "Dense frosty buds • Sweet dessert aroma • Indica-leaning structure",
  "plant_class": "Indica-dominant Flowering Plant",
  "plant_name": "Ready Whip",
  "suitable_space": "Indoor or Greenhouse"
}
```

## Workflow Integration

When Martine notifies you about a new product:

1. **Find the product:**
   ```bash
   python3 list_products.py --search "Product Name"
   ```

2. **View current details:**
   ```bash
   python3 update_product.py --product-name "Product Name" --show-current
   ```

3. **Create metafields JSON** using the template

4. **Update the product:**
   ```bash
   python3 update_product.py --product-name "Product Name" \
     --description "Your short description" \
     --tags "Indica, Relaxing, Dessert" \
     --metafields product_metafields.json
   ```

## API Reference

- **API Version:** 2024-01
- **Store URL:** cannibisters.myshopify.com
- **Rate Limits:** 2 requests/second (Shopify standard)
- **Documentation:** https://shopify.dev/docs/api/admin-rest

## Troubleshooting

**Python not working?**
- Use the shell scripts instead (`list_products.sh`)
- Or use curl commands directly

**Can't find product?**
- Check the product status (active, draft, archived)
- Search by partial name
- List all products and grep for the name

**Metafield not updating?**
- Verify the JSON format
- Check that the product ID is correct
- Ensure metafield namespace is "custom"
