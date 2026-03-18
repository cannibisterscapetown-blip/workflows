#!/bin/bash
# setup_openclaw_ec2.sh — Install and configure OpenClaw on an EC2 instance
# Requires: Ubuntu 22.04/24.04 LTS, t3.large or better (4+ GB RAM recommended)
# Usage: bash setup_openclaw_ec2.sh

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()  { echo -e "${GREEN}[+]${NC} $*"; }
warn() { echo -e "${YELLOW}[!]${NC} $*"; }
err()  { echo -e "${RED}[✗]${NC} $*"; exit 1; }

# ── 1. System check ──────────────────────────────────────────────────────────
log "Checking system requirements..."

TOTAL_RAM_MB=$(awk '/MemTotal/ { printf "%d", $2/1024 }' /proc/meminfo)
if [ "$TOTAL_RAM_MB" -lt 3500 ]; then
    warn "Only ${TOTAL_RAM_MB} MB RAM detected. OpenClaw recommends 4+ GB (t3.large or higher)."
    warn "Installation may fail on t2.micro / t3.micro instances."
    read -rp "Continue anyway? [y/N] " confirm
    [[ "$confirm" =~ ^[Yy]$ ]] || exit 1
else
    log "RAM: ${TOTAL_RAM_MB} MB — OK"
fi

# ── 2. System dependencies ───────────────────────────────────────────────────
log "Updating system packages..."
sudo apt-get update -y -qq
sudo apt-get install -y -qq curl git unzip build-essential

# ── 3. Node.js >= 22 ─────────────────────────────────────────────────────────
REQUIRED_NODE=22
if command -v node &>/dev/null; then
    NODE_VER=$(node -e "process.stdout.write(process.version.slice(1).split('.')[0])")
    if [ "$NODE_VER" -ge "$REQUIRED_NODE" ]; then
        log "Node.js v$(node --version) already installed — OK"
    else
        warn "Node.js v$(node --version) found but OpenClaw requires >= v${REQUIRED_NODE}. Upgrading..."
        INSTALL_NODE=1
    fi
else
    INSTALL_NODE=1
fi

if [ "${INSTALL_NODE:-0}" = "1" ]; then
    log "Installing Node.js ${REQUIRED_NODE}.x via NodeSource..."
    curl -fsSL "https://deb.nodesource.com/setup_${REQUIRED_NODE}.x" | sudo -E bash - -qq
    sudo apt-get install -y -qq nodejs
    log "Node.js $(node --version) installed"
fi

# ── 4. Install OpenClaw ───────────────────────────────────────────────────────
log "Installing OpenClaw..."
curl -fsSL https://openclaw.ai/install.sh | bash

# Reload PATH so `openclaw` is available in this session
export PATH="$HOME/.openclaw/bin:$PATH"

if ! command -v openclaw &>/dev/null; then
    err "'openclaw' command not found after install. Check https://docs.openclaw.ai/install for troubleshooting."
fi
log "OpenClaw $(openclaw --version 2>/dev/null || echo '(version unknown)') installed"

# ── 5. Install as a system daemon ────────────────────────────────────────────
log "Setting up OpenClaw daemon (runs in background on boot)..."
openclaw onboard --install-daemon

# ── 6. Verify installation ────────────────────────────────────────────────────
log "Running openclaw doctor..."
openclaw doctor || warn "'openclaw doctor' reported issues — review output above."

# ── 7. Security reminder ──────────────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
warn "SECURITY CHECKLIST — please review before using OpenClaw:"
echo "  1. Keep port 22 (SSH) restricted to YOUR IP in the EC2 security group."
echo "  2. Do NOT expose the OpenClaw Gateway port publicly — use an SSH tunnel:"
echo "       ssh -L 3000:localhost:3000 ubuntu@<your-ec2-ip>"
echo "  3. Optionally add Tailscale for zero-config secure access:"
echo "       curl -fsSL https://tailscale.com/install.sh | sh && tailscale up"
echo "  4. Use a dedicated phone number / messaging account with OpenClaw."
echo "  5. Review installed skills carefully — malicious skills can exfiltrate data."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ── 8. Next steps ─────────────────────────────────────────────────────────────
log "Installation complete! Next steps:"
echo "  • Add your AI model API key:"
echo "      openclaw config set api_key <YOUR_CLAUDE_OR_OPENAI_KEY>"
echo "  • Check daemon status:"
echo "      openclaw status"
echo "  • Open the dashboard (via SSH tunnel → http://localhost:3000):"
echo "      openclaw dashboard"
echo "  • Full docs: https://docs.openclaw.ai"
echo ""
log "Done."
