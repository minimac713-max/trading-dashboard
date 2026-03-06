# Setup Checklist - Bitcoin Trading Bot

Complete checklist for deploying the trading bot from zero to live trading.

---

## Pre-Flight Check (Before You Start)

- [ ] You have a Kraken account (kraken.com)
- [ ] Kraken account is fully verified (ID verification complete)
- [ ] You have at least $100 available in Kraken (for live trading)
- [ ] You have Python 3 installed (`python3 --version`)
- [ ] You're comfortable with command line / terminal
- [ ] You understand the strategy (read TRADING_STRATEGY.md first)

---

## Part 1: Get Kraken API Credentials

### Step 1.1: Log in to Kraken

1. Go to https://www.kraken.com
2. Sign in with your username/password
3. Go to **Settings** (top right)

### Step 1.2: Create API Key

1. Click **API** in left menu
2. Click **Generate New Key**
3. **Key name:** `Trading Bot` (or any name)
4. **Nonce window:** 0 (default)

### Step 1.3: Set Permissions

Under **Permissions**, check ONLY:
- [ ] ✓ Query Funds
- [ ] ✓ Query Open Orders & Trades
- [ ] ✓ Query Closed Orders & Trades
- [ ] ✓ Create & Modify Orders
- [ ] ✗ All others (unchecked)

**Important:** Do NOT enable "Access Funding" or other permissions.

### Step 1.4: Copy Credentials

1. Click **Generate Key**
2. You'll see:
   - **API Key** (long string starting with something)
   - **Private Key** (very long string)
3. **Copy both** — you'll need them next

### Step 1.5: Store Credentials Securely

Open terminal and run:

```bash
mkdir -p ~/.kraken
```

Then create file with:

```bash
cat > ~/.kraken/api.json << 'EOF'
{
  "apiKey": "PASTE_YOUR_API_KEY_HERE",
  "secret": "PASTE_YOUR_PRIVATE_KEY_HERE"
}
EOF
```

**Replace:**
- `PASTE_YOUR_API_KEY_HERE` with your actual API Key
- `PASTE_YOUR_PRIVATE_KEY_HERE` with your actual Private Key

Then protect the file:

```bash
chmod 600 ~/.kraken/api.json
```

**Verify it worked:**

```bash
cat ~/.kraken/api.json
```

Should show your credentials in JSON format.

---

## Part 2: Install Python Dependencies

### Step 2.1: Check Python

```bash
python3 --version
```

Should show version 3.7 or higher.

If not installed, use Homebrew:

```bash
brew install python3
```

### Step 2.2: Install Libraries

```bash
pip3 install ccxt python-dotenv requests
```

### Step 2.3: Verify Installation

```bash
python3 -c "import ccxt; print(ccxt.__version__)"
```

Should print a version number like `4.0.150`.

---

## Part 3: Test Paper Trading

### Step 3.1: Run Simulator

```bash
cd /Users/macdaddy/.openclaw/workspace/trading
python3 kraken_simulator.py
```

The script will:
1. Fetch live Bitcoin price data
2. Run 10 simulated trading cycles
3. Show statistics at the end

### Step 3.2: Check Results

Look for output like:

```
SIMULATION STATISTICS
======================================================================
Starting Balance: $1000.00
Current Balance: $1096.50
Total P&L: +$96.50 (9.65%)
Completed Trades: 3
Wins: 2, Losses: 1
Win Rate: 66.7%
```

- [ ] Simulator runs without errors
- [ ] It completed 3+ trades
- [ ] Total P&L is positive (good sign)

### Step 3.3: Review Logs

```bash
tail -50 /Users/macdaddy/.openclaw/workspace/trading/logs/simulator.log
```

You should see entries like:

```
[2024-03-06 15:42:15] Entry signal: Uptrend detected (momentum: 2.35%)
[2024-03-06 15:42:16] BUY SIMULATED: 0.00111 BTC @ $45,100.00
[2024-03-06 15:45:32] PROFIT TARGET HIT: $90,200.00
[2024-03-06 15:45:33] SELL SIMULATED: $90,200.00 - P&L: +$50.00 (100.00%)
```

---

## Part 4: Test Production Bot (Dry Run)

### Step 4.1: Verify API Connection

Create a test script to verify API credentials work:

```bash
cd /Users/macdaddy/.openclaw/workspace/trading

python3 << 'EOF'
import ccxt
import json

with open(os.path.expanduser('~/.kraken/api.json')) as f:
    creds = json.load(f)

exchange = ccxt.kraken({
    'apiKey': creds['apiKey'],
    'secret': creds['secret'],
    'enableRateLimit': True,
})

# Test: Fetch balance
balance = exchange.fetch_balance()
print(f"USD Balance: ${balance['free'].get('USD', 0):.2f}")
print(f"BTC Balance: {balance['free'].get('BTC', 0):.8f}")
print("✓ API connection successful!")
EOF
```

