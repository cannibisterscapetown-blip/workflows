#!/usr/bin/env python3
"""
Builds the AfrikaBurn 2026 in-store special email in BF 2025 style,
then creates a new Klaviyo template and campaign.
"""
import subprocess, json, time

KLAVIYO_KEY = "pk_2b57d9dd3402b67a041cb42568247ac52b"
SHOP        = "cannibisters.com"
LIST_ID     = "Wk5g7N"

HEADERS = [
    "-H", f"Authorization: Klaviyo-API-Key {KLAVIYO_KEY}",
    "-H", "revision: 2024-10-15",
    "-H", "Content-Type: application/json",
]

BANNER_URL = "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/In_Store_Only_1.png?v=1777032189"


# ── Klaviyo API helpers ───────────────────────────────────────────────────────

def _kv_call(method, path, payload=None, retries=5):
    url = f"https://a.klaviyo.com{path}"
    cmd = ["curl", "-s", "-w", "\n__HTTP_STATUS__%{http_code}", "-X", method, url] + HEADERS
    if payload:
        cmd += ["-d", json.dumps(payload)]
    for attempt in range(retries):
        r = subprocess.run(cmd, capture_output=True, text=True)
        raw = r.stdout
        status_code = None
        if "__HTTP_STATUS__" in raw:
            body, status_str = raw.rsplit("__HTTP_STATUS__", 1)
            try:
                status_code = int(status_str.strip())
            except ValueError:
                body = raw
        else:
            body = raw
        body = body.strip()
        if status_code and 200 <= status_code < 300:
            if not body:
                return {}
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                return {}
        wait = 2 ** attempt
        print(f"    DNS retry {attempt+1}/{retries}, waiting {wait}s...")
        time.sleep(wait)
    raise RuntimeError(f"All {retries} attempts failed for {method} {path}")

def _kv_call_file(method, path, payload_file, retries=5):
    url = f"https://a.klaviyo.com{path}"
    cmd = ["curl", "-s", "-w", "\n__HTTP_STATUS__%{http_code}", "-X", method, url] + HEADERS + ["--data-binary", f"@{payload_file}"]
    for attempt in range(retries):
        r = subprocess.run(cmd, capture_output=True, text=True)
        raw = r.stdout
        status_code = None
        if "__HTTP_STATUS__" in raw:
            body, status_str = raw.rsplit("__HTTP_STATUS__", 1)
            try:
                status_code = int(status_str.strip())
            except ValueError:
                body = raw
        else:
            body = raw
        body = body.strip()
        if status_code and 200 <= status_code < 300:
            if not body:
                return {}
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                return {}
        wait = 2 ** attempt
        print(f"    DNS retry {attempt+1}/{retries}, waiting {wait}s...")
        time.sleep(wait)
    raise RuntimeError(f"All {retries} attempts failed for {method} {path}")

def kv_get(path):           return _kv_call("GET", path)
def kv_post(path, payload): return _kv_call("POST", path, payload)
def kv_patch(path, payload): return _kv_call("PATCH", path, payload)


# ── Product data (confirmed from Shopify API) ─────────────────────────────────

NEW_ARRIVALS = [
    dict(title="Greendoor Green Candy",    price="R 135,00", handle="greendoor-green-candy",    img="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/IMG_4413.jpg?v=1777018585"),
    dict(title="Greendoor Gelato Frosting",price="R 135,00", handle="greendoor-gelato-frosting", img="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/IMG_4390.jpg?v=1777018121"),
    dict(title="Ghost Train Haze Joint",   price="R 175,00", handle="ghost-train-haze-joint",   img="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/cannibisters_joint_tube_11b22e82-b216-4e15-8333-1a8ffd31c4a5.jpg?v=1776676871"),
]

JOINTS = [
    dict(title="Joint Special — 3x Indoor Joints", price="R 450,00", handle="bundle-3-joints-assorted", img="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/uploaded_image_1767192210692_39b93834-c472-4ff8-b50f-53f7a0a0c351.jpg?v=1767192280"),
    dict(title="Super Joint — Sativa",             price="R 250,00", handle="moonstick-sativa",         img="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/uploaded_image_1767191356385_51b2a83d-4422-45e0-a574-1982f282452f.jpg?v=1767192352"),
    dict(title="Living Soil Joints — 3x Bundle",   price="R 350,00", handle="living-soil-joints",       img="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/uploaded_image_1767192210692_fe5c7357-627e-45b1-bb4e-1fa14c79cc2f.jpg?v=1767192273"),
]

