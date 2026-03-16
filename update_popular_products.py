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

# Fetch current template HTML
resp = requests.get(f'https://a.klaviyo.com/api/campaign-messages/{MSG_ID}/template/', headers=HEADERS)
resp.raise_for_status()
data = resp.json()['data']
html = data['attributes']['html']
editor_type = data['attributes'].get('editor_type', 'CODE')
print(f"Fetched template HTML, length: {len(html)}, editor_type: {editor_type}")

# 1. Rename heading
html = html.replace(
    '<span style="font-size:23px;font-weight:700;text-decoration:underline;">Your Favourites</span>',
    '<span style="font-size:23px;font-weight:700;text-decoration:underline;">Popular Products</span>'
)

# 2. Update subtitle
html = html.replace(
    '    They are your favourites for a reason.',
    '    Our most popular products right now.'
)

# 3. Replace product cell 1: Near Death Drops -> Karamel Cut Throat
old_cell1 = '<td style="padding:8px 6px;text-align:center;" valign="top" width="33%">\n<a href="https://cannibisters.com/products/near-death-drops-full-strength-tincture-oil-10ml-2400mg" style="text-decoration:none;color:#1a1a1a;" target="_blank">\n<img alt="Near Death Drops Full Strength Tinctur\u2026" height="150" src="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/Untitled_design_14.png?v=1750776822" style="display:block;margin:0 auto 10px;width:150px;height:150px;object-fit:cover;border-radius:6px;" width="150"/>\n<p style="margin:0 0 4px;font-family:Helvetica,Arial,sans-serif;font-size:13px;\n              font-weight:700;color:#1a1a1a;line-height:1.3;">Near Death Drops Full Strength Tinctur\u2026</p>\n<p style="margin:0 0 10px;font-family:Helvetica,Arial,sans-serif;font-size:12px;\n              color:#555555;">R 1,650</p>\n</a>\n<a href="https://cannibisters.com/products/near-death-drops-full-strength-tincture-oil-10ml-2400mg" style="display:inline-block;background:#f5a623;color:#1a1a1a;\n            font-family:Helvetica,Arial,sans-serif;font-size:12px;font-weight:700;\n            text-decoration:none;padding:8px 20px;border-radius:5px;" target="_blank">Shop now</a>\n</td>'

new_cell1 = '<td style="padding:8px 6px;text-align:center;" valign="top" width="33%">\n<a href="https://cannibisters.com/products/karamel-cut-throat" style="text-decoration:none;color:#1a1a1a;" target="_blank">\n<img alt="Karamel Cut Throat" height="150" src="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/karamelkutthroat.jpg?v=1769439062" style="display:block;margin:0 auto 10px;width:150px;height:150px;object-fit:cover;border-radius:6px;" width="150"/>\n<p style="margin:0 0 4px;font-family:Helvetica,Arial,sans-serif;font-size:13px;\n              font-weight:700;color:#1a1a1a;line-height:1.3;">Karamel Cut Throat</p>\n<p style="margin:0 0 10px;font-family:Helvetica,Arial,sans-serif;font-size:12px;\n              color:#555555;">R 190</p>\n</a>\n<a href="https://cannibisters.com/products/karamel-cut-throat" style="display:inline-block;background:#f5a623;color:#1a1a1a;\n            font-family:Helvetica,Arial,sans-serif;font-size:12px;font-weight:700;\n            text-decoration:none;padding:8px 20px;border-radius:5px;" target="_blank">Shop now</a>\n</td>'

# 4. Replace product cell 2: Miami Blue Hash -> Manna Gummies THC
old_cell2 = '<td style="padding:8px 6px;text-align:center;" valign="top" width="33%">\n<a href="https://cannibisters.com/products/miami-blue-hash" style="text-decoration:none;color:#1a1a1a;" target="_blank">\n<img alt="Miami Blue Hash" height="150" src="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/HashRosin.png?v=1763716214" style="display:block;margin:0 auto 10px;width:150px;height:150px;object-fit:cover;border-radius:6px;" width="150"/>\n<p style="margin:0 0 4px;font-family:Helvetica,Arial,sans-serif;font-size:13px;\n              font-weight:700;color:#1a1a1a;line-height:1.3;">Miami Blue Hash</p>\n<p style="margin:0 0 10px;font-family:Helvetica,Arial,sans-serif;font-size:12px;\n              color:#555555;">R 450</p>\n</a>\n<a href="https://cannibisters.com/products/miami-blue-hash" style="display:inline-block;background:#f5a623;color:#1a1a1a;\n            font-family:Helvetica,Arial,sans-serif;font-size:12px;font-weight:700;\n            text-decoration:none;padding:8px 20px;border-radius:5px;" target="_blank">Shop now</a>\n</td>'

