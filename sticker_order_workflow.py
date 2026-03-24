#!/usr/bin/env python3
"""
Sticker Order Workflow for Cannibisters
========================================
Checks how many units of each packaging type were sold on Shopify last month,
accounts for leftover stickers from the previous order, and calculates how many
new stickers to order so we order exactly what we need — no more, no less.

Usage:
    python3 sticker_order_workflow.py               # uses last calendar month
    python3 sticker_order_workflow.py --month 2026-02  # specify a month (YYYY-MM)
    python3 sticker_order_workflow.py --save        # save projected leftovers to inventory file
"""

import json
import sys
import argparse
from datetime import datetime, timezone
from calendar import monthrange
from shopify_api import list_orders

CONFIG_FILE = 'sticker_config.json'
INVENTORY_FILE = 'sticker_inventory.json'


def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)


def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def get_last_month(reference_date=None):
    """Returns (year, month) for the previous calendar month."""
    if reference_date is None:
        reference_date = datetime.now(timezone.utc)
    year, month = reference_date.year, reference_date.month
    if month == 1:
        return year - 1, 12
    return year, month - 1


def month_date_range(year, month):
    """Returns ISO 8601 start and end strings for a given month."""
    _, last_day = monthrange(year, month)
    start = f"{year}-{month:02d}-01T00:00:00Z"
    end = f"{year}-{month:02d}-{last_day:02d}T23:59:59Z"
    return start, end


def match_packaging_type(product_title, packaging_types):
    """
    Returns the first packaging type whose keywords all appear in the product title.
    Returns None if no match is found.
    """
    title_lower = product_title.lower()
    for ptype, config in packaging_types.items():
        keywords = config.get('keywords', [])
        if keywords and all(kw.lower() in title_lower for kw in keywords):
            return ptype
    return None


def count_sales_by_type(orders, packaging_types):
    """
    Iterates over all order line items and tallies units sold per packaging type.
    Returns:
        sales_by_type: dict {packaging_type: units_sold}
        unmapped: dict {product_title: units_sold} for products that didn't match any type
    """
    sales_by_type = {ptype: 0 for ptype in packaging_types}
    unmapped = {}

    for order in orders:
        for item in order.get('line_items', []):
            title = item.get('title', '')
            qty = item.get('quantity', 0)
            ptype = match_packaging_type(title, packaging_types)
            if ptype:
                sales_by_type[ptype] += qty
            else:
                unmapped[title] = unmapped.get(title, 0) + qty

    return sales_by_type, unmapped


def calculate_order(sales_by_type, leftovers):
    """
    For each packaging type:
      order_qty   = max(0, units_sold - leftover)
      new_leftover = max(0, leftover - units_sold)   [0 if we ordered more]

    Returns:
        order_quantities: dict {ptype: qty_to_order}
        projected_leftovers: dict {ptype: projected_leftover_next_month}
    """
    order_quantities = {}
    projected_leftovers = {}

    all_types = set(list(sales_by_type.keys()) + list(leftovers.keys()))
    for ptype in all_types:
        if ptype.startswith('_'):  # skip meta keys like _note
            continue
        sold = sales_by_type.get(ptype, 0)
        leftover = leftovers.get(ptype, 0)
        order_qty = max(0, sold - leftover)
        new_leftover = max(0, leftover - sold)  # 0 when we order new stock

        order_quantities[ptype] = order_qty
        projected_leftovers[ptype] = new_leftover

    return order_quantities, projected_leftovers


