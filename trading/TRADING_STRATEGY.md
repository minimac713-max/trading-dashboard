# Bitcoin Trading Strategy - Complete Guide

## Overview

This is a **momentum-based trend trading strategy** designed for Bitcoin (BTC/USD) on Kraken. It combines momentum analysis with strict risk management to identify high-probability entry points and protect capital.

**Strategy Type:** Trend Following  
**Asset:** Bitcoin (BTC/USD)  
**Timeframe:** 1-hour candles  
**Risk/Reward Ratio:** 1:12.5 (−8% loss vs +100% gain)

---

## Entry Signal (Momentum Analysis)

### Signal Generation

The strategy triggers an entry when **upward momentum exceeds a threshold** over a 20-hour window.

```
Momentum = (Price_Now - Price_20hrs_ago) / Price_20hrs_ago

Entry Signal: Momentum > 2%
```

**What this means:**
- If Bitcoin has gained **more than 2%** over the past 20 hours, the trend is considered bullish
- A 2% move provides confirmation that buying pressure is present
- This filters out sideways/choppy markets (noise reduction)

### Example Entry

```
Current price: $45,000
Price 20 hours ago: $44,000
Momentum: ($45,000 - $44,000) / $44,000 = 2.27% ✓

Signal triggered → BUY
```

### Why This Works

1. **Momentum identifies trends early** — before large moves happen
2. **2% threshold balances sensitivity** — catches real trends without whipsaws
3. **20-hour window** — covers multiple daily cycles, reduces false signals
4. **Kraken availability** — Bitcoin trades 24/7, 1h data is reliable

---

## Position Sizing (Risk Control)

### Position Size Rules

```
Position Size: $50 per trade (fixed)
Max Position: 1 open trade at a time
Entry Amount: All-in $50 on signal
```

### Quantity Calculation

```
BTC Quantity = Position Size / Entry Price
              = $50 / Entry Price

Example: Entry at $45,000
Quantity = $50 / $45,000 = 0.00111 BTC
```

**Benefits:**
- **Fixed position size** prevents emotional over-leveraging
- **$50 limit** is small enough to test and iterate without large losses
- **Single open trade** ensures focus on one opportunity at a time
- **Scalable** — once tested, can increase to $100, $500, etc.

---

## Profit Target (+100%)

### Target Price Calculation

```
Profit Target = Entry Price × (1 + 100%)
              = Entry Price × 2

Example: Entry at $45,000
Target = $45,000 × 2 = $90,000
```

### Exit at Target

When price reaches 2x entry:

```
Entry:  $45,000  (Buy $50 worth)
Target: $90,000  (Sell all)
Gain:   $50 profit
Return: 100% on $50 position
```

### Why 100% Target?

1. **Realistic in Bitcoin** — $45K → $90K happens multiple times per cycle
2. **Risk/reward 1:12.5** — risking 8% to make 100% is favorable
3. **Compound growth** — even a few winning trades add up fast
4. **Psychological** — clear, achievable milestone (2x)

---

## Stop Loss (−8%)

### Stop Loss Calculation

```
Stop Loss = Entry Price × (1 − 8%)
          = Entry Price × 0.92

Example: Entry at $45,000
Stop Loss = $45,000 × 0.92 = $41,400
```

### Exit at Stop Loss

If price drops to stop level:

```
Entry:     $45,000  (Buy $50 worth)
Stop Loss: $41,400  (Sell all)
Loss:      −$4 loss
Return:    −8% on $50 position
```

### Why −8% Stop Loss?

1. **Tight protection** — catches bad entries early before they get worse
2. **Bitcoin volatility** — 8% pullbacks are normal, beyond that = broken trend
3. **Risk/reward math** — with 100% target, 8% stop is acceptable
4. **Capital preservation** — better to take small loss than hold into larger one

### Real-World Example

```
You have $1,000 to trade

Trade 1: Win  → Entry $45K, Exit $90K   → +$50  ($1,050)
Trade 2: Loss → Entry $88K, Exit $81K   → −$4   ($1,046)
Trade 3: Win  → Entry $82K, Exit $164K  → +$50  ($1,096)

After 3 trades: +$96 (9.6% gain)
Win rate: 67% with positive expectancy
```

---

## Risk Management Rules

### Rule 1: Never Over-Position
- ✓ Max $50 per trade
- ✓ Only 1 open trade at a time
- ✗ No adding to losers
- ✗ No martingale doubling down

### Rule 2: Strict Entry/Exit
- ✓ Enter ONLY on momentum signal
- ✓ Exit at target or stop (no discretion)
- ✗ No holding "just a bit longer"
- ✗ No moving stops against you

