#!/usr/bin/env bash
# Run this on YOUR local machine (not the server)
# Polymarket blocks US IPs — SA is fine.
#
# Prerequisites: polymarket-cli installed
#   curl -sSL https://raw.githubusercontent.com/Polymarket/polymarket-cli/main/install.sh | sh
#   Or: download from https://github.com/Polymarket/polymarket-cli/releases/latest
#
# Usage:
#   bash run_trades_now.sh

set -euo pipefail

export POLYMARKET_PRIVATE_KEY=0x596f0fd605045fb9cbab9e8af35320ed2ffc3a26e9c4773709f336be8b3c837d
export POLYMARKET_SIGNATURE_TYPE=proxy

echo "Wallet: $(polymarket wallet show | grep Address)"
echo "Balance: $(polymarket clob balance --asset-type collateral)"
echo ""

# ── TRADE 1: Fed no change (99.35% YES, resolves midnight UTC tonight) ──────
# Token: YES share of "Will there be no change in Fed interest rates after March 2026 meeting?"
# Stake: $5 | Expected ROI: +0.65% | Max loss: ~0 (near-certain)
echo "=== Trade 1: Fed holds rates — \$5 (99.35%) ==="
polymarket clob market-order \
  --token 0xe2becca195119686dd1166bd0e62f5d966c3fd730fb18604199b1d01e1a6587f \
  --side buy \
  --amount 5 \
  --order-type FOK
echo ""

# ── TRADE 2: BTC dip to $73k today (44.5% YES, resolves midnight UTC tonight) ─
# BTC currently ~$74.2k and already touched $74k — bearish lean
# Token: YES share of "Will Bitcoin dip to $73,000 on March 17?"
# Stake: $2 | Expected ROI: +124.7% if correct
echo "=== Trade 2: BTC dip to \$73k today — \$2 (44.5%) ==="
polymarket clob market-order \
  --token 0x6df693a6034e78d09ce28a074a2bfef1bafbcaf92c2d7f01d965396bf57f239b \
  --side buy \
  --amount 2 \
  --order-type FOK
echo ""

# ── TRADE 3: BTC reach $75k today (47% YES, resolves midnight UTC tonight) ────
# Hedges the upside in case BTC bounces
# Token: YES share of "Will Bitcoin reach $75,000 on March 17?"
# Stake: $2 | Expected ROI: +112.8% if correct
echo "=== Trade 3: BTC reaches \$75k today — \$2 (47%) ==="
polymarket clob market-order \
  --token 0x373f63300c2b8ad08f25ee854a61bff8ff2d90acd750c05f69524aef8fcc61b8 \
  --side buy \
  --amount 2 \
  --order-type FOK
echo ""

echo "=== All trades placed. Total deployed: \$9 | Reserved: ~\$5.97 ==="
echo "Positions: $(polymarket data positions 2>/dev/null || polymarket clob orders)"
