'use client'

import { useTradingStore } from '@/lib/store'
import { formatPrice, formatPercentage } from '@/lib/utils'

export default function Header() {
  const { btcPrice } = useTradingStore()

  if (!btcPrice) return null

  const changePercent = btcPrice.change24h > 0 ? (btcPrice.change24h / (btcPrice.price - btcPrice.change24h)) * 100 : 0
  const isPositive = btcPrice.change24h >= 0

  return (
    <header className="sticky top-0 z-50 bg-gradient-to-r from-slate-900/95 to-slate-800/95 backdrop-blur-md border-b border-slate-700/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center space-x-3">
            <div className="text-3xl font-bold gradient-text">₿</div>
            <div>
              <h1 className="text-xl font-bold text-white">Trading Dashboard</h1>
              <p className="text-xs text-slate-400">Real-Time Kraken Analytics</p>
            </div>
          </div>

          {/* Live Price */}
          <div className="hidden md:flex items-center space-x-6">
            <div className="text-right">
              <p className="text-2xl font-bold text-white">${formatPrice(btcPrice.price)}</p>
              <p className={`text-sm font-semibold ${isPositive ? 'text-green-400' : 'text-red-400'}`}>
                {formatPrice(btcPrice.change24h)} ({formatPercentage(changePercent)})
              </p>
            </div>
            {isPositive && <div className="animate-pulse-glow w-3 h-3 rounded-full bg-green-400"></div>}
            {!isPositive && <div className="w-3 h-3 rounded-full bg-red-400"></div>}
          </div>

          {/* Status Indicator */}
          <div className="flex items-center space-x-2">
            <div className="hidden sm:block px-3 py-1 rounded-full bg-green-400/20 border border-green-400/50">
              <span className="text-xs font-semibold text-green-400">● Live</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}
