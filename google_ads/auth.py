import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from .config import (
    DEVELOPER_TOKEN, CLIENT_ID, CLIENT_SECRET,
    REFRESH_TOKEN, CUSTOMER_ID, LOGIN_CUSTOMER_ID
)


def validate_credentials():
    required = {
        'GOOGLE_ADS_DEVELOPER_TOKEN': DEVELOPER_TOKEN,
        'GOOGLE_ADS_CLIENT_ID': CLIENT_ID,
        'GOOGLE_ADS_CLIENT_SECRET': CLIENT_SECRET,
        'GOOGLE_ADS_REFRESH_TOKEN': REFRESH_TOKEN,
        'GOOGLE_ADS_CUSTOMER_ID': CUSTOMER_ID,
    }
    missing = [k for k, v in required.items() if not v]
    if missing:
        print("Error: Missing required environment variables:")
        for m in missing:
            print(f"  {m}")
        print("\nSee google_ads/SETUP.md for credential setup instructions.")
        sys.exit(1)


def get_client() -> GoogleAdsClient:
    """Returns an authenticated Google Ads API client."""
    validate_credentials()
    config = {
        'developer_token': DEVELOPER_TOKEN,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': REFRESH_TOKEN,
        'use_proto_plus': True,
    }
    if LOGIN_CUSTOMER_ID:
        config['login_customer_id'] = LOGIN_CUSTOMER_ID.replace('-', '')
    return GoogleAdsClient.load_from_dict(config)


def clean_customer_id(customer_id: str) -> str:
    """Strips dashes from customer ID (123-456-7890 → 1234567890)."""
    return (customer_id or CUSTOMER_ID).replace('-', '')


def handle_google_ads_exception(ex: GoogleAdsException):
    print(f"Request ID: {ex.request_id}")
    print(f"Failure: {ex.failure}")
    for error in ex.failure.errors:
        print(f"  Error code: {error.error_code}")
        print(f"  Message: {error.message}")
        if error.location:
            for field_path_element in error.location.field_path_elements:
                print(f"  Field: {field_path_element.field_name}")
