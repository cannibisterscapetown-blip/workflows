
import json
import shopify_api

SOURCE_PRODUCT_ID = "7973893505236"  # Cherry Pie

def main():
    print(f"Fetching metafields for product {SOURCE_PRODUCT_ID}...")
    metafields = shopify_api.get_product_metafields(SOURCE_PRODUCT_ID)
    
    if metafields:
        print("Metafields found:")
        print(json.dumps(metafields, indent=2))
        
        with open('cherry_pie_metafields.json', 'w') as f:
            json.dump(metafields, f, indent=2)
        print("Saved to cherry_pie_metafields.json")
    else:
        print("No metafields found or error occurred.")

if __name__ == "__main__":
    main()
