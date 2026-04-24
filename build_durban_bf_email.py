#!/usr/bin/env python3
"""
Builds the Durban Poison back-in-stock email in exact BF 2025 style
then creates/updates the Klaviyo template and campaign.
"""
import subprocess, json, textwrap

KLAVIYO_KEY = "pk_2b57d9dd3402b67a041cb42568247ac52b"
SHOP        = "cannibisters.com"

HEADERS = [
    "-H", f"Authorization: Klaviyo-API-Key {KLAVIYO_KEY}",
    "-H", "revision: 2024-10-15",
    "-H", "Content-Type: application/json",
]

import time

def _kv_call(method, path, payload=None, retries=5, allow_empty=False):
    url = f"https://a.klaviyo.com{path}"
    cmd = ["curl","-s","-w","\n__HTTP_STATUS__%{http_code}","-X",method,url] + HEADERS
    if payload:
        cmd += ["-d", json.dumps(payload)]
    for attempt in range(retries):
        r = subprocess.run(cmd, capture_output=True, text=True)
        raw = r.stdout
        # Extract status code appended by -w flag
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
        # 2xx with no body = success (e.g. 200/204 on assign-template)
        if status_code and 200 <= status_code < 300:
            if not body:
                return {}
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                return {}
        if body:
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                pass
        wait = 2 ** attempt
        print(f"    DNS retry {attempt+1}/{retries}, waiting {wait}s...")
        time.sleep(wait)
    raise RuntimeError(f"All {retries} attempts failed for {method} {path}")

def kv_get(path):   return _kv_call("GET", path)
def kv_post(path, payload): return _kv_call("POST", path, payload)
def kv_patch(path, payload): return _kv_call("PATCH", path, payload)

# ── Product data ──────────────────────────────────────────────────────────────
DURBAN = dict(
    title="Premium Durban Poison",
    price="R 240,00",
    handle="durban-poison-living-soil",
    img="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/Durban_poison_budshot_1.png?v=1776669088",
)

NEW_ARRIVALS = [
    # Source: Shopify "New Strains" smart collection (active products)
    dict(title="Red Velvet Gary", price="R 200,00", handle="red-velvet",        img="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/IMG_4349.jpg?v=1777018728"),
    dict(title="Colt 45",         price="R 200,00", handle="colt-45",           img="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/Colt_45.png?v=1772799342"),
    dict(title="LA Rosa",         price="R 200,00", handle="la-rosa",           img="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/LaRosa.png?v=1770639107"),
]

FAN_FAVS = [
    # Source: Shopify "Premium Bud" custom collection (active products)
    dict(title="Elvis",                price="R 200,00", handle="elvis-90-10-sativa", img="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/elvis.jpg?v=1740402820"),
    dict(title="Premium Lion's Bread", price="R 240,00", handle="lions-bread",        img="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/Lions_bread_183fdfd4-f2f0-4582-94bb-72b688e47d89.jpg?v=1752828397"),
    dict(title="Jessica Rabbit",       price="R 200,00", handle="jessica-rabbit",     img="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/Jessica_Rabbit_Cannibister_Discover_with_Leigh_Photography_03.03.26_2_of_5.jpg?v=1772611089"),
]

HASH = [
    dict(title="Afghan Mazar Sharif Hash",      price="R 450,00", handle="afghan-mazar-sharif-hash",    img="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/HashRosin.png?v=1763716214"),
    dict(title="Bubble Hash — Bruce Banner",    price="R 450,00", handle="bubble-hash-bruce-banner",    img="https://cdn.shopify.com/s/files/1/0631/7749/0644/products/BruceBannerHash.png?v=1669130132"),
    dict(title="Light Bringer Hash Rosin",      price="R 1240,00",handle="light-bringer-hash-rosin",   img="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/Light_bringer.jpg?v=1760619918"),
]

MEMBERSHIP = [
    dict(title="30 Day Membership", price="R 100,00",  handle="cannibisters-the-herbal-apothecary-30-day-membership", img="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/30day_membership.png?v=1711745615"),
    dict(title="3 Month Membership",price="R 300,00",  handle="cannibisters-the-herbal-apothecary-3-month-membership",img="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/3month_membership.png?v=1711745656"),
    dict(title="12 Month Membership",price="R 1000,00",handle="cannibisters-the-herbal-apothecary-12-month-membership",img="https://cdn.shopify.com/s/files/1/0631/7749/0644/files/12month_membership.png?v=1711745687"),
]


