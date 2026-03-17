# Polymarket ROI Experiment
**Start Date:** 2026-03-17
**Starting Capital:** $15.00 USDC
**Goal:** Maximise ROI via disciplined position-sizing on high-edge markets

---

## Market Context (as of 2026-03-17)
| Asset | Current Price |
|-------|--------------|
| Bitcoin (BTC) | $74,202 |
| Ethereum (ETH) | $2,331 |
| Gold (GC) | $5,019/oz |
| Crude Oil (CL) | ~$93/barrel |

---

## Portfolio Allocation Strategy

### Tier 1 — Near-Certain, Near-Term (40% = $6.00)
Low variance, fast-compounding bets on central bank decisions resolving within 24-48h.

| Market | Yes Price | Prob | Days | Expected ROI |
|--------|-----------|------|------|-------------|
| Fed no change March 2026 | 99.4¢ | ~99.4% | 0.4d | 0.6% |
| ECB no change March 2026 | 99.3¢ | ~99.3% | 1.4d | 0.7% |
| BOJ no change March 2026 | 98.5¢ | ~98.5% | 1.4d | 1.5% |
| Bank of England no change March 2026 | 97.7¢ | ~97.7% | 1.4d | 2.3% |

**Rationale:** These are nearly resolved — all major central banks have already signalled holds. The BOE at 97.7% gives the best yield in this tier.

### Tier 2 — High Conviction, Medium-Term (35% = $5.25)
Strong edge plays with moderate time horizon.

| Market | Yes Price | Prob | Days | Expected ROI |
|--------|-----------|------|------|-------------|
| Anthropic has best AI model end-March | 92.8¢ | ~92.8% | 13.4d | 7.8% |
| Anthropic has #2 AI model end-March | 90.1¢ | ~90.1% | 13.4d | 11.0% |
| 150+ US tornadoes in March 2026 | 94.5¢ | ~94.5% | 23.4d | 5.8% |
| Crude Oil over $72 end-March | 92.0¢ | ~92.0% | 13.4d | 8.7% |
| Gold over $4,600 end-March | 95.4¢ | ~95.4% | 13.4d | 4.8% |

**Rationale:**
- Anthropic AI model: Claude 4.x is currently top-ranked on LMArena/Chatbot Arena. High confidence.
- 150+ tornadoes: March is peak tornado season in the US — historical average exceeds 150. 94.5% seems fair.
- CL over $72: Oil at ~$93, needs a 22% drop to fail. Very unlikely in 13 days.

### Tier 3 — Higher Risk / Higher Reward (25% = $3.75)
Positive-EV plays with higher variance for outsized returns.

| Market | Yes Price | Prob | Days | Expected ROI |
|--------|-----------|------|------|-------------|
| Gold stay above $4,800 end-March | 75.0¢ | ~75.0% | 13.4d | 33% |
| BTC outperform Gold in March 2026 | 84.0¢ | ~84.0% | 13.4d | 19% |
| BTC outperform S&P 500 in March 2026 | 73.5¢ | ~73.5% | 13.4d | 36% |

**Rationale:**
- Gold at $5,019 needs to DROP to below $4,800 (a 4.4% decline) for NO. 75% probability seems underpriced.
- BTC vs Gold: BTC at $74k against gold's recent momentum — this is a close call.

---

## Suggested Trade Plan

### Phase 1 — Deploy Today (Day 0)

```
$1.50 → Fed no change March 2026 (YES at 99.4¢)          Resolves: 2026-03-18
$1.50 → Bank of England no change March 2026 (YES at 97.7¢) Resolves: 2026-03-19
$1.00 → ECB no change March 2026 (YES at 99.3¢)           Resolves: 2026-03-19
$1.00 → BOJ no change March 2026 (YES at 98.5¢)           Resolves: 2026-03-19
$3.00 → Anthropic best AI model end-March (YES at 92.8¢)   Resolves: 2026-03-31
$2.25 → Crude Oil over $72 end-March (YES at 92.0¢)        Resolves: 2026-03-31
$2.00 → Gold above $4,800 end-March (YES at 75.0¢)         Resolves: 2026-03-31
$2.75 → BTC outperform Gold in March (YES at 84.0¢)        Resolves: 2026-03-31
------
$15.00 TOTAL
```

### Phase 2 — Reinvest Phase 1 Proceeds (~Day 2)
- Reinvest central bank winnings (~$5.05) into best available Tier 2/3 markets at that time.

---

## Expected Outcome

| Scenario | Return | Notes |
|----------|--------|-------|
| Bear (all Tier 3 wrong) | +$0.10 | +0.7% — central bank bets rescue the portfolio |
| Base case (Tier 1 + Tier 2 hit, Tier 3 mixed) | +$1.20 | +8% |
| Bull (all hit) | +$2.80 | +19% |

---

## Trade Log

| Date | Market | Side | Price | Amount | Status | P&L |
|------|--------|------|-------|--------|--------|-----|
| — | — | — | — | — | — | — |

---

## Setup Instructions

### 1. Create Polymarket Account
1. Go to https://polymarket.com
2. Sign up / connect wallet
3. Bridge $15 USDC to Polygon (Polymarket uses Polygon network)
4. Enable trading (CLOB approval)

### 2. Configure polymarket-cli
```bash
# Generate or import your wallet
polymarket wallet import

# Or generate new:
polymarket wallet generate

# Save config (private key stored at ~/.config/polymarket/config.json)
polymarket config set private-key <YOUR_PRIVATE_KEY>
polymarket config set signature-type proxy
```

### 3. Verify Setup
```bash
polymarket portfolio balance
```

### 4. Execute Trades
```bash
# See trade_executor.sh for automated trade execution
bash polymarket_experiment/trade_executor.sh
```

---

## Notes
- Minimum trade size on Polymarket CLOB: ~$1 USDC
- Slippage is low on high-liquidity markets (Fed/ECB decisions have $10M+ liquidity)
- Polymarket uses Polygon — gas fees are negligible ($0.001 per tx)
- All prices are in USDC; payouts are $1.00 per winning share