VAPES = [
    dict(title="Vape Cartridge — Durban Poison", price="R 900,00", handle="vape-cartridge-durban-poison", img="https://cdn.shopify.com/s/files/1/0631/7749/0644/products/VapeCartUser_8b5b1728-449e-4cab-95de-2da443531230.png?v=1669893473"),
    dict(title="Vape Cartridge — Skywalker",     price="R 900,00", handle="skywalker",                   img="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/MG_9764.jpg?v=1742304425"),
    dict(title="Vape Cartridge — AK 47",         price="R 900,00", handle="vape-cartridge-ak-48",        img="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/MG_9769.jpg?v=1742305114"),
]

EDIBLES = [
    dict(title="Gummy Bears — THC",             price="R 180,00", handle="gummie-bears-thc",              img="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/Untitled_2_5.jpg?v=1751011092"),
    dict(title="Small THC Chocolate",           price="R 180,00", handle="small-thc-chocolate",           img="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/Untitled_2_4.jpg?v=1751011147"),
    dict(title="Manna Chocolate Brownies",      price="R 180,00", handle="manna-chocolate-brownies-strong",img="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/IMG_8074.jpg?v=1698409802"),
]


# ── HTML builders (exact BF 2025 kl-section structure) ───────────────────────

def section_wrap(inner_content, bg="#FFFFFF", is_first=False, is_last=False):
    pad_class = "kl-first" if is_first else ("kl-last" if is_last else "")
    return f"""
<table align="center" border="0" cellpadding="0" cellspacing="0" class="kl-section" role="presentation" style="width:100%;">
<tbody><tr><td>
<!--[if mso | IE]><table align="center" border="0" cellpadding="0" cellspacing="0" class="kl-section-outlook" style="width:600px;" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
<div style="margin:0px auto;max-width:600px;">
<table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
<tbody><tr>
<td style="direction:ltr;font-size:0px;padding:0px;text-align:center;">
<!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" bgcolor="{bg}" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
<div style="background:{bg};background-color:{bg};margin:0px auto;border-radius:0px;max-width:600px;">
<table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:{bg};background-color:{bg};width:100%;">
<tbody><tr>
<td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:0px;padding-left:0px;padding-right:0px;padding-top:0px;text-align:center;">
<!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><![endif]-->
<div class="content-padding {pad_class}">
<!--[if true]><table border="0" cellpadding="0" cellspacing="0" width="600" style="width:600px;direction:ltr"><tr><![endif]-->
<div class="kl-row colstack" style="display:table;table-layout:fixed;width:100%;">
<!--[if true]><td style="vertical-align:top;width:600px;"><![endif]-->
<div class="kl-column" style="display:table-cell;vertical-align:top;width:100%;">
{inner_content}
</div>
<!--[if true]></td><![endif]-->
</div>
<!--[if true]></tr></table><![endif]-->
</div>
<!--[if mso | IE]></table><![endif]-->
</td></tr></tbody></table></div>
<!--[if mso | IE]></td></tr></table></table><![endif]-->
</td></tr></tbody></table></div>
<!--[if mso | IE]></td></tr></table><![endif]-->
</td></tr></tbody></table>"""


def text_block(html_content, padding="9px 18px"):
    parts = padding.split()
    if len(parts) == 2:
        pt, pr, pb, pl = parts[0], parts[1], parts[0], parts[1]
    elif len(parts) == 4:
        pt, pr, pb, pl = parts
    else:
        pt = pr = pb = pl = "9px"
    return f"""
<div class="mj-column-per-100 mj-outlook-group-fix component-wrapper" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%"><tbody><tr>
<td class="" style="vertical-align:top;padding-top:{pt};padding-right:{pr};padding-bottom:{pb};padding-left:{pl};">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%"><tbody><tr>
<td align="left" class="kl-text" style="font-size:0px;padding:0px;word-break:break-word;">
<div style="font-family:Helvetica, Arial, sans-serif;font-size:16px;font-style:normal;font-weight:400;letter-spacing:0px;line-height:1.3;text-align:left;color:#060606;">
{html_content}
</div>
</td></tr></tbody></table>
</td></tr></tbody></table></div>"""


