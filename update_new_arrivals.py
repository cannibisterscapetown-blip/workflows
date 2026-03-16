#!/usr/bin/env python3
import requests
import os

KLAVIYO_API_KEY = os.environ.get('KLAVIYO_API_KEY', 'pk_bbe3e99a1e058ba1b45decc3d66d9575ac')
MSG_ID = '01KKV9756FFVM81A7BR2VQTXG8'
HEADERS = {
    'Authorization': f'Klaviyo-API-Key {KLAVIYO_API_KEY}',
    'revision': '2024-10-15',
    'Content-Type': 'application/json',
}

resp = requests.get(f'https://a.klaviyo.com/api/campaign-messages/{MSG_ID}/template/', headers=HEADERS)
resp.raise_for_status()
data = resp.json()['data']
html = data['attributes']['html']
editor_type = data['attributes'].get('editor_type', 'CODE')
print(f"Fetched HTML length: {len(html)}")

# New products
products = [
    {
        'handle': 'lemon-cherry-gelato',
        'title': 'Lemon Cherry Gelato',
        'price': 'R 190',
        'image': 'https://cdn.shopify.com/s/files/1/0631/7749/0644/files/Lemon_Cherry_Gelato_Cannibisters_Discover_with_Leigh_Photography_12.03_1.jpg?v=1773388867',
    },
    {
        'handle': 'greendoor-g-rolls-preroll-joint',
        'title': 'Greendoor G Rolls Preroll Joint',
        'price': 'R 150',
        'image': 'https://cdn.shopify.com/s/files/1/0631/7749/0644/files/cannibisters_joint_tube_efe63e23-bae5-492c-bfb5-2fe0de4328cc.jpg?v=1772622453',
    },
    {
        'handle': 'miami-blu-preroll-joint-living-soil-copy',
        'title': 'Space Cake Preroll Joint - Living Soil',
        'price': 'R 150',
        'image': 'https://cdn.shopify.com/s/files/1/0631/7749/0644/files/uploaded_image_1767192210692_4ceaa3df-5d33-4ca2-b717-0b21998c88d6.jpg?v=1767192283',
    },
]

def make_cell(p):
    url = f"https://cannibisters.com/products/{p['handle']}"
    return (
        f'<td style="padding:8px 6px;text-align:center;" valign="top" width="33%">\n'
        f'<a href="{url}" style="text-decoration:none;color:#1a1a1a;" target="_blank">\n'
        f'<img alt="{p["title"]}" height="150" src="{p["image"]}" style="display:block;margin:0 auto 10px;width:150px;height:150px;object-fit:cover;border-radius:6px;" width="150"/>\n'
        f'<p style="margin:0 0 4px;font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:700;color:#1a1a1a;line-height:1.3;">{p["title"]}</p>\n'
        f'<p style="margin:0 0 10px;font-family:Helvetica,Arial,sans-serif;font-size:12px;color:#555555;">{p["price"]}</p>\n'
        f'</a>\n'
        f'<a href="{url}" style="display:inline-block;background:#f5a623;color:#1a1a1a;font-family:Helvetica,Arial,sans-serif;font-size:12px;font-weight:700;text-decoration:none;padding:8px 20px;border-radius:5px;" target="_blank">Shop now</a>\n'
        f'</td>'
    )

# Old cells (exact strings from the current template)
old_cell1 = (
    '<td style="padding:8px 6px;text-align:center;" valign="top" width="33%">\n'
    '<a href="https://cannibisters.com/products/blue-muffin-joints" style="text-decoration:none;color:#1a1a1a;" target="_blank">\n'
    '<img alt="Blue Muffin Joints" height="150" src="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/uploaded_image_1767192210692_8f2b3b98-1ee8-427d-a261-d38ebb27113d.jpg?v=1770906120" style="display:block;margin:0 auto 10px;width:150px;height:150px;object-fit:cover;border-radius:6px;" width="150"/>\n'
    '<p style="margin:0 0 4px;font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:700;color:#1a1a1a;line-height:1.3;">Blue Muffin Joints</p>\n'
    '<p style="margin:0 0 10px;font-family:Helvetica,Arial,sans-serif;font-size:12px;color:#555555;">R 175</p>\n'
    '</a>\n'
    '<a href="https://cannibisters.com/products/blue-muffin-joints" style="display:inline-block;background:#f5a623;color:#1a1a1a;font-family:Helvetica,Arial,sans-serif;font-size:12px;font-weight:700;text-decoration:none;padding:8px 20px;border-radius:5px;" target="_blank">Shop now</a>\n'
    '</td>'
)

