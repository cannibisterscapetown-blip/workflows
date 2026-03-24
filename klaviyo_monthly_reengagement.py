#!/usr/bin/env python3
"""
Cannibisters — Monthly Re-engagement Campaign Sender
Clones the template campaign and sends it on the first Tuesday of each month.

Usage:
    python3 klaviyo_monthly_reengagement.py           # Run now (checks if today is send day)
    python3 klaviyo_monthly_reengagement.py --force   # Force send regardless of date
    python3 klaviyo_monthly_reengagement.py --dry-run # Preview without sending

Cron (runs daily at 08:00 SAST = 06:00 UTC):
    0 6 * * 2 /usr/bin/python3 /home/user/workflows/klaviyo_monthly_reengagement.py
"""

import os
import json
import time
import datetime
import argparse
import urllib.request
import urllib.error

# ── Config ─────────────────────────────────────────────────────────────────────
API_KEY       = os.environ.get("KLAVIYO_API_KEY", "pk_552612cc562841ff962ceb13c1b1776d4d")
API_REVISION  = "2024-02-15"
BASE_URL      = "https://a.klaviyo.com/api"

# The draft April campaign — used as the template for cloning each month.
# Update this ID each month after verifying the new draft is ready.
TEMPLATE_CAMPAIGN_ID = "01KMFM2QBBA59FNXH6ATMWY384"  # Re-engagement - April 2026

# Audience segment: Lapsed Members — 90+ Days No Order
AUDIENCE_SEGMENT_ID  = "QZkYEP"

SEND_HOUR_UTC = 6   # 06:00 UTC = 08:00 SAST
# ──────────────────────────────────────────────────────────────────────────────


def api_request(method: str, path: str, body: dict = None) -> dict:
    url  = f"{BASE_URL}/{path}"
    data = json.dumps(body).encode() if body else None
    req  = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Klaviyo-API-Key {API_KEY}")
    req.add_header("revision", API_REVISION)
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            err = json.loads(raw)
        except Exception:
            err = {"raw": raw}
        raise RuntimeError(f"HTTP {e.code} {method} {path}: {json.dumps(err)}")


def first_tuesday_of_month(year: int, month: int) -> datetime.date:
    """Return the date of the first Tuesday in the given month."""
    d = datetime.date(year, month, 1)
    days_until_tuesday = (1 - d.weekday()) % 7   # Tuesday = weekday 1
    return d + datetime.timedelta(days=days_until_tuesday)


def is_send_day() -> bool:
    today = datetime.date.today()
    target = first_tuesday_of_month(today.year, today.month)
    return today == target


def month_label(d: datetime.date) -> str:
    return d.strftime("%B %Y")


def clone_campaign(template_id: str, name: str) -> str:
    """Clone a campaign and return the new campaign ID."""
    print(f"  Cloning campaign '{template_id}' as '{name}'...")
    result = api_request("POST", "campaign-clone/", {
        "data": {"type": "campaign", "id": template_id}
    })
    new_id = result["data"]["id"]
    print(f"  Cloned → {new_id}")

    # Rename
    api_request("PATCH", f"campaigns/{new_id}/", {
        "data": {
            "type": "campaign",
            "id": new_id,
            "attributes": {"name": name}
        }
    })
    print(f"  Renamed to '{name}'")
    return new_id


def send_campaign(campaign_id: str) -> None:
    """Trigger an immediate send for the campaign."""
    print(f"  Triggering send for campaign {campaign_id}...")
    api_request("POST", "campaign-send-jobs/", {
        "data": {
            "type": "campaign-send-job",
            "id": campaign_id
        }
    })
    print("  Send job created.")


def verify_campaign(campaign_id: str) -> dict:
    result = api_request("GET", f"campaigns/{campaign_id}/")
    attrs = result["data"]["attributes"]
    return {
        "id": campaign_id,
        "name": attrs.get("name"),
        "status": attrs.get("status"),
    }


def run(force: bool = False, dry_run: bool = False) -> None:
    today = datetime.date.today()
    target = first_tuesday_of_month(today.year, today.month)
    label = month_label(target)
    campaign_name = f"Re-engagement campaign - {label}"

    print("=" * 60)
    print(f"Cannibisters Monthly Re-engagement Sender")
    print(f"Today: {today}  |  Target send day: {target}")
    print(f"Campaign name: {campaign_name}")
    print("=" * 60)

    if not force and not is_send_day():
        print(f"\nNot the send day (first Tuesday = {target}). Nothing to do.")
        print("Use --force to override.\n")
        return

    if dry_run:
        print(f"\n[DRY RUN] Would clone and send '{campaign_name}' today.")
        print(f"[DRY RUN] Template campaign: {TEMPLATE_CAMPAIGN_ID}")
        print(f"[DRY RUN] Audience segment: {AUDIENCE_SEGMENT_ID}")
        return

    print(f"\nSend day confirmed. Proceeding...\n")

    try:
        new_id = clone_campaign(TEMPLATE_CAMPAIGN_ID, campaign_name)
        time.sleep(2)   # brief pause to allow Klaviyo to finish setup

        info = verify_campaign(new_id)
        print(f"\n  Pre-send check: {info}")

        if info["status"].lower() != "draft":
            raise RuntimeError(f"Campaign is not in Draft status: {info['status']}")

        send_campaign(new_id)
        time.sleep(3)

        final = verify_campaign(new_id)
        print(f"\n  Final status: {final}")
        print(f"\nDone. Campaign '{campaign_name}' ({new_id}) is now sending.")

    except RuntimeError as e:
        print(f"\nERROR: {e}")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send monthly re-engagement campaign")
    parser.add_argument("--force",   action="store_true", help="Send regardless of date")
    parser.add_argument("--dry-run", action="store_true", help="Preview without sending")
    args = parser.parse_args()

    run(force=args.force, dry_run=args.dry_run)
