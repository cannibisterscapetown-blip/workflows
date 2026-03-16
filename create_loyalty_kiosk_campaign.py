#!/usr/bin/env python3
"""
Klaviyo Email Campaign Creator — Cannibisters Loyalty Points Kiosk
Creates a campaign using the "General Canni Template" to announce
the new Loyalty Points Kiosk where members can redeem points for products.

Usage:
    KLAVIYO_API_KEY=pk_xxx python3 create_loyalty_kiosk_campaign.py

Requires:
    pip install requests python-dotenv
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("KLAVIYO_API_KEY")
if not API_KEY:
    print("ERROR: KLAVIYO_API_KEY not set. Add it to your .env file or export it.")
    sys.exit(1)

BASE_URL = "https://a.klaviyo.com/api"
HEADERS = {
    "Authorization": f"Klaviyo-API-Key {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "revision": "2024-10-15",
}

TEMPLATE_NAME = "General Canni Template"
LIST_NAME = "Email List"  # Main Cannibisters email list (Wk5g7N)

# ---------------------------------------------------------------------------
# Email content
# ---------------------------------------------------------------------------

CAMPAIGN_NAME = "Loyalty Kiosk Launch — Redeem Your Points"
SUBJECT_LINE = "Your points are worth more than you think 🏆"
PREVIEW_TEXT = "Redeem your loyalty points for real Cannibisters products — right from the kiosk."

# HTML email body — uses inline styles for broad email client compatibility.
# Replace {{BANNER_IMAGE_URL}} with your actual hosted banner image URL.
EMAIL_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Cannibisters Loyalty Kiosk</title>
</head>
<body style="margin:0;padding:0;background-color:#f5f5f5;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;">

  <!-- Wrapper -->
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f5f5f5;">
    <tr>
      <td align="center" style="padding:32px 16px;">

        <!-- Card -->
        <table width="600" cellpadding="0" cellspacing="0" border="0"
               style="background-color:#ffffff;border-radius:12px;overflow:hidden;max-width:600px;">

          <!-- Banner image -->
          <tr>
            <td>
              <img src="{{BANNER_IMAGE_URL}}"
                   alt="Cannibisters Loyalty Kiosk"
                   width="600"
                   style="display:block;width:100%;max-width:600px;height:auto;" />
            </td>
          </tr>

          <!-- Body copy -->
          <tr>
            <td style="padding:40px 40px 24px;">
              <h1 style="margin:0 0 16px;font-size:28px;font-weight:700;color:#1a1a1a;line-height:1.2;">
                Your points just got a whole lot more powerful.
              </h1>
              <p style="margin:0 0 20px;font-size:16px;color:#444444;line-height:1.6;">
                We've launched the <strong>Cannibisters Loyalty Points Kiosk</strong> — your new way to
                turn every point you've earned into something real. Whether it's a membership upgrade,
                a fan-favourite product, or exclusive Canni merch, your loyalty is now redeemable
                <em>on the spot</em>.
              </p>
              <p style="margin:0 0 28px;font-size:16px;color:#444444;line-height:1.6;">
                Head to the kiosk, browse what's available, and choose your reward. No fuss, no expiry
                stress — just your points working for you.
              </p>
            </td>
          </tr>

          <!-- Highlighted rewards table -->
          <tr>
            <td style="padding:0 40px 32px;">
              <table width="100%" cellpadding="0" cellspacing="0" border="0"
                     style="background-color:#f9f4ff;border-radius:10px;overflow:hidden;">
                <tr>
                  <td style="padding:24px;">
                    <h2 style="margin:0 0 18px;font-size:18px;font-weight:700;color:#6b21a8;">
                      What can you redeem?
                    </h2>
                    <!-- Rewards list -->
                    <table width="100%" cellpadding="0" cellspacing="0" border="0">
                      <tr>
                        <td style="font-size:14px;color:#333;padding:6px 0;border-bottom:1px solid #e5e5e5;width:70%;">50mg THC Lollipop</td>
                        <td style="font-size:14px;color:#6b21a8;font-weight:600;text-align:right;padding:6px 0;border-bottom:1px solid #e5e5e5;">7,500 pts</td>
                      </tr>
                      <tr>
                        <td style="font-size:14px;color:#333;padding:6px 0;border-bottom:1px solid #e5e5e5;">1 Day Membership</td>
                        <td style="font-size:14px;color:#6b21a8;font-weight:600;text-align:right;padding:6px 0;border-bottom:1px solid #e5e5e5;">2,000 pts</td>
                      </tr>
                      <tr>
                        <td style="font-size:14px;color:#333;padding:6px 0;border-bottom:1px solid #e5e5e5;">Canni THC Breath Mint</td>
                        <td style="font-size:14px;color:#6b21a8;font-weight:600;text-align:right;padding:6px 0;border-bottom:1px solid #e5e5e5;">19,999 pts</td>
                      </tr>
                      <tr>
                        <td style="font-size:14px;color:#333;padding:6px 0;border-bottom:1px solid #e5e5e5;">Bucket Hat</td>
                        <td style="font-size:14px;color:#6b21a8;font-weight:600;text-align:right;padding:6px 0;border-bottom:1px solid #e5e5e5;">10,000 pts</td>
                      </tr>
                      <tr>
                        <td style="font-size:14px;color:#333;padding:6px 0;border-bottom:1px solid #e5e5e5;">Gummies 100mg</td>
                        <td style="font-size:14px;color:#6b21a8;font-weight:600;text-align:right;padding:6px 0;border-bottom:1px solid #e5e5e5;">35,000 pts</td>
                      </tr>
                      <tr>
                        <td style="font-size:14px;color:#333;padding:6px 0;border-bottom:1px solid #e5e5e5;">Canni Grinder</td>
                        <td style="font-size:14px;color:#6b21a8;font-weight:600;text-align:right;padding:6px 0;border-bottom:1px solid #e5e5e5;">25,000 pts</td>
                      </tr>
                      <tr>
                        <td style="font-size:14px;color:#333;padding:6px 0;border-bottom:1px solid #e5e5e5;">Canni Hoodie</td>
                        <td style="font-size:14px;color:#6b21a8;font-weight:600;text-align:right;padding:6px 0;border-bottom:1px solid #e5e5e5;">60,000 pts</td>
                      </tr>
                      <tr>
                        <td style="font-size:14px;color:#333;padding:6px 0;border-bottom:1px solid #e5e5e5;">Gummies 200mg</td>
                        <td style="font-size:14px;color:#6b21a8;font-weight:600;text-align:right;padding:6px 0;border-bottom:1px solid #e5e5e5;">45,000 pts</td>
                      </tr>
                      <tr>
                        <td style="font-size:14px;color:#333;padding:6px 0;">12 Month Membership</td>
                        <td style="font-size:14px;color:#6b21a8;font-weight:600;text-align:right;padding:6px 0;">100,000 pts</td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- CTA -->
          <tr>
            <td align="center" style="padding:0 40px 40px;">
              <a href="https://cannibisters.co.za"
                 style="display:inline-block;background-color:#6b21a8;color:#ffffff;font-size:16px;
                        font-weight:700;text-decoration:none;padding:16px 40px;border-radius:8px;
                        letter-spacing:0.3px;">
                Redeem My Points
              </a>
            </td>
          </tr>

          <!-- Divider -->
          <tr>
            <td style="padding:0 40px;">
              <hr style="border:none;border-top:1px solid #eeeeee;margin:0;" />
            </td>
          </tr>

          <!-- Footer note -->
          <tr>
            <td style="padding:24px 40px 32px;">
              <p style="margin:0;font-size:13px;color:#888888;line-height:1.5;">
                Not sure how many points you have? Log in to your Cannibisters account to check your
                balance. The kiosk is available in-store — ask a team member if you need a hand.
              </p>
            </td>
          </tr>

        </table>
        <!-- /Card -->

        <!-- Footer -->
        <table width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;">
          <tr>
            <td align="center" style="padding:24px 16px;font-size:12px;color:#aaaaaa;line-height:1.6;">
              © 2026 Cannibisters. All rights reserved.<br />
              <a href="{{ unsubscribe_url }}" style="color:#aaaaaa;text-decoration:underline;">Unsubscribe</a>
            </td>
          </tr>
        </table>
        <!-- /Footer -->

      </td>
    </tr>
  </table>

</body>
</html>
"""

