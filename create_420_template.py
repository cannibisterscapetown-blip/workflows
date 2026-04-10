#!/usr/bin/env python3
"""
Create a new Klaviyo template for the 4/20 Carnival event.
Cannibisters brand style: white bg, #ff9501 orange, Helvetica.
"""

import requests

KLAVIYO_API_KEY = "pk_2b57d9dd3402b67a041cb42568247ac52b"
HEADERS = {
    "Authorization": f"Klaviyo-API-Key {KLAVIYO_API_KEY}",
    "accept": "application/json",
    "content-type": "application/json",
    "revision": "2024-10-15",
}

BANNER_PLACEHOLDER = "https://via.placeholder.com/600x300/ff9501/000000?text=4%2F20+Banner+Coming+Soon"

HTML = """<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>4/20 Carnival — Cannibisters Herbal Apothecary</title>
<style>
body,table,td,p,a{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;}
table,td{border-collapse:collapse;mso-table-lspace:0;mso-table-rspace:0;}
img{border:0;line-height:100%;outline:none;text-decoration:none;max-width:100%;height:auto;display:block;}
body{margin:0;padding:0;background-color:#f5f5f5;}
p{margin:0;padding:0;}
a:link,a:visited,a:active{color:#ff9501;}
@media only screen and (max-width:620px){
  .email-container{width:100%!important;}
  .mob-pad{padding-left:16px!important;padding-right:16px!important;}
  .hero-title{font-size:30px!important;line-height:1.2!important;}
  .activity-cell{display:block!important;width:100%!important;padding:0 0 12px!important;}
  .two-col{display:block!important;width:100%!important;}
}
</style>
</head>
<body style="margin:0;padding:0;background-color:#f5f5f5;">
<table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color:#f5f5f5;padding:30px 0;">
<tr><td align="center">

<!-- EMAIL CONTAINER -->
<table border="0" cellpadding="0" cellspacing="0" class="email-container" width="600" style="max-width:600px;background-color:#ffffff;">

  <!-- BANNER -->
  <tr>
    <td style="padding:0;line-height:0;font-size:0;">
      <img src="BANNER_URL_HERE" alt="4/20 Carnival — Cannibisters" width="600"
           style="width:100%;max-width:600px;display:block;"/>
    </td>
  </tr>

  <!-- ORANGE HEADER BAR -->
  <tr>
    <td align="center" style="background-color:#ff9501;padding:10px 20px;">
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:11px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#000000;margin:0;">
        Sunday 20 April 2025 &nbsp;·&nbsp; 65 Regent Road, Sea Point &nbsp;·&nbsp; Members Only
      </p>
    </td>
  </tr>

  <!-- HERO -->
  <tr>
    <td align="left" class="mob-pad" style="padding:40px 40px 28px;background-color:#ffffff;">
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#333333;margin:0 0 14px 0;">Hi Member,</p>
      <h1 class="hero-title" style="font-family:Helvetica,Arial,sans-serif;font-size:36px;font-weight:700;line-height:1.15;color:#060606;margin:0 0 16px 0;">
        The Cannibisters<br/>4/20 Carnival is here. 🎪
      </h1>
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:15px;line-height:1.75;color:#555555;margin:0 0 16px 0;">
        The biggest cannabis holiday of the year deserves the biggest party we've thrown yet. Join us on Sunday the 20th for a full day of live music, games, prizes, giveaways — and a whole lot of smoke.
      </p>
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:15px;font-weight:700;color:#060606;margin:0;">It's free to attend. Members only. 🌿</p>
      <table border="0" cellpadding="0" cellspacing="0" style="margin:22px 0 0;">
        <tr><td width="48" height="3" style="background-color:#ff9501;border-radius:2px;font-size:0;line-height:0;"> </td></tr>
      </table>
    </td>
  </tr>

  <!-- LIVE MUSIC HIGHLIGHT -->
  <tr>
    <td class="mob-pad" style="padding:0 40px 24px;background-color:#ffffff;">
      <table border="0" cellpadding="0" cellspacing="0" width="100%"
             style="background-color:#060606;border-radius:10px;overflow:hidden;">
        <tr>
          <td style="padding:28px 28px 24px;">
            <p style="font-family:Helvetica,Arial,sans-serif;font-size:11px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#ff9501;margin:0 0 10px 0;">🎤 Live Performance</p>
            <h2 style="font-family:Helvetica,Arial,sans-serif;font-size:24px;font-weight:700;color:#ffffff;margin:0 0 8px 0;">C.H.A.D.</h2>
            <p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:1.7;color:#aaaaaa;margin:0;">
              Live hip hop on the 20th. One of Cape Town's finest hitting the stage right here at the Apothecary. Don't miss it.
            </p>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- NEW THIS YEAR -->
  <tr>
    <td align="center" class="mob-pad" style="padding:8px 40px 16px;background-color:#ffffff;">
      <h2 style="font-family:Helvetica,Arial,sans-serif;font-size:20px;font-weight:700;color:#060606;margin:0 0 4px 0;">New this year ✨</h2>
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#666666;margin:0;">Fresh attractions making their debut at 4/20.</p>
    </td>
  </tr>

  <!-- NEW ATTRACTIONS GRID -->
  <tr>
    <td class="mob-pad" style="padding:8px 30px 28px;background-color:#ffffff;">
      <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
          <!-- Canni Hotbox -->
          <td class="activity-cell" align="center" style="padding:8px;vertical-align:top;width:33%;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%"
                   style="background-color:#fff8ee;border-radius:10px;border-top:3px solid #ff9501;height:100%;">
              <tr><td style="padding:20px 16px 20px;">
                <p style="font-size:28px;margin:0 0 10px 0;text-align:center;">💨</p>
                <p style="font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:700;color:#060606;margin:0 0 6px 0;text-align:center;">Canni Hotbox</p>
                <p style="font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:1.6;color:#666666;margin:0;text-align:center;">Can you survive 10 minutes in a hotbox full of stoners? Prove it.</p>
              </td></tr>
            </table>
          </td>
          <!-- PS5 Tournament -->
          <td class="activity-cell" align="center" style="padding:8px;vertical-align:top;width:33%;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%"
                   style="background-color:#fff8ee;border-radius:10px;border-top:3px solid #ff9501;height:100%;">
              <tr><td style="padding:20px 16px 20px;">
                <p style="font-size:28px;margin:0 0 10px 0;text-align:center;">🎮</p>
                <p style="font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:700;color:#060606;margin:0 0 6px 0;text-align:center;">PS5 Tournament</p>
                <p style="font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:1.6;color:#666666;margin:0;text-align:center;">FC26 · Mortal Kombat · F1<br/>Winner takes the glory.</p>
              </td></tr>
            </table>
          </td>
          <!-- Popcorn Machine -->
          <td class="activity-cell" align="center" style="padding:8px;vertical-align:top;width:33%;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%"
                   style="background-color:#fff8ee;border-radius:10px;border-top:3px solid #ff9501;height:100%;">
              <tr><td style="padding:20px 16px 20px;">
                <p style="font-size:28px;margin:0 0 10px 0;text-align:center;">🍿</p>
                <p style="font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:700;color:#060606;margin:0 0 6px 0;text-align:center;">Popcorn Machine</p>
                <p style="font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:1.6;color:#666666;margin:0;text-align:center;">Fresh carnival popcorn on the house. Munchies sorted.</p>
              </td></tr>
            </table>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- RETURNING FAVOURITES -->
  <tr>
    <td align="center" class="mob-pad" style="padding:8px 40px 16px;background-color:#ffffff;">
      <h2 style="font-family:Helvetica,Arial,sans-serif;font-size:20px;font-weight:700;color:#060606;margin:0 0 4px 0;">Back by popular demand 🔁</h2>
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#666666;margin:0;">The fan favourites from last year's 4/20.</p>
    </td>
  </tr>

  <!-- GAMES GRID -->
  <tr>
    <td class="mob-pad" style="padding:8px 30px 12px;background-color:#ffffff;">
      <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
          <!-- Bong Pong -->
          <td class="activity-cell" align="center" style="padding:8px;vertical-align:top;width:33%;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%"
                   style="background-color:#fff8ee;border-radius:10px;height:100%;">
              <tr><td style="padding:20px 16px 20px;">
                <p style="font-size:28px;margin:0 0 10px 0;text-align:center;">🏓</p>
                <p style="font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:700;color:#060606;margin:0 0 6px 0;text-align:center;">Bong Pong</p>
                <p style="font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:1.6;color:#666666;margin:0;text-align:center;">The game where the loser gets high. Choose your partner wisely.</p>
              </td></tr>
            </table>
          </td>
          <!-- Free Throw -->
          <td class="activity-cell" align="center" style="padding:8px;vertical-align:top;width:33%;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%"
                   style="background-color:#fff8ee;border-radius:10px;height:100%;">
              <tr><td style="padding:20px 16px 20px;">
                <p style="font-size:28px;margin:0 0 10px 0;text-align:center;">🏀</p>
                <p style="font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:700;color:#060606;margin:0 0 6px 0;text-align:center;">Free Throw</p>
                <p style="font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:1.6;color:#666666;margin:0;text-align:center;">Land your Cannibisters container in the hoop, win a prize.</p>
              </td></tr>
            </table>
          </td>
          <!-- Joint Rolling -->
          <td class="activity-cell" align="center" style="padding:8px;vertical-align:top;width:33%;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%"
                   style="background-color:#fff8ee;border-radius:10px;height:100%;">
              <tr><td style="padding:20px 16px 20px;">
                <p style="font-size:28px;margin:0 0 10px 0;text-align:center;">🌿</p>
                <p style="font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:700;color:#060606;margin:0 0 6px 0;text-align:center;">Joint Rolling</p>
                <p style="font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:1.6;color:#666666;margin:0;text-align:center;">Best roll · Most creative · Fastest roll<br/>Three titles. Three prizes.</p>
              </td></tr>
            </table>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- PRIZES BANNER -->
  <tr>
    <td class="mob-pad" style="padding:16px 40px 28px;background-color:#ffffff;">
      <table border="0" cellpadding="0" cellspacing="0" width="100%"
             style="background-color:#fff8ee;border-left:4px solid #ff9501;border-radius:4px;">
        <tr><td style="padding:16px 20px;">
          <p style="font-family:Helvetica,Arial,sans-serif;font-size:13px;line-height:1.7;color:#555555;margin:0;">
            <strong style="color:#060606;">Prizes, giveaways & competitions throughout the day.</strong><br/>
            Show up, play hard, smoke well. The more you participate, the more you can win.
          </p>
        </td></tr>
      </table>
    </td>
  </tr>

  <!-- MAIN CTA -->
  <tr>
    <td align="center" class="mob-pad" style="padding:0 40px 48px;background-color:#ffffff;">
      <table border="0" cellpadding="0" cellspacing="0">
        <tr>
          <td align="center" bgcolor="#ff9501" style="border-radius:8px;">
            <a href="https://www.cannibisters.com" style="display:inline-block;font-family:Helvetica,Arial,sans-serif;font-size:16px;font-weight:700;color:#000000;text-decoration:none;padding:16px 48px;">I'm Coming 🎪</a>
          </td>
        </tr>
      </table>
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:12px;color:#999999;margin:16px 0 0 0;letter-spacing:0.5px;">
        Sunday 20 April &nbsp;·&nbsp; 65 Regent Road, Sea Point &nbsp;·&nbsp; Members only
      </p>
    </td>
  </tr>

  <!-- FOOTER -->
  <tr>
    <td align="center" class="mob-pad" style="background-color:#f5f5f5;border-top:1px solid #eeeeee;padding:30px 40px;">
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:700;color:#333333;margin:0 0 4px 0;">Cannibisters - The Herbal Apothecary</p>
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:12px;color:#888888;margin:0 0 4px 0;">65 Regent Rd, Sea Point, Cape Town, 8001</p>
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:12px;color:#888888;margin:0 0 4px 0;">087 537 8000 &nbsp;·&nbsp; <a href="mailto:high@cannibisters.com" style="color:#ff9501;text-decoration:none;">high@cannibisters.com</a></p>
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:12px;color:#888888;margin:0 0 20px 0;"><a href="http://www.cannibisters.com" style="color:#ff9501;text-decoration:none;">www.cannibisters.com</a></p>
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:11px;color:#aaaaaa;margin:0 0 10px 0;">{% unsubscribe 'Unsubscribe' %}</p>
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:10px;color:#cccccc;line-height:1.6;margin:0;">For adults 18+. Members only. Private &amp; responsible.</p>
    </td>
  </tr>

</table>
</td></tr>
</table>
</body>
</html>"""

# Create the template
payload = {
    "data": {
        "type": "template",
        "attributes": {
            "name": "4/20 Carnival 2025 — Event Invite",
            "html": HTML,
            "editor_type": "CODE",
        }
    }
}

resp = requests.post("https://a.klaviyo.com/api/templates/", headers=HEADERS, json=payload)
if resp.status_code == 201:
    tid = resp.json()["data"]["id"]
    print(f"Template created! ID: {tid}")
    print(f"Edit: https://www.klaviyo.com/email-editor/{tid}/edit")
else:
    print(f"Error {resp.status_code}: {resp.text[:500]}")
