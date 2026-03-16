#!/usr/bin/env python3
"""
Shopify Webhook Seal Token Verification
Verifies incoming Shopify webhook requests using HMAC-SHA256 seal tokens.
"""

import hmac
import hashlib
import base64
import os
from dotenv import load_dotenv

load_dotenv()

SHOPIFY_WEBHOOK_SECRET = os.getenv('SHOPIFY_WEBHOOK_SECRET')


def verify_webhook(data: bytes, hmac_header: str, secret: str = None) -> bool:
    """
    Verify a Shopify webhook request using HMAC-SHA256 seal token.

    Shopify signs each webhook with a base64-encoded HMAC-SHA256 digest
    of the raw request body using the webhook secret as the key.

    Args:
        data: Raw request body bytes
        hmac_header: Value of the X-Shopify-Hmac-Sha256 header
        secret: Webhook secret (defaults to SHOPIFY_WEBHOOK_SECRET env var)

    Returns:
        True if the webhook signature is valid, False otherwise
    """
    webhook_secret = secret or SHOPIFY_WEBHOOK_SECRET
    if not webhook_secret:
        raise ValueError("Missing SHOPIFY_WEBHOOK_SECRET. Set it in your .env file.")

    digest = hmac.new(
        webhook_secret.encode('utf-8'),
        data,
        hashlib.sha256
    ).digest()
    computed_hmac = base64.b64encode(digest).decode('utf-8')

    return hmac.compare_digest(computed_hmac, hmac_header)


def get_seal_token() -> str:
    """
    Return the configured webhook seal token (secret).

    Returns:
        The SHOPIFY_WEBHOOK_SECRET value
    """
    token = SHOPIFY_WEBHOOK_SECRET
    if not token:
        raise ValueError("Missing SHOPIFY_WEBHOOK_SECRET in .env file.")
    return token


if __name__ == '__main__':
    # Verify configuration
    try:
        token = get_seal_token()
        masked = token[:8] + '...' + token[-4:]
        print(f"✅ Seal token configured: {masked}")
    except ValueError as e:
        print(f"❌ {e}")