EMAIL_TEXT = """\
YOUR POINTS JUST GOT A WHOLE LOT MORE POWERFUL.

We've launched the Cannibisters Loyalty Points Kiosk — your new way to turn every point you've earned into something real.

Browse memberships, exclusive products, and Canni merch. Redeem on the spot, no fuss.

WHAT'S AVAILABLE:
- 1 Day Membership — 2,000 pts
- 50mg THC Lollipop — 7,500 pts
- Bucket Hat — 10,000 pts
- Canni THC Breath Mint — 19,999 pts
- Canni Grinder — 25,000 pts
- Gummies 100mg — 35,000 pts
- Gummies 200mg — 45,000 pts
- Canni Hoodie — 60,000 pts
- 12 Month Membership — 100,000 pts
...and more.

Head in-store to redeem: https://cannibisters.co.za

Unsubscribe: {{ unsubscribe_url }}
"""

# ---------------------------------------------------------------------------
# Klaviyo API helpers
# ---------------------------------------------------------------------------

def get_template_id(name: str) -> str | None:
    """Return the template ID whose name matches `name` (case-insensitive)."""
    url = f"{BASE_URL}/templates/"
    params = {"filter": f"equals(name,\"{name}\")"}
    resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json().get("data", [])
    if not data:
        # Fallback: list all and match locally
        resp2 = requests.get(f"{BASE_URL}/templates/", headers=HEADERS, timeout=15)
        resp2.raise_for_status()
        for tpl in resp2.json().get("data", []):
            if tpl["attributes"]["name"].lower() == name.lower():
                return tpl["id"]
        return None
    return data[0]["id"]