old_cell2 = (
    '<td style="padding:8px 6px;text-align:center;" valign="top" width="33%">\n'
    '<a href="https://cannibisters.com/products/animal-tsunami-joint" style="text-decoration:none;color:#1a1a1a;" target="_blank">\n'
    '<img alt="Animal Tsunami Joint" height="150" src="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/uploaded_image_1767192210692_40e0815b-f5bd-4b85-a1b9-9c415896dc57.jpg?v=1770896939" style="display:block;margin:0 auto 10px;width:150px;height:150px;object-fit:cover;border-radius:6px;" width="150"/>\n'
    '<p style="margin:0 0 4px;font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:700;color:#1a1a1a;line-height:1.3;">Animal Tsunami Joint</p>\n'
    '<p style="margin:0 0 10px;font-family:Helvetica,Arial,sans-serif;font-size:12px;color:#555555;">R 175</p>\n'
    '</a>\n'
    '<a href="https://cannibisters.com/products/animal-tsunami-joint" style="display:inline-block;background:#f5a623;color:#1a1a1a;font-family:Helvetica,Arial,sans-serif;font-size:12px;font-weight:700;text-decoration:none;padding:8px 20px;border-radius:5px;" target="_blank">Shop now</a>\n'
    '</td>'
)

old_cell3 = (
    '<td style="padding:8px 6px;text-align:center;" valign="top" width="33%">\n'
    '<a href="https://cannibisters.com/products/canni-ltd-collection-joints-x3" style="text-decoration:none;color:#1a1a1a;" target="_blank">\n'
    '<img alt="Canni Ltd Collection Joints Special x3" height="150" src="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/cannibisters_joint_tube_12cad8c5-b320-48a1-93be-734ad2c24bf3.jpg?v=1768209352" style="display:block;margin:0 auto 10px;width:150px;height:150px;object-fit:cover;border-radius:6px;" width="150"/>\n'
    '<p style="margin:0 0 4px;font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:700;color:#1a1a1a;line-height:1.3;">Canni Ltd Collection Joints Special x3</p>\n'
    '<p style="margin:0 0 10px;font-family:Helvetica,Arial,sans-serif;font-size:12px;color:#555555;">R 550</p>\n'
    '</a>\n'
    '<a href="https://cannibisters.com/products/canni-ltd-collection-joints-x3" style="display:inline-block;background:#f5a623;color:#1a1a1a;font-family:Helvetica,Arial,sans-serif;font-size:12px;font-weight:700;text-decoration:none;padding:8px 20px;border-radius:5px;" target="_blank">Shop now</a>\n'
    '</td>'
)

assert old_cell1 in html, "cell1 not found"
assert old_cell2 in html, "cell2 not found"
assert old_cell3 in html, "cell3 not found"

html = html.replace(old_cell1, make_cell(products[0]))
html = html.replace(old_cell2, make_cell(products[1]))
html = html.replace(old_cell3, make_cell(products[2]))

print("All 3 replacements applied")

# Verify
assert 'lemon-cherry-gelato' in html
assert 'greendoor-g-rolls-preroll-joint' in html
assert 'miami-blu-preroll-joint-living-soil-copy' in html
assert 'blue-muffin-joints' not in html
assert 'animal-tsunami-joint' not in html
assert 'canni-ltd-collection-joints-x3' not in html
print("Verification passed")

# Create new template
create_resp = requests.post('https://a.klaviyo.com/api/templates/', headers=HEADERS, json={
    'data': {
        'type': 'template',
        'attributes': {
            'name': 'Loyalty Kiosk — New Arrivals + Popular Products',
            'editor_type': editor_type,
            'html': html
        }
    }
})
print(f"Create template status: {create_resp.status_code}")
if create_resp.status_code not in (200, 201):
    print(create_resp.text)
    raise Exception("Failed to create template")

new_id = create_resp.json()['data']['id']
print(f"New template ID: {new_id}")

assign_resp = requests.post('https://a.klaviyo.com/api/campaign-message-assign-template/', headers=HEADERS, json={
    'data': {
        'type': 'campaign-message',
        'id': MSG_ID,
        'relationships': {
            'template': {'data': {'type': 'template', 'id': new_id}}
        }
    }
})
print(f"Assign status: {assign_resp.status_code}")
if assign_resp.status_code not in (200, 201, 204):
    print(assign_resp.text)
    raise Exception("Failed to assign template")

print(f"Done! Template '{new_id}' assigned to campaign message {MSG_ID}")
