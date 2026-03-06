'use client'

import { useState, useEffect } from 'react'
import Header from '@/components/Header'
import LiveMetrics from '@/components/LiveMetrics'
import PositionMonitor from '@/components/PositionMonitor'
import Charts from '@/components/Charts'
import TradeHistory from '@/components/TradeHistory'
import ControlsPanel from '@/components/ControlsPanel'
import Alerts from '@/components/Alerts'
import { useTradingStore } from '@/lib/store'
import { fetchKrakenPrice } from '@/lib/kraken'

export default function Dashboard() {
  const { initializeDashboard } = useTradingStore()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const initialize = async () => {
      try {
        setLoading(true)
        // Fetch initial Kraken price
        const priceData = await fetchKrakenPrice()
        // Initialize the store with initial data
        initializeDashboard(priceData)
        setError(null)
      } catch (err) {
        setError('Failed to initialize dashboard')
        console.error('Initialization error:', err)
      } finally {
        setLoading(false)
      }
    }

    initialize()
  }, [initializeDashboard])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-b from-slate-900 to-slate-800">
        <div className="text-center">
          <div className="text-4xl mb-4 animate-pulse">₿</div>
          <p className="text-xl text-slate-400">Initializing Dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      <Header />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {error && (
          <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-4 text-red-200">
            {error}
          </div>
        )}

        {/* Live Metrics */}
        <LiveMetrics />

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Position Monitor */}
          <div className="lg:col-span-1">
            <PositionMonitor />
          </div>

          {/* Controls Panel */}
          <div className="lg:col-span-2">
            <ControlsPanel />
          </div>
        </div>

        {/* Charts Section */}
        <Charts />

        {/* Trade History */}
        <TradeHistory />

        {/* Alerts */}
        <Alerts />
      </div>
    </main>
  )
}
