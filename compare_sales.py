#!/usr/bin/env python3
import json

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def compare_sales():
    advent = load_json('advent_performance_results.json')
    usual = load_json('usual_sales_baseline.json')
    
    # Create comparison data
    comparison = []
    
    for date, advent_data in advent.items():
        name = advent_data['product_name']
        advent_sold = advent_data['quantity_sold']
        
        usual_data = usual.get(name, {})
        usual_avg = usual_data.get('daily_avg', 0.0)
        
        lift = 0.0
        if usual_avg > 0:
            lift = ((advent_sold - usual_avg) / usual_avg) * 100
        elif advent_sold > 0:
            lift = 100.0 # From 0 to something
            
        comparison.append({
            'date': date,
            'product': name,
            'advent_sold': advent_sold,
            'usual_avg': usual_avg,
            'lift_percent': round(lift, 1)
        })
        
    # Sort by date
    comparison.sort(key=lambda x: x['date'])
    
    print("\n" + "="*95)
    print(f"{'Date':<12} | {'Product':<35} | {'Advent Sold':<12} | {'Usual Avg':<10} | {'Lift %':<10}")
    print("-" * 95)
    
    for row in comparison:
        lift_str = f"{row['lift_percent']:>+7.1f}%" if row['usual_avg'] > 0 else "NEW" if row['advent_sold'] > 0 else "0.0%"
        print(f"{row['date']:<12} | {row['product'][:35]:<35} | {row['advent_sold']:<12} | {row['usual_avg']:<10} | {lift_str:<10}")
        
    print("-" * 95)
    print("="*95)
    
    with open('sales_comparison_results.json', 'w') as f:
        json.dump(comparison, f, indent=4)

if __name__ == '__main__':
    compare_sales()
