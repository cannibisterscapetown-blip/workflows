"""
Customer Match audience upload for Google Ads.

Uploads existing leads/customers as a hashed audience list so Google can
match them to signed-in Google users. This lets us run search ads targeted
specifically at people already in our Klaviyo / CRM database.

Why this matters for Cannibisters:
  - Warm audience = higher conversion rates and lower CPAs
  - People who gave us their email are already interested in the brand
  - We can bid more aggressively on these users without wasting budget on cold traffic
  - Policy risk is lower since we're not blasting unknown audiences

Requirements:
  - Minimum ~1,000 matched users for the list to activate (Google needs ~1,000 matches)
  - Emails must be hashed (SHA-256) before upload — this module handles that
  - Google Customer Match must be enabled on the account (requires $50k+ lifetime spend
    or approval from Google — check Account Settings > Audiences)

Usage:
  python google_ads_agent.py --action upload_customer_match --file Cleaned_Leads_Master_March_2026.csv
"""

import csv
import hashlib
import sys
from pathlib import Path
from typing import List, Optional
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

from .config import CUSTOMER_ID, BRAND_NAME
from .auth import clean_customer_id, handle_google_ads_exception


def _sha256(value: str) -> str:
    """Hash and normalise a PII value as required by Google."""
    return hashlib.sha256(value.strip().lower().encode()).hexdigest()


def _normalise_phone(phone: str) -> str:
    """Strip non-digit chars and ensure E.164-ish format for SA numbers."""
    digits = ''.join(c for c in phone if c.isdigit())
    if digits.startswith('0') and len(digits) == 10:
        digits = '27' + digits[1:]
    elif not digits.startswith('27'):
        digits = '27' + digits
    return '+' + digits


