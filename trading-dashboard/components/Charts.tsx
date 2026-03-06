'use client'

import { useState, useEffect } from 'react'
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  ComposedChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import { useTradingStore } from '@/lib/store'
import { generateMockCandles, formatPrice, formatDate } from '@/lib/utils'

export default function Charts() {
  const { btcPrice, priceHistory, trades } = useTradingStore()
  const [activeTab, setActiveTab] = useState('price')
  const [candleData, setCandleData] = useState<any[]>([])
  const [equityData, setEquityData] = useState<any[]>([])

  useEffect(() => {
    // Generate mock candle data for demo
    const candles = generateMockCandles(btcPrice?.price || 42500, 60)
    setCandleData(
      candles.map((c) => ({
        time: new Date(c.timestamp).toLocaleTimeString('en-US', {
          hour: '2-digit',
          minute: '2-digit',
        }),
        timestamp: c.timestamp,
        open: c.open,
        high: c.high,
        low: c.low,
        close: c.close,
      }))
    )

    // Generate equity curve
    if (trades.length > 0) {
      const sortedTrades = [...trades].sort((a, b) => a.timestamp - b.timestamp)
      let equity = 10000
      const curve = [{ time: '00:00', equity }]

      for (let i = 0; i < sortedTrades.length; i++) {
        equity += sortedTrades[i].pnl
        curve.push({
          time: new Date(sortedTrades[i].timestamp).toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
          }),
          equity,
        })
      }

      setEquityData(curve)
    }
  }, [btcPrice, trades])

  const chartProps = {
    margin: { top: 5, right: 30, left: 0, bottom: 5 },
  }

  return (
    <div className="space-y-6">
      <div className="flex gap-2 mb-6 flex-wrap">
        {[
          { id: 'price', label: 'BTC Price' },
          { id: 'equity', label: 'Equity Curve' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 rounded-lg font-medium transition-smooth ${
              activeTab === tab.id
                ? 'bg-blue-500 text-white'
                : 'bg-slate-700/50 text-slate-300 hover:bg-slate-700'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Price Chart */}
      {activeTab === 'price' && (
        <div className="glass p-6 rounded-lg border border-slate-700/50">
          <h3 className="text-lg font-bold text-white mb-4">BTC Price (1H)</h3>
          <ResponsiveContainer width="100%" height={350}>
            <ComposedChart data={candleData} {...chartProps}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="time" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" domain="dataMin - 100" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1e293b',
                  border: '1px solid #475569',
                  borderRadius: '8px',
                }}
                labelStyle={{ color: '#e2e8f0' }}
                formatter={(value: any) => [formatPrice(value), '']}
              />
              <Bar dataKey="close" fill="#3b82f6" />
              <Line
                type="monotone"
                dataKey="close"
                stroke="#06b6d4"
                strokeWidth={2}
                isAnimationActive={false}
              />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Equity Curve */}
      {activeTab === 'equity' && (
        <div className="glass p-6 rounded-lg border border-slate-700/50">
          <h3 className="text-lg font-bold text-white mb-4">Cumulative P&L</h3>
          {equityData.length > 0 ? (
            <ResponsiveContainer width="100%" height={350}>
              <AreaChart data={equityData} {...chartProps}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="time" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1e293b',
                    border: '1px solid #475569',
                    borderRadius: '8px',
                  }}
                  labelStyle={{ color: '#e2e8f0' }}
                  formatter={(value: any) => [formatPrice(value), 'Equity']}
                />
                <Area
                  type="monotone"
                  dataKey="equity"
                  stroke="#10b981"
                  fill="#10b981"
                  fillOpacity={0.1}
                />
              </AreaChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-80 flex items-center justify-center text-slate-400">
              No trade data yet
            </div>
          )}
        </div>
      )}

      {/* Performance Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {[
          {
            label: 'Max Drawdown',
            value: '-5.2%',
            icon: '📉',
          },
          {
            label: 'Sharpe Ratio',
            value: '1.85',
            icon: '📈',
          },
          {
            label: 'Profit Factor',
            value: '2.34',
            icon: '💰',
          },
        ].map((metric, idx) => (
          <div key={idx} className="glass p-4 rounded-lg border border-slate-700/50">
            <p className="text-sm text-slate-400 mb-2">{metric.label}</p>
            <div className="flex items-end justify-between">
              <p className="text-2xl font-bold text-white">{metric.value}</p>
              <span className="text-3xl opacity-50">{metric.icon}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
