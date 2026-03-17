#!/usr/bin/env bash
# Polymarket ROI Experiment — Trade Executor
# Usage: bash trade_executor.sh [--dry-run]
#
# Prerequisites:
#   1. polymarket-cli installed and wallet configured
#   2. USDC deposited to Polygon wallet
#   3. CLOB approvals granted

set -euo pipefail

POLYMARKET="$HOME/.local/bin/polymarket"
DRY_RUN=false
LOG_FILE="$(dirname "$0")/trade_log.csv"

# ── helpers ────────────────────────────────────────────────────────────────

log() { echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] $*"; }

die() { log "ERROR: $*" >&2; exit 1; }

# Write a row to the CSV trade log
record_trade() {
    local market_slug="$1" side="$2" price="$3" amount="$4" status="$5"
    echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ'),$market_slug,$side,$price,$amount,$status" >> "$LOG_FILE"
}

# Place a market buy order; if --dry-run just print
place_buy() {
    local slug="$1"
    local amount="$2"    # USDC to spend
    local description="$3"

    log "BUY $amount USDC → $description (slug: $slug)"

    if $DRY_RUN; then
        log "  [DRY RUN] skipping execution"
        record_trade "$slug" "BUY" "market" "$amount" "dry-run"
        return
    fi

    if "$POLYMARKET" clob buy --market "$slug" --amount "$amount" --side yes; then
        log "  Order placed successfully"
        record_trade "$slug" "BUY" "market" "$amount" "placed"
    else
        log "  WARNING: Order failed for $slug"
        record_trade "$slug" "BUY" "market" "$amount" "failed"
    fi
}

# ── argument parsing ────────────────────────────────────────────────────────

for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        *) die "Unknown argument: $arg" ;;
    esac
done

# ── init log ────────────────────────────────────────────────────────────────

if $DRY_RUN; then
    log "=== DRY RUN MODE — no real orders will be placed ==="
fi

if [[ ! -f "$LOG_FILE" ]]; then
    echo "timestamp,market_slug,side,price,amount_usdc,status" > "$LOG_FILE"
    log "Created trade log: $LOG_FILE"
fi

# ── sanity check ────────────────────────────────────────────────────────────

log "Checking wallet balance..."
"$POLYMARKET" portfolio balance || die "Cannot read wallet balance. Is your key configured?"

# ── Phase 1 Trades ─────────────────────────────────────────────────────────
#
# Strategy summary:
#   Tier 1 ($5.00): Near-certain central bank rate decisions (24-48h)
#   Tier 2 ($5.25): High-confidence medium-term markets
#   Tier 3 ($4.75): Higher-reward macro plays
#
# Market slugs below — verify with:
#   polymarket markets search "<term>" -o json | jq '.[].slug'
# ---------------------------------------------------------------------------

log "=== PHASE 1: Deploying $15.00 across 8 markets ==="

# ── TIER 1: Central Bank Decisions ─────────────────────────────────────────

log "-- Tier 1: Central Bank Decisions --"

# Fed no change (~99.4% YES, resolves 2026-03-18)
place_buy \
    "will-there-be-no-change-in-fed-interest-rates-after-the-march-2026-meeting" \
    "1.50" \
    "Fed no change March 2026 (99.4%)"

# Bank of England no change (~97.7% YES, resolves 2026-03-19)
place_buy \
    "no-change-in-bank-of-englands-interest-rates-after-march-2026-meeting" \
    "1.50" \
    "BOE no change March 2026 (97.7%)"

# ECB no change (~99.3% YES, resolves 2026-03-19)
place_buy \
    "will-the-ecb-announce-no-change-at-the-march-2026-meeting" \
    "1.00" \
    "ECB no change March 2026 (99.3%)"

# Bank of Japan no change (~98.5% YES, resolves 2026-03-19)
place_buy \
    "no-change-in-bank-of-japans-interest-rates-after-march-2026-meeting" \
    "1.00" \
    "BOJ no change March 2026 (98.5%)"

# ── TIER 2: High Conviction Medium-Term ────────────────────────────────────

log "-- Tier 2: High Conviction --"

# Anthropic best AI model end March (~92.8% YES, resolves 2026-03-31)
place_buy \
    "will-anthropic-have-the-best-ai-model-at-the-end-of-march-2026" \
    "3.00" \
    "Anthropic #1 AI model end-March (92.8%)"

# Crude Oil above $72 end March (~92% YES, resolves 2026-03-31)
# Oil at ~$93, needs 22% drop to fail — very unlikely
place_buy \
    "will-crude-oil-cl-settle-over-72-on-the-final-trading-day-of-march-2026" \
    "2.25" \
    "Crude Oil > \$72 end-March (92%)"

# ── TIER 3: Higher Variance, Higher Reward ─────────────────────────────────

log "-- Tier 3: Higher Reward --"

# Gold above $4,800 end March (~75% YES, resolves 2026-03-31)
# Gold at $5,019 — needs 4.4% DROP to fail; market pricing 25% chance of that
place_buy \
    "will-gold-gc-settle-over-4800-on-the-final-trading-day-of-march-2026" \
    "2.00" \
    "Gold > \$4800 end-March (75%, gold currently \$5019)"

# Bitcoin outperform Gold in March (~84% YES, resolves 2026-03-31)
place_buy \
    "will-bitcoin-outperform-gold-in-march-2026" \
    "2.75" \
    "BTC outperform Gold March 2026 (84%)"

log "=== Phase 1 complete. Total deployed: ~\$15.00 ==="
log "Check positions: $POLYMARKET portfolio positions"
log "Trade log: $LOG_FILE"
