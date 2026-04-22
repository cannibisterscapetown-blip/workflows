#!/usr/bin/env python3
"""
Cannibisters Google Ads Agent
==============================
Create, manage and optimize Google Ads campaigns for Cannibisters Herbal Apothecary.

Conversion pipeline:
  Google Search/Display → cannibisters.co.za (membership sign-up)
  → Klaviyo email nurture → cannibisters.com (product purchase)

Policy approach:
  All Google Ads point exclusively to cannibisters.co.za (social club membership app).
  The .com product store is NEVER used as a landing page in Google Ads.
  Ad copy focuses on club membership — never on cannabis products.

Usage:
  python google_ads_agent.py --action scaffold_campaign
  python google_ads_agent.py --action scaffold_campaign --execute --budget 300

  python google_ads_agent.py --action create_display_campaign
  python google_ads_agent.py --action create_display_campaign --execute

  python google_ads_agent.py --action upload_customer_match --file Cleaned_Leads_Master_March_2026.csv
  python google_ads_agent.py --action upload_customer_match --file Cleaned_Leads_Master_March_2026.csv --execute

  python google_ads_agent.py --action list_campaigns
  python google_ads_agent.py --action report
  python google_ads_agent.py --action report --period LAST_7_DAYS

  python google_ads_agent.py --action optimize
  python google_ads_agent.py --action optimize --execute

  python google_ads_agent.py --action check_compliance --headline "Join Our Social Club" --description "Members only access"
  python google_ads_agent.py --action show_compliant_copy

Required environment variables (.env):
  GOOGLE_ADS_DEVELOPER_TOKEN
  GOOGLE_ADS_CLIENT_ID
  GOOGLE_ADS_CLIENT_SECRET
  GOOGLE_ADS_REFRESH_TOKEN
  GOOGLE_ADS_CUSTOMER_ID
  GOOGLE_ADS_LOGIN_CUSTOMER_ID  (optional, if using MCC/manager account)

See google_ads/SETUP.md for credential setup instructions.
"""

import argparse
import sys
from dotenv import load_dotenv

load_dotenv()


