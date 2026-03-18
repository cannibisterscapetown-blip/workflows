#!/usr/bin/env bash
# Run this on YOUR local machine (not the server)
# Polymarket blocks US IPs — SA is fine.
#
# Prerequisites: polymarket-cli installed
#   curl -sSL https://raw.githubusercontent.com/Polymarket/polymarket-cli/main/install.sh | sh
#   Or: download from https://github.com/Polymarket/polymarket-cli/releases/latest
#
# Usage:
#   export POLYMARKET_PRIVATE_KEY=0x<your_key>
#   bash run_trades_now.sh

set -euo pipefail

export POLYMARKET_PRIVATE_KEY="${POLYMARKET_PRIVATE_KEY:?Set POLYMARKET_PRIVATE_KEY env var before running}"
export POLYMARKET_SIGNATURE_TYPE=proxy

echo "=== Polymarket Trade Runner — 2026-03-18 ==="
echo "Wallet: $(polymarket wallet address 2>/dev/null || echo 'check wallet')"
echo "Balance: $(polymarket clob balance --asset-type collateral)"
echo ""

# ── TRADE 1: Arsenal YES EPL (89%, ~$792k liq, resolves ~June 25) ───────────
# "Will Arsenal win the 2025-26 English Premier League?"
# Arsenal leading; Liverpool eliminated (0.1%). Strong conviction.
# Stake: $4 | Expected profit: +$0.49 (+12.4% ROI)
echo "=== Trade 1: Arsenal YES EPL — \$4 (89%) ==="
polymarket clob market-order \
  0x9e5f6f156e74674f05cfc289b52cd2b1ee7c45151612ef1ed78007af222e50e6 \
  --side buy \
  --amount 4
echo ""

# ── TRADE 2: Russia/Ukraine NO ceasefire by March 31 (98.4%, $279k liq) ────
# Near-certain. Peace talks stalled; no ceasefire possible in 13 days.
# Stake: $3 | Expected profit: +$0.05 (+1.6% ROI in 13 days)
echo "=== Trade 2: Russia/Ukraine NO ceasefire — \$3 (98.4%) ==="
polymarket clob market-order \
  0xb77bb7337a54d0b28b7f5587fa8361f13bc1249ed6b42bb340c2e41f49174c1d \
  --side buy \
  --amount 3
echo ""

# ── TRADE 3: Man City NO EPL (90%, $337k liq, resolves ~June 25) ────────────
# Arsenal winning = Man City cannot. Correlated upside with Trade 1.
# Stake: $3 | Expected profit: +$0.33 (+11.1% ROI)
echo "=== Trade 3: Man City NO EPL — \$3 (90%) ==="
polymarket clob market-order \
  0x4e9cd5bbe2913b58188f0332e32889aa3c7db2695cc72e526265201a5d829349 \
  --side buy \
  --amount 3
echo ""

# ── TRADE 4: Inter Milan YES Serie A (90%, $196k liq, resolves ~June 1) ─────
# Inter leading Serie A. Diversifies away from EPL.
# Stake: $3 | Expected profit: +$0.33 (+11.1% ROI)
echo "=== Trade 4: Inter YES Serie A — \$3 (90%) ==="
polymarket clob market-order \
  0xce34babde54ea0e7af1b7acd729842265989fa433c9f1f459ea3430b4a342a2f \
  --side buy \
  --amount 3
echo ""

# ── TRADE 5: Rory McIlroy NO Masters (91%, $57k liq, resolves April 13) ────
# Fastest-resolving non-ceasefire bet. Even top golfers rarely win majors.
# Stake: $2 | Expected profit: +$0.20 (+10% ROI)
echo "=== Trade 5: Rory McIlroy NO Masters — \$2 (91%) ==="
polymarket clob market-order \
  0xf4ca29d3494f7e5a86cbb242dcca49c200cbc56cabcd4d57f5eed3ed18b04a7d \
  --side buy \
  --amount 2
echo ""

echo "=== All 5 trades placed. Total deployed: \$15.00 ==="
echo "Expected EV: +\$1.27 (+8.5%)"
echo ""
echo "Positions:"
polymarket data positions 2>/dev/null || polymarket clob orders
