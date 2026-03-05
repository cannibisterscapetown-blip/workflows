import shopify_api
import os

# Mapping of Product Name -> Image Filename
uploads = {
    "Northern Grape Fruit": "uploaded_image_1764921898591.png",
    "Ready Whip": "uploaded_image_1764921909698.png",
    "Platinum Dosi": "uploaded_image_1764921917965.png"
}

base_path = "/Users/norton/.gemini/antigravity/brain/c0ee51dd-8b6c-41fb-b85e-fbe5456b6b48"

for product_name, filename in uploads.items():
    print(f"Processing {product_name}...")
    products = shopify_api.search_products(product_name)
    
    if not products:
        print(f"❌ Product '{product_name}' not found.")
        continue
        
    product_id = products[0]['id']
    image_path = os.path.join(base_path, filename)
    
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        continue
        
    print(f"Uploading {filename} to {product_name} ({product_id})...")
    shopify_api.upload_product_image(product_id, image_path)