- [ ] Shows your USD balance correctly
- [ ] Shows your BTC balance correctly
- [ ] No errors or authentication issues

### Step 4.2: Run Single Production Cycle

Now run the actual bot (it will check signals but won't trade without $50+ in USD):

```bash
python3 kraken_trader.py
```

Output should show:

```
======================================================================
Starting trading cycle
======================================================================
USD Balance: $1234.56
Entry signal: Uptrend detected (momentum: 2.45%)
SIGNAL TRIGGERED - Current price: $45,120.00
Executing BUY: 0.00111 BTC @ $45,120.00
Order executed: [order-id]
Position monitoring: Entry=45120.00, Target=90240.00, Stop=41510.40
```

- [ ] Sees the USD balance correctly
- [ ] Checks entry signal
- [ ] No API errors

**Don't worry if no signal triggers** — momentum might not meet 2% threshold. That's normal.

---

## Part 5: Fund Your Trading Account

### Step 5.1: Decide Amount

- **Conservative start:** $100 (2 trades at $50 each)
- **Moderate start:** $250 (5 trades at $50 each)
- **Never start with more than you can afford to lose**

### Step 5.2: Deposit to Kraken

1. Log in to Kraken
2. Click **Funding** → **Deposit**
3. Select USD (or your currency)
4. Follow deposit instructions
5. Wait for funds to arrive (usually 1-3 days)

### Step 5.3: Check Balance in Kraken

```
Kraken → Balances → USD
```

Should show your deposit amount.

---

## Part 6: First Live Trade (Manual)

### Step 6.1: Run Bot Manually

Once you have $50+ USD in Kraken:

```bash
python3 /Users/macdaddy/.openclaw/workspace/trading/kraken_trader.py
```

The bot will:
1. Check your balance
2. Check if momentum signal is present
3. **IF signal is triggered:** Execute a real $50 buy
4. Monitor the position
5. Exit on profit target or stop loss

### Step 6.2: Watch the Trade

Once the trade executes, you'll see:

```
Executing BUY: 0.00111 BTC @ $45,120.00
Order executed: order-123456
Position monitoring: Entry=45120.00, Target=90240.00, Stop=41510.40
```

The bot will now monitor until it hits profit target or stop loss.

### Step 6.3: Check Kraken UI

Go to Kraken and verify:
- [ ] Under **Balances**, you see BTC added
- [ ] Under **Orders**, you see the buy order filled
- [ ] Your average entry price matches the bot's entry

---

## Part 7: Automate with Cron (24/7 Trading)

### Step 7.1: Choose Frequency

Edit `/Users/macdaddy/.openclaw/workspace/trading/cron-setup.sh`

Find the line:
```bash
FREQUENCY="10-minutes"  # Options: "10-minutes", "hourly", "daily"
```

Change to your preference:
- `"10-minutes"` — Run every 10 minutes (active trading, recommended)
- `"hourly"` — Run once per hour
- `"daily"` — Run once per day at 9:00 AM

### Step 7.2: Install Cron Job

```bash
bash /Users/macdaddy/.openclaw/workspace/trading/cron-setup.sh --install
```

Output should show:
```
✓ Cron jobs installed!

Monitor logs:
  tail -f /Users/macdaddy/.openclaw/workspace/trading/logs/cron.log
```

- [ ] Cron job installed successfully
- [ ] No permission errors

### Step 7.3: Verify Installation

```bash
bash /Users/macdaddy/.openclaw/workspace/trading/cron-setup.sh --status
```

Should show:
```
*/10 * * * * /Users/macdaddy/.openclaw/workspace/trading/run_trader.sh
```

---

## Part 8: Monitor Live Trading

### Step 8.1: Watch Logs in Real-Time

```bash
tail -f /Users/macdaddy/.openclaw/workspace/trading/logs/trades.log
```

You'll see entries like:

```
[2024-03-06 15:42:15 UTC] USD Balance: $150.00
[2024-03-06 15:42:16 UTC] Entry signal: Uptrend (momentum: 2.3%)
[2024-03-06 15:42:17 UTC] SIGNAL TRIGGERED - buying
[2024-03-06 15:42:18 UTC] Executing BUY: 0.00111 BTC @ $45,100.00
[2024-03-06 15:45:22 UTC] Position open: $89,500.00 (P&L: +97.7%)
[2024-03-06 15:47:33 UTC] PROFIT TARGET HIT: $90,200.00
[2024-03-06 15:47:34 UTC] Exit successful - P&L: +$50.00 (100.0%)
```

### Step 8.2: Daily Checklist

Every day, run:

```bash
bash /Users/macdaddy/.openclaw/workspace/trading/cron-setup.sh --logs
```

Review:
- [ ] Any trades executed?
- [ ] Any errors in error log?
- [ ] Win rate trending positive?
- [ ] P&L increasing?

### Step 8.3: Weekly Review

Every Friday, run:

```bash
grep "Exit successful\|Stop Loss\|Profit Target" /Users/macdaddy/.openclaw/workspace/trading/logs/trades.log | tail -10
```

Track:
- [ ] Total number of trades
- [ ] Number of wins vs losses
- [ ] Average P&L per trade
- [ ] Win rate percentage

---

## Part 9: Emergency Controls

### Pause Trading

```bash
bash /Users/macdaddy/.openclaw/workspace/trading/cron-setup.sh --remove
```

This **stops all automated trading immediately**. Cron jobs are disabled.

### Resume Trading

```bash
bash /Users/macdaddy/.openclaw/workspace/trading/cron-setup.sh --install
```

This **re-enables cron jobs**. Bot will resume trading.

### Check What's Running

```bash
crontab -l
```

Shows your active cron jobs.

---

## Part 10: Scaling (After Consistent Wins)

### When to Scale

Only after:
- [ ] 20+ trades completed
- [ ] Win rate 50%+
- [ ] Positive cumulative P&L
- [ ] At least 2 weeks of live data
- [ ] Consistent daily monitoring

### How to Scale

1. Edit `kraken_trader.py`
2. Find line: `POSITION_SIZE = 50`
3. Change to: `POSITION_SIZE = 100` (or higher)
4. Save file
5. Restart cron: `bash cron-setup.sh --remove && bash cron-setup.sh --install`

**Suggested scaling:**
- Week 1-2: $50 per trade
- Week 3-4: $100 per trade (if win rate > 60%)
- Week 5+: $250 per trade (if cumulative P&L > $500)

---

## Troubleshooting Checklist

### Bot not executing trades?

- [ ] Check USD balance: `curl https://api.kraken.com/0/public/Ticker?pair=BTCUSD`
- [ ] Verify API key has "Create & Modify Orders" permission
- [ ] Check momentum signal: `tail logs/trades.log`
- [ ] Look for errors: `tail logs/errors.log`

### Getting permission errors?

- [ ] Make sure file is: `chmod 600 ~/.kraken/api.json`
- [ ] Make sure API key has correct permissions in Kraken settings
- [ ] Try regenerating key in Kraken

### Cron job not running?

- [ ] Verify it's installed: `crontab -l`
- [ ] Check logs: `tail /Users/macdaddy/.openclaw/workspace/trading/logs/cron.log`
- [ ] Make sure script is executable: `ls -la cron-setup.sh`

### Losing money consistently?

- [ ] Review TRADING_STRATEGY.md again
- [ ] Run simulator to verify logic
- [ ] Check win rate — should be 50%+
- [ ] Pause trading and pause: `bash cron-setup.sh --remove`
- [ ] Re-test in paper trading before resuming

---

## Final Verification

Before going live, confirm:

- [ ] Part 1: Kraken API credentials stored in `~/.kraken/api.json`
- [ ] Part 2: Python libraries installed (`pip3 install ccxt`)
- [ ] Part 3: Simulator runs successfully with positive P&L
- [ ] Part 4: Production bot connects to API without errors
- [ ] Part 5: Kraken account has $50+ USD funding
- [ ] Part 6: First manual trade executes correctly
- [ ] Part 7: Cron job installed (`cron-setup.sh --install`)
- [ ] Part 8: Logs are being written to `/logs/` directory
- [ ] Part 9: You know how to pause trading (`cron-setup.sh --remove`)
- [ ] Part 10: You understand when to scale position size

---

## You're Ready!

Once all items are checked, your bot is:
- ✓ Configured
- ✓ Tested
- ✓ Funded
- ✓ Automated
- ✓ Monitored

It will now trade 24/7 according to the momentum strategy.

**Monitor daily. Pause if win rate drops below 40%. Scale gradually.**

---

## Support Resources

| Need | Resource |
|------|----------|
| Strategy questions | `TRADING_STRATEGY.md` |
| Platform setup | `TRADING_INTEGRATIONS.md` |
| Code reference | `kraken_trader.py` (comments) |
| Setup help | This file |
| Kraken help | support.kraken.com |
| CCXT docs | docs.ccxt.com |

---

**Start here. Follow each step. You'll be live in an afternoon.**
