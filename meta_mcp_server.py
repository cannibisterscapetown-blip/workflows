#!/usr/bin/env python3
"""
meta_mcp_server.py — MCP server for Meta Graph API (Lead Ads focus)

Gives Claude direct access to:
  - list_lead_forms     → all lead gen forms in the ad account
  - get_leads           → all leads from a specific form (or all forms)
  - get_campaigns       → campaign list with basic stats
  - get_ad_insights     → reach/impressions/clicks/leads for campaigns

Setup (run once on your Mac):
    pip3 install mcp requests

Add to ~/Library/Application Support/Claude/claude_desktop_config.json:
    {
      "mcpServers": {
        "meta-graph": {
          "command": "python3",
          "args": ["/path/to/meta_mcp_server.py"],
          "env": {
            "META_ACCESS_TOKEN": "YOUR_TOKEN_HERE",
            "META_AD_ACCOUNT":   "act_735867919102256"
          }
        }
      }
    }

Then restart the Claude desktop app.
"""

import os
import sys
import json
import time
import requests
from mcp.server.fastmcp import FastMCP

META_TOKEN  = os.environ.get("META_ACCESS_TOKEN", "")
AD_ACCOUNT  = os.environ.get("META_AD_ACCOUNT", "act_735867919102256")
API_VERSION = "v18.0"
BASE_URL    = f"https://graph.facebook.com/{API_VERSION}"

mcp = FastMCP("meta-graph")


# ── helpers ────────────────────────────────────────────────────────────────

