# Bets to Place NOW — March 18, 2026
**BTC:** ~$76k+ (confirmed above $75k)  |  **Bankroll:** $2.10 USDC

---

## Yesterday's Outcome (March 17 — ⚠️ TRADES NOT PLACED)
Wallet was not configured on the server. These were *hypothetical* results:

| Bet | Result | Note |
|-----|--------|------|
| A: BTC touch $75k on Mar 17 | ✅ WOULD HAVE WON | BTC crossed $75k (Mar market now at 100% YES) |
| B: Fed hold rates | ✅ WOULD HAVE WON | Fed held at March meeting |
| C: BTC dip to $73k on Mar 17 | ❌ WOULD HAVE LOST | BTC rallied, never dipped |

**Missed profit on $15 stake: ~+$6.71.** To avoid this again: configure wallet on SA Mac before running.

---

## Today's Portfolio — 2 Bets, $0.80 Total (~10-20% of balance each)

### Bet 1 — Russia/Ukraine NO Ceasefire by March 31 ⭐ Safest Bet
| Field | Value |
|-------|-------|
| Question | Russia x Ukraine ceasefire by March 31, 2026? |
| Slug | `russia-x-ukraine-ceasefire-by-march-31-2026` |
| Token (NO) | `0xb77bb7337a54d0b28b7f5587fa8361f13bc1249ed6b42bb340c2e41f49174c1d` |
| Side | **NO at 98.4¢** |
| Resolves | 2026-03-31 (13 days) |
| Stake | **$0.40 (~19% of $2.10)** |
| Liquidity | $279,000 |
| Profit if correct | +$0.01 (+1.6% in 13 days = ~45% annualised) |

**Why:** Near-zero risk. A formal ceasefire by March 31 requires signing in 13 days — talks remain stalled. Quickest-resolving bet.

---

### Bet 2 — Arsenal WIN English Premier League ⭐ Best EV
| Field | Value |
|-------|-------|
| Question | Will Arsenal win the 2025–26 English Premier League? |
| Slug | `will-arsenal-win-the-202526-english-premier-league` |
| Token (YES) | `0x9e5f6f156e74674f05cfc289b52cd2b1ee7c45151612ef1ed78007af222e50e6` |
| Side | **YES at 89¢** |
| Resolves | ~June 25, 2026 (70 days) |
| Stake | **$0.40 (~19% of $2.10)** |
| Liquidity | $792,000 |
| Profit if correct | +$0.05 (+12.4% ROI) |

**Why:** Liverpool are at 0.1% — mathematically eliminated. Arsenal lead the EPL by a wide margin and are 89% favourites. Deep liquidity means clean execution.

---

## Summary

| Bet | Stake | Prob | Profit | EV |
|-----|-------|------|--------|----|
| 1: Russia NO ceasefire | $0.40 | 98.4% | +$0.01 | +$0.01 |
| 2: Arsenal YES EPL | $0.40 | 89% | +$0.05 | +$0.04 |
| **TOTAL** | **$0.80** | — | **+$0.06** | **+$0.05 (+6.6% EV)** |

**Balance remaining unrisked:** $1.30
**Best case (both hit):** +$0.06 → $2.16 portfolio (+2.9%)
**Worst case (both miss):** -$0.80 → $1.30 (extremely unlikely)

---

## Execute from Your SA Mac

```bash
export POLYMARKET_PRIVATE_KEY=0x<your_key_here>
export POLYMARKET_SIGNATURE_TYPE=proxy

bash polymarket_experiment/run_trades_now.sh
```

---

## Notes
- ⚠️ **This server has a US IP — Polymarket is geoblocked here.** Run from your SA Mac.
- Arsenal (Bet 1) + Man City (Bet 3) are correlated — they rise and fall together.
- Masters resolves April 13. Russia resolves March 31. Football bets resolve May–June.
- After March 31: reinvest the $0.41 from the ceasefire bet into the next opportunity (e.g. Real Madrid NO Champions League — 88.5%, 13% ROI, $298k liquidity).
- As balance grows, scale bets up proportionally (always 10-20% per bet).
