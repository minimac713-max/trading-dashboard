# Professional Trading Dashboard

A real-time trading dashboard built with **Next.js**, **React**, and **Kraken API** integration. Features live metrics, position monitoring, performance charts, and automated trade management.

## 🚀 Features

### Live Metrics (Top Section)
- ✅ Current BTC price (live from Kraken API)
- ✅ Portfolio balance (USD + BTC)
- ✅ Total P&L (profit/loss)
- ✅ Win rate % and trade count

### Position Monitor
- ✅ Current open positions
- ✅ Entry price, current price, profit/loss
- ✅ Stop loss and profit target levels
- ✅ Time in trade counter

### Charts & Graphs
- ✅ BTC price chart with 1H, 4H, 1D candles
- ✅ Cumulative P&L equity curve
- ✅ Trade history visualization with entry/exit markers
- ✅ Performance metrics (max drawdown, Sharpe ratio)

### Trade History Table
- ✅ All past trades with timestamps
- ✅ Entry/exit prices and P&L
- ✅ Trade duration tracking
- ✅ Strategy signal labels

### Controls Panel
- ✅ Start/Stop bot button
- ✅ Manual trade entry form
- ✅ Trade size selector (slider)
- ✅ Risk settings adjustment
- ✅ Real-time account balance display

### Real-time Alerts
- ✅ Trade executed notification
- ✅ Target hit notification
- ✅ Stop loss triggered notification
- ✅ Dismissible alert history
- ✅ Alert type indicators

## 🛠️ Tech Stack

- **Framework**: Next.js 15 + React 19 (TypeScript)
- **Styling**: TailwindCSS 3.4
- **Charts**: Recharts 2.12
- **State Management**: Zustand 4.5
- **HTTP Client**: Axios 1.7
- **WebSocket**: Native WS API + Kraken WebSocket
- **Deployment**: Vercel

## 📦 Installation

### Prerequisites
- Node.js 18+ (LTS recommended)
- npm or yarn

### Setup

```bash
# Clone or extract the project
cd trading-dashboard

# Install dependencies
npm install

# Copy environment example
cp .env.example .env.local

# Edit .env.local with your configuration (optional)
```

## 🏃 Running Locally

### Development Mode
```bash
npm run dev
```
Visit `http://localhost:3000` in your browser.

### Production Build
```bash
npm run build
npm start
```

## 🌐 Deployment to Vercel

### Option 1: Vercel CLI
```bash
# Install Vercel CLI globally
npm i -g vercel

# Deploy
vercel

# Set as production
vercel --prod
```

### Option 2: Git Integration (Recommended)
1. Push this code to a GitHub repository
2. Go to [vercel.com](https://vercel.com)
3. Click "New Project"
4. Select your GitHub repository
5. Framework: **Next.js**
6. Deploy!

Vercel will automatically:
- Install dependencies
- Build the project
- Deploy to a live URL
- Set up automatic deployments on push

### Environment Variables on Vercel
1. Go to Project Settings → Environment Variables
2. Add:
   ```
   NEXT_PUBLIC_KRAKEN_API_URL=https://api.kraken.com/0/public
   ```
3. Redeploy

## 🔌 API Integration

### Kraken API (Public Endpoints)
The dashboard uses **free public endpoints** from Kraken:

- **Ticker Data**: `/Ticker` - Current price, high/low, volume
- **OHLC Data**: `/OHLC` - Candlestick data for charts
- **WebSocket**: `wss://ws.kraken.com` - Real-time price updates

**No API key required** for public data. For authenticated trading:

```bash
# In .env.local (keep secret!)
KRAKEN_API_KEY=your_api_key
KRAKEN_API_SECRET=your_api_secret
```

### Adding Kraken Trade Integration (Advanced)

To connect live trading, add your credentials:

```typescript
// lib/kraken-auth.ts
const krakenAuth = {
  apiKey: process.env.KRAKEN_API_KEY!,
  apiSecret: process.env.KRAKEN_API_SECRET!,
}
```

Then implement authenticated endpoints:
```typescript
// Example: Place a market order
POST /0/private/AddOrder
- pair: XBTUSDT
- type: market
- volume: 0.01
```

## 📊 State Management (Zustand)

The dashboard uses **Zustand** for lightweight state management:

```typescript
import { useTradingStore } from '@/lib/store'

const { btcPrice, trades, addTrade } = useTradingStore()
```

## 🎨 Customization

### Colors & Theme
Edit `tailwind.config.ts` to customize:
- Dark theme colors
- Gradient backgrounds
- Component spacing

### Default Portfolio Balance
Edit `lib/store.ts`:
```typescript
portfolioBalance: { usd: 10000, btc: 0.25 }
```

### Trade Defaults
Edit `components/ControlsPanel.tsx`:
```typescript
tradeSize: 0.01        // BTC quantity
riskPercentage: 2      // % of portfolio per trade
```

## 📈 Performance Monitoring

Monitor your dashboard performance:

```bash
npm run build
# Check bundle size and performance metrics
```

## 🚨 Important Notes

⚠️ **This is a frontend dashboard only.** It:
- Displays data, doesn't execute trades automatically
- Requires manual API key setup for live trading
- Should be used with a backend trading engine/bot

✅ **What's included:**
- Real-time price data from Kraken
- Portfolio tracking interface
- Trade management UI
- Performance metrics & analytics

## 🔐 Security Best Practices

1. **Never commit** `.env.local` with real API keys
2. **Use environment variables** on Vercel for secrets
3. **Implement server-side** authenticated API calls
4. **Enable CORS** restrictions on production
5. **Keep dependencies updated**: `npm audit`

## 📝 File Structure

```
trading-dashboard/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Main dashboard
│   └── globals.css         # Global styles
├── components/
│   ├── Header.tsx          # Top header
│   ├── LiveMetrics.tsx     # KPI cards
│   ├── PositionMonitor.tsx # Open positions
│   ├── Charts.tsx          # Charts & graphs
│   ├── TradeHistory.tsx    # Past trades table
│   ├── ControlsPanel.tsx   # Controls & forms
│   └── Alerts.tsx          # Alert notifications
├── lib/
│   ├── store.ts            # Zustand state
│   ├── kraken.ts           # Kraken API functions
│   └── utils.ts            # Helper functions
├── public/                 # Static assets
├── next.config.js          # Next.js config
├── tailwind.config.ts      # Tailwind config
├── tsconfig.json           # TypeScript config
└── package.json            # Dependencies
```

## 🤝 Contributing

Feel free to extend this dashboard:

1. Add more indicators (RSI, MACD, etc.)
2. Integrate other exchanges
3. Add backtesting features
4. Implement automated trading signals
5. Add mobile responsiveness improvements

## 📞 Support

For issues with:
- **Kraken API**: Visit [docs.kraken.com](https://docs.kraken.com)
- **Next.js**: Visit [nextjs.org](https://nextjs.org)
- **Recharts**: Visit [recharts.org](https://recharts.org)
- **TailwindCSS**: Visit [tailwindcss.com](https://tailwindcss.com)

## 📜 License

MIT License - Feel free to use this project commercially.

---

**🚀 Ready to deploy?**

1. Push to GitHub
2. Connect to Vercel
3. Set environment variables
4. Deploy with one click!

Enjoy your professional trading dashboard! ₿
