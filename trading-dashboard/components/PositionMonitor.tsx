'use client'

import { useTradingStore } from '@/lib/store'
import { formatPrice, formatPercentage, formatDuration, getPnLColor, getPnLBgColor } from '@/lib/utils'

export default function PositionMonitor() {
  const { openPositions } = useTradingStore()

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-bold text-white">Open Positions</h2>

      {openPositions.length === 0 ? (
        <div className="glass p-8 rounded-lg border border-slate-700/50 text-center">
          <p className="text-slate-400">No active positions</p>
        </div>
      ) : (
        openPositions.map((position, idx) => (
          <div
            key={idx}
            className={`glass p-4 rounded-lg border transition-smooth ${getPnLBgColor(position.pnl)}`}
          >
            <div className="space-y-3">
              {/* Header */}
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-sm text-slate-400">BTC/USD</p>
                  <p className="text-lg font-semibold text-white">
                    {position.quantity.toFixed(4)} BTC
                  </p>
                </div>
                <p className={`text-xl font-bold ${getPnLColor(position.pnl)}`}>
                  {formatPrice(position.pnl)}
                </p>
              </div>

              {/* Prices */}
              <div className="grid grid-cols-2 gap-4 text-xs">
                <div>
                  <p className="text-slate-500">Entry Price</p>
                  <p className="font-semibold text-slate-300">${formatPrice(position.entryPrice)}</p>
                </div>
                <div>
                  <p className="text-slate-500">Current Price</p>
                  <p className="font-semibold text-slate-300">${formatPrice(position.currentPrice)}</p>
                </div>
              </div>

              {/* Targets */}
              <div className="grid grid-cols-2 gap-4 text-xs">
                <div>
                  <p className="text-slate-500">Stop Loss</p>
                  <p className="font-semibold text-red-400">${formatPrice(position.stopLoss)}</p>
                </div>
                <div>
                  <p className="text-slate-500">Profit Target</p>
                  <p className="font-semibold text-green-400">${formatPrice(position.profitTarget)}</p>
                </div>
              </div>

              {/* Duration & P&L % */}
              <div className="pt-2 border-t border-slate-600/30 flex justify-between items-center">
                <span className="text-xs text-slate-500">
                  {formatDuration(position.timeInTrade)}
                </span>
                <span className={`text-sm font-semibold ${getPnLColor(position.pnl)}`}>
                  {formatPercentage(position.pnlPercent)}
                </span>
              </div>
            </div>
          </div>
        ))
      )}
    </div>
  )
}
