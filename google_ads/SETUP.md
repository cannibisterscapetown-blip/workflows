# Google Ads Agent — Setup Guide

## Overview

This agent manages Google Ads for Cannibisters via the Google Ads API.
All ad traffic is directed to **cannibisters.co.za** (membership site) — never to
cannibisters.com (product store). This is the core policy compliance strategy.

---

## Step 1: Get a Google Ads Developer Token

1. Sign in to your Google Ads Manager (MCC) account at ads.google.com
2. Go to **Tools & Settings → API Center**
3. Apply for a developer token (starts as "Test Account" access)
4. For production use (real campaigns), apply for "Basic Access" — requires
   completing a form about your use case
5. Copy the token — this becomes `GOOGLE_ADS_DEVELOPER_TOKEN`

> Note: With Test Account access you can still read data and test API calls,
> but cannot create live campaigns. Apply for Basic Access before going live.

---

## Step 2: Create a Google Cloud Project & OAuth2 Credentials

1. Go to console.cloud.google.com
2. Create a new project: "Cannibisters Ads Agent"
3. Enable the **Google Ads API** (APIs & Services → Library → search "Google Ads API")
4. Go to **APIs & Services → Credentials → Create Credentials → OAuth 2.0 Client ID**
5. Application type: **Desktop app**
6. Name it "Cannibisters Ads Agent"
7. Download the credentials JSON
8. Copy `client_id` → `GOOGLE_ADS_CLIENT_ID`
9. Copy `client_secret` → `GOOGLE_ADS_CLIENT_SECRET`

---

## Step 3: Get a Refresh Token (OAuth2 Flow)

Run the following one-time flow to generate your refresh token:

```bash
pip install google-ads
python google_ads/get_refresh_token.py
```

This opens a browser window. Sign in with the Google account that has access
to your Google Ads account. Paste the authorization code when prompted.

The script prints your `refresh_token` — copy it into your `.env` file.

---

## Step 4: Find Your Customer ID

Your Google Ads Customer ID is the 10-digit number at the top of the Google Ads
interface (format: 123-456-7890).

If you use a Manager (MCC) account:
- `GOOGLE_ADS_LOGIN_CUSTOMER_ID` = the MCC account ID
- `GOOGLE_ADS_CUSTOMER_ID` = the specific ad account ID

---

## Step 5: Add credentials to .env

Add the following to your `.env` file:

```
GOOGLE_ADS_DEVELOPER_TOKEN=your_developer_token_here
GOOGLE_ADS_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_ADS_CLIENT_SECRET=your_client_secret_here
GOOGLE_ADS_REFRESH_TOKEN=your_refresh_token_here
GOOGLE_ADS_CUSTOMER_ID=123-456-7890
GOOGLE_ADS_LOGIN_CUSTOMER_ID=  # only if using MCC, else leave blank
```

---

## Step 6: Install dependencies

```bash
pip install -r requirements.txt
```

---

## Step 7: Test the connection

```bash
# Dry run — no changes, just previews
python google_ads_agent.py --action list_campaigns

# Check compliance of ad copy
python google_ads_agent.py --action check_compliance \
  --headline "Join Our Social Club" \
  --description "Private members club - apply now"

# See all compliant copy templates
python google_ads_agent.py --action show_compliant_copy
```

---

## First Campaign Launch Sequence

**Recommended order:**

```bash
# 1. Preview the campaign scaffold (dry run)
python google_ads_agent.py --action scaffold_campaign --budget 200

# 2. Upload existing leads as Customer Match (warm targeting)
python google_ads_agent.py --action upload_customer_match \
  --file Cleaned_Leads_Master_March_2026.csv

# 3. Review everything in Google Ads UI, then launch
python google_ads_agent.py --action scaffold_campaign --budget 200 --execute
python google_ads_agent.py --action upload_customer_match \
  --file Cleaned_Leads_Master_March_2026.csv --execute

# 4. After 7+ days of data, run optimization
python google_ads_agent.py --action optimize

# 5. Generate a performance report
python google_ads_agent.py --action report --period LAST_7_DAYS
```

---

## Policy Notes for Cannabis Advertising on Google

- **Never** set the landing page to cannibisters.com or any product URL
- **Never** mention cannabis, weed, THC, dagga, or any drug terms in ad copy
- **Always** frame ads as social club membership — not product promotion
- If an ad gets disapproved, the compliance checker (`check_compliance`) can help
  identify and fix the offending terms before resubmission
- Google's cannabis advertising policy is country-specific — SA has no licensed
  dispensary program, so search/display ads are restricted to lifestyle/membership
  framing only

---

## Conversion Tracking Setup

To track membership sign-ups as conversions in Google Ads:

1. In Google Ads UI: **Tools → Conversions → + New Conversion Action**
2. Select **Website**
3. Conversion name: "Membership Sign-Up"
4. Value: Leave blank or set to estimated LTV of a member
5. Count: **One** (one sign-up per user)
6. Copy the Google Tag code
7. Add to the cannibisters.co.za sign-up confirmation page via Google Tag Manager

Once tracking is live, the CPA optimization in this agent will use real sign-up
data to guide budget decisions.
