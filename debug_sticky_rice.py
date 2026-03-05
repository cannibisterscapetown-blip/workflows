
from shopify_api import create_or_update_metafield
import requests

# Sticky Rice
product_id = "9016555864276"

print("Attempting to update 'lineage' for Sticky Rice...")
try:
    # Try with single_line_text_field
    success = create_or_update_metafield(product_id, "my_fields", "lineage", "Lemon Cherry Gelato x Permanent Marker")
    if success:
        print("✅ Success with single_line_text_field")
    else:
        print("❌ Failed with single_line_text_field")
        
        # Try with multi_line_text_field
        print("Attempting with multi_line_text_field...")
        success = create_or_update_metafield(product_id, "my_fields", "lineage", "Lemon Cherry Gelato x Permanent Marker", value_type="multi_line_text_field")
        if success:
             print("✅ Success with multi_line_text_field")
        else:
             print("❌ Failed with multi_line_text_field")

except Exception as e:
    print(f"Exception: {e}")
