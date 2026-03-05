#!/usr/bin/env python3
import json
from shopify_api import list_orders

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def analyze_usual_sales():
    mapping = load_json('advent_product_mapping.json')
    product_ids = {data['id']: name for name, data in mapping.items()}
    
    print("📦 Fetching orders for November 2025 (Baseline)...")
    orders = list_orders(
        created_at_min="2025-11-01T00:00:00Z",
        created_at_max="2025-11-30T23:59:59Z",
        status='any'
    )
    print(f"✅ Retrieved {len(orders)} orders.")
    
    # Store aggregate sales for each product ID
    usual_sales = {pid: {'total_sold': 0, 'product_name': name} for pid, name in product_ids.items()}
    
    for order in orders:
        for item in order.get('line_items', []):
            pid = item.get('product_id')
            if pid in usual_sales:
                usual_sales[pid]['total_sold'] += item['quantity']
    
    # Calculate daily average (over 30 days)
    results = {}
    for pid, data in usual_sales.items():
        daily_avg = data['total_sold'] / 30.0
        results[data['product_name']] = {
            'product_id': pid,
            'total_nov_sold': data['total_sold'],
            'daily_avg': round(daily_avg, 2)
        }
    
    # Save results
    with open('usual_sales_baseline.json', 'w') as f:
        json.dump(results, f, indent=4)
    
    print("✅ Baseline analysis complete. Saved to usual_sales_baseline.json")

if __name__ == '__main__':
    analyze_usual_sales()