def main():
    parser = argparse.ArgumentParser(
        description='Cannibisters Google Ads Agent',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        '--action', required=True,
        choices=[
            'scaffold_campaign',
            'create_display_campaign',
            'list_campaigns',
            'report',
            'optimize',
            'upload_customer_match',
            'check_compliance',
            'show_compliant_copy',
            'pause_campaign',
        ],
        help='Action to perform',
    )

    # Execution mode (default: dry run)
    parser.add_argument(
        '--execute', action='store_true', default=False,
        help='Apply changes to Google Ads (default: dry run / preview only)',
    )

    # Campaign options
    parser.add_argument('--name', help='Campaign or list name')
    parser.add_argument(
        '--budget', type=float, default=200,
        help='Daily budget in ZAR (default: 200)',
    )
    parser.add_argument(
        '--campaign-id',
        help='Google Ads campaign ID (for pause_campaign action)',
    )

    # Report options
    parser.add_argument(
        '--period', default='LAST_30_DAYS',
        choices=[
            'LAST_7_DAYS', 'LAST_14_DAYS', 'LAST_30_DAYS',
            'THIS_MONTH', 'LAST_MONTH', 'THIS_WEEK_SUN_TODAY',
        ],
        help='Date range for report (default: LAST_30_DAYS)',
    )

    # Customer Match options
    parser.add_argument(
        '--file',
        help='Path to CSV file for Customer Match upload (leads/customers)',
    )

    # Compliance check options
    parser.add_argument(
        '--headline', action='append', dest='headlines',
        help='Headline to check (use multiple times for multiple headlines)',
    )
    parser.add_argument(
        '--description', action='append', dest='descriptions',
        help='Description to check (use multiple times)',
    )
    parser.add_argument(
        '--url', default=None,
        help='Landing page URL to check (default: cannibisters.co.za)',
    )

    args = parser.parse_args()

    # ---------------------------------------------------------------------------
    # Actions that don't need API auth
    # ---------------------------------------------------------------------------

    if args.action == 'check_compliance':
        from google_ads.compliance import (
            check_ad, print_compliance_report,
            COMPLIANT_HEADLINES, COMPLIANT_DESCRIPTIONS,
            MEMBERSHIP_SIGNUP_URL,
        )
        headlines = args.headlines or []
        descriptions = args.descriptions or []
        url = args.url or MEMBERSHIP_SIGNUP_URL

        if not headlines and not descriptions:
            print("Provide at least one --headline or --description to check.")
            print("\nExample:")
            print("  python google_ads_agent.py --action check_compliance \\")
            print('    --headline "Join Our Social Club" \\')
            print('    --description "Exclusive members club - apply now"')
            sys.exit(1)

        result = check_ad(headlines, descriptions, url)
        print_compliance_report(result, "Ad Compliance Check")
        sys.exit(0 if result.is_safe_to_submit else 1)

    if args.action == 'show_compliant_copy':
        from google_ads.compliance import (
            COMPLIANT_HEADLINES, COMPLIANT_DESCRIPTIONS,
            RECOMMENDED_KEYWORDS, NEGATIVE_KEYWORDS,
        )
        print("\n=== Compliant Headlines (≤30 chars each) ===")
        for h in COMPLIANT_HEADLINES:
            marker = "OK" if len(h) <= 30 else "TOO LONG"
            print(f"  [{marker}] {h!r} ({len(h)} chars)")

        print("\n=== Compliant Descriptions (≤90 chars each) ===")
        for d in COMPLIANT_DESCRIPTIONS:
            marker = "OK" if len(d) <= 90 else "TOO LONG"
            print(f"  [{marker}] {d!r} ({len(d)} chars)")

        print("\n=== Recommended Keywords ===")
        for match_type, keywords in RECOMMENDED_KEYWORDS.items():
            print(f"\n  {match_type}:")
            for kw in keywords:
                print(f"    {kw}")

        print("\n=== Negative Keywords (add to every campaign) ===")
        print("  " + ", ".join(NEGATIVE_KEYWORDS))
        sys.exit(0)

    # ---------------------------------------------------------------------------
    # Actions that require Google Ads API auth
    # ---------------------------------------------------------------------------

    from google_ads.auth import get_client
    from google_ads.config import CUSTOMER_ID

    try:
        client = get_client()
    except SystemExit:
        raise
    except Exception as e:
        print(f"Failed to authenticate with Google Ads API: {e}")
        print("See google_ads/SETUP.md for credential setup instructions.")
        sys.exit(1)

    mode = "EXECUTE" if args.execute else "DRY RUN"
    print(f"\nCannibisters Google Ads Agent")
    print(f"Action: {args.action} | Mode: {mode}")
    print(f"Account: {CUSTOMER_ID}")
    print("-" * 50)

    if args.action == 'scaffold_campaign':
        from google_ads.manager import scaffold_membership_campaign
        scaffold_membership_campaign(
            client,
            customer_id=CUSTOMER_ID,
            campaign_name=args.name,
            daily_budget_zar=args.budget,
            execute=args.execute,
        )

    elif args.action == 'create_display_campaign':
        from google_ads.manager import create_display_awareness_campaign
        create_display_awareness_campaign(
            client,
            name=args.name,
            daily_budget_zar=args.budget,
            customer_id=CUSTOMER_ID,
            execute=args.execute,
        )

    elif args.action == 'list_campaigns':
        from google_ads.manager import list_campaigns
        campaigns = list_campaigns(client, CUSTOMER_ID)
        if not campaigns:
            print("No active campaigns found.")
            return

        print(f"\n{'Campaign':<45} {'Status':<8} {'Type':<10} {'Budget':>8} "
              f"{'Spend':>8} {'Clicks':>7} {'Conv':>5} {'CPA':>8}")
        print("-" * 105)
        for c in campaigns:
            cpa_str = f"R{c['cpa_zar']:.0f}" if c['cpa_zar'] else "N/A"
            print(f"{c['name'][:43]:<45} {c['status'][:6]:<8} {c['type'][:8]:<10} "
                  f"R{c['daily_budget_zar']:>6.0f} R{c['spend_zar']:>6.0f} "
                  f"{c['clicks']:>7,} {c['conversions']:>5.0f} {cpa_str:>8}")

    elif args.action == 'report':
        from google_ads.reporter import generate_full_report
        generate_full_report(client, CUSTOMER_ID, args.period)

    elif args.action == 'optimize':
        from google_ads.optimizer import run_full_optimization
        run_full_optimization(client, CUSTOMER_ID, execute=args.execute)

    elif args.action == 'upload_customer_match':
        if not args.file:
            print("Error: --file is required for upload_customer_match")
            print("Example: python google_ads_agent.py --action upload_customer_match \\")
            print("         --file Cleaned_Leads_Master_March_2026.csv --execute")
            sys.exit(1)
        from google_ads.customer_match import upload_customer_match_from_file
        upload_customer_match_from_file(
            client,
            filepath=args.file,
            list_name=args.name,
            customer_id=CUSTOMER_ID,
            execute=args.execute,
        )

    elif args.action == 'pause_campaign':
        if not args.campaign_id:
            print("Error: --campaign-id is required for pause_campaign")
            sys.exit(1)
        from google_ads.manager import pause_campaign
        pause_campaign(client, args.campaign_id, CUSTOMER_ID, execute=args.execute)


if __name__ == '__main__':
    main()