def load_leads_from_csv(filepath: str) -> List[dict]:
    """
    Load leads from CSV file. Handles the Cannibisters leads CSV format.
    Looks for columns: Email, Phone, First Name, Last Name (case-insensitive).
    """
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    leads = []
    with open(path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        headers = [h.lower().strip() for h in reader.fieldnames or []]

        email_col = next((h for h in reader.fieldnames if h.lower().strip() in
                          ('email', 'email address', 'e-mail')), None)
        phone_col = next((h for h in reader.fieldnames if h.lower().strip() in
                          ('phone', 'phone number', 'mobile', 'cell', 'contact number')), None)
        first_col = next((h for h in reader.fieldnames if h.lower().strip() in
                          ('first name', 'firstname', 'first')), None)
        last_col = next((h for h in reader.fieldnames if h.lower().strip() in
                         ('last name', 'lastname', 'surname', 'last')), None)

        for row in reader:
            lead = {}
            if email_col and row.get(email_col, '').strip():
                lead['email'] = row[email_col].strip()
            if phone_col and row.get(phone_col, '').strip():
                lead['phone'] = row[phone_col].strip()
            if first_col and row.get(first_col, '').strip():
                lead['first_name'] = row[first_col].strip()
            if last_col and row.get(last_col, '').strip():
                lead['last_name'] = row[last_col].strip()
            if lead:
                leads.append(lead)

    print(f"Loaded {len(leads)} leads from {path.name}")
    if email_col:
        email_count = sum(1 for l in leads if 'email' in l)
        print(f"  Leads with email: {email_count}")
    if phone_col:
        phone_count = sum(1 for l in leads if 'phone' in l)
        print(f"  Leads with phone: {phone_count}")

    return leads


def create_customer_match_list(
    client: GoogleAdsClient,
    list_name: str,
    description: str = "",
    membership_life_span_days: int = 540,
    customer_id: str = None,
    execute: bool = False,
) -> Optional[str]:
    """Create a new Customer Match user list."""
    cid = clean_customer_id(customer_id)

    print(f"\nCreating Customer Match list: {list_name}")
    if not execute:
        print(f"  [DRY RUN] Would create list '{list_name}' ({membership_life_span_days} day membership)")
        return None

    try:
        user_list_service = client.get_service("UserListService")
        op = client.get_type("UserListOperation")
        user_list = op.create

        user_list.name = list_name
        user_list.description = description
        user_list.membership_life_span = membership_life_span_days
        user_list.crm_based_user_list.upload_key_type = (
            client.enums.CustomerMatchUploadKeyTypeEnum.CONTACT_INFO
        )
        user_list.crm_based_user_list.data_source_type = (
            client.enums.UserListCrmDataSourceTypeEnum.FIRST_PARTY
        )

        response = user_list_service.mutate_user_lists(
            customer_id=cid, operations=[op]
        )
        resource_name = response.results[0].resource_name
        print(f"  User list created: {resource_name}")
        return resource_name

    except GoogleAdsException as ex:
        handle_google_ads_exception(ex)
        return None


def upload_leads_to_list(
    client: GoogleAdsClient,
    user_list_resource: str,
    leads: List[dict],
    customer_id: str = None,
    execute: bool = False,
) -> int:
    """Hash and upload leads to a Customer Match user list."""
    cid = clean_customer_id(customer_id)

    print(f"\nUploading {len(leads)} leads to Customer Match list")
    if not execute:
        print("  [DRY RUN] Would hash and upload leads. Use --execute to apply.")
        sample = leads[:3]
        for l in sample:
            print(f"    Email: {l.get('email', 'N/A')[:20]}... → [SHA-256 hash]")
        return 0

    try:
        offline_user_data_service = client.get_service("OfflineUserDataJobService")

        # Create the upload job
        job_op = client.get_type("CreateOfflineUserDataJobRequest")
        job_type = client.get_type("OfflineUserDataJob")
        job_type.type_ = (
            client.enums.OfflineUserDataJobTypeEnum.CUSTOMER_MATCH_USER_LIST
        )
        job_type.customer_match_user_list_metadata.user_list = user_list_resource

        job_resource = offline_user_data_service.create_offline_user_data_job(
            customer_id=cid,
            job=job_type,
        ).resource_name

        print(f"  Upload job created: {job_resource}")

        # Build user data operations in batches of 100
        batch_size = 100
        total_uploaded = 0

        for i in range(0, len(leads), batch_size):
            batch = leads[i:i + batch_size]
            user_data_ops = []

            for lead in batch:
                user_data_op = client.get_type("OfflineUserDataJobOperation")
                user_identifier = client.get_type("UserIdentifier")

                if 'email' in lead:
                    user_identifier.hashed_email = _sha256(lead['email'])
                    user_data_op.create.user_identifiers.append(user_identifier)

                if 'phone' in lead:
                    try:
                        normalised = _normalise_phone(lead['phone'])
                        phone_id = client.get_type("UserIdentifier")
                        phone_id.hashed_phone_number = _sha256(normalised)
                        user_data_op.create.user_identifiers.append(phone_id)
                    except Exception:
                        pass  # Skip malformed phone numbers

                if user_data_op.create.user_identifiers:
                    user_data_ops.append(user_data_op)

            if user_data_ops:
                offline_user_data_service.add_offline_user_data_job_operations(
                    resource_name=job_resource,
                    operations=user_data_ops,
                )
                total_uploaded += len(user_data_ops)

        # Run the job
        offline_user_data_service.run_offline_user_data_job(resource_name=job_resource)
        print(f"  Uploaded {total_uploaded} user records. Job running — takes ~6-24h to process.")
        return total_uploaded

    except GoogleAdsException as ex:
        handle_google_ads_exception(ex)
        return 0


def upload_customer_match_from_file(
    client: GoogleAdsClient,
    filepath: str,
    list_name: str = None,
    customer_id: str = None,
    execute: bool = False,
):
    """Full flow: load CSV → create list → upload leads."""
    name = list_name or f"{BRAND_NAME} - Leads Upload - {__import__('datetime').datetime.now().strftime('%Y%m%d')}"

    leads = load_leads_from_csv(filepath)
    if len(leads) < 100:
        print(f"Warning: Only {len(leads)} leads loaded. Google requires ~1,000 matches to activate the list.")

    user_list_resource = create_customer_match_list(
        client, name,
        description="Cannibisters Klaviyo leads and customers for membership targeting",
        customer_id=customer_id,
        execute=execute,
    )

    placeholder = user_list_resource or "customers/XXX/userLists/YYY [dry run]"
    uploaded = upload_leads_to_list(
        client, placeholder, leads, customer_id, execute
    )

    print(f"\nCustomer Match upload complete.")
    print(f"  List: {name}")
    print(f"  Records uploaded: {uploaded}")
    if execute:
        print("  Note: The list will show 0 size until Google processes it (up to 24h).")
        print("  After processing, attach this audience to your campaigns with Observation or Targeting mode.")
