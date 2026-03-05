
from shopify_api import create_or_update_metafield
import json

# Sticky Rice
product_id = "9016555864276"

print("Attempting to update 'lineage' as list for Sticky Rice...")
try:
    # Value must be a JSON string of a list
    value = json.dumps(["Lemon Cherry Gelato x Permanent Marker"])
    type_ = "list.single_line_text_field"
    
    success = create_or_update_metafield(product_id, "my_fields", "lineage", value, value_type=type_)
    if success:
        print("✅ Success with list.single_line_text_field")
    else:
        print("❌ Failed with list.single_line_text_field")

except Exception as e:
    print(f"Exception: {e}")
