# Deployment Guide - Trading Dashboard

Deploy your trading dashboard to Vercel in under 5 minutes.

## 🚀 Quick Start (Recommended)

### Step 1: Prepare Your Repository

```bash
# Initialize Git (if not already done)
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: Trading Dashboard"

# Push to GitHub
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/trading-dashboard.git
git push -u origin main
```

### Step 2: Connect to Vercel

1. Visit [vercel.com](https://vercel.com)
2. Sign up (free) with GitHub
3. Click **"New Project"**
4. Select your GitHub repository
5. **Framework**: Next.js (auto-detected)
6. **Build Command**: `npm run build`
7. **Output Directory**: `.next`
8. Click **"Deploy"**

✅ Your dashboard is live! Vercel gives you a unique URL.

## 🔧 Environment Variables

Add Kraken API configuration:

### Via Vercel UI:
1. Go to **Project Settings** → **Environment Variables**
2. Add:
   ```
   NEXT_PUBLIC_KRAKEN_API_URL=https://api.kraken.com/0/public
   ```
3. Click **"Save"**
4. Redeploy (Vercel will auto-redeploy)

### Optional: Trading Credentials
```
KRAKEN_API_KEY=your_api_key
KRAKEN_API_SECRET=your_api_secret
```

⚠️ **Never commit secrets to Git!** Use Vercel's environment variables.

## 📱 Custom Domain

### Link a Custom Domain:

1. **Buy a domain** (Vercel, Namecheap, GoDaddy, etc.)
2. In Vercel → **Project Settings** → **Domains**
3. Add your domain
4. Update DNS records (Vercel shows instructions)
5. Wait 24-48h for propagation

Example domains:
- `trading-dashboard.com`
- `btc-trader.io`
- `mytrader.dev`

## 🔄 Automatic Deployments

Every time you push to `main` branch, Vercel automatically:
1. Runs `npm install`
2. Runs `npm run build`
3. Deploys to production
4. Provides a preview URL for pull requests

## 📦 Database/Backend (Optional)

If you want to add persistent storage (trades, settings):

### Option 1: Vercel KV (Redis)
```bash
vercel env pull .env.local
# Edit .env.local with KV connection
```

### Option 2: Firebase Realtime DB
```typescript
// lib/firebase.ts
import { initializeApp } from 'firebase/app'
const app = initializeApp(firebaseConfig)
```

### Option 3: Supabase (PostgreSQL)
Add connection string to environment variables.

## 🔍 Monitoring

### Vercel Analytics:
1. Project → **Analytics**
   - Page load times
   - Core Web Vitals
   - Error tracking

### Real-time Logs:
1. Project → **Deployment**
2. Click any deployment
3. View live logs

## 🚨 Troubleshooting

### Build Fails

**Error**: `Failed to build`

Check logs in Vercel → **Deployments** → Failed build

**Common causes**:
- TypeScript errors: `npm run build` locally
- Missing dependencies: `npm install`
- Node version mismatch: Use Node 18+

### API Not Responding

**Error**: Kraken API returns 429 (rate limited)

Add rate limiting handler in `lib/kraken.ts`:
```typescript
const delay = ms => new Promise(r => setTimeout(r, ms))
// Add exponential backoff between requests
```

### WebSocket Connection Fails

Check browser console (DevTools → Console). Kraken WebSocket requires:
- Valid origin headers
- No CORS issues (public endpoints)

### Environment Variables Not Loading

1. Verify in **Project Settings** → **Environment Variables**
2. Trigger a redeploy
3. Check `.env.local` for local development

## 📊 Performance Optimization

### Bundle Size
```bash
npm run build
# Check output size
```

Target: < 500KB JS (gzip)

### Caching
- Static pages: 60 seconds (ISR)
- API responses: Use SWR or TanStack Query
- Images: Auto-optimized by Next.js

## 🔐 Security Checklist

- [ ] Never commit `.env.local`
- [ ] Use Vercel's environment variables
- [ ] Enable branch protection on GitHub
- [ ] Set up 2FA on Vercel account
- [ ] Review deployed secrets
- [ ] Use HTTPS only
- [ ] Keep dependencies updated

## 🎯 Advanced: CI/CD Pipeline

Add automated tests before deployment:

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install
      - run: npm run lint
      - run: npm run build
      - run: npm test  # If you add tests
```

## 📞 Support

- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **Next.js Docs**: [nextjs.org/docs](https://nextjs.org/docs)
- **Vercel Support**: [vercel.com/support](https://vercel.com/support)

## 🎉 You're Done!

Your trading dashboard is now live on Vercel!

**What's next?**
- Monitor performance in Vercel Analytics
- Set up custom domain
- Add authentication for secure access
- Integrate live trading (requires backend)
- Add more indicators and features

---

**Live Dashboard Checklist:**
- [ ] Code on GitHub
- [ ] Deployed to Vercel
- [ ] Custom domain connected
- [ ] Environment variables set
- [ ] Monitoring enabled
- [ ] Team access configured

**Happy trading! 🚀**
