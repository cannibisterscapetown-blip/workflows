#!/usr/bin/env python3
"""
Flag Maxwell I. — Coupon Exploitation Investigation
Searches Shopify for a customer named Maxwell I. and pulls all orders
with discount codes used. Generates a fraud report.

Usage: python flag_maxwell_fraud.py
Output: maxwell_fraud_report.txt
"""

import os
import json
import requests
from collections import defaultdict
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

SHOPIFY_ACCESS_TOKEN = os.getenv('SHOPIFY_ACCESS_TOKEN')
SHOPIFY_STORE_URL = os.getenv('SHOPIFY_STORE_URL')
API_VERSION = '2024-01'
BASE_URL = f'https://{SHOPIFY_STORE_URL}/admin/api/{API_VERSION}'
HEADERS = {
    'X-Shopify-Access-Token': SHOPIFY_ACCESS_TOKEN,
    'Content-Type': 'application/json'
}


def search_customers(query: str):
    """Search Shopify customers by name."""
    url = f'{BASE_URL}/customers/search.json'
    params = {'query': query, 'limit': 50}
    resp = requests.get(url, headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json().get('customers', [])


def get_orders_for_customer(customer_id: int):
    """Fetch all orders for a given customer ID (paginated)."""
    orders = []
    url = f'{BASE_URL}/orders.json'
    params = {'customer_id': customer_id, 'limit': 250, 'status': 'any'}
    page = 0

    while url:
        page += 1
        current_params = params if page == 1 else None
        resp = requests.get(url, headers=HEADERS, params=current_params)
        resp.raise_for_status()
        batch = resp.json().get('orders', [])
        orders.extend(batch)

        link = resp.headers.get('Link', '')
        url = None
        if 'rel="next"' in link:
            for part in link.split(','):
                if 'rel="next"' in part:
                    url = part.split(';')[0].strip('< >')

    return orders


def analyse_orders(orders: list):
    """Return discount-code stats from a list of orders."""
    codes_used = defaultdict(int)       # code -> usage count
    orders_with_discount = []
    total_discount_value = 0.0

    for order in orders:
        order_codes = []
        discount_apps = order.get('discount_applications', [])
        for app in discount_apps:
            code = app.get('code') or app.get('title') or 'unknown'
            codes_used[code] += 1
            order_codes.append(code)

        # Also pick up legacy discount_codes field
        for dc in order.get('discount_codes', []):
            code = dc.get('code', 'unknown')
            if code not in order_codes:
                codes_used[code] += 1
                order_codes.append(code)

        if order_codes:
            orders_with_discount.append({
                'order_id': order['id'],
                'order_number': order.get('order_number'),
                'created_at': order.get('created_at'),
                'total_price': order.get('total_price'),
                'total_discounts': order.get('total_discounts'),
                'codes': order_codes,
            })
            total_discount_value += float(order.get('total_discounts', 0) or 0)

    return codes_used, orders_with_discount, total_discount_value


def write_report(customer, codes_used, orders_with_discount, total_discount_value, all_orders):
    lines = []
    lines.append("=" * 70)
    lines.append("FRAUD FLAG REPORT — COUPON EXPLOITATION")
    lines.append(f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("=" * 70)
    lines.append("")

    lines.append("CUSTOMER")
    lines.append(f"  Name      : {customer.get('first_name', '')} {customer.get('last_name', '')}")
    lines.append(f"  Email     : {customer.get('email', 'N/A')}")
    lines.append(f"  Phone     : {customer.get('phone', 'N/A')}")
    lines.append(f"  ID        : {customer['id']}")
    lines.append(f"  Created   : {customer.get('created_at', 'N/A')}")
    lines.append(f"  Tags      : {customer.get('tags', 'none')}")
    lines.append("")

    lines.append("SUMMARY")
    lines.append(f"  Total orders          : {len(all_orders)}")
    lines.append(f"  Orders with discounts : {len(orders_with_discount)}")
    lines.append(f"  Unique discount codes : {len(codes_used)}")
    lines.append(f"  Total discount value  : R{total_discount_value:,.2f}")
    lines.append("")

    lines.append("UNIQUE CODES USED")
    for code, count in sorted(codes_used.items(), key=lambda x: -x[1]):
        lines.append(f"  {count:>3}x  {code}")
    lines.append("")

    lines.append("DISCOUNTED ORDERS (chronological)")
    lines.append(f"  {'Order #':<12} {'Date':<25} {'Total':>10} {'Discount':>10}  Codes")
    lines.append(f"  {'-'*12} {'-'*24} {'-'*10} {'-'*10}  -----")
    for o in sorted(orders_with_discount, key=lambda x: x['created_at']):
        date_str = o['created_at'][:10] if o['created_at'] else 'N/A'
        codes_str = ', '.join(o['codes'])
        lines.append(
            f"  #{o['order_number']:<11} {date_str:<25} "
            f"R{float(o['total_price'] or 0):>9,.2f} "
            f"R{float(o['total_discounts'] or 0):>9,.2f}  {codes_str}"
        )
    lines.append("")

    lines.append("RECOMMENDED ACTIONS")
    if len(codes_used) >= 10:
        lines.append("  [URGENT] Disable single-use code generation for this customer.")
        lines.append("  [URGENT] Review how wheel-of-fortune / one-time codes are created.")
    lines.append("  [ ] Add 'fraud-flagged' tag to customer in Shopify admin.")
    lines.append("  [ ] Suspend or restrict account pending review.")
    lines.append("  [ ] Audit the discount code generator for rate-limiting / per-customer caps.")
    lines.append("  [ ] Check whether codes were shared publicly (WhatsApp, social).")
    lines.append("")
    lines.append("=" * 70)

    report = "\n".join(lines)
    output_path = 'maxwell_fraud_report.txt'
    with open(output_path, 'w') as f:
        f.write(report)

    print(report)
    print(f"\n✅ Report saved to {output_path}")


def main():
    print("🔍 Searching for customer 'Maxwell I.'...")

    # Try several name variants
    candidates = []
    for q in ['Maxwell', 'Maxwell I']:
        results = search_customers(q)
        for c in results:
            if c['id'] not in [x['id'] for x in candidates]:
                candidates.append(c)

    if not candidates:
        print("❌ No customers found matching 'Maxwell I.' — check the name spelling in Shopify.")
        return

    # Pick the one whose last name starts with I (if multiple matches)
    maxwell = None
    for c in candidates:
        if c.get('last_name', '').upper().startswith('I'):
            maxwell = c
            break
    if not maxwell:
        maxwell = candidates[0]
        print(f"⚠️  Could not narrow to last-name 'I.' — using first match: "
              f"{maxwell.get('first_name')} {maxwell.get('last_name')}")

    print(f"✅ Found: {maxwell.get('first_name')} {maxwell.get('last_name')} (ID {maxwell['id']})")
    print("📦 Fetching all orders...")

    all_orders = get_orders_for_customer(maxwell['id'])
    print(f"   Retrieved {len(all_orders)} orders total.")

    codes_used, orders_with_discount, total_discount_value = analyse_orders(all_orders)

    write_report(maxwell, codes_used, orders_with_discount, total_discount_value, all_orders)


if __name__ == '__main__':
    main()
