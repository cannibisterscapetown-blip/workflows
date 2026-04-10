#!/usr/bin/env python3
import requests

KLAVIYO_API_KEY = "pk_2b57d9dd3402b67a041cb42568247ac52b"
TEMPLATE_ID = "U3EWKp"
HEADERS = {
    "Authorization": f"Klaviyo-API-Key {KLAVIYO_API_KEY}",
    "accept": "application/json",
    "content-type": "application/json",
    "revision": "2024-10-15",
}

PIZZA_BLOCK = """
  <!-- PIZZA HIGHLIGHT -->
  <tr>
    <td class="mob-pad" style="padding:0 40px 24px;background-color:#ffffff;">
      <table border="0" cellpadding="0" cellspacing="0" width="100%"
             style="background-color:#fff8ee;border-radius:10px;border:2px solid #ff9501;">
        <tr>
          <td style="padding:22px 24px;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
              <tr>
                <td style="vertical-align:middle;padding-right:16px;width:52px;">
                  <p style="font-size:36px;margin:0;">&#127829;</p>
                </td>
                <td style="vertical-align:middle;">
                  <p style="font-family:Helvetica,Arial,sans-serif;font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#ff9501;margin:0 0 4px 0;">On the house</p>
                  <p style="font-family:Helvetica,Arial,sans-serif;font-size:15px;font-weight:700;color:#060606;margin:0 0 4px 0;">42 Slices of Pizza from NY Slice</p>
                  <p style="font-family:Helvetica,Arial,sans-serif;font-size:13px;line-height:1.6;color:#555555;margin:0;">First come, first served. Because 42 is the only number that matters today.</p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </td>
  </tr>

"""

resp = requests.get(f"https://a.klaviyo.com/api/templates/{TEMPLATE_ID}/", headers=HEADERS)
resp.raise_for_status()
html = resp.json()["data"]["attributes"]["html"]

INSERT_BEFORE = "<!-- MAIN CTA -->"
if INSERT_BEFORE not in html:
    print("ERROR: marker not found")
    exit(1)

html = html.replace(INSERT_BEFORE, PIZZA_BLOCK + INSERT_BEFORE)
print("NY Slice inserted:", "NY Slice" in html)

r = requests.patch(f"https://a.klaviyo.com/api/templates/{TEMPLATE_ID}/", headers=HEADERS,
    json={"data": {"type": "template", "id": TEMPLATE_ID, "attributes": {"html": html}}})
print(f"HTTP {r.status_code}")
