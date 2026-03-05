
import json
import shopify_api

TARGET_PRODUCT_ID = "8374576021716"  # Cherry Pie Joint
SOURCE_METAFIELDS_FILE = "cherry_pie_metafields.json"

# Define types for known keys
KEY_TYPES = {
    "effects": "list.single_line_text_field",
    "lineage": "list.single_line_text_field",
    "flowering_time": "list.single_line_text_field", # inferred from ["..."]
    "breeder": "list.single_line_text_field",
    "profile": "single_line_text_field",
    "height": "single_line_text_field",
    "stretch_percentage": "single_line_text_field",
    "average_thc_levels": "single_line_text_field",
    "flavours": "single_line_text_field", # string in source
    "used_for": "single_line_text_field",
    "plant_characteristics": "list.metaobject_reference", # If we were copying shopify namespace
    "plant_name": "list.metaobject_reference",
    "suitable_space": "list.metaobject_reference"
}

def main():
    print(f"Loading metafields from {SOURCE_METAFIELDS_FILE}...")
    try:
        with open(SOURCE_METAFIELDS_FILE, 'r') as f:
            all_metafields = json.load(f)
            
        if 'my_fields' in all_metafields:
            fields = all_metafields['my_fields']
            
            print(f"Updating product {TARGET_PRODUCT_ID} with typed metafields...")
            
            success_count = 0
            fail_count = 0
            
            for key, value in fields.items():
                # Determine type
                mf_type = KEY_TYPES.get(key, "single_line_text_field")
                
                # Special check: if value looks like a list but type says string, or vice versa
                # But we trust our mapping.
                
                print(f"Updating {key} as {mf_type}...")
                
                # We use create_or_update_metafield directly so we can pass type
                result = shopify_api.create_or_update_metafield(
                    TARGET_PRODUCT_ID,
                    "my_fields",
                    key,
                    value,
                    value_type=mf_type
                )
                
                if result:
                    print(f"✅ {key} updated")
                    success_count += 1
                else:
                    print(f"❌ {key} failed")
                    fail_count += 1
                    
            print(f"\nDone. Success: {success_count}, Fail: {fail_count}")
            
        else:
            print("❌ 'my_fields' namespace not found.")
            
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
