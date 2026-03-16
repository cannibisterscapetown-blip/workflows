# Gemini Nano — Banner Image Prompt
## Campaign: Cannibisters Loyalty Points Kiosk

---

## Prompt to give Gemini Nano Bannana

```
Create a wide-format email banner (1200 × 450 px, landscape orientation) for Cannibisters,
a premium South African cannabis brand.

SCENE:
A sleek, modern in-store kiosk touchscreen display glowing with a deep purple (#6b21a8)
and soft gold/amber gradient interface. The screen shows a clean loyalty rewards UI with
a list of redeemable products. Place the kiosk in a clean, warmly lit dispensary-style
interior — dark wood accents, soft ambient lighting, minimal and premium feel.

FOREGROUND TEXT (render as part of the image design):
- Large bold headline: "Redeem Your Points"
- Subtext below: "Your loyalty. Your rewards. Your way."

BRANDING:
- Colour palette: Deep purple (#6b21a8), warm white, soft gold/amber highlights,
  dark charcoal background
- Overall vibe: Premium, calm, aspirational — like a luxury loyalty rewards card come to life
- Cannabis leaf motif may be subtly incorporated (small, tasteful, not cartoonish)
- Include the Cannibisters wordmark or logo space in the top-left corner
  (leave a clean white/transparent zone approx 160×60px for the logo overlay)

STYLE:
- Photorealistic with a high-end editorial feel
- Soft depth of field — kiosk in focus, background slightly blurred
- Lighting: warm ambient glow from the kiosk screen illuminating the surrounding area
- No people in the scene
- No text other than the specified headline and subtext
- Clean, uncluttered composition suitable for email header use

OUTPUT: 1200 × 450 px, RGB, suitable for web/email use
```

---

## Notes for the campaign designer

- Replace `{{BANNER_IMAGE_URL}}` in `create_loyalty_kiosk_campaign.py` with the hosted
  URL of the final banner once uploaded (Klaviyo CDN or your own CDN).
- Recommended upload: Klaviyo > Content > Images, then copy the CDN URL.
- Banner displays at 600px wide in the email template; provide at least 1200px wide
  for retina screens.
- Alt text to use: `"Cannibisters Loyalty Points Kiosk — Redeem Your Points"`
