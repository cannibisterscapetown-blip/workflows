"""
fetch_meta_leads.py — Run this on your Mac to pull all leads from Meta's
Lead Ads API and export them as a CSV ready to drop into Claude.

Usage:
    pip3 install requests
    python3 fetch_meta_leads.py

Output:
    meta_leads_export.csv  — all leads with name, email, phone, city
"""

import requests
import csv
import sys
import time
from datetime import datetime

# ── Config ─────────────────────────────────────────────────────────────────
META_TOKEN   = "EAARNuTktbgkBQZBFW4623uES0KirDOLwTuXuI2bNNDTpMHIczjhEG9xDiUXqTsvq4CYUfViJ4SH3mFOj52OKOvZAKJmkzW4NgTgf6U0nbQ9o0ZCJ2Pfy5OYZCUN4pGsJNHarZA2k5h0DUGQ8H9IYfLIr13XNTxF0QN7JG1xjXhlphYLA1QvwTR8FHhlaRSDoWlQZDZD"
AD_ACCOUNT   = "act_735867919102256"
OUTPUT_FILE  = "meta_leads_export.csv"
API_VERSION  = "v18.0"
BASE_URL     = f"https://graph.facebook.com/{API_VERSION}"
# ───────────────────────────────────────────────────────────────────────────


def get_all_pages(url: str, params: dict) -> list:
    """Follow cursor pagination and collect all results."""
    results = []
    while url:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if "error" in data:
            print(f"  API error: {data['error']['message']}")
            break
        results.extend(data.get("data", []))
        paging = data.get("paging", {})
        cursors = paging.get("cursors", {})
        after = cursors.get("after")
        if after:
            params = {**params, "after": after}
        elif "next" in paging:
            url = paging["next"]
            params = {}
        else:
            break
    return results


def get_lead_forms() -> list:
    print("Fetching lead forms...")
    url = f"{BASE_URL}/{AD_ACCOUNT}/leadgen_forms"
    params = {
        "fields": "id,name,leads_count,created_time",
        "access_token": META_TOKEN,
        "limit": 100,
    }
    forms = get_all_pages(url, params)
    print(f"  Found {len(forms)} form(s)")
    for f in forms:
        print(f"    [{f['id']}] {f['name']}  —  {f.get('leads_count', '?')} leads  ({f.get('created_time','')[:10]})")
    return forms


def get_leads_for_form(form_id: str, form_name: str) -> list:
    """Fetch all leads from a single form, extracting field values."""
    print(f"  Pulling leads from '{form_name}' ({form_id})...")
    url = f"{BASE_URL}/{form_id}/leads"
    params = {
        "fields": "id,created_time,field_data",
        "access_token": META_TOKEN,
        "limit": 500,
    }
    raw_leads = get_all_pages(url, params)
    print(f"    → {len(raw_leads)} leads")

    leads = []
    for lead in raw_leads:
        row = {
            "Lead ID":       lead.get("id", ""),
            "Created":       lead.get("created_time", "")[:10],
            "Form Name":     form_name,
            "Form ID":       form_id,
            "First Name":    "",
            "Last Name":     "",
            "Email Address": "",
            "Phone Number":  "",
            "Address":       "",
            "External ID":   f"l:{lead.get('id', '')}",
        }
        for field in lead.get("field_data", []):
            name  = field.get("name", "").lower()
            value = (field.get("values") or [""])[0].strip()
            if "first" in name:
                row["First Name"] = value.title()
            elif "last" in name:
                row["Last Name"] = value.title()
            elif "email" in name:
                row["Email Address"] = value.lower()
            elif "phone" in name or "mobile" in name:
                # Normalise to E.164 (+27...)
                v = value.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                if v.startswith("0") and len(v) == 10:
                    v = "+27" + v[1:]
                elif v.startswith("27") and not v.startswith("+"):
                    v = "+" + v
                row["Phone Number"] = v
            elif "city" in name or "address" in name or "location" in name:
                row["Address"] = value.title()
        leads.append(row)
    return leads


def main():
    all_leads = []

    try:
        forms = get_lead_forms()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Meta API: {e}")
        sys.exit(1)

    if not forms:
        print("No lead forms found. Check your token and ad account ID.")
        sys.exit(1)

    for form in forms:
        try:
            leads = get_leads_for_form(form["id"], form["name"])
            all_leads.extend(leads)
            time.sleep(0.3)  # gentle rate limiting
        except requests.exceptions.RequestException as e:
            print(f"  Warning: failed to fetch form {form['id']}: {e}")

    if not all_leads:
        print("No leads found.")
        sys.exit(0)

    # Deduplicate by email
    seen_emails = set()
    deduped = []
    for lead in all_leads:
        email = lead["Email Address"].lower()
        if email and email not in seen_emails:
            seen_emails.add(email)
            deduped.append(lead)
        elif not email:
            deduped.append(lead)  # keep leads without email too

    print(f"\nTotal leads: {len(all_leads)}  |  After dedup by email: {len(deduped)}")

    fieldnames = ["First Name", "Last Name", "Email Address", "Phone Number",
                  "Address", "External ID", "Created", "Form Name", "Form ID", "Lead ID"]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(deduped)

    print(f"Saved {len(deduped)} leads to {OUTPUT_FILE}")
    print("Drop that file into Claude to import them all into Klaviyo.")


if __name__ == "__main__":
    main()
