# Bets to Place NOW → Tomorrow Noon
**Date:** 2026-03-17  |  **BTC:** $74,202  |  **ETH:** $2,331  |  **Gold:** $5,019

> Time-sensitive. All bets below close before 2026-03-18 12:00 UTC.

---

## 🏆 Priority 1 — Best Risk/Reward (ACT WITHIN 13h)

### Bet A: Bitcoin touches $75,000 today
| Field | Value |
|-------|-------|
| Market | "Will Bitcoin reach $75,000 on March 17?" |
| Slug | `will-bitcoin-reach-75k-on-march-17` |
| Side | YES |
| Current price | 54.5¢ |
| Resolves | 2026-03-17T23:59:00Z (tonight) |
| ROI if correct | **+83.5%** |
| Suggested stake | **$8** |

**Why:** BTC is at $74,202 — only $798 (1.08%) away from the $75k trigger. This market pays off if BTC *touches* $75k at any point before midnight UTC. Given BTC's typical intraday range of 2–4%, a 1% bounce from here is very achievable in 13 hours. The 54.5% market price feels slightly low.

---

## 🛡️ Priority 2 — Near-Certain, Resolves Tonight

### Bet B: Fed holds rates (no change)
| Field | Value |
|-------|-------|
| Market | "Will there be no change in Fed interest rates after the March 2026 meeting?" |
| Slug | `will-there-be-no-change-in-fed-interest-rates-after-the-march-2026-meeting` |
| Side | YES |
| Current price | 99.4¢ |
| Resolves | 2026-03-18T00:00:00Z (midnight UTC) |
| ROI if correct | **+0.6%** |
| Suggested stake | **$5** |

**Why:** Near-zero risk. The Fed meeting is today. CME FedWatch shows 99.9% probability of hold. This is essentially free money; the tiny ROI compounds your bankroll safely.

---

## 🎯 Priority 3 — Hedge / Downside Play

### Bet C: Bitcoin dips to $73,000 today
| Field | Value |
|-------|-------|
| Market | "Will Bitcoin dip to $73,000 on March 17?" |
| Slug | `will-bitcoin-dip-to-73k-on-march-17` |
| Side | YES |
| Current price | 38.0¢ |
| Resolves | 2026-03-17T23:59:00Z (tonight) |
| ROI if correct | **+163%** |
| Suggested stake | **$2** |

**Why:** With BTC at $74.2k, a $1.2k (1.6%) dip to $73k is plausible — especially given global macro jitters. If BTC sells off instead of rallying, this pays 163% ROI. It also partially hedges Bet A (if BTC goes down hard, you lose Bet A but win Bet C).

---

## Summary

| Bet | Stake | Win | EV |
|-----|-------|-----|----|
| A: BTC reach $75k | $8 | +$6.68 | +$1.84 |
| B: Fed hold | $5 | +$0.03 | +$0.03 |
| C: BTC dip $73k | $2 | +$3.26 | +$1.24 |
| **Total** | **$15** | — | **+$3.11** (20.7% EV) |

**Best case** (A + B hit): +$6.71 → portfolio $21.71 (+44.7%)
**Worst case** (only B hits): -$9.97 → portfolio $5.03
**Base case** (either A or C, plus B): ~+$3-4 → portfolio $18-19

---

## How to Execute (once wallet is funded)

```bash
export PATH="$HOME/.local/bin:$PATH"

# Bet A – $8 on BTC reaching $75k
polymarket clob buy \
  --market will-bitcoin-reach-75k-on-march-17 \
  --side yes \
  --amount 8

# Bet B – $5 on Fed holding
polymarket clob buy \
  --market will-there-be-no-change-in-fed-interest-rates-after-the-march-2026-meeting \
  --side yes \
  --amount 5

# Bet C – $2 on BTC dipping to $73k
polymarket clob buy \
  --market will-bitcoin-dip-to-73k-on-march-17 \
  --side yes \
  --amount 2

# Check positions
polymarket portfolio positions
```

---

## After These Resolve Tomorrow

With expected ~$18-22 to redeploy, the next wave of opportunities:
- Crude Oil > $72 end-March (92%, 8.7% ROI, 13 days)
- Anthropic #1 AI model end-March (92.8%, 7.8% ROI, 13 days)
- Gold above $4,800 end-March (75%, 33% ROI, 13 days)

See `EXPERIMENT.md` for full strategy.
