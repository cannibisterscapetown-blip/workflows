import os
from dotenv import load_dotenv

load_dotenv()

# --- Google Ads API credentials ---
DEVELOPER_TOKEN = os.getenv('GOOGLE_ADS_DEVELOPER_TOKEN')
CLIENT_ID = os.getenv('GOOGLE_ADS_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_ADS_CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('GOOGLE_ADS_REFRESH_TOKEN')
CUSTOMER_ID = os.getenv('GOOGLE_ADS_CUSTOMER_ID')          # e.g. "123-456-7890"
LOGIN_CUSTOMER_ID = os.getenv('GOOGLE_ADS_LOGIN_CUSTOMER_ID')  # MCC account if used

# --- Cannibisters brand constants ---
BRAND_NAME = "Cannibisters"
MAIN_DOMAIN = "www.cannibisters.com"        # product store - DO NOT use as ad destination
APP_DOMAIN = "www.cannibisters.co.za"       # membership app - safe for Google Ads
MEMBERSHIP_URL = "https://www.cannibisters.co.za"
MEMBERSHIP_SIGNUP_URL = "https://www.cannibisters.co.za/join"

# ZAR: 1 ZAR = 1,000,000 micros (Google Ads internal currency unit)
MICROS_PER_ZAR = 1_000_000

# Default daily budget per campaign (ZAR)
DEFAULT_DAILY_BUDGET_ZAR = 200

# Default max CPC bid (ZAR)
DEFAULT_MAX_CPC_ZAR = 8

# Target audience age range (based on existing lead data)
AGE_MIN = 18
AGE_MAX = 45

# South African geo-target criterion IDs for city-level targeting
# Source: Google Ads GeoTargetConstant — these are verified SA city IDs
GEO_TARGETS = {
    "South Africa": 2710,
    "Cape Town":     20228,
    "Johannesburg":  20226,
    "Pretoria":      20230,
    "Durban":        20224,
    "Port Elizabeth":20231,
    "Bloemfontein":  20222,
    "East London":   20223,
}

# Primary targets based on existing lead distribution
PRIMARY_GEO_TARGETS = [
    GEO_TARGETS["Cape Town"],
    GEO_TARGETS["Johannesburg"],
    GEO_TARGETS["Pretoria"],
    GEO_TARGETS["Durban"],
]

# Optimization thresholds
CTR_FLOOR = 0.5           # pause ad if CTR < 0.5% after 1000 impressions
CPA_TARGET_ZAR = 150      # target cost per membership sign-up
CPA_CEILING_ZAR = 300     # pause/reduce if CPA exceeds this
IMPRESSION_SHARE_FLOOR = 0.3  # flag if impression share drops below 30%