# ── HTML builders (exact BF 2025 structure) ───────────────────────────────────

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
    pt, pr, pb, pl = "9px","18px","9px","18px"
    if padding:
        parts = padding.split()
        if len(parts)==2: pt,pr,pb,pl = parts[0],parts[1],parts[0],parts[1]
        elif len(parts)==4: pt,pr,pb,pl = parts
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
<td class="" style="vertical-align:top;padding-top:18px;padding-right:18px;padding-bottom:18px;padding-left:18px;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%"><tbody><tr>
<td align="center" style="font-size:0px;padding:0px;word-break:break-word;">
<p style="padding-bottom:0;border-top:solid 1px #CCC;font-size:1px;margin:0 auto;width:100%"></p>
<!--[if mso | IE]><table align="center" border="0" cellpadding="0" cellspacing="0" style="border-top:solid 1px #CCCCCC;font-size:1px;margin:0px auto;width:564px;" role="presentation" width="564px"><tr><td style="height:0;line-height:0;">&nbsp;</td></tr></table><![endif]-->
</td></tr></tbody></table>
</td></tr></tbody></table></div>"""


def section_title(title):
    return text_block(f'<div style="text-align:center;"><span style="text-decoration:underline;font-size:23px;"><strong>{title}</strong></span></div>')


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
<tr><td align="center">
<table align="center"><tr><td align="center" style="color:#060606;font-family:Helvetica,Arial,sans-serif;font-size:16px;font-weight:700;font-style:normal;text-align:center;letter-spacing:0px;padding-top:5px;padding-bottom:0px;line-height:1.3;">{p['title']}</td></tr></table>
</td></tr>
<tr><td align="center">
<table align="center"><tr><td align="center" style="color:#060606;font-family:Helvetica,Arial,sans-serif;font-size:16px;font-weight:400;font-style:normal;text-align:center;letter-spacing:0px;padding-top:5px;padding-bottom:0px;padding-left:1.5px;padding-right:1.5px;line-height:1.3;display:inline-block;">{p['price']}</td></tr></table>
</td></tr>
<tr><td style="height:100%;"></td></tr>
<tr><td align="center" style="padding-top:9px;">
<table border="0" cellpadding="0" cellspacing="0" style="border-collapse:separate;line-height:100%;"><tr>
<td align="center" bgcolor="#ff9501" role="presentation" style="border:none;border-radius:8px;cursor:auto;font-style:normal;mso-padding-alt:16px 40px 16px 40px;text-align:center;background:#ff9501;" valign="middle">
<a href="{url}" style="color:#000;text-decoration:none;display:inline-block;background:#ff9501;font-family:Helvetica,Arial;font-size:16px;font-style:normal;font-weight:700;line-height:1.3;letter-spacing:0;margin:0;text-transform:none;padding:16px 40px 16px 40px;mso-padding-alt:0;border-radius:8px" target="_blank">Shop now</a>
</td></tr></table>
</td></tr>
</tbody></table>
</td></tr></tbody></table>
<!--[if !true]><!--></div><!--<![endif]-->
<!--[if true]></td><![endif]-->"""


def product_grid(products):
    cards = "".join(product_card(p) for p in products)
    return f"""
<div class="mj-column-per-100 mj-outlook-group-fix component-wrapper" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%"><tbody><tr>
<td class="" style="vertical-align:top;padding-top:9px;padding-right:18px;padding-bottom:9px;padding-left:18px;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%"><tbody><tr>
<td align="left" style="font-size:0px;padding:0px;word-break:break-word;">
<div style="font-family:Ubuntu,Helvetica,Arial,sans-serif;font-size:13px;line-height:1;text-align:left;color:#000000;">
<!--[if true]><table class="kl-product" role="presentation" width="100%" style="all:unset;opacity:0;"><tr><![endif]-->
<!--[if false]></td></tr></table><![endif]-->
<div class="kl-product" style="display:table;width:100%;height:100%">
{cards}
</div>
<!--[if true]></tr></table><![endif]-->
</div>
</td></tr></tbody></table>
</td></tr></tbody></table></div>"""


