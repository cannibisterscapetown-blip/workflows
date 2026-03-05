import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adsinsights import AdsInsights

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

def fetch_campaigns(account):
    """Fetch all campaigns with their performance data."""
    print("\n" + "="*80)
    print("CAMPAIGNS OVERVIEW")
    print("="*80)
    
    # Date range for insights (last 30 days)
    date_preset = 'last_30d'
    
    campaigns = account.get_campaigns(fields=[
        Campaign.Field.id,
        Campaign.Field.name,
        Campaign.Field.status,
        Campaign.Field.objective,
        Campaign.Field.daily_budget,
        Campaign.Field.lifetime_budget,
        Campaign.Field.created_time,
        Campaign.Field.updated_time,
    ])
    
    campaign_data = []
    
    for campaign in campaigns:
        print(f"\n📊 Campaign: {campaign.get('name', 'N/A')}")
        print(f"   ID: {campaign.get('id')}")
        print(f"   Status: {campaign.get('status', 'N/A')}")
        print(f"   Objective: {campaign.get('objective', 'N/A')}")
        print(f"   Created: {campaign.get('created_time', 'N/A')}")
        
        # Fetch insights for this campaign
        try:
            insights = campaign.get_insights(params={
                'date_preset': date_preset,
                'level': 'campaign',
            }, fields=[
                AdsInsights.Field.impressions,
                AdsInsights.Field.reach,
                AdsInsights.Field.clicks,
                AdsInsights.Field.spend,
                AdsInsights.Field.ctr,
                AdsInsights.Field.cpc,
                AdsInsights.Field.cpp,
                AdsInsights.Field.cpm,
                AdsInsights.Field.frequency,
                AdsInsights.Field.actions,
                AdsInsights.Field.cost_per_action_type,
            ])
            
            if insights:
                insight = insights[0]
                print(f"\n   📈 Performance (Last 30 Days):")
                print(f"      Spend: R{float(insight.get('spend', 0)):.2f}")
                print(f"      Impressions: {insight.get('impressions', 0):,}")
                print(f"      Reach: {insight.get('reach', 0):,}")
                print(f"      Clicks: {insight.get('clicks', 0):,}")
                print(f"      CTR: {float(insight.get('ctr', 0)):.2f}%")
                print(f"      CPC: R{float(insight.get('cpc', 0)):.2f}")
                print(f"      CPM: R{float(insight.get('cpm', 0)):.2f}")
                print(f"      Frequency: {float(insight.get('frequency', 0)):.2f}")
                
                # Actions
                actions = insight.get('actions', [])
                if actions:
                    print(f"\n   🎯 Actions:")
                    for action in actions:
                        print(f"      {action.get('action_type')}: {action.get('value')}")
                
                campaign_data.append({
                    'campaign': campaign,
                    'insights': insight
                })
            else:
                print(f"   ⚠️  No performance data available")
                campaign_data.append({
                    'campaign': campaign,
                    'insights': None
                })
                
        except Exception as e:
            print(f"   ❌ Error fetching insights: {e}")
            campaign_data.append({
                'campaign': campaign,
                'insights': None
            })
    
    return campaign_data

def fetch_ad_sets(account):
    """Fetch all ad sets with their performance data."""
    print("\n" + "="*80)
    print("AD SETS OVERVIEW")
    print("="*80)
    
    date_preset = 'last_30d'
    
    ad_sets = account.get_ad_sets(fields=[
        AdSet.Field.id,
        AdSet.Field.name,
        AdSet.Field.status,
        AdSet.Field.campaign_id,
        AdSet.Field.daily_budget,
        AdSet.Field.lifetime_budget,
        AdSet.Field.optimization_goal,
        AdSet.Field.billing_event,
        AdSet.Field.bid_strategy,
        AdSet.Field.targeting,
        AdSet.Field.start_time,
        AdSet.Field.end_time,
    ])
    
    ad_set_data = []
    
    for ad_set in ad_sets:
        print(f"\n📊 Ad Set: {ad_set.get('name', 'N/A')}")
        print(f"   ID: {ad_set.get('id')}")
        print(f"   Status: {ad_set.get('status', 'N/A')}")
        print(f"   Optimization Goal: {ad_set.get('optimization_goal', 'N/A')}")
        print(f"   Bid Strategy: {ad_set.get('bid_strategy', 'N/A')}")
        print(f"   Daily Budget: R{float(ad_set.get('daily_budget', 0))/100:.2f}" if ad_set.get('daily_budget') else "   Lifetime Budget")
        
        # Fetch insights
        try:
            insights = ad_set.get_insights(params={
                'date_preset': date_preset,
                'level': 'adset',
            }, fields=[
                AdsInsights.Field.impressions,
                AdsInsights.Field.reach,
                AdsInsights.Field.clicks,
                AdsInsights.Field.spend,
                AdsInsights.Field.ctr,
                AdsInsights.Field.cpc,
                AdsInsights.Field.cpm,
                AdsInsights.Field.frequency,
            ])
            
            if insights:
                insight = insights[0]
                print(f"\n   📈 Performance (Last 30 Days):")
                print(f"      Spend: R{float(insight.get('spend', 0)):.2f}")
                print(f"      Impressions: {insight.get('impressions', 0):,}")
                print(f"      Reach: {insight.get('reach', 0):,}")
                print(f"      Clicks: {insight.get('clicks', 0):,}")
                print(f"      CTR: {float(insight.get('ctr', 0)):.2f}%")
                print(f"      CPC: R{float(insight.get('cpc', 0)):.2f}")
                print(f"      CPM: R{float(insight.get('cpm', 0)):.2f}")
                print(f"      Frequency: {float(insight.get('frequency', 0)):.2f}")
                
                ad_set_data.append({
                    'ad_set': ad_set,
                    'insights': insight
                })
            else:
                print(f"   ⚠️  No performance data available")
                ad_set_data.append({
                    'ad_set': ad_set,
                    'insights': None
                })
                
        except Exception as e:
            print(f"   ❌ Error fetching insights: {e}")
            ad_set_data.append({
                'ad_set': ad_set,
                'insights': None
            })
    
    return ad_set_data