def image_block(src, alt="", width=600):
    return f"""
<div class="mj-column-per-100 mj-outlook-group-fix component-wrapper" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%"><tbody><tr>
<td class="" style="vertical-align:top;padding-top:0px;padding-right:0px;padding-bottom:0px;padding-left:0px;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%"><tbody><tr>
<td align="center" class="kl-image" style="font-size:0px;word-break:break-word;">
<table border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse;border-spacing:0px;"><tbody><tr>
<td class="kl-img-base-auto-width" style="border:0;padding:0px;width:{width}px;" valign="top">
<img src="{src}" alt="{alt}" style="display:block;outline:none;text-decoration:none;height:auto;font-size:13px;width:100%;" width="{width}"/>
</td></tr></tbody></table>
</td></tr></tbody></table>
</td></tr></tbody></table></div>"""


def spacer(height=20):
    return f"""
<div class="mj-column-per-100 mj-outlook-group-fix component-wrapper" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%"><tbody><tr>
<td class="" style="vertical-align:top;padding:0;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%"><tbody><tr>
<td style="font-size:0px;word-break:break-word;">
<div style="height:{height}px;line-height:{height}px;"> </div>
</td></tr></tbody></table>
</td></tr></tbody></table></div>"""


def divider():
    return """
<div class="mj-column-per-100 mj-outlook-group-fix component-wrapper" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%"><tbody><tr>
<td class="" style="vertical-align:top;padding-top:9px;padding-right:18px;padding-bottom:9px;padding-left:18px;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%"><tbody><tr>
<td style="border-top:1px solid #EEEEEE;font-size:1px;margin:0px auto;word-break:break-word;"> </td>
</tr></tbody></table>
</td></tr></tbody></table></div>"""


def section_title(title):
    return f"""
<div class="mj-column-per-100 mj-outlook-group-fix component-wrapper kl-text-table-layout" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%"><tbody><tr>
<td class="" style="vertical-align:top;padding:0;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%"><tbody><tr>
<td align="center" class="kl-text" style="font-size:0px;padding:0;padding-top:18px;padding-right:18px;padding-bottom:9px;padding-left:18px;word-break:break-word;">
<div style="font-family:Helvetica,Arial,sans-serif;font-size:24px;font-style:normal;font-weight:700;letter-spacing:0px;line-height:1.3;text-align:center;color:#060606;">
{title}
</div>
</td></tr></tbody></table>
</td></tr></tbody></table></div>"""


def product_card(p):
    url = f"https://{SHOP}/products/{p['handle']}"
    return f"""
<!--[if true]><td width="33.333333333333336%" style="vertical-align:top;"><![endif]-->
<!--[if !true]><!--><div class="kl-product-cell-stack" style="display:table-cell;vertical-align:top;font-size:0;width:33.333333333333336%;"><!--<![endif]-->
<table cellpadding="0" cellspacing="0" height="100%" role="presentation" style="" width="100%"><tbody><tr>
<td style="font-size:0px;padding:10px;word-break:break-word;vertical-align:top;">
<table align="left" border="0" cellpadding="0" cellspacing="0" class="kl-product-subblock" style="table-layout:fixed;height:100%;" width="100%"><tbody>
<tr><td align="center">
<a href="{url}" style="color:#ff9501;text-decoration:underline">
<img alt="Image of {p['title']}" src="{p['img']}" style="display:block;max-width:100%;width:auto;max-height:125px;" width="176"/>
</a>
</td></tr>
<tr><td align="center" style="padding-top:9px;">
<table align="center" border="0" cellpadding="0" cellspacing="0"><tbody><tr>
<td align="center" style="color:#060606;font-family:Helvetica,Arial,sans-serif;font-size:16px;font-weight:700;letter-spacing:0px;line-height:1.3;text-align:center;">
{p['title']}
</td></tr></tbody></table>
</td></tr>
<tr><td align="center" style="padding-top:4px;">
<table align="center" border="0" cellpadding="0" cellspacing="0"><tbody><tr>
<td align="center" style="color:#060606;font-family:Helvetica,Arial,sans-serif;font-size:16px;font-weight:400;letter-spacing:0px;line-height:1.3;text-align:center;">
{p['price']}
</td></tr></tbody></table>
</td></tr>
<tr><td style="height:100%;"></td></tr>
<tr><td align="center" style="padding-top:9px;">
<table border="0" cellpadding="0" cellspacing="0" style="border-collapse:separate;line-height:100%;"><tbody><tr>
<td align="center" bgcolor="#ff9501" role="presentation" style="border:none;border-radius:8px;cursor:auto;font-style:normal;padding:0;background:#ff9501;" valign="middle">
<a href="{url}" style="display:inline-block;background:#ff9501;color:#000000;font-family:Helvetica,Arial,sans-serif;font-size:16px;font-weight:700;line-height:120%;letter-spacing:0px;margin:0;text-decoration:none;text-transform:none;padding:16px 40px;border-radius:8px;" target="_blank">Shop now</a>
</td></tr></tbody></table>
</td></tr>
</tbody></table>
</td></tr></tbody></table>
<!--[if true]></td><![endif]-->
<!--[if !true]><!--></div><!--<![endif]-->"""


