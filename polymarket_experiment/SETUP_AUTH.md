# How to Connect Your Polymarket Account

## Option 1 — Easiest: Magic Link / Google Login (Recommended for beginners)

Polymarket creates an embedded proxy wallet when you sign in with Google/email.

### Steps:
1. Go to **https://polymarket.com** → click **Sign In**
2. Sign in with **Google** (or email magic link)
3. Polymarket creates a wallet automatically — no MetaMask needed
4. Deposit $15 USDC:
   - Click **Deposit** in the app
   - Bridge from your bank/exchange via the built-in bridge (supports Visa/Mastercard, Coinbase, etc.)
   - Or send USDC on Polygon directly if you have it

### Export your private key:
1. In Polymarket → **Settings** (or Account) → **Export Private Key**
2. Copy the hex key (starts with `0x...`)

### Configure polymarket-cli:
```bash
export PATH="$HOME/.local/bin:$PATH"

# Import your exported private key
polymarket wallet import

# When prompted, paste the 0x... key from Polymarket
# Signature type for Magic Link / Google login = "proxy" (default)

# Verify wallet loaded
polymarket wallet show

# Check balance (should show your $15 USDC)
polymarket portfolio balance
```

---

## Option 2 — MetaMask / Hardware Wallet (EOA)

If you prefer to use your own wallet (MetaMask, Ledger, etc.):

1. Connect MetaMask to Polymarket at polymarket.com
2. Approve the CLOB contract (one-time gas-free approval on Polygon)
3. Export your MetaMask private key (Settings → Security → Export Private Key)
4. Configure cli:

```bash
polymarket wallet import
# paste your MetaMask private key

# Set signature type to EOA:
polymarket config set signature-type eoa
```

---

## Option 3 — Environment Variable (Most secure for scripting)

Don't save the key to disk — pass it at runtime:

```bash
POLYMARKET_PRIVATE_KEY=0x<your_key> \
POLYMARKET_SIGNATURE_TYPE=proxy \
polymarket portfolio balance
```

Or add to a `.env` file (never commit this):
```bash
# .env  (add to .gitignore)
POLYMARKET_PRIVATE_KEY=0x...
POLYMARKET_SIGNATURE_TYPE=proxy
```

Then:
```bash
source .env && polymarket portfolio balance
```

---

## Verify Everything Works

```bash
export PATH="$HOME/.local/bin:$PATH"

# 1. Check wallet address
polymarket wallet show

# 2. Check USDC balance
polymarket portfolio balance

# 3. Dry-run a trade (no real order)
bash polymarket_experiment/trade_executor.sh --dry-run
```

---

## Security Notes
- Your private key = full access to your funds. Never share it.
- For this $15 experiment, the risk is bounded — but treat the key carefully.
- The polymarket-cli stores keys in `~/.config/polymarket/config.json` (permissions: 600)
- You can always revoke CLOB approvals from polymarket.com → Settings → Revoke
