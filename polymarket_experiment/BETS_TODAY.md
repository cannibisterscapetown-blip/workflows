# Bets to Place NOW — March 18, 2026
**BTC:** ~$76k+ (confirmed above $75k)  |  **Bankroll:** $15.00 USDC

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

## Today's Portfolio — 5 Bets, $15.00 Total

### Bet 1 — Arsenal WIN English Premier League ⭐ Best Bet
| Field | Value |
|-------|-------|
| Question | Will Arsenal win the 2025–26 English Premier League? |
| Slug | `will-arsenal-win-the-202526-english-premier-league` |
| Token (YES) | `0x9e5f6f156e74674f05cfc289b52cd2b1ee7c45151612ef1ed78007af222e50e6` |
| Side | **YES at 89¢** |
| Resolves | ~June 25, 2026 (70 days) |
| Stake | **$4.00** |
| Liquidity | $792,000 |
| Profit if correct | +$0.49 (+12.4% ROI) |

**Why:** Liverpool are at 0.1% — mathematically eliminated. Arsenal lead the EPL by a wide margin and are 89% favourites. Deep liquidity means clean execution. 70-day hold with strong conviction.

---

### Bet 2 — Russia/Ukraine NO Ceasefire by March 31
| Field | Value |
|-------|-------|
| Question | Russia x Ukraine ceasefire by March 31, 2026? |
| Slug | `russia-x-ukraine-ceasefire-by-march-31-2026` |
| Token (NO) | `0xb77bb7337a54d0b28b7f5587fa8361f13bc1249ed6b42bb340c2e41f49174c1d` |
| Side | **NO at 98.4¢** |
| Resolves | 2026-03-31 (13 days) |
| Stake | **$3.00** |
| Liquidity | $279,000 |
| Profit if correct | +$0.05 (+1.6% in 13 days = ~45% annualised) |

**Why:** Near-zero risk. A formal ceasefire by March 31 requires signing in 13 days — talks remain stalled. Fastest-resolving bet in the portfolio.

---

### Bet 3 — Manchester City NO EPL Win
| Field | Value |
|-------|-------|
| Question | Will Manchester City win the 2025–26 English Premier League? |
| Slug | `will-manchester-city-win-the-202526-english-premier-league` |
| Token (NO) | `0x4e9cd5bbe2913b58188f0332e32889aa3c7db2695cc72e526265201a5d829349` |
| Side | **NO at 90¢** |
| Resolves | ~June 25, 2026 (70 days) |
| Stake | **$3.00** |
| Liquidity | $337,000 |
| Profit if correct | +$0.33 (+11.1% ROI) |

**Why:** Arsenal essentially have the title. Man City NO and Arsenal YES are correlated — if Arsenal win the league (Bet 1), Man City definitely cannot (Bet 3 also pays). Portfolio synergy.

---

### Bet 4 — Inter Milan WIN Serie A
| Field | Value |
|-------|-------|
| Question | Will Inter win the 2025–26 Serie A league? |
| Slug | `will-inter-win-the-202526-serie-a-league` |
| Token (YES) | `0xce34babde54ea0e7af1b7acd729842265989fa433c9f1f459ea3430b4a342a2f` |
| Side | **YES at 90¢** |
| Resolves | ~June 1, 2026 (75 days) |
| Stake | **$3.00** |
| Liquidity | $196,000 |
| Profit if correct | +$0.33 (+11.1% ROI) |

**Why:** Inter leading Serie A with a solid cushion. Serie A tends to be more predictable once a team goes clear. Diversifies away from EPL exposure.

---

### Bet 5 — Rory McIlroy NO Masters Win
| Field | Value |
|-------|-------|
| Question | Will Rory McIlroy win the 2026 Masters tournament? |
| Slug | `will-rory-mcilroy-win-the-2026-masters-tournament` |
| Token (NO) | `0xf4ca29d3494f7e5a86cbb242dcca49c200cbc56cabcd4d57f5eed3ed18b04a7d` |
| Side | **NO at 91¢** |
| Resolves | April 13, 2026 (26 days) |
| Stake | **$2.00** |
| Liquidity | $57,000 |
| Profit if correct | +$0.20 (+10.0% ROI) |

**Why:** Rory is Masters favourite but still only ~9% to win. Even the world's best golfer wins fewer than 1 in 10 majors. Quickest-resolving of the non-ceasefire bets.

---

## Summary

| Bet | Stake | Prob | Profit | EV |
|-----|-------|------|--------|----|
| 1: Arsenal YES EPL | $4.00 | 89% | +$0.49 | +$0.44 |
| 2: Russia NO ceasefire | $3.00 | 98.4% | +$0.05 | +$0.05 |
| 3: Man City NO EPL | $3.00 | 90% | +$0.33 | +$0.30 |
| 4: Inter YES Serie A | $3.00 | 90% | +$0.33 | +$0.30 |
| 5: Rory NO Masters | $2.00 | 91% | +$0.20 | +$0.18 |
| **TOTAL** | **$15.00** | — | **+$1.40** | **+$1.27 (+8.5% EV)** |

**Best case (all 5 hit):** +$1.40 → $16.40 portfolio (+9.3%)
**Base case (4/5 hit):** +$0.90 to +$1.20
**Worst case (only Bet 2 hits):** -$12.95 (extremely unlikely — 4 independent markets all failing)

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
- After March 31: reinvest the $3.05 from the ceasefire bet into Real Madrid NO Champions League (88.5%, 13% ROI, $298k liquidity).
