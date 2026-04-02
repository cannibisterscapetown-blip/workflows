#!/usr/bin/env python3
"""
Email List Hygiene — Remove Hard Bounces via Klaviyo
=====================================================
Fetches all suppressed (hard-bounce) email addresses from Klaviyo,
then strips those addresses from the leads CSV before re-upload.

Usage:
    python clean_email_bounces.py [--input FILE] [--output FILE]

Defaults:
    --input  Final_Purified_Leads_March_2026.csv
    --output Bounce_Cleaned_Leads.csv

Requires KLAVIYO_API_KEY in .env
"""

import os
import sys
import csv
import argparse
import requests
from dotenv import load_dotenv

load_dotenv()

KLAVIYO_API_KEY = os.getenv('KLAVIYO_API_KEY')
KLAVIYO_BASE = 'https://a.klaviyo.com/api'
KLAVIYO_HEADERS = {
    'Authorization': f'Klaviyo-API-Key {KLAVIYO_API_KEY}',
    'revision': '2024-02-15',
    'Accept': 'application/json',
}


def get_suppressed_emails() -> set:
    """
    Fetch all suppressed (hard bounce + manual) profiles from Klaviyo.
    Returns a set of lowercase email addresses.
    """
    suppressed = set()
    url = f'{KLAVIYO_BASE}/profiles/'
    # Filter to suppression reasons that indicate deliverability risk
    params = {
        'filter': 'any(subscriptions.email.marketing.suppressions[].reason,'
                  '["hard_bounce","invalid_email","reported_as_spam"])',
        'fields[profile]': 'email',
        'page[size]': 100,
    }

    page = 0
    while url:
        page += 1
        resp = requests.get(url, headers=KLAVIYO_HEADERS, params=params if page == 1 else None)
        if resp.status_code == 401:
            print("❌ Klaviyo auth failed — check KLAVIYO_API_KEY in .env")
            sys.exit(1)
        resp.raise_for_status()
        data = resp.json()

        for profile in data.get('data', []):
            email = profile.get('attributes', {}).get('email', '').lower().strip()
            if email:
                suppressed.add(email)

        # Follow pagination
        next_cursor = data.get('links', {}).get('next')
        url = next_cursor if next_cursor else None
        params = None  # cursor URL is fully formed

    return suppressed


def clean_leads(input_path: str, output_path: str, suppressed: set) -> dict:
    """
    Read the leads CSV, strip bounced emails, write cleaned output.
    Returns stats dict.
    """
    rows_in = []
    with open(input_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            rows_in.append(row)

    rows_out = []
    removed = []
    email_col = next(
        (h for h in fieldnames if 'email' in h.lower()), None
    )
    if not email_col:
        print(f"❌ Could not find an email column in {input_path}")
        print(f"   Available columns: {fieldnames}")
        sys.exit(1)

    for row in rows_in:
        email = row.get(email_col, '').lower().strip()
        if email in suppressed:
            removed.append(row)
        else:
            rows_out.append(row)

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_out)

    # Write a removed-addresses log for records
    removed_path = output_path.replace('.csv', '_removed_bounces.csv')
    with open(removed_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(removed)

    return {
        'total_in': len(rows_in),
        'total_out': len(rows_out),
        'bounces_removed': len(removed),
        'output': output_path,
        'removed_log': removed_path,
    }


def main():
    parser = argparse.ArgumentParser(description='Strip hard-bounce emails from leads CSV')
    parser.add_argument('--input', default='Final_Purified_Leads_March_2026.csv')
    parser.add_argument('--output', default='Bounce_Cleaned_Leads.csv')
    args = parser.parse_args()

    if not KLAVIYO_API_KEY:
        print("❌ KLAVIYO_API_KEY not set in .env — cannot fetch suppression list.")
        sys.exit(1)

    if not os.path.exists(args.input):
        print(f"❌ Input file not found: {args.input}")
        sys.exit(1)

    print(f"📬 Fetching suppressed emails from Klaviyo...")
    suppressed = get_suppressed_emails()
    print(f"   Found {len(suppressed):,} suppressed addresses (hard bounces, spam reports, invalid).")

    print(f"🧹 Cleaning {args.input}...")
    stats = clean_leads(args.input, args.output, suppressed)

    print()
    print("=" * 50)
    print("EMAIL LIST HYGIENE — RESULTS")
    print("=" * 50)
    print(f"  Input rows        : {stats['total_in']:,}")
    print(f"  Bounces removed   : {stats['bounces_removed']:,}")
    print(f"  Clean rows out    : {stats['total_out']:,}")
    print(f"  Cleaned list      : {stats['output']}")
    print(f"  Removed log       : {stats['removed_log']}")
    print("=" * 50)
    print(f"\n✅ Upload {stats['output']} to Klaviyo to replace your current list.")


if __name__ == '__main__':
    main()