def featured_product(p):
    """Single centred product with larger image — used for the hero Durban Poison card."""
    url = f"https://{SHOP}/products/{p['handle']}"
    return f"""
<div class="mj-column-per-100 mj-outlook-group-fix component-wrapper" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%"><tbody><tr>
<td class="" style="vertical-align:top;padding-top:9px;padding-right:18px;padding-bottom:9px;padding-left:18px;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%"><tbody><tr>
<td align="center" style="font-size:0px;padding:0px;word-break:break-word;">
<table align="center" border="0" cellpadding="0" cellspacing="0" style="width:280px;" width="280"><tbody>
<tr><td align="center">
<a href="{url}" style="color:#ff9501;text-decoration:underline">
<img alt="Image of {p['title']}" src="{p['img']}" style="display:block;max-width:100%;width:auto;max-height:260px;" width="260"/>
</a>
</td></tr>
<tr><td align="center">
<table align="center"><tr><td align="center" style="color:#060606;font-family:Helvetica,Arial,sans-serif;font-size:18px;font-weight:700;font-style:normal;text-align:center;letter-spacing:0px;padding-top:8px;padding-bottom:0px;line-height:1.3;">{p['title']}</td></tr></table>
</td></tr>
<tr><td align="center">
<table align="center"><tr><td align="center" style="color:#060606;font-family:Helvetica,Arial,sans-serif;font-size:16px;font-weight:400;font-style:normal;text-align:center;letter-spacing:0px;padding-top:5px;padding-bottom:0px;line-height:1.3;">{p['price']}</td></tr></table>
</td></tr>
<tr><td align="center" style="padding-top:12px;">
<table border="0" cellpadding="0" cellspacing="0" style="border-collapse:separate;line-height:100%;"><tr>
<td align="center" bgcolor="#ff9501" role="presentation" style="border:none;border-radius:8px;cursor:auto;mso-padding-alt:16px 40px;text-align:center;background:#ff9501;" valign="middle">
<a href="{url}" style="color:#000;text-decoration:none;display:inline-block;background:#ff9501;font-family:Helvetica,Arial;font-size:16px;font-style:normal;font-weight:700;line-height:1.3;letter-spacing:0;margin:0;padding:16px 40px;mso-padding-alt:0;border-radius:8px" target="_blank">Shop Durban Poison</a>
</td></tr></table>
</td></tr>
</tbody></table>
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
<a href="http://manage.kmail-lists.com/subscriptions/placeholder" rel="noopener" style="color:rgb(255,255,255);text-decoration:underline;font-size:12px;background-color:rgb(0,0,0);" target="_blank"><span style="color:rgb(246,246,246);">Our store number: 087 537 8000</span><br/><span style="color:rgb(249,248,247);">high@cannibisters.com</span></a><br/>
<span style="font-size:12px;color:rgb(255,149,1);background-color:rgb(0,0,0);"><a class="unsubscribe-link" href="http://manage.kmail-lists.com/subscriptions/placeholder" rel="noopener" style="color:rgb(255,149,1);text-decoration:underline" target="_blank">Unsubscribe</a></span><br/>
<span style="font-size:12px;color:rgb(255,255,255);background-color:rgb(0,0,0);">&#169; 2026 Cannibisters - The Herbal Apothecary</span>
</div>
</div>
</td></tr></tbody></table>
</td></tr></tbody></table></div>
""", bg="#000000", is_last=True)


# ── Build the full email HTML ─────────────────────────────────────────────────

