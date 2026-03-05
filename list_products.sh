#!/bin/bash
# List all products from Cannibisters Shopify store

source .env

# Default parameters
LIMIT=250
STATUS="active"
OUTPUT_FILE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --limit)
            LIMIT="$2"
            shift 2
            ;;
        --status)
            STATUS="$2"
            shift 2
            ;;
        --output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --help)
            echo "Usage: ./list_products.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --limit NUM      Maximum number of products (default: 250)"
            echo "  --status STATUS  Filter by status: active, draft, archived, any (default: active)"
            echo "  --output FILE    Save output to file"
            echo "  --help           Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Make API request
echo "📦 Fetching products from Cannibisters..."
echo "   Status: $STATUS"
echo "   Limit: $LIMIT"
echo ""

RESPONSE=$(curl -s -X GET \
  "https://${SHOPIFY_STORE_URL}/admin/api/2024-01/products.json?limit=${LIMIT}&status=${STATUS}" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json")

# Save to file if requested
if [ -n "$OUTPUT_FILE" ]; then
    echo "$RESPONSE" > "$OUTPUT_FILE"
    echo "✅ Saved to $OUTPUT_FILE"
fi

# Parse and display products
echo "$RESPONSE" | grep -o '"id":[0-9]*,"title":"[^"]*",".*"status":"[^"]*"' | head -20 || echo "$RESPONSE"
