#!/usr/bin/env python3
import json
from datetime import datetime
from shopify_api import list_orders

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def analyze_performance():
    schedule = load_json('advent_calendar_schedule.json')
    mapping = load_json('advent_product_mapping.json')
    
    # Create a lookup: Date -> ProductID
    # Day 1 = 2025-12-01, etc.
    schedule_lookup = {}
    for item in schedule:
        day = item['day']
        product_name = item['product']
        if product_name in mapping:
            product_id = mapping[product_name]['id']
            date_str = f"2025-12-{day:02d}"
            schedule_lookup[date_str] = {
                'id': product_id,
                'name': product_name,
                'discount': item['discount_percent']
            }
    
    print("📦 Fetching orders for December 2025...")
    # Fetch orders for the whole month
    orders = list_orders(
        created_at_min="2025-12-01T00:00:00Z",
        created_at_max="2025-12-31T23:59:59Z",
        status='any'
    )
    print(f"✅ Retrieved {len(orders)} orders.")
    
    # Analysis results
    performance = {} # Day -> {featured_sold: X, total_revenue_delta: Y}
    
    for order in orders:
        # Shopify format: 2025-12-01T14:30:00+02:00
        order_date_full = order['created_at']
        order_date = order_date_full.split('T')[0]
        
        if order_date in schedule_lookup:
            featured = schedule_lookup[order_date]
            target_id = featured['id']
            
            if order_date not in performance:
                performance[order_date] = {
                    'product_name': featured['name'],
                    'discount': featured['discount'],
                    'quantity_sold': 0,
                    'order_count': 0
                }
            
            # Check line items
            found_featured = False
            for item in order.get('line_items', []):
                if item.get('product_id') == target_id:
                    performance[order_date]['quantity_sold'] += item['quantity']
                    found_featured = True
            
            if found_featured:
                performance[order_date]['order_count'] += 1

    # Print Report
    print("\n" + "="*80)
    print(f"{'Date':<12} | {'Product':<45} | {'Sold':<5} | {'Orders':<6}")
    print("-" * 80)
    
    total_sold = 0
    for day in range(1, 25):
        d_str = f"2025-12-{day:02d}"
        if d_str in performance:
            data = performance[d_str]
            print(f"{d_str:<12} | {data['product_name'][:45]:<45} | {data['quantity_sold']:<5} | {data['order_count']:<6}")
            total_sold += data['quantity_sold']
        else:
            # Maybe no sales on that day for that product?
            featured = schedule_lookup.get(d_str)
            if featured:
                print(f"{d_str:<12} | {featured['name'][:45]:<45} | 0     | 0")
            else:
                print(f"{d_str:<12} | {'-- Not Scheduled --':<45} | --    | --")

    print("-" * 80)
    print(f"Total Advent Products Sold on Featured Days: {total_sold}")
    print("="*80)

    # Save details to JSON for walkthrough
    with open('advent_performance_results.json', 'w') as f:
        json.dump(performance, f, indent=4)

if __name__ == '__main__':
    analyze_performance()
