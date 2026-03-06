# Quick Reference - Common Commands

Fast lookup for frequently used commands.

---

## Setup Commands

### Create API Credentials File

```bash
mkdir -p ~/.kraken
cat > ~/.kraken/api.json << 'EOF'
{
  "apiKey": "YOUR_API_KEY",
  "secret": "YOUR_PRIVATE_KEY"
}
EOF
chmod 600 ~/.kraken/api.json
```

### Install Python Libraries

```bash
pip3 install ccxt python-dotenv requests
```

### Verify Installation

```bash
python3 -c "import ccxt; print('✓ CCXT installed')"
```

---

## Testing Commands

### Run Paper Trading Simulator

```bash
python3 /Users/macdaddy/.openclaw/workspace/trading/kraken_simulator.py
```

### Run Live Bot (Manual)

```bash
python3 /Users/macdaddy/.openclaw/workspace/trading/kraken_trader.py
```

### Test API Connection

```bash
python3 << 'EOF'
import ccxt
import json
import os

with open(os.path.expanduser('~/.kraken/api.json')) as f:
    creds = json.load(f)

exchange = ccxt.kraken({
    'apiKey': creds['apiKey'],
    'secret': creds['secret'],
    'enableRateLimit': True,
})

balance = exchange.fetch_balance()
print(f"USD: ${balance['free'].get('USD', 0):.2f}")
print(f"BTC: {balance['free'].get('BTC', 0):.8f}")
EOF
```

---

## Automation Commands

### Install Cron Jobs (Every 10 Minutes)

```bash
bash /Users/macdaddy/.openclaw/workspace/trading/cron-setup.sh --install
```

### Check Cron Jobs

```bash
bash /Users/macdaddy/.openclaw/workspace/trading/cron-setup.sh --status
```

### View Cron/Error Logs

```bash
bash /Users/macdaddy/.openclaw/workspace/trading/cron-setup.sh --logs
```

### Stop Automation

```bash
bash /Users/macdaddy/.openclaw/workspace/trading/cron-setup.sh --remove
```

### Manual Cron Check

```bash
crontab -l  # View all cron jobs
```

---

## Monitoring Commands

### Stream Trade Logs (Real-Time)

```bash
tail -f /Users/macdaddy/.openclaw/workspace/trading/logs/trades.log
```

### Stream Error Logs (Real-Time)

```bash
tail -f /Users/macdaddy/.openclaw/workspace/trading/logs/errors.log
```

### Stream Cron Logs (Real-Time)

```bash
tail -f /Users/macdaddy/.openclaw/workspace/trading/logs/cron.log
```

### View Last 50 Trades

```bash
tail -50 /Users/macdaddy/.openclaw/workspace/trading/logs/trades.log
```

### Find All Completed Trades

```bash
grep "Exit successful" /Users/macdaddy/.openclaw/workspace/trading/logs/trades.log
```

### Count Wins vs Losses

```bash
echo "Wins:"
grep "Profit Target" /Users/macdaddy/.openclaw/workspace/trading/logs/trades.log | wc -l
echo "Losses:"
grep "Stop Loss" /Users/macdaddy/.openclaw/workspace/trading/logs/trades.log | wc -l
```

### View Total P&L

```bash
grep "P&L:" /Users/macdaddy/.openclaw/workspace/trading/logs/trades.log | tail -20
```

---

## File Reference

| File | Purpose |
|------|---------|
| `kraken_trader.py` | Production bot (real trades) |
| `kraken_simulator.py` | Paper trading (no risk) |
| `TRADING_STRATEGY.md` | Strategy guide & rules |
| `TRADING_INTEGRATIONS.md` | Platform setup (3Commas, TradingView, etc) |
| `cron-setup.sh` | Automation scheduler |
| `SETUP_CHECKLIST.md` | Step-by-step deployment guide |
| `README.md` | Overview and overview |
| `logs/trades.log` | All executed trades |
| `logs/simulator.log` | Simulation results |
| `logs/cron.log` | Automation logs |
| `logs/errors.log` | Error messages |

---

## Directory Shortcuts

```bash
# Go to trading directory
cd /Users/macdaddy/.openclaw/workspace/trading

# Go to logs directory
cd /Users/macdaddy/.openclaw/workspace/trading/logs

# View logs directory contents
ls -la /Users/macdaddy/.openclaw/workspace/trading/logs
```

---

## Common Scenarios

### "I want to test the strategy before going live"

```bash
python3 kraken_simulator.py
```

### "I want to run a single manual trade"

```bash
python3 kraken_trader.py
```

### "I want to start 24/7 automated trading"

```bash
bash cron-setup.sh --install
```

### "I want to stop all trading immediately"

```bash
bash cron-setup.sh --remove
```

### "I want to check if a trade happened today"

```bash
grep "$(date +'%Y-%m-%d')" /Users/macdaddy/.openclaw/workspace/trading/logs/trades.log
```

