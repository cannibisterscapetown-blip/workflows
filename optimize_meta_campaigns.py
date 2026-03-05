import os
import sys
import argparse
from datetime import datetime
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet

# Load environment variables
load_dotenv()

# Configuration from .env
ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
AD_ACCOUNT_ID = os.getenv('META_AD_ACCOUNT_ID')

def initialize_api():
    """Initializes the Facebook Ads API."""
    if not ACCESS_TOKEN:
        print("Error: META_ACCESS_TOKEN not found in environment variables.")
        sys.exit(1)
    if not AD_ACCOUNT_ID:
        print("Error: META_AD_ACCOUNT_ID not found in environment variables.")
        sys.exit(1)
        
    FacebookAdsApi.init(access_token=ACCESS_TOKEN)

def get_ad_account():
    """Returns the Ad Account object."""
    account_id = AD_ACCOUNT_ID
    if not account_id.startswith('act_'):
        account_id = 'act_' + account_id
    return AdAccount(account_id)

def archive_old_campaigns(account, days_old=90, dry_run=True):
    """Archive paused campaigns older than specified days."""
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Archiving campaigns older than {days_old} days...")
    
    campaigns = account.get_campaigns(fields=[
        Campaign.Field.id,
        Campaign.Field.name,
        Campaign.Field.status,
        Campaign.Field.created_time,
    ])
    
    archived_count = 0
    cutoff_date = datetime.now()
    
    for campaign in campaigns:
        if campaign.get('status') == 'PAUSED':
            created_time = datetime.strptime(campaign.get('created_time'), '%Y-%m-%dT%H:%M:%S%z')
            days_since_created = (cutoff_date.replace(tzinfo=created_time.tzinfo) - created_time).days
            
            if days_since_created > days_old:
                print(f"  {'[WOULD ARCHIVE]' if dry_run else '[ARCHIVING]'} {campaign.get('name')} (Created: {created_time.date()}, {days_since_created} days ago)")
                
                if not dry_run:
                    try:
                        campaign.update(params={
                            Campaign.Field.status: Campaign.Status.archived
                        })
                        archived_count += 1
                    except Exception as e:
                        print(f"    ❌ Error archiving: {e}")
                else:
                    archived_count += 1
    
    print(f"\n{'Would archive' if dry_run else 'Archived'} {archived_count} campaigns")
    return archived_count

def pause_high_frequency_ads(account, frequency_threshold=3.5, dry_run=True):
    """Pause ad sets with frequency above threshold."""
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Pausing ad sets with frequency > {frequency_threshold}...")
    
    ad_sets = account.get_ad_sets(fields=[
        AdSet.Field.id,
        AdSet.Field.name,
        AdSet.Field.status,
    ])
    
    paused_count = 0
    
    for ad_set in ad_sets:
        if ad_set.get('status') == 'ACTIVE':
            try:
                insights = ad_set.get_insights(params={
                    'date_preset': 'last_7d',
                    'level': 'adset',
                }, fields=['frequency'])
                
                if insights and len(insights) > 0:
                    frequency = float(insights[0].get('frequency', 0))
                    
                    if frequency > frequency_threshold:
                        print(f"  {'[WOULD PAUSE]' if dry_run else '[PAUSING]'} {ad_set.get('name')} (Frequency: {frequency:.2f})")
                        
                        if not dry_run:
                            ad_set.update(params={
                                AdSet.Field.status: AdSet.Status.paused
                            })
                            paused_count += 1
                        else:
                            paused_count += 1
            except Exception as e:
                # Skip if we can't get insights (likely no data)
                pass
    
    print(f"\n{'Would pause' if dry_run else 'Paused'} {paused_count} ad sets")
    return paused_count

def list_campaigns_by_spend(account, days=30):
    """List campaigns sorted by spend."""
    print(f"\nTop campaigns by spend (last {days} days):")
    
    campaigns = account.get_campaigns(fields=[
        Campaign.Field.id,
        Campaign.Field.name,
        Campaign.Field.status,
        Campaign.Field.objective,
    ])
    
    campaign_spend = []
    
    for campaign in campaigns:
        try:
            insights = campaign.get_insights(params={
                'date_preset': f'last_{days}d',
                'level': 'campaign',
            }, fields=['spend'])
            
            if insights and len(insights) > 0:
                spend = float(insights[0].get('spend', 0))
                if spend > 0:
                    campaign_spend.append({
                        'name': campaign.get('name'),
                        'status': campaign.get('status'),
                        'objective': campaign.get('objective'),
                        'spend': spend
                    })
        except Exception as e:
            pass
    
    # Sort by spend
    campaign_spend.sort(key=lambda x: x['spend'], reverse=True)
    
    print(f"\n{'Campaign':<50} {'Status':<10} {'Objective':<20} {'Spend':>10}")
    print("-" * 95)
    
    for camp in campaign_spend[:20]:  # Top 20
        print(f"{camp['name'][:48]:<50} {camp['status']:<10} {camp['objective']:<20} R{camp['spend']:>8.2f}")
    
    return campaign_spend

