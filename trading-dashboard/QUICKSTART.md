# Quick Start Guide

Get your trading dashboard running in **3 minutes**.

## 1️⃣ Install & Setup (1 minute)

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

Open `http://localhost:3000` in your browser. ✅ **Dashboard is live!**

## 2️⃣ View Live Data (30 seconds)

The dashboard automatically fetches BTC price from Kraken API.

- **Live Metrics**: Shows current BTC price
- **Position Monitor**: (Empty until you add trades)
- **Charts**: Mock candlestick data
- **Controls Panel**: Manage bot and trades

## 3️⃣ Test Features (30 seconds)

### Add a Manual Trade:
1. Scroll to **Controls Panel** → **Manual Trade Entry**
2. Enter:
   - Entry Price: `42500`
   - Quantity: `0.01`
   - Stop Loss: `41000`
   - Profit Target: `44000`
3. Click **"Execute Trade"**

### Monitor Position:
- **Position Monitor** updates with your trade
- See P&L change as price moves
- Track stop loss and profit target

### Check Alerts:
- Alerts section logs all actions
- Dismissible with ✕ button

## 🚀 Deploy to Vercel (1 click)

### Fastest Way:

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Trading Dashboard"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/trading-dashboard
   git push -u origin main
   ```

2. **Deploy**:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Select your repo
   - Click "Deploy"

✅ **Live on Vercel!** Your unique URL appears instantly.

3. **Add Custom Domain** (Optional):
   - Settings → Domains
   - Add your custom domain
   - Update DNS records
   - Done!

## 🎯 Key Features to Try

| Feature | Location | How to Use |
|---------|----------|-----------|
| **Live BTC Price** | Header | Auto-updates every 10 seconds |
| **Portfolio Balance** | Live Metrics | Shows USD + BTC holdings |
| **Total P&L** | Live Metrics | Calculates profit/loss |
| **Position Monitor** | Left sidebar | Add manual trades to see |
| **Price Chart** | Charts tab | Shows BTC candlesticks |
| **Equity Curve** | Charts tab | Shows portfolio growth |
| **Trade History** | Bottom section | All closed trades listed |
| **Bot Controls** | Controls Panel | Start/stop trading bot |
| **Risk Settings** | Controls Panel | Adjust trade size & risk |
| **Alerts** | Bottom section | All notifications logged |

## 📊 API Integration

The dashboard **uses free Kraken API endpoints**:

```
https://api.kraken.com/0/public/Ticker?pair=XBTUSDT
```

No API key needed for public data. ✅

**For live trading** (optional), add Kraken API credentials in `.env.local`:
```
KRAKEN_API_KEY=your_key
KRAKEN_API_SECRET=your_secret
```

## 🛠️ Development Commands

```bash
npm run dev      # Start dev server (port 3000)
npm run build    # Create production build
npm start        # Run production build
npm run lint     # Check code quality
```

## 📱 Responsive Design

Dashboard works on:
- ✅ Desktop (1920px+)
- ✅ Tablet (768px - 1919px)
- ✅ Mobile (< 768px) - Limited features

## 🎨 Customization

### Change Default Portfolio:
Edit `lib/store.ts`:
```typescript
portfolioBalance: { usd: 50000, btc: 1.0 }  // Your defaults
```

### Change Trade Size:
Edit `components/ControlsPanel.tsx`:
```typescript
const [manualTrade, setManualTrade] = useState({
  entryPrice: btcPrice?.price || 50000,  // Default entry
  quantity: 0.05,  // Change this
  // ...
})
```

### Change Colors:
Edit `tailwind.config.ts` or `app/globals.css`

## 🔒 Security

- ❌ Never commit `.env.local` with real API keys
- ✅ Use Vercel's environment variables instead
- ✅ Keep dependencies updated: `npm audit`

## 📞 Quick Help

| Issue | Solution |
|-------|----------|
| Port 3000 busy | `lsof -i :3000` then kill process |
| Build fails | Run `npm install` then `npm run build` |
| API 429 error | Wait 10 minutes (rate limit cooldown) |
| Charts empty | Add trades to see equity curve |

## 🎓 Next Steps

1. **Explore the code**: Check `components/` and `lib/`
2. **Add features**: Integrate your trading bot
3. **Deploy**: Push to Vercel
4. **Monitor**: Watch live trading data

## 📚 Learn More

- [Next.js Docs](https://nextjs.org/docs)
- [Recharts Docs](https://recharts.org)
- [TailwindCSS Docs](https://tailwindcss.com/docs)
- [Kraken API Docs](https://docs.kraken.com)

## ✅ Checklist

- [ ] Dashboard running locally (`npm run dev`)
- [ ] Live BTC price displaying
- [ ] Added test trade manually
- [ ] Alerts working
- [ ] Code pushed to GitHub
- [ ] Deployed to Vercel
- [ ] Custom domain set up (optional)

---

**🎉 You now have a professional trading dashboard!**

Deploy to Vercel and go live immediately. 🚀
