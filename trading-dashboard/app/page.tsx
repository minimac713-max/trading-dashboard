'use client'

import { useState } from 'react'
import Header from '@/components/Header'
import LiveMetrics from '@/components/LiveMetrics'
import PositionMonitor from '@/components/PositionMonitor'
import Charts from '@/components/Charts'
import TradeHistory from '@/components/TradeHistory'
import ControlsPanel from '@/components/ControlsPanel'
import Alerts from '@/components/Alerts'

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      <Header />
      <main className="max-w-7xl mx-auto px-4 py-8 space-y-8">
        {/* Top Section: Key Metrics */}
        <LiveMetrics />

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left: Charts & Position */}
          <div className="lg:col-span-2 space-y-8">
            <Charts />
            <PositionMonitor />
          </div>

          {/* Right: Controls & Alerts */}
          <div className="space-y-8">
            <ControlsPanel />
            <Alerts />
          </div>
        </div>

        {/* Bottom: Trade History */}
        <TradeHistory />
      </main>
    </div>
  )
}