new_cell2 = '<td style="padding:8px 6px;text-align:center;" valign="top" width="33%">\n<a href="https://cannibisters.com/products/manna-gummies" style="text-decoration:none;color:#1a1a1a;" target="_blank">\n<img alt="Manna Gummies THC" height="150" src="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/IMG_6026_49.jpg?v=1710930039" style="display:block;margin:0 auto 10px;width:150px;height:150px;object-fit:cover;border-radius:6px;" width="150"/>\n<p style="margin:0 0 4px;font-family:Helvetica,Arial,sans-serif;font-size:13px;\n              font-weight:700;color:#1a1a1a;line-height:1.3;">Manna Gummies THC</p>\n<p style="margin:0 0 10px;font-family:Helvetica,Arial,sans-serif;font-size:12px;\n              color:#555555;">R 300</p>\n</a>\n<a href="https://cannibisters.com/products/manna-gummies" style="display:inline-block;background:#f5a623;color:#1a1a1a;\n            font-family:Helvetica,Arial,sans-serif;font-size:12px;font-weight:700;\n            text-decoration:none;padding:8px 20px;border-radius:5px;" target="_blank">Shop now</a>\n</td>'

# 5. Replace product cell 3: Mazar Kush Outdoor Rosin -> Afghan Kush Moonstick
old_cell3 = '<td style="padding:8px 6px;text-align:center;" valign="top" width="33%">\n<a href="https://cannibisters.com/products/mazar-kush-outdoor-rosin" style="text-decoration:none;color:#1a1a1a;" target="_blank">\n<img alt="Mazar Kush Outdoor Rosin" height="150" src="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/Mazar_kush.jpg?v=1760619747" style="display:block;margin:0 auto 10px;width:150px;height:150px;object-fit:cover;border-radius:6px;" width="150"/>\n<p style="margin:0 0 4px;font-family:Helvetica,Arial,sans-serif;font-size:13px;\n              font-weight:700;color:#1a1a1a;line-height:1.3;">Mazar Kush Outdoor Rosin</p>\n<p style="margin:0 0 10px;font-family:Helvetica,Arial,sans-serif;font-size:12px;\n              color:#555555;">R 650</p>\n</a>\n<a href="https://cannibisters.com/products/mazar-kush-outdoor-rosin" style="display:inline-block;background:#f5a623;color:#1a1a1a;\n            font-family:Helvetica,Arial,sans-serif;font-size:12px;font-weight:700;\n            text-decoration:none;padding:8px 20px;border-radius:5px;" target="_blank">Shop now</a>\n</td>'

new_cell3 = '<td style="padding:8px 6px;text-align:center;" valign="top" width="33%">\n<a href="https://cannibisters.com/products/afghan-kush-moonstick" style="text-decoration:none;color:#1a1a1a;" target="_blank">\n<img alt="Afghan Kush Moonstick" height="150" src="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/uploaded_image_1767192229900_8e2056dd-50a5-41cd-9c3a-1cbb02f3df07.jpg?v=1770896945" style="display:block;margin:0 auto 10px;width:150px;height:150px;object-fit:cover;border-radius:6px;" width="150"/>\n<p style="margin:0 0 4px;font-family:Helvetica,Arial,sans-serif;font-size:13px;\n              font-weight:700;color:#1a1a1a;line-height:1.3;">Afghan Kush Moonstick</p>\n<p style="margin:0 0 10px;font-family:Helvetica,Arial,sans-serif;font-size:12px;\n              color:#555555;">R 495</p>\n</a>\n<a href="https://cannibisters.com/products/afghan-kush-moonstick" style="display:inline-block;background:#f5a623;color:#1a1a1a;\n            font-family:Helvetica,Arial,sans-serif;font-size:12px;font-weight:700;\n            text-decoration:none;padding:8px 20px;border-radius:5px;" target="_blank">Shop now</a>\n</td>'

# Apply replacements
assert old_cell1 in html, "Could not find cell 1 to replace"
html = html.replace(old_cell1, new_cell1)

assert old_cell2 in html, "Could not find cell 2 to replace"
html = html.replace(old_cell2, new_cell2)

assert old_cell3 in html, "Could not find cell 3 to replace"
html = html.replace(old_cell3, new_cell3)

print("All replacements applied successfully")

# Verify
assert 'Popular Products' in html
assert 'Our most popular products right now.' in html
assert 'karamel-cut-throat' in html
assert 'manna-gummies' in html
assert 'afghan-kush-moonstick' in html
assert 'near-death-drops' not in html
assert 'miami-blue-hash' not in html
assert 'mazar-kush-outdoor-rosin' not in html
print("Verification passed")

# Create new template
create_resp = requests.post('https://a.klaviyo.com/api/templates/', headers=HEADERS, json={
    'data': {
        'type': 'template',
        'attributes': {
            'name': 'Loyalty Kiosk — Popular Products',
            'editor_type': editor_type,
            'html': html
        }
    }
})
print(f"Create template status: {create_resp.status_code}")
if create_resp.status_code not in (200, 201):
    print(create_resp.text)
    raise Exception("Failed to create template")

new_template_id = create_resp.json()['data']['id']
print(f"New template ID: {new_template_id}")

# Assign to campaign message
assign_resp = requests.post('https://a.klaviyo.com/api/campaign-message-assign-template/', headers=HEADERS, json={
    'data': {
        'type': 'campaign-message',
        'id': MSG_ID,
        'relationships': {
            'template': {
                'data': {
                    'type': 'template',
                    'id': new_template_id
                }
            }
        }
    }
})
print(f"Assign template status: {assign_resp.status_code}")
if assign_resp.status_code not in (200, 201, 204):
    print(assign_resp.text)
    raise Exception("Failed to assign template")

print(f"Done! Template '{new_template_id}' assigned to campaign message {MSG_ID}")