def print_report(year, month, sales_by_type, leftovers, order_quantities, projected_leftovers, unmapped):
    month_name = datetime(year, month, 1).strftime('%B %Y')
    print()
    print("=" * 62)
    print(f"  STICKER ORDER REPORT  —  Based on {month_name} sales")
    print("=" * 62)

    col_w = [28, 8, 10, 9, 12]
    header = (
        f"{'Packaging Type':<{col_w[0]}}"
        f"{'Sold':>{col_w[1]}}"
        f"{'Leftover':>{col_w[2]}}"
        f"{'Order':>{col_w[3]}}"
        f"{'Proj. Left':>{col_w[4]}}"
    )
    print(f"\n{header}")
    print("-" * 62)

    all_types = sorted(
        set(list(sales_by_type.keys()) + list(leftovers.keys()) + list(order_quantities.keys())),
        key=lambda x: x
    )

    for ptype in all_types:
        sold = sales_by_type.get(ptype, 0)
        leftover = leftovers.get(ptype, 0)
        order_qty = order_quantities.get(ptype, 0)
        proj = projected_leftovers.get(ptype, 0)

        order_str = str(order_qty) if order_qty > 0 else "-"
        proj_str = str(proj) if proj > 0 else "-"

        print(
            f"{ptype:<{col_w[0]}}"
            f"{sold:>{col_w[1]}}"
            f"{leftover:>{col_w[2]}}"
            f"{order_str:>{col_w[3]}}"
            f"{proj_str:>{col_w[4]}}"
        )

    print("-" * 62)
    total_order = sum(order_quantities.values())
    print(f"{'TOTAL TO ORDER':<{col_w[0]}}{'':{col_w[1]}}{'':{col_w[2]}}{total_order:>{col_w[3]}}")
    print()

    if unmapped:
        print("  Products not matched to any packaging type:")
        for title, qty in sorted(unmapped.items(), key=lambda x: -x[1]):
            print(f"    {qty:>4}x  {title}")
        print()
        print("  To include these in your order, add matching keywords")
        print("  for them in sticker_config.json.")
        print()

    print("=" * 62)
    print()


def main():
    parser = argparse.ArgumentParser(description='Calculate monthly sticker order for Cannibisters.')
    parser.add_argument('--month', help='Month to analyse (YYYY-MM). Defaults to last calendar month.')
    parser.add_argument('--save', action='store_true', help='Save projected leftover counts to sticker_inventory.json.')
    args = parser.parse_args()

    # Determine month to analyse
    if args.month:
        try:
            dt = datetime.strptime(args.month, '%Y-%m')
            year, month = dt.year, dt.month
        except ValueError:
            print(f"ERROR: Invalid month format '{args.month}'. Use YYYY-MM.")
            sys.exit(1)
    else:
        year, month = get_last_month()

    month_label = f"{year}-{month:02d}"
    print(f"\nAnalysing Shopify sales for: {month_label}")

    # Load config
    try:
        config = load_json(CONFIG_FILE)
    except FileNotFoundError:
        print(f"ERROR: Config file '{CONFIG_FILE}' not found.")
        sys.exit(1)

    packaging_types = config.get('packaging_types', {})
    if not packaging_types:
        print("ERROR: No packaging_types defined in sticker_config.json.")
        sys.exit(1)

    # Load inventory (leftovers)
    try:
        inventory = load_json(INVENTORY_FILE)
    except FileNotFoundError:
        print(f"WARNING: Inventory file '{INVENTORY_FILE}' not found. Assuming zero leftovers.")
        inventory = {}

    leftovers = inventory.get('leftovers', {})
    # Strip meta keys
    leftovers = {k: v for k, v in leftovers.items() if not k.startswith('_')}

    # Fetch orders from Shopify
    start_date, end_date = month_date_range(year, month)
    print(f"Fetching orders from {start_date} to {end_date}...")
    orders = list_orders(created_at_min=start_date, created_at_max=end_date, status='any')
    print(f"Retrieved {len(orders)} orders.\n")

    # Count sales by packaging type
    sales_by_type, unmapped = count_sales_by_type(orders, packaging_types)

    # Calculate what to order
    order_quantities, projected_leftovers = calculate_order(sales_by_type, leftovers)

    # Print the report
    print_report(year, month, sales_by_type, leftovers, order_quantities, projected_leftovers, unmapped)

    # Optionally save projected leftovers
    if args.save:
        inventory['last_updated'] = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        inventory['leftovers'] = projected_leftovers
        save_json(INVENTORY_FILE, inventory)
        print(f"Projected leftovers saved to {INVENTORY_FILE}.")
        print("Edit that file to correct the actual leftover count before running next month.\n")
    else:
        print("Tip: Run with --save to store projected leftover counts for next month's calculation.")
        print()


if __name__ == '__main__':
    main()
