"""
One-time script to generate a Google Ads OAuth2 refresh token.
Run this once, save the refresh_token to your .env, and you're done.

Usage:
  python google_ads/get_refresh_token.py
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('GOOGLE_ADS_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_ADS_CLIENT_SECRET')

SCOPES = ['https://www.googleapis.com/auth/adwords']
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'  # Desktop app out-of-band flow


def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("Error: GOOGLE_ADS_CLIENT_ID and GOOGLE_ADS_CLIENT_SECRET must be set in .env")
        sys.exit(1)

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        print("Install google-auth-oauthlib: pip install google-auth-oauthlib")
        sys.exit(1)

    client_config = {
        "installed": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uris": [REDIRECT_URI],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }

    flow = InstalledAppFlow.from_client_config(client_config, scopes=SCOPES)
    flow.redirect_uri = REDIRECT_URI

    auth_url, _ = flow.authorization_url(access_type='offline', prompt='consent')
    print("\nOpen this URL in your browser and sign in with your Google Ads account:")
    print(f"\n  {auth_url}\n")
    code = input("Paste the authorization code here: ").strip()

    flow.fetch_token(code=code)
    credentials = flow.credentials

    print(f"\nRefresh token obtained successfully.")
    print(f"\nAdd this to your .env file:")
    print(f"\n  GOOGLE_ADS_REFRESH_TOKEN={credentials.refresh_token}")
    print("\nDo not share this token — it grants access to your Google Ads account.")


if __name__ == '__main__':
    main()
