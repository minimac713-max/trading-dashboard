# Trading Bot Integration Guide

Complete setup instructions for automating the Bitcoin trading strategy on 3Commas, TradingView, and other platforms.

---

## Option 1: 3Commas (Recommended for Beginners)

### Why 3Commas?

✓ **Easiest setup** — GUI-based, no code required  
✓ **Dollar-cost averaging** — build positions gradually  
✓ **Backtesting** — test strategy before live  
✓ **Multi-exchange** — supports Kraken, Binance, Coinbase, etc.  
✓ **Mobile app** — monitor and adjust on the go  
✗ Subscription required ($10–50/month)  
✗ Slightly higher fees (bot overhead)

### Step-by-Step Setup

#### 1. Create 3Commas Account

1. Go to [3commas.io](https://3commas.io)
2. Sign up with email
3. Verify email and set strong password
4. Enable 2FA (Settings → Security)

#### 2. Connect Kraken Exchange

1. Log in to **3Commas**
2. Go **Account Settings → API Keys**
3. Click **Connect an Exchange**
4. Select **Kraken**

#### 3. Generate Kraken API Key

1. Log in to **Kraken** (kraken.com)
2. Go **Settings → API**
3. Click **Generate New Key**
4. Set permissions:
   - ✓ Query Funds
   - ✓ Query Open Orders & Trades
   - ✓ Query Closed Orders & Trades
   - ✓ Create & Modify Orders
   - ✗ Cancel/Close Orders (optional for safety)
   - ✗ Access Funding (never needed)

5. **Nonce Window:** 0 (default)
6. **2FA:** Optional but recommended
7. Copy **API Key** and **Private Key**
8. Save in secure location

#### 4. Paste Kraken Credentials into 3Commas

1. Back in **3Commas API Keys**
2. Select **Kraken**
3. Paste **API Key**
4. Paste **Private Key**
5. Click **Connect**
6. Verify connection — should show your balance

#### 5. Create a Bot

1. Go **My Bots → Create New Bot**
2. **Bot name:** "BTC Momentum Bot"
3. **Strategy:** Select **DCA (Dollar Cost Averaging)** or **Long Only**
4. **Exchange:** Kraken
5. **Pair:** BTC/USD

#### 6. Configure Bot Settings

**Entry Configuration:**
- **Base Order:** $50 (your position size)
- **Take Profit:** 100% (double your entry)
- **Stop Loss:** −8% (protection)
- **Signal Source:** Custom Webhook (see below)

**Safety Limits:**
- **Max Active Deals:** 1 (only one trade at a time)
- **Auto-Sell on Red:** Disabled (use stop loss instead)

#### 7. Set Up Momentum Signal Webhook

3Commas can receive signals via **webhook** from TradingView or custom scripts.

**To enable webhook:**

1. In bot settings, find **Strategy Settings**
2. Enable **Webhook for strategy signals**
3. Copy the **webhook URL** (looks like `https://3commas.io/trade_signal/...`)

**Send signal from TradingView alert:**
```
POST to webhook URL with JSON:
{
  "action": "buy",
  "message": "Momentum > 2%"
}
```

#### 8. Test the Bot

1. Go **My Bots → [Your Bot Name]**
2. Click **Backtest** 
3. Set date range: Last 30 days
4. Review results:
   - Should show 5-10 completed trades
   - Win rate 50%+ 
   - P&L trending positive

#### 9. Start Bot (Live)

1. Click **Start Bot**
2. Confirm you have sufficient USD balance
3. Bot is now active — will execute trades on signals

**Monitor:**
- Check daily for active positions
- Review P&L and trade log
- Adjust if win rate drops below 40%

---

## Option 2: TradingView Alerts (Advanced)

### Why TradingView?

✓ **Free plan available** — no ongoing fees  
✓ **Advanced charting** — visualize your strategy  
✓ **Strategy backtester** — built-in testing  
✓ **Flexible webhooks** — send signals anywhere  
✓ **Custom scripts** — write exact entry/exit rules  
✗ Requires coding (Pine Script)  
✗ Manual setup more complex

### Step-by-Step Setup

#### 1. Create TradingView Account

1. Go to [TradingView.com](https://tradingview.com)
2. Sign up (email or social)
3. Create an alert-enabled account (Free or Pro)

#### 2. Write Pine Script Strategy

Go to **Pine Script Editor** and create this strategy:

```pine
//@version=5
strategy("BTC Momentum Strategy", overlay=true)

// Parameters
MOMENTUM_WINDOW = 20
MOMENTUM_THRESHOLD = 0.02
PROFIT_TARGET = 1.00  // 100%
STOP_LOSS = -0.08  // -8%

// Calculate momentum
close_now = close
close_20h_ago = ta.valuewhen(barindex(barindex(ta.barssince(true)) == MOMENTUM_WINDOW), close, 0)
momentum = (close_now - close_20h_ago) / close_20h_ago

// Entry signal
entry_signal = momentum > MOMENTUM_THRESHOLD

// Plot signals
plotshape(entry_signal, title="Buy Signal", style=shape.diamond, location=location.belowbar, color=color.green, size=size.small)

// Strategy execution
if entry_signal
    strategy.entry("Long", strategy.long, alert_message="BUY Signal: Momentum > 2%")

// Exit on profit target
strategy.exit("Take Profit", "Long", profit_percent=100, alert_message="SELL: Profit Target")

// Exit on stop loss
strategy.exit("Stop Loss", "Long", loss_percent=8, alert_message="SELL: Stop Loss")
```

#### 3. Add Alert to Strategy

1. Right-click on chart
2. Select **Add Alert**
3. **Condition:** Momentum > 2%
4. **Actions:**
   - Send notification ✓
   - Webhook URL ← add your bot platform webhook
5. **Webhook message:**
```json
{
  "side": "buy",
  "pair": "BTC/USD",
  "signal": "momentum > 2%"
}
```

#### 4. Backtest the Strategy

1. Open strategy in editor
2. Click **Strategy Tester** (right panel)
3. Set date range
4. Review results:
   - Entry/exit marks on chart
   - Trade log with P&L
   - Win rate statistics

#### 5. Deploy to Live Chart

1. Apply script to 1H BTC/USD chart
2. Green diamond = buy signal
3. Red X = sell signal
4. Monitor in real-time

#### 6. Connect Webhook to Broker

**Option A: TradingView → 3Commas**
- Copy 3Commas webhook URL (from Option 1)
- Paste into TradingView alert webhook field
- Test with a small amount

**Option B: TradingView → Direct API**
- Use Python script to listen for alerts
- Execute Kraken orders via ccxt
- More control, requires coding

---

## Option 3: Custom Python Script (Maximum Control)

### Why This Approach?

✓ **Full control** — execute exactly as written  
✓ **No third-party fees** — just Kraken exchange fees  
✓ **Customizable** — add indicators, adjust parameters  
✗ Requires Python knowledge  
✗ Must keep script running 24/7

### Step-by-Step Setup

#### 1. Install Dependencies

```bash
pip install ccxt python-dotenv requests
```

#### 2. Create Configuration File

Save as `~/.kraken/api.json`:

```json
{
  "apiKey": "your-kraken-api-key",
  "secret": "your-kraken-private-key"
}
```

**Permissions needed in Kraken:**
- Query Funds
- Query Open Orders
- Create & Modify Orders

#### 3. Use Provided Bot Files

Use the bots in your trading folder:

**For live trading:**
```bash
python /Users/macdaddy/.openclaw/workspace/trading/kraken_trader.py
```

**For paper trading (safe):**
```bash
python /Users/macdaddy/.openclaw/workspace/trading/kraken_simulator.py
```

#### 4. Set Up Cron Job (Automatic Runs)

```bash
# Run trading bot every 10 minutes
bash /Users/macdaddy/.openclaw/workspace/trading/cron-setup.sh
```

This script:
- Installs monitoring
- Logs all trades to `logs/trades.log`
- Handles errors gracefully
- Can be paused/resumed without restart

#### 5. Monitor Logs

```bash
tail -f ~/.openclaw/workspace/trading/logs/trades.log
```

---

## Comparison: Which Option?

| Feature | 3Commas | TradingView | Custom Python |
|---------|---------|-------------|----------------|
| **Setup Time** | 20 min | 30 min | 45 min |
| **Cost** | $10-50/mo | Free (alert limits) | $0 |
| **Ease of Use** | Easiest | Medium | Hardest |
| **Customization** | Limited | Good | Unlimited |
| **Mobile Monitoring** | Yes (app) | Yes (app) | No (but can log) |
| **Reliability** | High | High | Depends on uptime |
| **Support** | Excellent | Good | DIY |

**Recommendation for Abel:**
1. **Start with 3Commas** — easiest to set up and monitor
2. **Add TradingView** — better charting and visualization
3. **Keep Python script as backup** — pure automation without middleman

---

## Security Best Practices

### Kraken API Key Safety

1. **Create dedicated key for trading only**
   - Don't use your main Kraken login
   - Restricted to trading permissions (no funds transfer)

2. **Store securely**
   - Use `~/.kraken/api.json` (private directory)
   - Never commit to GitHub
   - Change key monthly if actively trading

3. **Monitor activity**
   - Check Kraken API logs weekly
   - Look for unfamiliar IPs
   - Disable key if suspicious activity

4. **Use IP whitelist** (Kraken Pro)
   - Restrict key to your home IP only
   - Prevents key usage from random locations

### Platform Security

- **3Commas:** Use their 2FA, unique password
- **TradingView:** Enable 2FA, separate strong password
- **Personal machine:** Keep software updated, use antivirus

---

## Troubleshooting

### "Bot not executing trades"

1. Check exchange balance — need at least $50 USD
2. Verify API key permissions in Kraken settings
3. Check 3Commas/TradingView connection status
4. Review bot logs for error messages
5. Test with webhook: `curl -X POST [webhook-url] -d '{"action":"buy"}'`

### "Trades executing but not hitting targets"

1. Check target price calculation in settings
2. Verify order size matches position size
3. Ensure stop loss is actually set
4. Review logs: is price even reaching target?

### "Too many false signals"

1. Increase momentum threshold (2% → 2.5%)
2. Add secondary filter (RSI, volume check)
3. Extend window (20h → 24h or daily)
4. Use TradingView backtest to refine

### "Slippage eating profits"

1. Use limit orders instead of market (smaller slippage)
2. Widen profit target slightly (110% instead of 100%)
3. Check Kraken fees (varies by maker/taker)
4. Consider scaling into position (DCA)

---

## Going Live Checklist

- [ ] Paper trade for 20+ cycles with simulator
- [ ] Win rate above 50%
- [ ] API key created and tested
- [ ] Platform connected and verified
- [ ] Fund account with $50+ (start small)
- [ ] Set up alerting/monitoring
- [ ] Run first trade with $50 position
- [ ] Watch first 3 trades live
- [ ] Log all trades for review
- [ ] Pause/stop plan documented

---

## Support Resources

- **Kraken support:** support.kraken.com
- **3Commas forum:** forum.3commas.io
- **TradingView docs:** pine-script-docs.readthedocs.io
- **CCXT library:** docs.ccxt.com

---

## Next: Cron Job Setup

See `cron-setup.sh` for automating periodic trading runs 24/7 without manual intervention.
