"""
Import Meta leads from CSV into Klaviyo by firing 'Filled out Lead Ad' events.
This triggers the Meta Lead Ad Nurture Flow (SK6Ayf) for each lead.

Klaviyo rate limit: ~75 requests / 10 seconds for private API keys.
~3,553 leads → estimated ~8 minutes to complete.
"""

import csv
import json
import time
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

KLAVIYO_KEY = "pk_5fc000523784ba538dc86738bc48cd0a45"
CSV_FILE = "/home/user/workflows/Final_Purified_Leads_March_2026.csv"
BATCH_SIZE = 10       # requests per batch
BATCH_DELAY = 1.5     # seconds between batches (10 batches/15s ≈ 40 req/10s, safe margin)
EVENTS_URL = "https://a.klaviyo.com/api/events/"


def create_event(lead: dict) -> tuple[bool, str]:
    """Fire 'Filled out Lead Ad' event for a single lead. Returns (success, message)."""
    email = lead.get("Email Address", "").strip()
    if not email:
        return False, "no email"

    first_name = lead.get("First Name", "").strip().title()
    last_name = lead.get("Last Name", "").strip().title()
    phone = lead.get("Phone Number", "").strip()
    city = lead.get("Address", "").strip().title()
    external_id = lead.get("External ID", "").strip()

    # Clean phone: must be E.164 format
    if phone and not phone.startswith("+"):
        phone = ""  # skip non-standard phones

    payload = {
        "data": {
            "type": "event",
            "attributes": {
                "metric": {
                    "data": {
                        "type": "metric",
                        "attributes": {"name": "Filled out Lead Ad"}
                    }
                },
                "profile": {
                    "data": {
                        "type": "profile",
                        "attributes": {
                            "email": email,
                            "first_name": first_name,
                            "last_name": last_name,
                            **({"phone_number": phone} if phone else {}),
                            **({"location": {"city": city}} if city else {}),
                            **({"external_id": external_id} if external_id else {}),
                        }
                    }
                },
                "properties": {
                    "source": "Meta Lead Ad",
                    "import_batch": "backfill_march2026",
                    "city": city,
                },
                "time": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                "value": 0,
            }
        }
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        EVENTS_URL,
        data=data,
        headers={
            "Authorization": f"Klaviyo-API-Key {KLAVIYO_KEY}",
            "revision": "2024-10-15",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return True, str(resp.status)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:200]
        if e.code == 429:
            return None, "rate_limited"  # None = retry
        return False, f"HTTP {e.code}: {body}"
    except Exception as e:
        return False, str(e)


def main():
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        leads = list(csv.DictReader(f))

    total = len(leads)
    print(f"Loaded {total} leads from CSV.")
    print(f"Starting import at {datetime.now().strftime('%H:%M:%S')} ...")
    print("-" * 60)

    success = 0
    failed = 0
    skipped = 0
    start = time.time()

    for i, lead in enumerate(leads):
        # Batch delay
        if i > 0 and i % BATCH_SIZE == 0:
            elapsed = time.time() - start
            rate = i / elapsed
            eta = (total - i) / rate if rate > 0 else 0
            print(
                f"  [{i}/{total}] {success} ok | {failed} fail | {skipped} skip | "
                f"{rate:.1f} req/s | ETA {eta/60:.1f}min"
            )
            time.sleep(BATCH_DELAY)

        email = lead.get("Email Address", "").strip()
        if not email or "@" not in email:
            skipped += 1
            continue

        # Retry once on rate limit
        result, msg = create_event(lead)
        if result is None:  # rate limited
            time.sleep(5)
            result, msg = create_event(lead)

        if result is True:
            success += 1
        elif result is False:
            failed += 1
            if failed <= 10 or failed % 100 == 0:
                print(f"  FAIL [{i}] {email}: {msg}")

    elapsed = time.time() - start
    print("-" * 60)
    print(f"Done in {elapsed/60:.1f} minutes.")
    print(f"  Success : {success}")
    print(f"  Failed  : {failed}")
    print(f"  Skipped : {skipped}")
    print(f"  Total   : {total}")


if __name__ == "__main__":
    main()
