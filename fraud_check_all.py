#!/usr/bin/env python3
"""
Discount Abuse Detector
Fetches all orders with discount codes, groups by customer, and flags
accounts where total discounts significantly exceed loyalty earnings.

Loyalty program: 5 points per R1 spent, 100 points = R1 discount (5% back).

Flagging thresholds:
  - Total discount exceeds loyalty value by more than R500 AND more than 30%
  - Customer has at least 5 orders
"""

import os
import re
import requests
from datetime import datetime
from collections import defaultdict
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

# Thresholds
MIN_ORDERS = 5
EXCESS_AMOUNT_THRESHOLD = 500    # R500 over loyalty value
EXCESS_PCT_THRESHOLD = 0.30      # 30% over loyalty value

# Loyalty: 5 pts per R1 spent, 100 pts = R1
POINTS_PER_RAND = 5
POINTS_PER_DISCOUNT_RAND = 100


def loyalty_value(total_spent):
    points = total_spent * POINTS_PER_RAND
    return points / POINTS_PER_DISCOUNT_RAND


def fetch_all_orders():
    """Fetch all orders (any status) paginated."""
    orders = []
    url = f'{BASE_URL}/orders.json'
    params = {'status': 'any', 'limit': 250}
    page = 0

    while url:
        page += 1
        print(f"  Fetching page {page}...", end='\r')
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

    print(f"  Fetched {len(orders)} orders total.          ")
    return orders


def is_auto_generated(code):
    """Heuristic: random alphanumeric codes like LLMK9AUD are auto-generated."""
    return bool(re.match(r'^[A-Z0-9]{6,12}$', code))


def build_customer_profiles(orders):
    """Group orders by customer and compute spend/discount totals."""
    profiles = defaultdict(lambda: {
        'name': '',
        'email': '',
        'customer_id': None,
        'orders': [],
        'total_spent': 0.0,
        'total_discount': 0.0,
        'code_usage': defaultdict(int),
    })

    for order in orders:
        customer = order.get('customer')
        if not customer:
            continue

        cid = customer['id']
        p = profiles[cid]
        p['customer_id'] = cid
        p['name'] = f"{customer.get('first_name', '')} {customer.get('last_name', '')}".strip()
        p['email'] = customer.get('email', 'N/A')

        total = float(order.get('total_price', 0))
        p['total_spent'] += total
        p['orders'].append(order['name'])

        for dc in order.get('discount_codes', []):
            code = dc.get('code', '')
            amount = float(dc.get('amount', 0))
            p['total_discount'] += amount
            p['code_usage'][code] += 1

    return profiles


def flag_profiles(profiles):
    flagged = []
    for cid, p in profiles.items():
        if len(p['orders']) < MIN_ORDERS:
            continue
        if p['total_discount'] == 0:
            continue

        lv = loyalty_value(p['total_spent'])
        excess_amount = p['total_discount'] - lv
        excess_pct = (excess_amount / lv) if lv > 0 else float('inf')

        if excess_amount > EXCESS_AMOUNT_THRESHOLD and excess_pct > EXCESS_PCT_THRESHOLD:
            flagged.append({
                **p,
                'loyalty_value': lv,
                'excess_amount': excess_amount,
                'excess_pct': excess_pct,
            })

    # Sort by excess amount descending
    flagged.sort(key=lambda x: x['excess_amount'], reverse=True)
    return flagged


def main():
    print("=" * 65)
    print("Discount Abuse Detector")
    print(f"Thresholds: min {MIN_ORDERS} orders | "
          f">R{EXCESS_AMOUNT_THRESHOLD} AND >{int(EXCESS_PCT_THRESHOLD*100)}% over loyalty")
    print("=" * 65)

    print("\n[1] Fetching all orders...")
    orders = fetch_all_orders()

    print("\n[2] Building customer profiles...")
    profiles = build_customer_profiles(orders)
    print(f"  {len(profiles)} customers with orders found.")

    print("\n[3] Flagging suspicious accounts...")
    flagged = flag_profiles(profiles)
    print(f"  {len(flagged)} account(s) flagged.")

    # Build report
    lines = []
    lines.append("=" * 65)
    lines.append("DISCOUNT ABUSE REPORT")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Orders analysed: {len(orders)}")
    lines.append(f"Customers with orders: {len(profiles)}")
    lines.append(f"Flagged accounts: {len(flagged)}")
    lines.append("=" * 65)
    lines.append("")

    for i, p in enumerate(flagged, 1):
        lv = p['loyalty_value']
        lines.append(f"[{i}] {p['name']} ({p['email']})")
        lines.append(f"  Customer ID:      {p['customer_id']}")
        lines.append(f"  Orders:           {len(p['orders'])}")
        lines.append(f"  Total spent:      R{p['total_spent']:,.2f}")
        lines.append(f"  Loyalty value:    R{lv:,.2f}")
        lines.append(f"  Actual discount:  R{p['total_discount']:,.2f}")
        lines.append(f"  Excess:           R{p['excess_amount']:,.2f}  ({p['excess_pct']*100:.1f}% over loyalty)")
        lines.append(f"  Discount codes used:")
        for code, count in sorted(p['code_usage'].items(), key=lambda x: -x[1]):
            tag = ' [auto]' if is_auto_generated(code) else ' [manual]'
            lines.append(f"    {code:35s} x{count}{tag}")
        lines.append("")

    lines.append("=" * 65)
    lines.append("RECOMMENDED ACTIONS")
    lines.append("  [ ] Review flagged accounts in Shopify")
    lines.append("  [ ] Investigate manual codes applied excessively")
    lines.append("  [ ] Check if auto-generated code volume matches loyalty redemption history")
    lines.append("  [ ] Tag confirmed abuse accounts with 'fraud-flagged'")
    lines.append("=" * 65)

    report = '\n'.join(lines)
    out_file = 'discount_abuse_report.txt'
    with open(out_file, 'w') as f:
        f.write(report)

    print(f"\n[4] Report written to: {out_file}\n")
    print(report)


if __name__ == '__main__':
    main()
