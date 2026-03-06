'use client'

import { useState } from 'react'
import { useTradingStore } from '@/lib/store'
import { formatCurrency } from '@/lib/utils'

export default function ControlsPanel() {
  const {
    botActive,
    toggleBot,
    tradeSize,
    setTradeSize,
    riskPercentage,
    setRiskPercentage,
    portfolioBalance,
    btcPrice,
    addTrade,
  } = useTradingStore()

  const [manualTrade, setManualTrade] = useState({
    entryPrice: btcPrice?.price || 42500,
    quantity: 0.01,
    stopLoss: 41000,
    profitTarget: 44000,
  })

  const handleExecuteTrade = () => {
    if (!btcPrice) return

    const trade = {
      id: `trade-${Date.now()}`,
      timestamp: Date.now(),
      entryPrice: manualTrade.entryPrice,
      exitPrice: null,
      quantity: manualTrade.quantity,
      pnl: 0,
      duration: 0,
      status: 'open' as const,
      signal: 'Manual',
      stopLoss: manualTrade.stopLoss,
      profitTarget: manualTrade.profitTarget,
    }

    addTrade(trade)
    setManualTrade({
      entryPrice: btcPrice.price,
      quantity: 0.01,
      stopLoss: 41000,
      profitTarget: 44000,
    })
  }

  return (
    <div className="space-y-6">
      {/* Bot Controls */}
      <div className="glass p-6 rounded-lg border border-slate-700/50">
        <h3 className="text-lg font-bold text-white mb-4">Bot Controls</h3>

        <div className="space-y-4">
          {/* Start/Stop Button */}
          <button
            onClick={toggleBot}
            className={`w-full py-3 px-4 rounded-lg font-bold transition-smooth ${
              botActive
                ? 'bg-red-500/80 hover:bg-red-600 text-white'
                : 'bg-green-500/80 hover:bg-green-600 text-white'
            }`}
          >
            {botActive ? '⏸ Stop Bot' : '▶ Start Bot'}
          </button>

          {/* Status */}
          <div className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg border border-slate-600/30">
            <span className="text-sm text-slate-400">Bot Status</span>
            <div className="flex items-center space-x-2">
              <div className={`w-2 h-2 rounded-full ${botActive ? 'bg-green-400 animate-pulse' : 'bg-slate-500'}`}></div>
              <span className={`text-sm font-semibold ${botActive ? 'text-green-400' : 'text-slate-400'}`}>
                {botActive ? 'Active' : 'Inactive'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Risk Settings */}
      <div className="glass p-6 rounded-lg border border-slate-700/50">
        <h3 className="text-lg font-bold text-white mb-4">Risk Settings</h3>

        <div className="space-y-4">
          {/* Trade Size */}
          <div>
            <label className="block text-sm font-semibold text-slate-300 mb-2">
              Trade Size (BTC): {tradeSize.toFixed(4)}
            </label>
            <input
              type="range"
              min="0.001"
              max="1"
              step="0.001"
              value={tradeSize}
              onChange={(e) => setTradeSize(parseFloat(e.target.value))}
              className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer"
            />
            <p className="text-xs text-slate-500 mt-2">
              Estimated cost: {formatCurrency(tradeSize * (btcPrice?.price || 42500))}
            </p>
          </div>

          {/* Risk Percentage */}
          <div>
            <label className="block text-sm font-semibold text-slate-300 mb-2">
              Risk Per Trade: {riskPercentage}%
            </label>
            <input
              type="range"
              min="0.1"
              max="5"
              step="0.1"
              value={riskPercentage}
              onChange={(e) => setRiskPercentage(parseFloat(e.target.value))}
              className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer"
            />
            <p className="text-xs text-slate-500 mt-2">
              Max loss: {formatCurrency(
                (portfolioBalance.usd + portfolioBalance.btc * (btcPrice?.price || 42500)) *
                  (riskPercentage / 100)
              )}
            </p>
          </div>
        </div>
      </div>

      {/* Manual Trade Entry */}
      <div className="glass p-6 rounded-lg border border-slate-700/50">
        <h3 className="text-lg font-bold text-white mb-4">Manual Trade Entry</h3>

        <div className="space-y-3">
          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1">
              Entry Price (USD)
            </label>
            <input
              type="number"
              value={manualTrade.entryPrice}
              onChange={(e) =>
                setManualTrade({ ...manualTrade, entryPrice: parseFloat(e.target.value) })
              }
              className="w-full bg-slate-700/50 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1">
              Quantity (BTC)
            </label>
            <input
              type="number"
              value={manualTrade.quantity}
              onChange={(e) =>
                setManualTrade({ ...manualTrade, quantity: parseFloat(e.target.value) })
              }
              step="0.0001"
              className="w-full bg-slate-700/50 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-400 mb-1">
                Stop Loss
              </label>
              <input
                type="number"
                value={manualTrade.stopLoss}
                onChange={(e) =>
                  setManualTrade({ ...manualTrade, stopLoss: parseFloat(e.target.value) })
                }
                className="w-full bg-slate-700/50 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-400 mb-1">
                Profit Target
              </label>
              <input
                type="number"
                value={manualTrade.profitTarget}
                onChange={(e) =>
                  setManualTrade({ ...manualTrade, profitTarget: parseFloat(e.target.value) })
                }
                className="w-full bg-slate-700/50 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>

          <button
            onClick={handleExecuteTrade}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition-smooth"
          >
            Execute Trade
          </button>
        </div>
      </div>
    </div>
  )
}
