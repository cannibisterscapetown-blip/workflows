---
description: Optimize Meta Ads campaigns with automated tools
---

# Meta Ads Campaign Optimization Workflow

## Quick Start

### 1. Analyze Current Campaigns
Run the analysis script to get a comprehensive overview of all campaigns:
```bash
python3 analyze_meta_campaigns.py
```

This will show you:
- All active and paused campaigns
- Performance metrics (spend, impressions, clicks, CTR, etc.)
- Optimization recommendations

### 2. Review Optimization Report
Check the detailed report at:
```
/Users/norton/.gemini/antigravity/brain/[conversation-id]/meta_ads_optimization_report.md
```

### 3. Run Optimization Actions

#### Preview Changes (Dry Run - Safe)
```bash
# Preview archiving old campaigns
python3 optimize_meta_campaigns.py --action archive_old --days 90

# Preview pausing high-frequency ads
python3 optimize_meta_campaigns.py --action pause_high_frequency --frequency 3.5

# List campaigns by spend
python3 optimize_meta_campaigns.py --action list_spend

# Get budget optimization recommendations
python3 optimize_meta_campaigns.py --action optimize_budget

# Run all optimizations (preview only)
python3 optimize_meta_campaigns.py --action all
```

#### Execute Changes (Use with Caution)
```bash
# Actually archive old campaigns
python3 optimize_meta_campaigns.py --action archive_old --days 90 --execute

# Actually pause high-frequency ads
python3 optimize_meta_campaigns.py --action pause_high_frequency --frequency 3.5 --execute

# Run all optimizations
python3 optimize_meta_campaigns.py --action all --execute
```

## Common Optimization Tasks

### Task 1: Clean Up Old Campaigns
**Goal:** Archive paused campaigns older than 90 days to declutter your account

```bash
# Preview first
python3 optimize_meta_campaigns.py --action archive_old --days 90

# Execute if satisfied
python3 optimize_meta_campaigns.py --action archive_old --days 90 --execute
```

### Task 2: Prevent Ad Fatigue
**Goal:** Pause ad sets with high frequency (>3.5) to avoid audience burnout

```bash
# Preview first
python3 optimize_meta_campaigns.py --action pause_high_frequency --frequency 3.5

# Execute if satisfied
python3 optimize_meta_campaigns.py --action pause_high_frequency --frequency 3.5 --execute
```

### Task 3: Identify Top Spenders
**Goal:** See which campaigns are consuming the most budget

```bash
python3 optimize_meta_campaigns.py --action list_spend
```

### Task 4: Budget Reallocation
**Goal:** Get recommendations for budget adjustments

```bash
python3 optimize_meta_campaigns.py --action optimize_budget
```

## Key Recommendations Summary

### Immediate Actions
1. ✅ **Archive old paused campaigns** (50+ campaigns cluttering account)
2. ✅ **Fix sales campaigns** (3 campaigns with no data - verify Pixel & catalog)
3. ✅ **Reallocate budget** (Shift from engagement to sales campaigns)
4. ✅ **Set up conversion tracking** (Install/verify Facebook Pixel)

### Budget Allocation
**Current:** 70% Engagement, 20% Link Clicks, 10% Sales  
**Recommended:** 50% Sales, 30% Link Clicks, 20% Engagement

### Campaign Structure
Focus on:
- **Prospecting** - Cold traffic campaigns
- **Retargeting** - Website visitors, cart abandoners
- **Testing** - Creative and audience testing

## Safety Notes

> [!CAUTION]
> Always run commands in **dry-run mode first** (default) to preview changes before executing.

> [!IMPORTANT]
> The `--execute` flag will make actual changes to your Meta ads account. Use carefully.

## Troubleshooting

### API Rate Limit Error
If you see "User request limit reached", wait 15-30 minutes before trying again.

### No Performance Data
Some campaigns may show no data if:
- They're newly created (< 24 hours)
- They have no spend
- They're paused and haven't run recently

## Next Steps

1. Review the optimization report
2. Run dry-run previews of recommended actions
3. Execute approved optimizations
4. Monitor performance for 7 days
5. Repeat analysis monthly