def product_grid(products):
    cards = "\n".join(product_card(p) for p in products)
    return f"""
<div class="mj-column-per-100 mj-outlook-group-fix component-wrapper" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%"><tbody><tr>
<td class="" style="vertical-align:top;padding:0;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%"><tbody><tr>
<td class="kl-product" style="font-size:0px;padding:0px;word-break:break-word;">
<div style="margin:0px auto;max-width:600px;">
<table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;"><tbody><tr>
<!--[if true]><table border="0" cellpadding="0" cellspacing="0" width="600" style="width:600px;direction:ltr"><tr><![endif]-->
{cards}
<!--[if true]></tr></table><![endif]-->
</tr></tbody></table></div>
</td></tr></tbody></table>
</td></tr></tbody></table></div>"""


def footer_section():
    return section_wrap(f"""
<div class="mj-column-per-100 mj-outlook-group-fix component-wrapper" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%"><tbody><tr>
<td class="" style="background-color:#000000;vertical-align:top;padding-top:9px;padding-right:9px;padding-bottom:9px;padding-left:9px;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%"><tbody><tr>
<td>
<div style="width:100%;text-align:center">
<!--[if true]><table border="0" cellpadding="0" cellspacing="0"><tr><![endif]-->
<!--[if !true]><!--><div class="" style="display:inline-block;padding-right:10px;"><!--<![endif]-->
<!--[if true]><td style="padding-right:10px;"><![endif]-->
<div style="text-align:center;"><a href="https://www.instagram.com/cannibisterscapetown" style="color:#ff9501;text-decoration:underline" target="_blank"><img alt="instagram" src="https://d3k81ch9hvuctc.cloudfront.net/assets/email/buttons/subtleinverse/instagram_96.png" style="width:32px;" width="32"/></a></div>
<!--[if true]></td><![endif]-->
<!--[if !true]><!--></div><!--<![endif]-->
<!--[if !true]><!--><div class="" style="display:inline-block;padding-right:10px;"><!--<![endif]-->
<!--[if true]><td style="padding-right:10px;"><![endif]-->
<div style="text-align:center;"><a href="https://www.youtube.com/channel/UCITZsSh7GgWeCQWejTUG4Jw" style="color:#ff9501;text-decoration:underline" target="_blank"><img alt="YouTube" src="https://d3k81ch9hvuctc.cloudfront.net/assets/email/buttons/subtleinverse/youtube_96.png" style="width:32px;" width="32"/></a></div>
<!--[if true]></td><![endif]-->
<!--[if !true]><!--></div><!--<![endif]-->
<!--[if true]></tr></table><![endif]-->
</div>
</td></tr></tbody></table>
</td></tr></tbody></table></div>
<div class="mj-column-per-100 mj-outlook-group-fix component-wrapper kl-text-table-layout" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%"><tbody><tr>
<td class="" style="background-color:#000000;vertical-align:top;padding:0;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%"><tbody><tr>
<td align="center" class="kl-text" style="font-size:0px;padding:0;padding-top:9px;padding-right:18px;padding-bottom:9px;padding-left:18px;word-break:break-word;">
<div style="font-family:Helvetica,Arial,sans-serif;font-size:12px;font-style:normal;font-weight:400;letter-spacing:0px;line-height:1.3;text-align:center;color:#FFFFFF;">
<div>
<span style="font-size:12px;color:rgb(255,255,255);background-color:rgb(0,0,0);">Cannibisters - The Herbal Apothecary</span><br/>
<span style="font-size:12px;color:rgb(255,255,255);background-color:rgb(0,0,0);">65 Regent Rd, Sea Point, Cape Town, Western Cape, 8001, South Africa</span><br/>
<a href="http://manage.kmail-lists.com/subscriptions/placeholder" rel="noopener" style="color:rgb(255,255,255);text-decoration:underline;font-size:12px;background-color:rgb(0,0,0);" target="_blank"><span style="color:rgb(246,246,246);">087 537 8000</span>&nbsp;&nbsp;<span style="color:rgb(249,248,247);">high@cannibisters.com</span></a><br/>
<span style="font-size:12px;color:rgb(255,149,1);background-color:rgb(0,0,0);"><a class="unsubscribe-link" href="http://manage.kmail-lists.com/subscriptions/placeholder" rel="noopener" style="color:rgb(255,149,1);text-decoration:underline" target="_blank">Unsubscribe</a></span><br/>
<span style="font-size:12px;color:rgb(255,255,255);background-color:rgb(0,0,0);">&#169; 2026 Cannibisters - The Herbal Apothecary</span>
</div>
</div>
</td></tr></tbody></table>
</td></tr></tbody></table></div>
""", bg="#000000", is_last=True)


