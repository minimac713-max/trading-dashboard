'use client'

import { useTradingStore } from '@/lib/store'
import { formatDate } from '@/lib/utils'

export default function Alerts() {
  const { alerts, dismissAlert } = useTradingStore()

  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'trade':
        return '🔔'
      case 'target':
        return '🎯'
      case 'stoploss':
        return '⚠️'
      default:
        return 'ℹ️'
    }
  }

  const getAlertColor = (type: string) => {
    switch (type) {
      case 'trade':
        return 'border-blue-500/50 bg-blue-500/10'
      case 'target':
        return 'border-green-500/50 bg-green-500/10'
      case 'stoploss':
        return 'border-red-500/50 bg-red-500/10'
      default:
        return 'border-slate-500/50 bg-slate-500/10'
    }
  }

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-bold text-white">Alerts</h2>

      <div className="space-y-2 max-h-96 overflow-y-auto">
        {alerts.length === 0 ? (
          <div className="glass p-8 rounded-lg border border-slate-700/50 text-center">
            <p className="text-slate-400">No alerts yet</p>
          </div>
        ) : (
          alerts.map((alert) => (
            <div
              key={alert.id}
              className={`glass p-4 rounded-lg border flex items-start justify-between transition-smooth ${
                alert.read ? 'opacity-60' : ''
              } ${getAlertColor(alert.type)}`}
            >
              <div className="flex items-start space-x-3 flex-1">
                <span className="text-xl mt-1">{getAlertIcon(alert.type)}</span>
                <div>
                  <p className="text-sm font-semibold text-white">{alert.message}</p>
                  <p className="text-xs text-slate-500 mt-1">{formatDate(alert.timestamp)}</p>
                </div>
              </div>
              <button
                onClick={() => dismissAlert(alert.id)}
                className="text-slate-400 hover:text-slate-200 transition-smooth ml-4"
              >
                ✕
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