def optimize_budget_allocation(account, dry_run=True):
    """Suggest budget reallocation based on performance."""
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Analyzing budget allocation...")
    
    # Get all active ad sets
    ad_sets = account.get_ad_sets(fields=[
        AdSet.Field.id,
        AdSet.Field.name,
        AdSet.Field.status,
        AdSet.Field.daily_budget,
        AdSet.Field.campaign_id,
    ])
    
    recommendations = []
    
    for ad_set in ad_sets:
        if ad_set.get('status') == 'ACTIVE' and ad_set.get('daily_budget'):
            try:
                insights = ad_set.get_insights(params={
                    'date_preset': 'last_7d',
                    'level': 'adset',
                }, fields=['spend', 'actions', 'cost_per_action_type'])
                
                if insights and len(insights) > 0:
                    insight = insights[0]
                    spend = float(insight.get('spend', 0))
                    actions = insight.get('actions', [])
                    
                    # Check if getting results
                    if spend > 100 and len(actions) == 0:
                        recommendations.append({
                            'ad_set_id': ad_set.get('id'),
                            'name': ad_set.get('name'),
                            'current_budget': float(ad_set.get('daily_budget')) / 100,
                            'spend': spend,
                            'recommendation': 'DECREASE',
                            'reason': 'No actions/conversions',
                            'suggested_budget': float(ad_set.get('daily_budget')) / 100 * 0.5
                        })
            except Exception as e:
                pass
    
    if recommendations:
        print(f"\nBudget Optimization Recommendations:")
        print(f"{'Ad Set':<40} {'Current':<10} {'Suggested':<10} {'Reason':<30}")
        print("-" * 95)
        
        for rec in recommendations:
            print(f"{rec['name'][:38]:<40} R{rec['current_budget']:<9.2f} R{rec['suggested_budget']:<9.2f} {rec['reason']:<30}")
    else:
        print("\n✅ No budget optimization recommendations at this time")
    
    return recommendations

def main():
    parser = argparse.ArgumentParser(description='Optimize Meta Ad Campaigns')
    parser.add_argument('--action', required=True, choices=[
        'archive_old',
        'pause_high_frequency',
        'list_spend',
        'optimize_budget',
        'all'
    ], help='Optimization action to perform')
    parser.add_argument('--dry-run', action='store_true', default=True, 
                       help='Preview changes without applying them (default: True)')
    parser.add_argument('--execute', action='store_true', 
                       help='Actually execute the changes (overrides --dry-run)')
    parser.add_argument('--days', type=int, default=90, 
                       help='Days threshold for archive_old action (default: 90)')
    parser.add_argument('--frequency', type=float, default=3.5, 
                       help='Frequency threshold for pause_high_frequency action (default: 3.5)')
    
    args = parser.parse_args()
    
    # Determine if this is a dry run
    dry_run = not args.execute
    
    initialize_api()
    account = get_ad_account()
    
    print(f"\n🎯 Meta Ads Optimization Tool")
    print(f"Account: {AD_ACCOUNT_ID}")
    print(f"Mode: {'DRY RUN (preview only)' if dry_run else 'EXECUTION MODE'}")
    print("=" * 80)
    
    if args.action == 'archive_old' or args.action == 'all':
        archive_old_campaigns(account, days_old=args.days, dry_run=dry_run)
    
    if args.action == 'pause_high_frequency' or args.action == 'all':
        pause_high_frequency_ads(account, frequency_threshold=args.frequency, dry_run=dry_run)
    
    if args.action == 'list_spend' or args.action == 'all':
        list_campaigns_by_spend(account, days=30)
    
    if args.action == 'optimize_budget' or args.action == 'all':
        optimize_budget_allocation(account, dry_run=dry_run)
    
    print("\n" + "=" * 80)
    if dry_run:
        print("✅ Preview complete. Use --execute to apply changes.")
    else:
        print("✅ Optimization complete!")

if __name__ == '__main__':
    main()