def _get(path: str, params: dict) -> dict:
    params = {"access_token": META_TOKEN, **params}
    resp = requests.get(f"{BASE_URL}{path}", params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def _paginate(path: str, params: dict, limit: int = 0) -> list:
    """Collect all pages of results up to `limit` (0 = all)."""
    results = []
    url = f"{BASE_URL}{path}"
    p = {"access_token": META_TOKEN, **params}
    while url:
        resp = requests.get(url, params=p, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if "error" in data:
            raise RuntimeError(data["error"]["message"])
        batch = data.get("data", [])
        results.extend(batch)
        if limit and len(results) >= limit:
            results = results[:limit]
            break
        paging = data.get("paging", {})
        after = paging.get("cursors", {}).get("after")
        if after:
            p = {**p, "after": after}
        elif "next" in paging:
            url = paging["next"]
            p = {}
        else:
            break
        time.sleep(0.1)
    return results


def _parse_lead(lead: dict, form_name: str = "") -> dict:
    row = {
        "lead_id":      lead.get("id", ""),
        "created":      lead.get("created_time", "")[:10],
        "form_name":    form_name,
        "first_name":   "",
        "last_name":    "",
        "email":        "",
        "phone":        "",
        "city":         "",
    }
    for field in lead.get("field_data", []):
        name  = field.get("name", "").lower()
        value = (field.get("values") or [""])[0].strip()
        if "first" in name:
            row["first_name"] = value.title()
        elif "last" in name:
            row["last_name"] = value.title()
        elif "email" in name:
            row["email"] = value.lower()
        elif "phone" in name or "mobile" in name:
            v = value.replace(" ", "").replace("-", "")
            if v.startswith("0") and len(v) == 10:
                v = "+27" + v[1:]
            elif v.startswith("27") and not v.startswith("+"):
                v = "+" + v
            row["phone"] = v
        elif "city" in name or "address" in name or "location" in name:
            row["city"] = value.title()
    return row


# ── tools ──────────────────────────────────────────────────────────────────

@mcp.tool()
def list_lead_forms() -> str:
    """List all lead gen forms in the Cannibisters Meta ad account with lead counts."""
    forms = _paginate(f"/{AD_ACCOUNT}/leadgen_forms",
                      {"fields": "id,name,leads_count,created_time", "limit": 100})
    if not forms:
        return "No lead forms found."
    lines = [f"Found {len(forms)} lead form(s):\n"]
    for f in forms:
        lines.append(f"  [{f['id']}] {f['name']}")
        lines.append(f"    Leads: {f.get('leads_count','?')}  |  Created: {f.get('created_time','')[:10]}")
    return "\n".join(lines)


@mcp.tool()
def get_leads(form_id: str = "", max_leads: int = 0) -> str:
    """
    Fetch leads from a specific form (or all forms if form_id is empty).
    Returns a JSON array of lead objects with name, email, phone, city.
    max_leads: cap on total leads returned (0 = all).
    """
    if form_id:
        forms = [{"id": form_id, "name": ""}]
    else:
        forms = _paginate(f"/{AD_ACCOUNT}/leadgen_forms",
                          {"fields": "id,name", "limit": 100})

    all_leads = []
    for form in forms:
        raw = _paginate(f"/{form['id']}/leads",
                        {"fields": "id,created_time,field_data", "limit": 500},
                        limit=max_leads if max_leads else 0)
        for lead in raw:
            all_leads.append(_parse_lead(lead, form.get("name", "")))
        if max_leads and len(all_leads) >= max_leads:
            all_leads = all_leads[:max_leads]
            break

    # Dedup by email
    seen, deduped = set(), []
    for lead in all_leads:
        e = lead["email"]
        if e and e in seen:
            continue
        if e:
            seen.add(e)
        deduped.append(lead)

    return json.dumps(deduped, ensure_ascii=False)


@mcp.tool()
def get_campaigns() -> str:
    """List all campaigns in the ad account with status and objective."""
    campaigns = _paginate(
        f"/{AD_ACCOUNT}/campaigns",
        {"fields": "id,name,status,objective,created_time,start_time,stop_time", "limit": 100}
    )
    if not campaigns:
        return "No campaigns found."
    lines = [f"Found {len(campaigns)} campaign(s):\n"]
    for c in campaigns:
        lines.append(f"  [{c['id']}] {c['name']}")
        lines.append(f"    Status: {c.get('status')}  |  Objective: {c.get('objective')}")
        lines.append(f"    Start: {c.get('start_time','?')[:10]}  |  Stop: {c.get('stop_time','ongoing')[:10] if c.get('stop_time') else 'ongoing'}")
    return "\n".join(lines)


@mcp.tool()
def get_ad_insights(campaign_id: str = "", date_preset: str = "last_90_days") -> str:
    """
    Get performance insights (reach, impressions, clicks, leads, spend) for campaigns.
    date_preset options: today, yesterday, last_7_days, last_30_days, last_90_days,
                         this_month, last_month, last_year, maximum
    campaign_id: leave empty to get account-level insights.
    """
    path = f"/{campaign_id}/insights" if campaign_id else f"/{AD_ACCOUNT}/insights"
    params = {
        "fields": "campaign_name,reach,impressions,clicks,actions,spend,date_start,date_stop",
        "date_preset": date_preset,
        "level": "campaign" if not campaign_id else "campaign",
        "limit": 100,
    }
    results = _paginate(path, params)
    if not results:
        return "No insights data found for that period."

    lines = [f"Ad insights ({date_preset}):\n"]
    for r in results:
        leads = next((a["value"] for a in r.get("actions", []) if a["action_type"] == "lead"), "0")
        lines.append(f"  {r.get('campaign_name', campaign_id)}")
        lines.append(f"    Period : {r.get('date_start')} → {r.get('date_stop')}")
        lines.append(f"    Reach  : {r.get('reach','?')}   Impressions: {r.get('impressions','?')}")
        lines.append(f"    Clicks : {r.get('clicks','?')}   Leads: {leads}   Spend: R{float(r.get('spend',0))*18.5:.2f}")
    return "\n".join(lines)


# ── main ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if not META_TOKEN:
        print("ERROR: META_ACCESS_TOKEN environment variable not set.", file=sys.stderr)
        sys.exit(1)
    mcp.run(transport="stdio")
