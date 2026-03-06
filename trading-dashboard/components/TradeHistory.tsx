'use client'

import { useTradingStore } from '@/lib/store'
import { formatPrice, formatDate, getPnLColor, getPnLBgColor, formatDuration } from '@/lib/utils'

export default function TradeHistory() {
  const { trades } = useTradingStore()
  const closedTrades = trades.filter((t) => t.status === 'closed')

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-bold text-white">Trade History</h2>

      <div className="glass rounded-lg border border-slate-700/50 overflow-hidden">
        {closedTrades.length === 0 ? (
          <div className="p-8 text-center text-slate-400">
            <p>No closed trades yet</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-800/50 border-b border-slate-700/50">
                <tr>
                  <th className="px-4 py-3 text-left font-semibold text-slate-300">Time</th>
                  <th className="px-4 py-3 text-left font-semibold text-slate-300">Entry</th>
                  <th className="px-4 py-3 text-left font-semibold text-slate-300">Exit</th>
                  <th className="px-4 py-3 text-left font-semibold text-slate-300">P&L</th>
                  <th className="px-4 py-3 text-left font-semibold text-slate-300">Duration</th>
                  <th className="px-4 py-3 text-left font-semibold text-slate-300">Signal</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-700/30">
                {closedTrades.map((trade) => (
                  <tr
                    key={trade.id}
                    className="hover:bg-slate-700/20 transition-smooth"
                  >
                    <td className="px-4 py-3 text-slate-400">
                      {formatDate(trade.timestamp)}
                    </td>
                    <td className="px-4 py-3 font-mono text-white">
                      ${formatPrice(trade.entryPrice)}
                    </td>
                    <td className="px-4 py-3 font-mono text-white">
                      ${formatPrice(trade.exitPrice || 0)}
                    </td>
                    <td className={`px-4 py-3 font-semibold ${getPnLColor(trade.pnl)}`}>
                      ${formatPrice(trade.pnl)}
                    </td>
                    <td className="px-4 py-3 text-slate-400">
                      {formatDuration(trade.duration)}
                    </td>
                    <td className="px-4 py-3">
                      <span className="px-2 py-1 rounded-full text-xs font-medium bg-blue-500/20 text-blue-300 border border-blue-500/50">
                        {trade.signal}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Summary Stats */}
      {closedTrades.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="glass p-4 rounded-lg border border-slate-700/50">
            <p className="text-sm text-slate-400 mb-2">Best Trade</p>
            <p className="text-2xl font-bold text-green-400">
              ${formatPrice(Math.max(...closedTrades.map((t) => t.pnl)))}
            </p>
          </div>
          <div className="glass p-4 rounded-lg border border-slate-700/50">
            <p className="text-sm text-slate-400 mb-2">Worst Trade</p>
            <p className="text-2xl font-bold text-red-400">
              ${formatPrice(Math.min(...closedTrades.map((t) => t.pnl)))}
            </p>
          </div>
        </div>
      )}
    </div>
  )
}