# ── Full email builder ────────────────────────────────────────────────────────

def build_html():
    with open("/tmp/bf_head.html") as f:
        head = f.read()

    intro = text_block("""
<div>
<span style="font-size:18px;">Hi {{ person.first_name|default:'there' }}, the Tankwa calls. &#128293;</span><br/><br/>
<span style="font-size:18px;">
AfrikaBurn is almost here — and we want to help you pack right and burn bright.
<br/><br/>
Come visit us <strong>in-store at the Apothecary</strong>, show us your <strong>AfrikaBurn ticket</strong> (or a copy thereof) and unlock <strong>exclusive in-store Burner pricing</strong> across our full range.
<br/><br/>
Whether you're loading up on pre-rolls for the journey, grabbing vapes for the dust, fuelling up on edibles for the long nights under the stars, or picking up something from our latest drops — we've got you sorted before you hit the playa.
<br/><br/>
&#128204; <strong>In-store only &nbsp;&#183;&nbsp; 65 Regent Rd, Sea Point &nbsp;&#183;&nbsp; Valid while stock lasts.</strong>
</span>
</div>""")

    section1 = section_wrap(
        image_block(BANNER_URL, "AfrikaBurn 2026 — In-Store Special") +
        image_block("https://d3k81ch9hvuctc.cloudfront.net/assets/email/bottom_shadow_222.png", "Shadow") +
        intro +
        divider(),
        is_first=True,
    )

    section2 = section_wrap(
        section_title("New Arrivals") +
        text_block('<div style="text-align:center;">Fresh drops just landed at the Apothecary.</div>') +
        product_grid(NEW_ARRIVALS) +
        divider(),
    )

    section3 = section_wrap(
        section_title("Pre-Rolled Joints") +
        text_block('<div style="text-align:center;">Ready to burn. No prep required.</div>') +
        product_grid(JOINTS) +
        divider(),
    )

    section4 = section_wrap(
        section_title("Vapes") +
        text_block('<div style="text-align:center;">Discreet, portable, playa-ready.</div>') +
        product_grid(VAPES) +
        divider(),
    )

    section5 = section_wrap(
        section_title("Edibles") +
        text_block('<div style="text-align:center;">For the long nights and slow mornings.</div>') +
        product_grid(EDIBLES) +
        spacer(20),
    )

    body = f"""<body style="word-spacing:normal;background-color:#FFFFFF;">
<!-- TRACKING_PIXEL_TOP -->
<div class="root-container" id="bodyTable" style="background-color:#FFFFFF;">
<div class="root-container-spacing">
{section1}
{section2}
{section3}
{section4}
{section5}
{footer_section()}
</div></div>
<!-- TRACKING_PIXEL_BOTTOM -->
</body>
</html>"""

    return head + body


# ── Klaviyo wiring ────────────────────────────────────────────────────────────

def create_template(html):
    return kv_post("/api/templates/", {
        "data": {
            "type": "template",
            "attributes": {
                "name": "AfrikaBurn 2026 — In-Store Special",
                "editor_type": "CODE",
                "html": html,
                "text": (
                    "THE TANKWA CALLS\n\n"
                    "AfrikaBurn is almost here. Come in-store at Cannibisters, show your AfrikaBurn ticket "
                    "and unlock exclusive Burner pricing across our full range.\n\n"
                    "In-store only. 65 Regent Rd, Sea Point. Valid while stock lasts.\n\n"
                    "— The Cannibisters Team"
                ),
            }
        }
    })