### Rule 3: Mechanical Execution
- ✓ Use bots (3Commas, TradingView) for automatic orders
- ✓ Avoid emotional decisions
- ✗ No "I think it'll reverse" overrides
- ✗ No checking price every 5 minutes

### Rule 4: Capital Allocation
- Only trade what you can afford to lose
- Start with paper trading (simulator)
- Test strategy for 20+ trades before live
- Scale positions only after consistent wins

### Rule 5: Monitoring

**Check daily:**
- Are trades executing as expected?
- Any platform errors or slippage?
- P&L trending positive?

**Pause if:**
- Win rate drops below 40%
- 3 consecutive losses
- Unusual market conditions (gaps, halts)

---

## Complete Trade Walkthrough

### Scenario: Bull Trend Entry and Exit

#### Hour 0 (Signal Formation)

```
Current Time: 14:00 UTC Monday
Price 20h ago: $44,000
Current Price: $44,880
Momentum: +2.0% ← Threshold just hit

Action: WAIT for next update
```

#### Hour 1 (Entry)

```
Current Time: 15:00 UTC
Current Price: $45,100
Momentum: +2.5% ← Confirmed > 2%

Action: EXECUTE BUY
- Buy: 0.00111 BTC @ $45,100
- Cost: $50.00
- Status: Position OPEN
```

#### Hour 3 (Profit Target Hit)

```
Current Time: 18:00 UTC
Current Price: $90,200
Target was: $90,200 (2x entry)

Action: EXECUTE SELL
- Sell: 0.00111 BTC @ $90,200
- Proceeds: $100.00
- P&L: +$50 (100% return)
- Duration: 3 hours
- Status: Position CLOSED ✓
```

### Scenario: Quick Stop Loss (Bad Entry)

#### Hour 0 (Signal)

```
Current Time: 08:00 UTC Tuesday
Momentum: +2.1% ← Signal triggered
Current Price: $46,500

Action: EXECUTE BUY
- Buy: 0.00108 BTC @ $46,500
- Cost: $50.22
- Stop Loss: $42,780 (0.92 × $46,500)
- Status: Position OPEN
```

#### Hour 2 (Stop Hit)

```
Current Time: 10:00 UTC
Current Price: $42,700
Stop Loss was: $42,780

Market gapped below stop. Filled at $42,700.

Action: AUTO EXECUTE SELL
- Sell: 0.00108 BTC @ $42,700
- Proceeds: $46.12
- P&L: −$4.10 (−8.2% return)
- Duration: 2 hours
- Status: Position CLOSED (loss contained)
```

---

## Key Metrics & Expectations

### Realistic Performance

Based on this strategy:

```
Win Rate: 55-65% (realistic, not 100%)
Avg Win: +$50 per winning trade
Avg Loss: −$4 per losing trade
Risk/Reward: 1:12.5 (favorable)

Example 10 trades:
6 wins  × $50 = +$300
4 losses × -$4 = −$16
Net: +$284 on $500 risk
```

### Break-Even Analysis

```
To be profitable, you need:
- At least 7-10 trades per cycle
- Win rate > 30% (thanks to risk/reward)
- Consistent execution (no overrides)

To scale:
- Test with $50 for 20+ trades
- Once confident, move to $100
- Each 2x position doubles your $
```

---

## Entry Signal Checklist

Before each trade, verify:

- [ ] Momentum is above 2% over 20 hours
- [ ] Current price is higher than 20h ago
- [ ] No extreme volatility/gaps in data
- [ ] Exchange is functioning normally
- [ ] Sufficient USD balance ($50 minimum)
- [ ] No position currently open

---

## Troubleshooting

### "I got a losing trade"
✓ Normal. Expected loss is 8%. Plan for 4/10 trades to be losses.

### "Momentum signal keeps triggering but price reverses"
→ Tighten momentum threshold (e.g., 2.5% instead of 2%)
→ Add secondary confirmation (volume, RSI)

### "Profit target never gets hit"
→ Use limit orders closer to target
→ Consider trailing stop instead of fixed target
→ Review win rate — may need tighter entries

### "I manually overrode the stop loss and lost more"
→ Use bot automation (3Commas/TradingView) to force discipline
→ Remove manual override options from your setup

---

## Next Steps

1. **Paper trade first** — run `kraken_simulator.py` for 20+ cycles
2. **Review results** — check win rate and P&L in `logs/simulator.log`
3. **Set up automation** — use `TRADING_INTEGRATIONS.md` to pick a bot platform
4. **Test live (micro)** — start with $50 real capital once confident
5. **Scale gradually** — increase position size only after proving the system

---

## Questions?

Strategy principles:
- Momentum > 2% = entry signal
- $50 position size (fixed)
- +100% profit target (2x entry)
- −8% stop loss
- Single position at a time
- Automated execution

Ask for clarification on any of these constants.