def fetch_ads(account):
    """Fetch all ads with their performance data."""
    print("\n" + "="*80)
    print("ADS OVERVIEW")
    print("="*80)
    
    date_preset = 'last_30d'
    
    ads = account.get_ads(fields=[
        Ad.Field.id,
        Ad.Field.name,
        Ad.Field.status,
        Ad.Field.adset_id,
        Ad.Field.creative,
        Ad.Field.created_time,
    ])
    
    ads_data = []
    
    for ad in ads:
        print(f"\n📊 Ad: {ad.get('name', 'N/A')}")
        print(f"   ID: {ad.get('id')}")
        print(f"   Status: {ad.get('status', 'N/A')}")
        print(f"   Created: {ad.get('created_time', 'N/A')}")
        
        # Fetch insights
        try:
            insights = ad.get_insights(params={
                'date_preset': date_preset,
                'level': 'ad',
            }, fields=[
                AdsInsights.Field.impressions,
                AdsInsights.Field.reach,
                AdsInsights.Field.clicks,
                AdsInsights.Field.spend,
                AdsInsights.Field.ctr,
                AdsInsights.Field.cpc,
                AdsInsights.Field.cpm,
                AdsInsights.Field.frequency,
                AdsInsights.Field.actions,
            ])
            
            if insights:
                insight = insights[0]
                print(f"\n   📈 Performance (Last 30 Days):")
                print(f"      Spend: R{float(insight.get('spend', 0)):.2f}")
                print(f"      Impressions: {insight.get('impressions', 0):,}")
                print(f"      Reach: {insight.get('reach', 0):,}")
                print(f"      Clicks: {insight.get('clicks', 0):,}")
                print(f"      CTR: {float(insight.get('ctr', 0)):.2f}%")
                print(f"      CPC: R{float(insight.get('cpc', 0)):.2f}")
                print(f"      CPM: R{float(insight.get('cpm', 0)):.2f}")
                
                ads_data.append({
                    'ad': ad,
                    'insights': insight
                })
            else:
                print(f"   ⚠️  No performance data available")
                ads_data.append({
                    'ad': ad,
                    'insights': None
                })
                
        except Exception as e:
            print(f"   ❌ Error fetching insights: {e}")
            ads_data.append({
                'ad': ad,
                'insights': None
            })
    
    return ads_data

def analyze_and_recommend(campaign_data, ad_set_data, ads_data):
    """Analyze performance and provide optimization recommendations."""
    print("\n" + "="*80)
    print("OPTIMIZATION RECOMMENDATIONS")
    print("="*80)
    
    recommendations = []
    
    # Analyze campaigns
    for data in campaign_data:
        campaign = data['campaign']
        insights = data['insights']
        
        if insights:
            spend = float(insights.get('spend', 0))
            ctr = float(insights.get('ctr', 0))
            frequency = float(insights.get('frequency', 0))
            
            # High frequency warning
            if frequency > 3:
                recommendations.append({
                    'type': 'WARNING',
                    'level': 'Campaign',
                    'name': campaign.get('name'),
                    'issue': f'High frequency ({frequency:.2f})',
                    'recommendation': 'Consider expanding your audience or refreshing creative to avoid ad fatigue'
                })
            
            # Low CTR warning
            if ctr < 1.0 and spend > 100:
                recommendations.append({
                    'type': 'WARNING',
                    'level': 'Campaign',
                    'name': campaign.get('name'),
                    'issue': f'Low CTR ({ctr:.2f}%)',
                    'recommendation': 'Test new ad creatives or refine targeting to improve engagement'
                })
    
    # Analyze ad sets
    for data in ad_set_data:
        ad_set = data['ad_set']
        insights = data['insights']
        
        if insights:
            spend = float(insights.get('spend', 0))
            ctr = float(insights.get('ctr', 0))
            cpc = float(insights.get('cpc', 0))
            
            # High CPC warning
            if cpc > 5 and spend > 50:
                recommendations.append({
                    'type': 'WARNING',
                    'level': 'Ad Set',
                    'name': ad_set.get('name'),
                    'issue': f'High CPC (R{cpc:.2f})',
                    'recommendation': 'Consider adjusting bid strategy or targeting to reduce cost per click'
                })
    
    # Print recommendations
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. [{rec['type']}] {rec['level']}: {rec['name']}")
            print(f"   Issue: {rec['issue']}")
            print(f"   💡 Recommendation: {rec['recommendation']}")
    else:
        print("\n✅ No major issues detected. Campaigns are performing within acceptable ranges.")
    
    return recommendations

def main():
    initialize_api()
    account = get_ad_account()
    
    print(f"\n🎯 Analyzing Meta Ads Account: {AD_ACCOUNT_ID}")
    print(f"📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Fetch all data
    campaign_data = fetch_campaigns(account)
    ad_set_data = fetch_ad_sets(account)
    ads_data = fetch_ads(account)
    
    # Analyze and provide recommendations
    recommendations = analyze_and_recommend(campaign_data, ad_set_data, ads_data)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)

if __name__ == '__main__':
    main()
