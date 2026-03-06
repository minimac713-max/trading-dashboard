'use client'

import { useTradingStore } from '@/lib/store'
import { formatCurrency, formatPercentage, getPnLColor } from '@/lib/utils'
import { useState, useEffect } from 'react'

interface MetricCard {
  label: string
  value: string | number
  subValue?: string
  color?: string
  icon: string
}

export default function LiveMetrics() {
  const {
    btcPrice,
    portfolioBalance,
    totalPnL,
    winRate,
    tradeCount,
  } = useTradingStore()

  const [metrics, setMetrics] = useState<MetricCard[]>([])

  useEffect(() => {
    if (!btcPrice || !portfolioBalance) return

    const portfolioValueUSD =
      portfolioBalance.usd + portfolioBalance.btc * btcPrice.price
    const pnlPercent =
      portfolioValueUSD > 0 ? (totalPnL / portfolioValueUSD) * 100 : 0

    setMetrics([
      {
        label: 'BTC Price',
        value: `$${btcPrice.price.toFixed(2)}`,
        subValue: formatPercentage(pnlPercent),
        icon: '₿',
      },
      {
        label: 'Portfolio Balance',
        value: formatCurrency(portfolioValueUSD),
        subValue: `${portfolioBalance.btc.toFixed(4)} BTC`,
        icon: '💼',
      },
      {
        label: 'Total P&L',
        value: formatCurrency(totalPnL),
        subValue: formatPercentage(pnlPercent),
        color: getPnLColor(totalPnL),
        icon: '📊',
      },
      {
        label: 'Win Rate',
        value: `${winRate.toFixed(1)}%`,
        subValue: `${tradeCount} trades`,
        icon: '🎯',
      },
    ])
  }, [btcPrice, portfolioBalance, totalPnL, winRate, tradeCount])

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {metrics.map((metric, idx) => (
        <div
          key={idx}
          className="glass p-6 rounded-lg border border-slate-700/50 hover:border-blue-500/50 transition-smooth"
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <p className="text-sm text-slate-400 mb-2">{metric.label}</p>
              <p className={`text-2xl font-bold text-white ${metric.color || ''}`}>
                {metric.value}
              </p>
              {metric.subValue && (
                <p className="text-xs text-slate-500 mt-1">{metric.subValue}</p>
              )}
            </div>
            <div className="text-3xl opacity-50">{metric.icon}</div>
          </div>
        </div>
      ))}
    </div>
  )
}
