import shopify_api
import json

def get_product_media(product_id):
    query = """
    query productMedia($id: ID!) {
      product(id: $id) {
        media(first: 50) {
          edges {
            node {
              id
              alt
              mediaContentType
            }
          }
        }
      }
    }
    """
    variables = {"id": f"gid://shopify/Product/{product_id}"}
    resp = shopify_api.graphql_query(query, variables)
    return resp.get('data', {}).get('product', {}).get('media', {}).get('edges', [])

def delete_media(media_id):
    query = """
    mutation productDeleteMedia($mediaIds: [ID!]!, $productId: ID!) {
      productDeleteMedia(mediaIds: $mediaIds, productId: $productId) {
        deletedMediaIds
        userErrors {
          field
          message
        }
      }
    }
    """
    # Note: productDeleteMedia requires a productId but deletes the media globally. 
    # We'll use a dummy ID or the correct one if we have it.
    # Actually, let's use the version that just needs the IDs if possible?
    # Shopify requires the Product ID for media deletion.
    pass

def cleanup():
    # List of product IDs we were uploading to
    from upload_new_rotating_buds import VIDEO_MAPPING
    from upload_new_rotating_buds import BASE_DIR
    
    all_pids = set()
    for ids in VIDEO_MAPPING.values():
        all_pids.update(ids)
    
    target_filenames = list(VIDEO_MAPPING.keys())
    
    print(f"🔍 Checking {len(all_pids)} products for videos to remove...")
    
    for pid in all_pids:
        media_edges = get_product_media(pid)
        media_to_delete = []
        for edge in media_edges:
            node = edge['node']
            if node['mediaContentType'] == 'VIDEO':
                # Check if alt (filename) matches our upload
                if node['alt'] in target_filenames:
                    media_to_delete.append(node['id'])
        
        if media_to_delete:
            print(f"   🗑️ Deleting {len(media_to_delete)} videos from {pid}...")
            delete_mutation = """
            mutation productDeleteMedia($mediaIds: [ID!]!, $productId: ID!) {
              productDeleteMedia(mediaIds: $mediaIds, productId: $productId) {
                deletedMediaIds
                userErrors {
                  field
                  message
                }
              }
            }
            """
            variables = {
                "productId": f"gid://shopify/Product/{pid}",
                "mediaIds": media_to_delete
            }
            resp = shopify_api.graphql_query(delete_mutation, variables)
            if resp.get('data', {}).get('productDeleteMedia', {}).get('userErrors'):
                print(f"      ❌ Errors: {resp['data']['productDeleteMedia']['userErrors']}")
            else:
                print(f"      ✅ Deleted: {resp.get('data', {}).get('productDeleteMedia', {}).get('deletedMediaIds')}")

if __name__ == "__main__":
    cleanup()