def create_campaign(template_id):
    resp = kv_post("/api/campaigns/", {
        "data": {
            "type": "campaign",
            "attributes": {
                "name": "AfrikaBurn 2026 — In-Store Special",
                "audiences": {
                    "included": [LIST_ID],
                    "excluded": [],
                },
                "send_strategy": {
                    "method": "static",
                    "options_static": {
                        "datetime": "2026-04-25T07:00:00+00:00",
                        "is_local": True,
                        "send_past_recipients_immediately": True,
                    }
                },
                "campaign-messages": {
                    "data": [{
                        "type": "campaign-message",
                        "attributes": {
                            "label": "AfrikaBurn 2026 — In-Store Special",
                            "channel": "email",
                            "content": {
                                "subject": "&#128293; Heading to AfrikaBurn? We've got something for you.",
                                "preview_text": "Show your ticket in-store for exclusive Burner pricing. In-store only.",
                                "from_email": "high@cannibisters.com",
                                "from_label": "Cannibisters",
                                "reply_to_email": "high@cannibisters.com",
                            }
                        }
                    }]
                }
            }
        }
    })
    return resp


def assign_template(msg_id, template_id):
    return _kv_call("POST", "/api/campaign-message-assign-template/", {
        "data": {
            "type": "campaign-message",
            "id": msg_id,
            "relationships": {"template": {"data": {"type": "template", "id": template_id}}}
        }
    })


def main():
    print("=" * 60)
    print("AfrikaBurn 2026 — Email Campaign Builder")
    print("=" * 60)

    # 1. Build HTML
    print("\n[1] Building email HTML...")
    html = build_html()
    print(f"    HTML: {len(html):,} characters")
    with open("/home/user/workflows/afrikaburn_email.html", "w") as f:
        f.write(html)
    print("    Saved: afrikaburn_email.html")

    # 2. Create template (write payload to file to handle large HTML)
    print("\n[2] Creating Klaviyo template...")
    payload = {
        "data": {
            "type": "template",
            "attributes": {
                "name": "AfrikaBurn 2026 — In-Store Special",
                "editor_type": "CODE",
                "html": html,
                "text": (
                    "THE TANKWA CALLS\n\n"
                    "AfrikaBurn is almost here. Come in-store at Cannibisters, show your AfrikaBurn ticket "
                    "and unlock exclusive Burner pricing across our full range.\n\n"
                    "In-store only. 65 Regent Rd, Sea Point. Valid while stock lasts.\n\n"
                    "— The Cannibisters Team"
                ),
            }
        }
    }
    with open("/tmp/ab_template_payload.json", "w") as f:
        json.dump(payload, f)
    tmpl_resp = _kv_call_file("POST", "/api/templates/", "/tmp/ab_template_payload.json")
    if "errors" in tmpl_resp:
        print(f"    Error: {tmpl_resp['errors']}")
        return
    template_id = tmpl_resp["data"]["id"]
    print(f"    Template ID: {template_id}")

    # 3. Create campaign
    print("\n[3] Creating campaign...")
    camp_resp = create_campaign(template_id)
    if "errors" in camp_resp:
        print(f"    Error: {camp_resp['errors']}")
        return
    campaign_id = camp_resp["data"]["id"]
    # Extract the auto-created message ID
    msg_id = camp_resp["data"]["relationships"]["campaign-messages"]["data"][0]["id"]
    print(f"    Campaign ID: {campaign_id}")
    print(f"    Message ID:  {msg_id}")

    # 4. Assign template to campaign message
    print(f"\n[4] Assigning template {template_id} to message {msg_id}...")
    assign_resp = assign_template(msg_id, template_id)
    if "errors" in assign_resp:
        print(f"    Error: {assign_resp['errors']}")
    else:
        print("    Template assigned.")

    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)
    print(f"  Campaign:   {campaign_id}")
    print(f"  Message:    {msg_id}")
    print(f"  Template:   {template_id}")
    print(f"  Scheduled:  25 Apr 2026 @ 09:00 SAST")
    print(f"  Review:     https://www.klaviyo.com/campaigns/{campaign_id}")
    print("=" * 60)


if __name__ == "__main__":
    main()
