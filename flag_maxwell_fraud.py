#!/usr/bin/env python3
"""
Flag Maxwell Fraud
Searches Shopify for customers named Maxwell, fetches all their orders,
extracts every discount code used, and writes a fraud report.
"""

import os
import requests
from datetime import datetime
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


def search_customers(query):
    customers = []
    url = f'{BASE_URL}/customers/search.json'
    params = {'query': query, 'limit': 250}
    while url:
        resp = requests.get(url, headers=HEADERS, params=params)
        resp.raise_for_status()
        batch = resp.json().get('customers', [])
        customers.extend(batch)
        link = resp.headers.get('Link', '')
        url = None
        params = None
        for part in link.split(','):
            if 'rel="next"' in part:
                url = part.split(';')[0].strip().strip('<>')
    return customers


def get_orders_for_customer(customer_id):
    orders = []
    url = f'{BASE_URL}/orders.json'
    params = {'customer_id': customer_id, 'status': 'any', 'limit': 250}
    page = 0
    while url:
        page += 1
        resp = requests.get(url, headers=HEADERS, params=params)
        resp.raise_for_status()
        batch = resp.json().get('orders', [])
        orders.extend(batch)
        link = resp.headers.get('Link', '')
        url = None
        params = None
        for part in link.split(','):
            if 'rel="next"' in part:
                url = part.split(';')[0].strip().strip('<>')
    return orders


def find_maxwell_customers():
    """Try multiple search variants to catch all Maxwell entries."""
    seen_ids = set()
    results = []
    for q in ['first_name:Maxwell', 'last_name:Maxwell']:
        print(f"  Searching: {q}")
        for c in search_customers(q):
            if c['id'] not in seen_ids:
                seen_ids.add(c['id'])
                results.append(c)
    return results


def main():
    print("=" * 60)
    print("Maxwell Fraud Detection Report")
    print("=" * 60)

    print("\n[1] Searching for Maxwell customers...")
    customers = find_maxwell_customers()
    print(f"    Found {len(customers)} customer(s).")

    if not customers:
        print("No Maxwell customers found. Nothing to report.")
        return

    report_lines = []
    report_lines.append("=" * 60)
    report_lines.append("MAXWELL FRAUD DETECTION REPORT")
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("=" * 60)
    report_lines.append("")

    total_orders = 0
    total_discount_uses = 0

    for customer in customers:
        cid = customer['id']
        name = f"{customer.get('first_name', '')} {customer.get('last_name', '')}".strip()
        email = customer.get('email', 'N/A')
        phone = customer.get('phone', 'N/A')
        created = customer.get('created_at', 'N/A')
        orders_count = customer.get('orders_count', '?')

        print(f"\n[2] Fetching orders for: {name} ({email})")
        orders = get_orders_for_customer(cid)
        print(f"    {len(orders)} order(s) found.")
        total_orders += len(orders)

        discount_code_usage = {}
        order_details = []
        for order in orders:
            order_name = order.get('name', order['id'])
            order_date = order.get('created_at', '')[:10]
            order_total = order.get('total_price', '0.00')
            codes_in_order = []
            for dc in order.get('discount_codes', []):
                code = dc.get('code', '')
                amount = dc.get('amount', '0.00')
                dtype = dc.get('type', '')
                codes_in_order.append(f"{code} ({dtype}, -{amount})")
                discount_code_usage[code] = discount_code_usage.get(code, 0) + 1
                total_discount_uses += 1
            order_details.append({
                'name': order_name,
                'date': order_date,
                'total': order_total,
                'codes': codes_in_order,
            })

        report_lines.append(f"CUSTOMER: {name}")
        report_lines.append(f"  ID:            {cid}")
        report_lines.append(f"  Email:         {email}")
        report_lines.append(f"  Phone:         {phone}")
        report_lines.append(f"  Account Since: {created[:10] if created != 'N/A' else 'N/A'}")
        report_lines.append(f"  Orders (API):  {len(orders)}  (Shopify record: {orders_count})")
        report_lines.append(f"  Unique Codes:  {len(discount_code_usage)}")
        report_lines.append(f"  Total Code Uses: {sum(discount_code_usage.values())}")
        report_lines.append("")

        if discount_code_usage:
            report_lines.append("  Discount Code Summary:")
            for code, count in sorted(discount_code_usage.items(), key=lambda x: -x[1]):
                flag = "  *** USED MULTIPLE TIMES ***" if count > 1 else ""
                report_lines.append(f"    {code:30s}  x{count}{flag}")
            report_lines.append("")

        report_lines.append("  Per-Order Breakdown:")
        for od in order_details:
            codes_str = ', '.join(od['codes']) if od['codes'] else 'None'
            report_lines.append(f"    {od['name']}  {od['date']}  R{od['total']:>8}  Codes: {codes_str}")
        report_lines.append("")
        report_lines.append("-" * 60)
        report_lines.append("")

    report_lines.append("SUMMARY")
    report_lines.append(f"  Maxwell customers found:  {len(customers)}")
    report_lines.append(f"  Total orders examined:    {total_orders}")
    report_lines.append(f"  Total discount code uses: {total_discount_uses}")
    report_lines.append("")
    report_lines.append("RECOMMENDED ACTIONS")
    report_lines.append("  [ ] Disable or expire discount codes used more than once per customer")
    report_lines.append("  [ ] Add 'fraud-flagged' tag to affected customer accounts in Shopify")
    report_lines.append("  [ ] Suspend account(s) pending review if abuse is confirmed")
    report_lines.append("  [ ] Audit the discount code generator: enforce per-customer usage caps")
    report_lines.append("  [ ] Review all orders with discounted totals for refund/chargeback risk")
    report_lines.append("")
    report_lines.append("=" * 60)

    report_text = '\n'.join(report_lines)
    out_file = 'maxwell_fraud_report.txt'
    with open(out_file, 'w') as f:
        f.write(report_text)

    print(f"\n[3] Report written to: {out_file}")
    print(report_text)


if __name__ == '__main__':
    main()
