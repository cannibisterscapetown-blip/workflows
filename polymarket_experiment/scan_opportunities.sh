#!/usr/bin/env bash
# Polymarket Opportunity Scanner
# Finds markets with high probability + reasonable resolution time
# Usage: bash scan_opportunities.sh [--days <max_days>] [--min-prob <0.85>]

set -euo pipefail

POLYMARKET="$HOME/.local/bin/polymarket"
MAX_DAYS=30
MIN_PROB=0.85

for arg in "$@"; do
    case "$arg" in
        --days) shift; MAX_DAYS="$1" ;;
        --min-prob) shift; MIN_PROB="$1" ;;
    esac
done

echo "=== Polymarket Opportunity Scanner ==="
echo "Scanning for YES probability >= $MIN_PROB, resolving within $MAX_DAYS days"
echo "Current date: $(date -u '+%Y-%m-%d')"
echo ""

"$POLYMARKET" markets list --active true --closed false --limit 500 -o json 2>/dev/null | python3 - <<PYEOF
import json, sys
from datetime import datetime, timezone

data = json.load(sys.stdin)
now = datetime.now(timezone.utc)
max_days = $MAX_DAYS
min_prob = $MIN_PROB

opportunities = []
for m in data:
    end = m.get('endDate', '')
    if not end or m.get('closed'):
        continue
    try:
        end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
        days_left = (end_dt - now).total_seconds() / 86400
        if days_left <= 0 or days_left > max_days:
            continue
        prices = json.loads(m.get('outcomePrices', '[0,0]'))
        yes_price = float(prices[0]) if prices else 0
        if yes_price < min_prob:
            continue
        roi = (1.0 - yes_price) / yes_price * 100
        ev = yes_price * roi
        vol = float(m.get('volume', 0) or 0)
        liq = float(m.get('liquidity', 0) or 0)
        opportunities.append({
            'days': days_left,
            'yes': yes_price,
            'roi': roi,
            'ev': ev,
            'vol': vol,
            'liq': liq,
            'q': m.get('question', '')[:75],
            'slug': m.get('slug', ''),
        })
    except:
        continue

# Sort by EV descending (probability × roi)
opportunities.sort(key=lambda x: -x['ev'])

print(f"{'Days':>5} {'YES':>6} {'ROI':>7} {'Liquidity':>12}  Question")
print("-" * 110)
for o in opportunities[:30]:
    print(f"{o['days']:>5.1f} {o['yes']:>6.1%} {o['roi']:>6.1f}%  \${o['liq']:>10,.0f}  {o['q']}")

print()
print(f"Total opportunities found: {len(opportunities)}")
PYEOF