### "I want to see how much money I've made"

```bash
grep "Exit successful" /Users/macdaddy/.openclaw/workspace/trading/logs/trades.log | tail -10
```

### "I want to check my current balance on Kraken"

```bash
python3 << 'EOF'
import ccxt
import json
import os

with open(os.path.expanduser('~/.kraken/api.json')) as f:
    creds = json.load(f)

exchange = ccxt.kraken({
    'apiKey': creds['apiKey'],
    'secret': creds['secret'],
    'enableRateLimit': True,
})

balance = exchange.fetch_balance()
total_usd = balance['free'].get('USD', 0)
total_btc = balance['free'].get('BTC', 0)
ticker = exchange.fetch_ticker('BTC/USD')
btc_value = total_btc * ticker['last']

print(f"USD: ${total_usd:.2f}")
print(f"BTC: {total_btc:.8f} (${btc_value:.2f})")
print(f"Total: ${total_usd + btc_value:.2f}")
EOF
```

### "I want to increase position size from $50 to $100"

1. Open `kraken_trader.py`
2. Find: `POSITION_SIZE = 50`
3. Change to: `POSITION_SIZE = 100`
4. Save file
5. Restart cron: `bash cron-setup.sh --remove && bash cron-setup.sh --install`

### "I want to change profit target from 100% to 150%"

1. Open `kraken_trader.py`
2. Find: `PROFIT_TARGET = 1.00`
3. Change to: `PROFIT_TARGET = 1.50`
4. Save file
5. Restart cron

### "I want to adjust stop loss from -8% to -10%"

1. Open `kraken_trader.py`
2. Find: `STOP_LOSS_PERCENT = -0.08`
3. Change to: `STOP_LOSS_PERCENT = -0.10`
4. Save file
5. Restart cron

---

## Emergency Commands

### Kill Any Stuck Trading Process

```bash
pkill -f kraken_trader
```

### Clear Old Logs (Keep Recent)

```bash
# Keep last 1000 lines of trades.log
tail -1000 /Users/macdaddy/.openclaw/workspace/trading/logs/trades.log > /tmp/trades_backup.log
cp /tmp/trades_backup.log /Users/macdaddy/.openclaw/workspace/trading/logs/trades.log
```

### Backup All Logs

```bash
cp -r /Users/macdaddy/.openclaw/workspace/trading/logs \
      /Users/macdaddy/.openclaw/workspace/trading/logs.backup-$(date +%Y%m%d)
```

---

## Debugging

### Enable Verbose Logging (Temporary)

Edit `kraken_trader.py`, find:
```python
logging.basicConfig(level=logging.INFO, ...)
```

Change to:
```python
logging.basicConfig(level=logging.DEBUG, ...)
```

Then run bot:
```bash
python3 kraken_trader.py
```

### Print Current BTC Price

```bash
python3 << 'EOF'
import ccxt
exchange = ccxt.kraken()
ticker = exchange.fetch_ticker('BTC/USD')
print(f"BTC/USD: ${ticker['last']:.2f}")
EOF
```

### Get Last 10 Prices (1H)

```bash
python3 << 'EOF'
import ccxt
exchange = ccxt.kraken()
ohlcv = exchange.fetch_ohlcv('BTC/USD', '1h', limit=10)
for candle in ohlcv:
    ts, o, h, l, c, v = candle
    from datetime import datetime
    time = datetime.utcfromtimestamp(ts/1000).strftime('%Y-%m-%d %H:%M')
    print(f"{time} - O:{o:.0f} H:{h:.0f} L:{l:.0f} C:{c:.0f}")
EOF
```

---

## Performance Review

### Win Rate (Last 20 Trades)

```bash
TOTAL=$(grep "Exit successful" /Users/macdaddy/.openclaw/workspace/trading/logs/trades.log | tail -20 | wc -l)
WINS=$(grep "profit target" /Users/macdaddy/.openclaw/workspace/trading/logs/trades.log | tail -20 | wc -l)
echo "Wins: $WINS / $TOTAL ($(( WINS * 100 / TOTAL ))%)"
```

### Total P&L (Last 50 Trades)

```bash
grep "P&L: \+" /Users/macdaddy/.openclaw/workspace/trading/logs/trades.log | tail -50 | grep -oE '\$[0-9.]+' | awk '{sum+=$1} END {print "Total: $" sum}'
```

### Average Trade Duration

```bash
grep "Trade cycle complete" /Users/macdaddy/.openclaw/workspace/trading/logs/trades.log | tail -20
```

---

## Notes

- All commands assume you're in the correct timezone (America/Chicago)
- Log files are timestamped in UTC, add 6 hours for Chicago time
- Backups are important — copy `logs/` directory weekly
- Never share `~/.kraken/api.json` with anyone

---

**Bookmark this page for quick reference!**