def build_html():
    with open("/tmp/bf_head.html") as f:
        head = f.read()

    BANNER_URL = "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/Durban_Poison_email_banner.png?v=1777027798"

    # ── Section 1: Hero banner + shadow + intro copy + featured Durban Poison ──
    intro_text = text_block("""
<div>
<span style="font-size:18px;">Hi {{ person.first_name|default:'there' }}, she&#39;s back. &#127807;</span><br/><br/>
<span style="font-size:18px;">
<strong>Durban Poison</strong> &#8212; one of the oldest surviving cannabis landraces on earth, and a strain that belongs to us.
Grown in the hills outside Durban long before the modern seed industry existed, it is shaped by centuries of South African sun, soil and culture.
<br/><br/>
In a world where virtually every strain has been crossed, blended and hybridised, Durban Poison stands apart as one of the only <em>100% pure sativas</em> left on earth &#8212; never diluted, never compromised, <em>proudly South African and utterly irreplaceable.</em>
Expect a sharp anise-sweet aroma, soaring cerebral energy and a creative clarity you simply cannot manufacture.
<br/><br/>
<strong>Limited stock. No compromises. Taste the history.</strong> &#9203;
</span>
</div>""")

    section1 = section_wrap(
        image_block(BANNER_URL, "Durban Poison — Back In Stock") +
        image_block("https://d3k81ch9hvuctc.cloudfront.net/assets/email/bottom_shadow_222.png", "Shadow") +
        intro_text +
        spacer(20) +
        section_title("&#127807; Back In Stock: Durban Poison") +
        featured_product(DURBAN) +
        divider(),
        is_first=True,
    )

    # ── Section 2: New Arrivals ───────────────────────────────────────────────
    section2 = section_wrap(
        section_title("New Arrivals") +
        text_block('<div style="text-align:center;">Fresh strains just landed at the Apothecary.</div>') +
        product_grid(NEW_ARRIVALS) +
        divider(),
    )

    # ── Section 3: Fan Favourites ─────────────────────────────────────────────
    section3 = section_wrap(
        section_title("Fan Favourites") +
        text_block('<div style="text-align:center;">The strains our community keeps coming back for.</div>') +
        product_grid(FAN_FAVS) +
        divider(),
    )

    # ── Section 4: Hash ───────────────────────────────────────────────────────
    section4 = section_wrap(
        section_title("Hash") +
        text_block('<div style="text-align:center;">Concentrated. Crafted. Coveted.</div>') +
        product_grid(HASH) +
        divider(),
    )

    # ── Section 5: Membership ─────────────────────────────────────────────────
    section5 = section_wrap(
        section_title("Membership") +
        text_block('<div style="text-align:center;">Join the Apothecary. Member pricing, exclusive access &amp; more.</div>') +
        product_grid(MEMBERSHIP) +
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

def assign_template_to_message(msg_id, template_id):
    return _kv_call("POST", "/api/campaign-message-assign-template/", {
        "data": {
            "type": "campaign-message",
            "id": msg_id,
            "relationships": {"template": {"data": {"type": "template", "id": template_id}}}
        }
    })


def main():
    print("="*60)
    print("Durban Poison — BF Style Email Builder")
    print("="*60)

    # 1. Build HTML
    print("\n[1] Building email HTML (BF 2025 style)...")
    html = build_html()
    print(f"    HTML: {len(html):,} characters")
    with open("/home/user/workflows/durban_poison_bf_email.html","w") as f:
        f.write(html)
    print("    Saved: durban_poison_bf_email.html")

    # 2. Update existing template (YgbmXr)
    print("\n[2] Updating Klaviyo template YgbmXr with new HTML...")
    tmpl_resp = kv_patch("/api/templates/YgbmXr/", {
        "data": {
            "type": "template",
            "id": "YgbmXr",
            "attributes": {
                "name": "Durban Poison — Back in Stock (Apr 2026)",
                "html": html,
                "text": (
                    "DURBAN POISON IS BACK\n\n"
                    "One of the oldest cannabis landraces on earth — pure sativa, proudly South African — "
                    "is back in limited stock at Cannibisters.\n\n"
                    f"Shop now: https://{SHOP}/products/durban-poison-living-soil\n\n"
                    "Limited stock. Don't sleep on it.\n\n"
                    "— The Cannibisters Team"
                ),
            }
        }
    })
    if "errors" in tmpl_resp:
        print(f"    Template update error: {tmpl_resp['errors']}")
        # Create new template if update fails
        print("    Creating new template instead...")
        tmpl_resp = kv_post("/api/templates/", {
            "data": {
                "type": "template",
                "attributes": {
                    "name": "Durban Poison — Back in Stock (Apr 2026) BF Style",
                    "editor_type": "CODE",
                    "html": html,
                    "text": "Durban Poison is back. Shop now at cannibisters.com"
                }
            }
        })
        template_id = tmpl_resp.get("data",{}).get("id")
    else:
        template_id = "YgbmXr"
    print(f"    Template ID: {template_id}")

    # 3. Re-assign template to existing campaign message
    CAMPAIGN_ID = "01KPWYTTYC8A4XS89K7ZA3RD54"
    MSG_ID      = "01KPWYTTYMMQX642W79M7WS408"

    print(f"\n[3] Re-assigning template to campaign message {MSG_ID}...")
    assign_resp = assign_template_to_message(MSG_ID, template_id)
    if "errors" in assign_resp:
        print(f"    Error: {assign_resp['errors']}")
    else:
        linked = assign_resp.get("data",{}).get("relationships",{}).get("template",{}).get("data",{}).get("id","?")
        print(f"    Template linked as: {linked}")

    print("\n" + "="*60)
    print("DONE")
    print("="*60)
    print(f"  Campaign:   {CAMPAIGN_ID}")
    print(f"  Message:    {MSG_ID}")
    print(f"  Template:   {template_id}")
    print(f"  Scheduled:  24 Apr 2026 @ 09:00 SAST")
    print(f"  Review:     https://www.klaviyo.com/campaigns/{CAMPAIGN_ID}")
    print("="*60)


if __name__ == "__main__":
    main()
