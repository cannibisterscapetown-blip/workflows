# Cannibisters — Re-engagement Campaign 2026
## Monthly Recurring | Target: Members Inactive 90+ Days

---

## Overview

| Field | Detail |
|---|---|
| Campaign name | Re-engagement Campaign 2026 |
| Type | Recurring monthly campaign (manual send or Flow) |
| Audience | Members with no orders in the last 90 days |
| Frequency | Minimum once per month (recommended: 1st Tuesday of each month) |
| Goal | Bring lapsed members back to the Club |

---

## Part 1: Klaviyo Segment Setup

**Segment name:** `Lapsed Members — 90+ Days No Order`

### Segment Definition (set in Klaviyo → Segments → Create Segment)

```
ALL of the following conditions:

1. What someone has done (or not done):
   > Has NOT placed an order
   > in the last 90 days

2. Properties about someone:
   > Email > is not empty

3. What someone has done (or not done):
   > Has been added to list
   > "Newsletter" (or your main members list)
   > at least once
```

> **Note:** If you track orders via Shopify–Klaviyo integration, use the
> "Placed Order" metric. If via custom event, substitute your event name.
> Suppress anyone who has unsubscribed or is globally suppressed — Klaviyo
> does this automatically for consented sends.

---

## Part 2: Email 1 — Primary Re-engagement Email

### Subject Line Options (A/B test recommended)

- **A:** `We've kept a spot open for you.`
- **B:** `It's been a while — here's what's new at the Club.`
- **C:** `Your Club has something for you.` *(most brand-aligned)*

### Preview Text

`A curated selection is waiting. Come back when you're ready.`

---

### Email Body

---

**[HEADER IMAGE: Cannibisters logo on black/cream background — minimal]**

---

**We've missed you.**

It's been a while since your last visit to the Club.

We understand — life moves fast. But the Club has been busy, and there's plenty
waiting for you when you're ready to return.

---

**What's new at Cannibisters:**

- Fresh strains and curated drops — added regularly
- New premium products, now available in-store and online
- Members-only exclusives you won't find elsewhere

---

**[CTA BUTTON: "Return to the Club" → https://www.cannibisters.co.za]**

---

*This is a private, members-only communication. As a responsible club, we respect
your inbox and your time. If you'd prefer not to receive these updates, you can
manage your preferences below.*

---

Warm regards,
The Cannibisters Team

---

**[Footer: Unsubscribe | Manage Preferences | Privacy Policy]**
*Cannibisters Herbal Apothecary | Cape Town, South Africa*

---

## Part 3: Email 2 — Follow-up (Send 7 days after Email 1, if no order placed)

### Subject Line Options

- **A:** `A quiet reminder from the Club.`
- **B:** `Still here, still curated — just for you.`

### Preview Text

`One final note before we step back.`

---

### Email Body

---

**[HEADER IMAGE: Clean product flat-lay or storefront — premium feel]**

---

**A gentle note.**

We sent a message last week — just in case it got lost.

Your membership is still active. Your Club is still here.

If there's anything we can help you find — a specific strain, a curated
recommendation, or simply a reason to visit — we're here.

---

**[CTA BUTTON: "Browse the Collection" → https://www.cannibisters.co.za]**

---

*If now isn't the right time, no worries at all. We'll give you space.
You can manage your email preferences at any time.*

---

Warm regards,
The Cannibisters Team

---

**[Footer: Unsubscribe | Manage Preferences | Privacy Policy]**
*Cannibisters Herbal Apothecary | Cape Town, South Africa*

---

## Part 4: Klaviyo Campaign Setup — Step by Step

### Option A: Manual Campaign (Simplest — send monthly)

1. Go to **Campaigns → Create Campaign → Email**
2. Campaign name: `Re-engagement — [Month] 2026` (e.g. `Re-engagement — April 2026`)
3. **From name:** Cannibisters
4. **From email:** your verified sending address (e.g. `hello@cannibisters.co.za`)
5. **Reply-to:** same or support address
6. **Recipients:** Select segment `Lapsed Members — 90+ Days No Order`
7. Paste in Email 1 body above using Klaviyo's drag-and-drop or HTML editor
8. Schedule for **1st Tuesday of each month, 10:00 AM SAST**
9. Review → Send

> Repeat this process monthly. Clone the previous campaign each month and
> update the campaign name and any product references.

---

### Option B: Automated Flow (Recommended for ongoing automation)

1. Go to **Flows → Create Flow → Create from Scratch**
2. Flow name: `Re-engagement Flow — 90 Day Lapsed`
3. **Trigger:** Metric — *Set a date-based trigger on "last order date"*
   - OR use **Segment Trigger**: `When someone enters the segment "Lapsed Members — 90+ Days No Order"`
4. **Flow structure:**

```
[Segment Entry Trigger]
        |
   [Wait: 0 days — send immediately on segment entry]
        |
   [Email: Re-engagement Email 1]
        |
   [Wait: 7 days]
        |
   [Conditional Split: Has placed order in last 7 days?]
        |                    |
      YES                   NO
        |                    |
   [Exit Flow]    [Email: Re-engagement Email 2]
                             |
                        [Exit Flow]
```

5. Set both emails to **Smart Send Time** or fixed time (10:00 AM SAST)
6. Enable **Quiet Hours** (no sends between 21:00–08:00)
7. Set Flow to **Live**

---

## Part 5: Monthly Sending Schedule 2026

| Month | Recommended Send Date | Notes |
|---|---|---|
| April | Tuesday 7 April | First send — monitor open rates closely |
| May | Tuesday 5 May | |
| June | Tuesday 2 June | |
| July | Tuesday 7 July | |
| August | Tuesday 4 August | |
| September | Tuesday 1 September | |
| October | Tuesday 6 October | |
| November | Tuesday 3 November | |
| December | Tuesday 1 December | Adjust copy for festive season |

---

## Part 6: Performance Benchmarks to Track

After each send, record in the monthly marketing report:

| Metric | Target |
|---|---|
| Open rate | > 30% |
| Click rate | > 3% |
| Unsubscribe rate | < 0.5% |
| Conversion (orders placed within 7 days) | > 1% |
| Revenue attributed (Klaviyo 5-day attribution) | Track monthly |

---

## Part 7: Copy Variation Ideas (Rotate Monthly)

To avoid fatigue, rotate the core message each month while keeping brand voice consistent.

| Month | Theme | Subject Line |
|---|---|---|
| April | New arrivals | `Something fresh has arrived at the Club.` |
| May | Member appreciation | `For members who know the difference.` |
| June | Winter warmth | `A curated selection for the cooler months.` |
| July | Quiet luxury | `The Club is quieter in winter. Room for you.` |
| August | Spring refresh | `A new season. New drops to explore.` |
| September | Community | `Your Club. Your community. Still here.` |
| October | Exclusives | `Members-only arrivals — first notice.` |
| November | Year-end | `The year is winding down. The Club is not.` |
| December | Festive | `A refined end to the year. For members only.` |

---

## Notes

- All sends must go to **opted-in members only** (Klaviyo enforces this by default)
- Keep subject lines under 50 characters where possible
- Do not use discount codes in re-engagement emails unless explicitly approved
  (discounts can attract low-intent returners and devalue the brand)
- If a member unsubscribes after Email 1, **do not send Email 2** —
  Klaviyo handles this automatically when suppression is set correctly
- Review segment size before each send; if fewer than 50 members, hold the
  campaign and review segment logic