def get_list_id(name: str) -> str | None:
    """Return the list ID whose name matches `name` (case-insensitive)."""
    url = f"{BASE_URL}/lists/"
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    for lst in resp.json().get("data", []):
        if lst["attributes"]["name"].lower() == name.lower():
            return lst["id"]
    return None


def create_campaign(list_id: str, template_id: str) -> dict:
    """Create a Klaviyo email campaign (draft)."""
    payload = {
        "data": {
            "type": "campaign",
            "attributes": {
                "name": CAMPAIGN_NAME,
                "audiences": {
                    "included": [list_id],
                    "excluded": [],
                },
                "send_options": {
                    "use_smart_sending": True,
                },
                "campaign-messages": {
                    "data": [{
                        "type": "campaign-message",
                        "attributes": {
                            "channel": "email",
                            "label": "Loyalty Kiosk Email",
                            "content": {
                                "subject": SUBJECT_LINE,
                                "preview_text": PREVIEW_TEXT,
                                "from_email": "hello@cannibisters.co.za",
                                "from_label": "Cannibisters",
                            },
                        },
                    }]
                },
            },
        }
    }
    resp = requests.post(f"{BASE_URL}/campaigns/", headers=HEADERS, json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()["data"]


def assign_template_to_message(message_id: str, template_id: str) -> dict:
    """
    Assign a template to a campaign message via the dedicated Klaviyo endpoint:
    POST /api/campaign-message-assign-template/
    """
    payload = {
        "data": {
            "type": "campaign-message",
            "id": message_id,
            "relationships": {
                "template": {
                    "data": {"type": "template", "id": template_id}
                }
            },
        }
    }
    resp = requests.post(
        f"{BASE_URL}/campaign-message-assign-template/",
        headers=HEADERS,
        json=payload,
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()["data"]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=== Cannibisters — Loyalty Kiosk Campaign Creator ===\n")

    # 1. Resolve template
    print(f"Looking up template: '{TEMPLATE_NAME}' ...")
    template_id = get_template_id(TEMPLATE_NAME)
    if not template_id:
        print(f"ERROR: Template '{TEMPLATE_NAME}' not found in your Klaviyo account.")
        print("       Available templates can be viewed at https://www.klaviyo.com/email-template/list")
        sys.exit(1)
    print(f"  Template ID: {template_id}")

    # 2. Resolve list
    print(f"\nLooking up list: '{LIST_NAME}' ...")
    list_id = get_list_id(LIST_NAME)
    if not list_id:
        print(f"ERROR: List '{LIST_NAME}' not found. Update LIST_NAME at the top of this script.")
        sys.exit(1)
    print(f"  List ID: {list_id}")

    # 3. Create campaign (draft)
    print("\nCreating campaign draft ...")
    campaign = create_campaign(list_id, template_id)
    campaign_id = campaign["id"]
    print(f"  Campaign ID: {campaign_id}")
    print(f"  Name: {campaign['attributes']['name']}")

    # 4. Assign template to the campaign message
    message_id = campaign["relationships"]["campaign-messages"]["data"][0]["id"]
    print(f"\nAssigning template to message {message_id} ...")
    message = assign_template_to_message(message_id, template_id)
    print(f"  Message ID: {message['id']}")

    print("\n✓ Campaign created as a DRAFT.")
    print(f"  → Review & schedule at: https://www.klaviyo.com/campaign/{campaign_id}/")
    print("\nNext steps:")
    print("  1. Upload your banner image and replace {{BANNER_IMAGE_URL}} in the template.")
    print("  2. Review the draft in Klaviyo, customise as needed.")
    print("  3. Send a test email before scheduling.")
    print("  4. Schedule or send when ready.")


if __name__ == "__main__":
    main()
