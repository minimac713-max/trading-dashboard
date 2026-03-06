export function formatPrice(price: number, decimals: number = 2): string {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(price)
}

export function formatCurrency(amount: number, currency: string = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency === 'USD' ? 'USD' : 'BTC',
    minimumFractionDigits: 2,
    maximumFractionDigits: 8,
  }).format(amount)
}

export function formatPercentage(value: number, decimals: number = 2): string {
  return `${value >= 0 ? '+' : ''}${value.toFixed(decimals)}%`
}

export function formatTime(timestamp: number): string {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })
}

export function formatDate(timestamp: number): string {
  const date = new Date(timestamp)
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function formatDuration(ms: number): string {
  const seconds = Math.floor(ms / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)

  if (days > 0) return `${days}d ${hours % 24}h`
  if (hours > 0) return `${hours}h ${minutes % 60}m`
  if (minutes > 0) return `${minutes}m ${seconds % 60}s`
  return `${seconds}s`
}

export function getPnLColor(value: number): string {
  if (value > 0) return 'text-green-400'
  if (value < 0) return 'text-red-400'
  return 'text-slate-400'
}

export function getPnLBgColor(value: number): string {
  if (value > 0) return 'bg-green-400/20 border-green-400/50'
  if (value < 0) return 'bg-red-400/20 border-red-400/50'
  return 'bg-slate-400/20 border-slate-400/50'
}

export function calculateMaxDrawdown(equity: number[]): number {
  if (equity.length === 0) return 0
  let maxDrawdown = 0
  let peak = equity[0]

  for (let i = 1; i < equity.length; i++) {
    if (equity[i] > peak) {
      peak = equity[i]
    } else {
      const drawdown = ((peak - equity[i]) / peak) * 100
      if (drawdown > maxDrawdown) {
        maxDrawdown = drawdown
      }
    }
  }

  return maxDrawdown
}

export function calculateSharpeRatio(returns: number[], riskFreeRate: number = 0.02): number {
  if (returns.length === 0) return 0

  const avgReturn = returns.reduce((a, b) => a + b, 0) / returns.length
  const variance =
    returns.reduce((sum, ret) => sum + Math.pow(ret - avgReturn, 2), 0) / returns.length
  const stdDev = Math.sqrt(variance)

  if (stdDev === 0) return 0
  return (avgReturn - riskFreeRate / 252) / stdDev
}

export function generateMockCandles(
  basePrice: number = 42500,
  count: number = 60,
  volatility: number = 0.01
): Array<{
  timestamp: number
  open: number
  high: number
  low: number
  close: number
  volume: number
}> {
  const now = Date.now()
  const candles = []
  let currentPrice = basePrice

  for (let i = count - 1; i >= 0; i--) {
    const timestamp = now - i * 60000 // 1 minute intervals

    const change = (Math.random() - 0.5) * basePrice * volatility
    const open = currentPrice
    const close = currentPrice + change
    const high = Math.max(open, close) * (1 + Math.random() * volatility * 0.5)
    const low = Math.min(open, close) * (1 - Math.random() * volatility * 0.5)
    const volume = Math.random() * 100 + 50

    candles.push({
      timestamp,
      open: parseFloat(open.toFixed(2)),
      high: parseFloat(high.toFixed(2)),
      low: parseFloat(low.toFixed(2)),
      close: parseFloat(close.toFixed(2)),
      volume: parseFloat(volume.toFixed(2)),
    })

    currentPrice = close
  }

  return candles
}

export function generateEquityCurve(
  trades: Array<{ pnl: number; timestamp: number }>,
  initialBalance: number = 10000
): Array<{ timestamp: number; equity: number }> {
  const sortedTrades = [...trades].sort((a, b) => a.timestamp - b.timestamp)
  const curve = [{ timestamp: Date.now() - 30 * 24 * 60 * 60 * 1000, equity: initialBalance }]

  let currentEquity = initialBalance

  for (const trade of sortedTrades) {
    currentEquity += trade.pnl
    curve.push({
      timestamp: trade.timestamp,
      equity: currentEquity,
    })
  }

  return curve
}

export function calculateWinRate(trades: Array<{ pnl: number }>, minTrades: number = 1): number {
  if (trades.length < minTrades) return 0
  const wins = trades.filter((t) => t.pnl > 0).length
  return (wins / trades.length) * 100
}

export function calculateProfitFactor(trades: Array<{ pnl: number }>): number {
  if (trades.length === 0) return 0

  const grossProfit = trades.reduce((sum, t) => sum + Math.max(0, t.pnl), 0)
  const grossLoss = Math.abs(
    trades.reduce((sum, t) => sum + Math.min(0, t.pnl), 0)
  )

  if (grossLoss === 0) return grossProfit > 0 ? Infinity : 0
  return grossProfit / grossLoss
}
