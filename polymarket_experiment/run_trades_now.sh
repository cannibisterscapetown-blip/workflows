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

# ── TRADE 1: Russia/Ukraine NO ceasefire by March 31 (98.4%, $279k liq) ────
# Near-certain. Peace talks stalled; no ceasefire possible in 13 days.
# Stake: $0.40 (~19% of $2.10 balance) | Expected profit: +$0.01 (+1.6% ROI in 13 days)
echo "=== Trade 1: Russia/Ukraine NO ceasefire — \$0.40 (98.4%) ==="
polymarket clob market-order \
  0xb77bb7337a54d0b28b7f5587fa8361f13bc1249ed6b42bb340c2e41f49174c1d \
  --side buy \
  --amount 0.40
echo ""

# ── TRADE 2: Arsenal YES EPL (89%, ~$792k liq, resolves ~June 25) ───────────
# Arsenal leading; Liverpool eliminated (0.1%). Strong conviction.
# Stake: $0.40 (~19% of $2.10 balance) | Expected profit: +$0.05 (+12.4% ROI)
echo "=== Trade 2: Arsenal YES EPL — \$0.40 (89%) ==="
polymarket clob market-order \
  0x9e5f6f156e74674f05cfc289b52cd2b1ee7c45151612ef1ed78007af222e50e6 \
  --side buy \
  --amount 0.40
echo ""

echo "=== Both trades placed. Total deployed: \$0.80 (~38% of \$2.10 balance) ==="
echo "Expected EV: ~+\$0.06"
echo ""
echo "Positions:"
polymarket data positions 2>/dev/null || polymarket clob orders
