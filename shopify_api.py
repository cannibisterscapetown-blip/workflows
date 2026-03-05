#!/usr/bin/env python3
"""
Shopify API Integration for Cannibisters
Provides core functionality for reading and writing product data via Shopify Admin API
"""

import os
import requests
import json
import base64
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SHOPIFY_ACCESS_TOKEN = os.getenv('SHOPIFY_ACCESS_TOKEN')
SHOPIFY_STORE_URL = os.getenv('SHOPIFY_STORE_URL')

if not SHOPIFY_ACCESS_TOKEN or not SHOPIFY_STORE_URL:
    raise ValueError("Missing SHOPIFY_ACCESS_TOKEN or SHOPIFY_STORE_URL in .env file")

API_VERSION = '2024-01'
BASE_URL = f'https://{SHOPIFY_STORE_URL}/admin/api/{API_VERSION}'

HEADERS = {
    'X-Shopify-Access-Token': SHOPIFY_ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

def graphql_query(query: str, variables: Optional[Dict] = None) -> Dict:
    """
    Execute a Shopify GraphQL query
    """
    url = f'https://{SHOPIFY_STORE_URL}/admin/api/{API_VERSION}/graphql.json'
    data = {'query': query}
    if variables:
        data['variables'] = variables
        
    try:
        response = requests.post(url, headers=HEADERS, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ GraphQL error: {e}")
        if hasattr(e, 'response') and e.response is not None:
             print(f"   Response: {e.response.text}")
        return {}


def test_connection() -> bool:
    """Test the Shopify API connection"""
    try:
        response = requests.get(f'{BASE_URL}/shop.json', headers=HEADERS)
        response.raise_for_status()
        shop_data = response.json()
        print(f"✅ Successfully connected to: {shop_data['shop']['name']}")
        print(f"   Store URL: {shop_data['shop']['domain']}")
        print(f"   Email: {shop_data['shop']['email']}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection failed: {e}")
        return False


def list_products(limit: int = 250, status: str = 'active') -> List[Dict]:
    """
    List all products from the store
    
    Args:
        limit: Maximum number of products to return (max 250)
        status: Product status filter ('active', 'draft', 'archived', or 'any')
    
    Returns:
        List of product dictionaries
    """
    try:
        params = {
            'limit': min(limit, 250),
            'status': status
        }
        response = requests.get(f'{BASE_URL}/products.json', headers=HEADERS, params=params)
        response.raise_for_status()
        products = response.json()['products']
        return products
    except requests.exceptions.RequestException as e:
        print(f"❌ Error listing products: {e}")
        return []


def get_product(product_id: str) -> Optional[Dict]:
    """
    Get detailed product information including metafields
    
    Args:
        product_id: Shopify product ID
    
    Returns:
        Product dictionary or None if not found
    """
    try:
        # Get product details
        response = requests.get(f'{BASE_URL}/products/{product_id}.json', headers=HEADERS)
        response.raise_for_status()
        product = response.json()['product']
        
        # Get product metafields
        metafields_response = requests.get(
            f'{BASE_URL}/products/{product_id}/metafields.json',
            headers=HEADERS
        )
        metafields_response.raise_for_status()
        product['metafields'] = metafields_response.json()['metafields']
        
        return product
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting product {product_id}: {e}")
        return None


def search_products(query: str, status: str = 'active') -> List[Dict]:
    """
    Search for products by title
    
    Args:
        query: Search query string
        status: Product status filter ('active', 'draft', 'archived', or 'any')
    
    Returns:
        List of matching products
    """
    try:
        params = {
            'title': query,
            'status': status
        }
        response = requests.get(f'{BASE_URL}/products.json', headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()['products']
    except requests.exceptions.RequestException as e:
        print(f"❌ Error searching products: {e}")
        return []


def update_product_description(product_id: str, description: str, tags: Optional[List[str]] = None) -> bool:
    """
    Update product description and tags
    
    Args:
        product_id: Shopify product ID
        description: HTML description
        tags: List of tags (optional)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        data = {
            'product': {
                'id': product_id,
                'body_html': description
            }
        }
        
        if tags:
            data['product']['tags'] = ', '.join(tags)
        
        response = requests.put(
            f'{BASE_URL}/products/{product_id}.json',
            headers=HEADERS,
            json=data
        )
        response.raise_for_status()
        print(f"✅ Successfully updated product {product_id}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error updating product {product_id}: {e}")
        return False


def update_product_tags(product_id: str, tags: List[str]) -> bool:
    """
    Update product tags only
    
    Args:
        product_id: Shopify product ID
        tags: List of tags
    
    Returns:
        True if successful, False otherwise
    """
    try:
        data = {
            'product': {
                'id': product_id,
                'tags': ', '.join(tags)
            }
        }
        
        response = requests.put(
            f'{BASE_URL}/products/{product_id}.json',
            headers=HEADERS,
            json=data
        )
        response.raise_for_status()
        print(f"✅ Successfully updated tags for product {product_id}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error updating tags for product {product_id}: {e}")
        return False


def create_or_update_metafield(product_id: str, namespace: str, key: str, value: str, value_type: str = 'single_line_text_field') -> bool:
    """
    Create or update a product metafield
    
    Args:
        product_id: Shopify product ID
        namespace: Metafield namespace (e.g., 'my_fields' for Cannibisters custom fields)
        key: Metafield key
        value: Metafield value
        value_type: Metafield type (default: 'single_line_text_field')
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # First, check if metafield exists
        metafields_response = requests.get(
            f'{BASE_URL}/products/{product_id}/metafields.json',
            headers=HEADERS,
            params={'namespace': namespace, 'key': key}
        )
        metafields_response.raise_for_status()
        existing_metafields = metafields_response.json()['metafields']
        
        data = {
            'metafield': {
                'namespace': namespace,
                'key': key,
                'value': value,
                'type': value_type
            }
        }
        
        if existing_metafields:
            # Update existing metafield
            metafield_id = existing_metafields[0]['id']
            response = requests.put(
                f'{BASE_URL}/metafields/{metafield_id}.json',
                headers=HEADERS,
                json=data
            )
        else:
            # Create new metafield
            response = requests.post(
                f'{BASE_URL}/products/{product_id}/metafields.json',
                headers=HEADERS,
                json=data
            )
        
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        # Check if it's a type mismatch error that we can fix
        if hasattr(e, 'response') and e.response is not None and e.response.status_code == 422:
            try:
                error_resp = e.response.json()
                error_msgs = error_resp.get('errors', {}).get('type', [])
                
                # Check for list.single_line_text_field requirement
                list_required = any("definition's type: 'list.single_line_text_field'" in msg for msg in error_msgs)
                
                if list_required and value_type == 'single_line_text_field':
                    print(f"⚠️  Retrying {namespace}.{key} as list.single_line_text_field...")
                    # Wrap value in list and json stringify
                    import json
                    list_value = json.dumps([value])
                    return create_or_update_metafield(product_id, namespace, key, list_value, 'list.single_line_text_field')
            except Exception as parse_error:
                print(f"   Error parsing 422 response: {parse_error}")

        print(f"❌ Error updating metafield {namespace}.{key}: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Response: {e.response.text}")
        return False


def update_product_metafields(product_id: str, metafields: Dict[str, Dict[str, str]]) -> bool:
    """
    Update multiple product metafields
    
    Args:
        product_id: Shopify product ID
        metafields: Dictionary of metafields organized by namespace
                   Example: {
                       'custom': {
                           'lineage': 'Ice Cream Cake x Whipped Cream',
                           'flowering_time': '8-9 weeks'
                       }
                   }
    
    Returns:
        True if all successful, False otherwise
    """
    success = True
    for namespace, fields in metafields.items():
        for key, value in fields.items():
            if not create_or_update_metafield(product_id, namespace, key, str(value)):
                success = False
    
    return success


def get_product_metafields(product_id: str) -> Dict[str, Dict[str, str]]:
    """
    Get all metafields for a product, organized by namespace
    
    Args:
        product_id: Shopify product ID
    
    Returns:
        Dictionary of metafields organized by namespace
    """
    try:
        response = requests.get(
            f'{BASE_URL}/products/{product_id}/metafields.json',
            headers=HEADERS
        )
        response.raise_for_status()
        metafields = response.json()['metafields']
        
        # Organize by namespace
        organized = {}
        for mf in metafields:
            namespace = mf['namespace']
            if namespace not in organized:
                organized[namespace] = {}
            organized[namespace][mf['key']] = mf['value']
        
        return organized
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting metafields: {e}")
        return {}


def update_product_status(product_id: str, status: str) -> bool:
    """
    Update product status (active/draft/archived)
    
    Args:
        product_id: Shopify product ID
        status: New status ('active', 'draft', 'archived')
    
    Returns:
        True if successful, False otherwise
    """
    try:
        data = {
            'product': {
                'id': product_id,
                'status': status
            }
        }
        response = requests.put(
            f'{BASE_URL}/products/{product_id}.json',
            headers=HEADERS,
            json=data
        )
        response.raise_for_status()
        print(f"✅ Updated status for product {product_id} to {status}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error updating product status: {e}")
        return False


def upload_product_image(product_id: str, image_path: str) -> bool:
    """
    Upload an image to a product
    
    Args:
        product_id: Shopify product ID
        image_path: Local path to the image file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            
        filename = os.path.basename(image_path)
        
        data = {
            "image": {
                "attachment": encoded_string,
                "filename": filename
            }
        }
        
        response = requests.post(
            f'{BASE_URL}/products/{product_id}/images.json',
            headers=HEADERS,
            json=data
        )
        response.raise_for_status()
        print(f"✅ Successfully uploaded image to product {product_id}")
        return True
    except Exception as e:
        print(f"❌ Error uploading image: {e}")
        return False


def upload_product_video(product_id: str, video_path: str) -> bool:
    """
    Upload a video to a product using GraphQL API
    This is a 3-step process:
    1. Request staged upload
    2. Upload file to S3
    3. Link video to product
    """
    try:
        if not os.path.exists(video_path):
            print(f"❌ Video file not found: {video_path}")
            return False

        filename = os.path.basename(video_path)
        file_size = os.path.getsize(video_path)
        
        # Step 1: Request staged upload
        staged_mutation = """
        mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
          stagedUploadsCreate(input: $input) {
            stagedTargets {
              url
              resourceUrl
              parameters {
                name
                value
              }
            }
            userErrors {
              field
              message
            }
          }
        }
        """
        
        variables = {
            "input": [
                {
                    "filename": filename,
                    "mimeType": "video/quicktime" if filename.endswith('.mov') else "video/mp4",
                    "resource": "VIDEO",
                    "fileSize": str(file_size)
                }
            ]
        }
        
        print(f"   [1/3] Requesting staged upload for {filename}...")
        resp = graphql_query(staged_mutation, variables)
        targets = resp.get('data', {}).get('stagedUploadsCreate', {}).get('stagedTargets', [])
        
        if not targets:
            print(f"❌ Failed to create staged upload: {resp}")
            return False
            
        target = targets[0]
        upload_url = target['url']
        resource_url = target['resourceUrl']
        params = target['parameters']
        
        # Step 2: Upload to S3
        print(f"   [2/3] Uploading file to S3...")
        # Prepare multipart form data
        form_data = {p['name']: p['value'] for p in params}
        with open(video_path, 'rb') as f:
            files = {'file': (filename, f)}
            upload_resp = requests.post(upload_url, data=form_data, files=files)
            upload_resp.raise_for_status()
            
        # Step 3: Link video to product
        print(f"   [3/3] Linking video to product {product_id}...")
        media_mutation = """
        mutation productCreateMedia($media: [CreateMediaInput!]!, $productId: ID!) {
          productCreateMedia(media: $media, productId: $productId) {
            media {
              alt
              mediaContentType
              status
            }
            userErrors {
              field
              message
            }
          }
        }
        """
        
        media_variables = {
            "productId": f"gid://shopify/Product/{product_id}",
            "media": [
                {
                    "alt": filename,
                    "mediaContentType": "VIDEO",
                    "originalSource": resource_url
                }
            ]
        }
        
        media_resp = graphql_query(media_mutation, media_variables)
        errors = media_resp.get('data', {}).get('productCreateMedia', {}).get('userErrors', [])
        
        if errors:
            print(f"❌ Media creation errors: {errors}")
            return False
            
        print(f"✅ Successfully uploaded video to product {product_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error uploading video: {e}")
        return False


def delete_all_product_images(product_id: str) -> bool:
    """
    Delete all images for a product
    
    Args:
        product_id: Shopify product ID
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # First get all images
        response = requests.get(f'{BASE_URL}/products/{product_id}/images.json', headers=HEADERS)
        response.raise_for_status()
        images = response.json()['images']
        
        if not images:
            print(f"ℹ️ No images to delete for product {product_id}")
            return True
            
        print(f"🗑️ Deleting {len(images)} images for product {product_id}...")
        
        success = True
        for image in images:
            image_id = image['id']
            try:
                delete_response = requests.delete(
                    f'{BASE_URL}/products/{product_id}/images/{image_id}.json',
                    headers=HEADERS
                )
                delete_response.raise_for_status()
                print(f"   ✅ Deleted image {image_id}")
            except requests.exceptions.RequestException as e:
                print(f"   ❌ Error deleting image {image_id}: {e}")
                success = False
                
        return success
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching images for deletion: {e}")
        return False




def get_collection_by_title(title: str) -> Optional[Dict]:
    """
    Find a custom collection by its title
    
    Args:
        title: Collection title to search for
    
    Returns:
        Collection dictionary or None if not found
    """
    try:
        params = {'title': title}
        response = requests.get(f'{BASE_URL}/custom_collections.json', headers=HEADERS, params=params)
        response.raise_for_status()
        collections = response.json()['custom_collections']
        
        # Exact match check
        for collection in collections:
            if collection['title'].lower() == title.lower():
                return collection
                
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error searching collections: {e}")
        return None


def get_products_in_collection(collection_id: str) -> List[Dict]:
    """
    Get all products in a specific collection
    
    Args:
        collection_id: Collection ID
    
    Returns:
        List of product dictionaries
    """
    try:
        response = requests.get(f'{BASE_URL}/collections/{collection_id}/products.json', headers=HEADERS)
        response.raise_for_status()
        return response.json()['products']
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting collection products: {e}")
        return []


def add_product_to_collection(collection_id: str, product_id: str) -> bool:
    """
    Add a product to a custom collection
    
    Args:
        collection_id: Collection ID
        product_id: Product ID
    
    Returns:
        True if successful, False otherwise
    """
    try:
        data = {
            'collect': {
                'product_id': product_id,
                'collection_id': collection_id
            }
        }
        response = requests.post(f'{BASE_URL}/collects.json', headers=HEADERS, json=data)
        response.raise_for_status()
        print(f"✅ Added product {product_id} to collection {collection_id}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error adding product to collection: {e}")
        return False


def remove_product_from_collection(collection_id: str, product_id: str) -> bool:
    """
    Remove a product from a custom collection
    
    Args:
        collection_id: Collection ID
        product_id: Product ID
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # First find the collect ID
        params = {
            'collection_id': collection_id,
            'product_id': product_id
        }
        response = requests.get(f'{BASE_URL}/collects.json', headers=HEADERS, params=params)
        response.raise_for_status()
        collects = response.json()['collects']
        
        if not collects:
            print(f"⚠️ Product {product_id} not found in collection {collection_id}")
            return True  # Already removed
            
        collect_id = collects[0]['id']
        
        # Delete the collect
        response = requests.delete(f'{BASE_URL}/collects/{collect_id}.json', headers=HEADERS)
        response.raise_for_status()
        print(f"✅ Removed product {product_id} from collection {collection_id}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error removing product from collection: {e}")
        return False


def update_product_price(product_id: str, price: float, compare_at_price: Optional[float] = None) -> bool:
    """
    Update product price and compare-at price (for sales)
    
    Args:
        product_id: Shopify product ID
        price: New price
        compare_at_price: Original price (optional, set to None to remove sale)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # We need to find the first variant ID to update the price
        product = get_product(product_id)
        if not product or not product.get('variants'):
            print(f"❌ Product {product_id} not found or has no variants")
            return False
            
        variant_id = product['variants'][0]['id']
        payload = {
            'variant': {
                'id': variant_id,
                'price': str(price),
                'compare_at_price': str(compare_at_price) if compare_at_price else None
            }
        }
        
        response = requests.put(f'{BASE_URL}/variants/{variant_id}.json', headers=HEADERS, json=payload)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error updating product price: {e}")
        return False

def list_orders(created_at_min: str = None, created_at_max: str = None, limit: int = 250, status: str = 'any') -> List[Dict]:
    """
    List orders from the store with date range filtering
    
    Args:
        created_at_min: Minimum creation date (ISO 8601)
        created_at_max: Maximum creation date (ISO 8601)
        limit: Maximum number of orders to return (max 250)
        status: Order status filter ('open', 'closed', 'cancelled', 'any')
    
    Returns:
        List of order dictionaries
    """
    try:
        initial_params = {
            'limit': min(limit, 250),
            'status': status
        }
        if created_at_min:
            initial_params['created_at_min'] = created_at_min
        if created_at_max:
            initial_params['created_at_max'] = created_at_max
            
        orders = []
        url = f'{BASE_URL}/orders.json'
        page_count = 0
        
        while url:
            page_count += 1
            # For the first request, use url + initial_params
            # For subsequent requests, url is the full next link, so params should be empty
            current_params = initial_params if page_count == 1 else None
            
            response = requests.get(url, headers=HEADERS, params=current_params)
            response.raise_for_status()
            batch = response.json().get('orders', [])
            orders.extend(batch)
            
            print(f"   [API] Fetched page {page_count}, orders in batch: {len(batch)}, total so far: {len(orders)}")
            
            link_header = response.headers.get('Link')
            if link_header and 'rel="next"' in link_header:
                links = link_header.split(',')
                url = None
                for link in links:
                    if 'rel="next"' in link:
                        url = link.split(';')[0].strip('< >')
            else:
                url = None
                
        return orders
    except requests.exceptions.RequestException as e:
        print(f"❌ Error listing orders: {e}")
        return []


if __name__ == '__main__':
    # Test connection
    print("Testing Shopify API connection...")
    test_connection()
