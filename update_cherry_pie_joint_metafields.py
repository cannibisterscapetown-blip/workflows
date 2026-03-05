
import json
import shopify_api

TARGET_PRODUCT_ID = "8374576021716"  # Cherry Pie Joint
SOURCE_METAFIELDS_FILE = "cherry_pie_metafields.json"

def main():
    print(f"Loading metafields from {SOURCE_METAFIELDS_FILE}...")
    try:
        with open(SOURCE_METAFIELDS_FILE, 'r') as f:
            all_metafields = json.load(f)
            
        # Extract only 'my_fields' namespace
        if 'my_fields' in all_metafields:
            fields_to_update = {'my_fields': all_metafields['my_fields']}
            
            print(f"Updating product {TARGET_PRODUCT_ID} with metafields...")
            print(json.dumps(fields_to_update, indent=2))
            
            success = shopify_api.update_product_metafields(TARGET_PRODUCT_ID, fields_to_update)
            
            if success:
                print("✅ Metafields updated successfully!")
            else:
                print("❌ Failed to update metafields.")
        else:
            print("❌ 'my_fields' namespace not found in source file.")
            
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
