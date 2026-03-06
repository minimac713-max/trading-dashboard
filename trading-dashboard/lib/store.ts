import { create } from 'zustand'

export interface Trade {
  id: string
  timestamp: number
  entryPrice: number
  exitPrice: number | null
  quantity: number
  pnl: number
  duration: number
  status: 'open' | 'closed'
  signal: string
  stopLoss: number
  profitTarget: number
}

export interface Position {
  entryPrice: number
  currentPrice: number
  quantity: number
  pnl: number
  pnlPercent: number
  stopLoss: number
  profitTarget: number
  timeInTrade: number
}

export interface PriceData {
  price: number
  timestamp: number
  change24h: number
  high24h: number
  low24h: number
}

export interface Alert {
  id: string
  timestamp: number
  type: 'trade' | 'target' | 'stoploss' | 'info'
  message: string
  read: boolean
}

interface TradingState {
  // Price data
  btcPrice: PriceData | null
  priceHistory: PriceData[]

  // Portfolio
  portfolioBalance: { usd: number; btc: number }
  totalPnL: number
  winRate: number
  tradeCount: number

  // Positions & Trades
  openPositions: Position[]
  trades: Trade[]

  // Alerts
  alerts: Alert[]

  // Settings
  botActive: boolean
  tradeSize: number
  riskPercentage: number

  // Actions
  setPriceData: (data: PriceData) => void
  addPriceHistory: (data: PriceData) => void
  setPortfolioBalance: (balance: { usd: number; btc: number }) => void
  updatePnL: () => void
  addTrade: (trade: Trade) => void
  updateTrade: (id: string, updates: Partial<Trade>) => void
  setOpenPositions: (positions: Position[]) => void
  updatePosition: (index: number, updates: Partial<Position>) => void
  addAlert: (alert: Omit<Alert, 'id' | 'timestamp'>) => void
  dismissAlert: (id: string) => void
  toggleBot: () => void
  setTradeSize: (size: number) => void
  setRiskPercentage: (risk: number) => void
  initializeDashboard: (priceData: PriceData) => void
  clearHistory: () => void
}

export const useTradingStore = create<TradingState>((set, get) => ({
  btcPrice: null,
  priceHistory: [],
  portfolioBalance: { usd: 10000, btc: 0.25 },
  totalPnL: 0,
  winRate: 0,
  tradeCount: 0,
  openPositions: [],
  trades: [],
  alerts: [],
  botActive: false,
  tradeSize: 0.01,
  riskPercentage: 2,

  setPriceData: (data) =>
    set((state) => ({
      btcPrice: data,
      priceHistory: [...state.priceHistory.slice(-119), data], // Keep last 120 points
    })),

  addPriceHistory: (data) =>
    set((state) => ({
      priceHistory: [...state.priceHistory.slice(-119), data],
    })),

  setPortfolioBalance: (balance) => set({ portfolioBalance: balance }),

  updatePnL: () => {
    const state = get()
    if (state.trades.length === 0) {
      set({ totalPnL: 0, winRate: 0, tradeCount: 0 })
      return
    }

    const closedTrades = state.trades.filter((t) => t.status === 'closed')
    const pnl = closedTrades.reduce((sum, t) => sum + t.pnl, 0)
    const wins = closedTrades.filter((t) => t.pnl > 0).length
    const winRate = closedTrades.length > 0 ? (wins / closedTrades.length) * 100 : 0

    set({
      totalPnL: pnl,
      winRate,
      tradeCount: closedTrades.length,
    })
  },

  addTrade: (trade) =>
    set((state) => {
      const newTrades = [...state.trades, trade]
      const newState = { trades: newTrades }
      return newState
    }),

  updateTrade: (id, updates) =>
    set((state) => ({
      trades: state.trades.map((t) => (t.id === id ? { ...t, ...updates } : t)),
    })),

  setOpenPositions: (positions) => set({ openPositions: positions }),

  updatePosition: (index, updates) =>
    set((state) => {
      const newPositions = [...state.openPositions]
      newPositions[index] = { ...newPositions[index], ...updates }
      return { openPositions: newPositions }
    }),

  addAlert: (alert) =>
    set((state) => ({
      alerts: [
        {
          ...alert,
          id: `alert-${Date.now()}`,
          timestamp: Date.now(),
        },
        ...state.alerts.slice(0, 9), // Keep last 10 alerts
      ],
    })),

  dismissAlert: (id) =>
    set((state) => ({
      alerts: state.alerts.map((a) => (a.id === id ? { ...a, read: true } : a)),
    })),

  toggleBot: () => set((state) => ({ botActive: !state.botActive })),

  setTradeSize: (size) => set({ tradeSize: size }),

  setRiskPercentage: (risk) => set({ riskPercentage: risk }),

  initializeDashboard: (priceData) =>
    set({
      btcPrice: priceData,
      priceHistory: [priceData],
    }),

  clearHistory: () =>
    set({
      trades: [],
      priceHistory: [],
      totalPnL: 0,
      winRate: 0,
      tradeCount: 0,
      alerts: [],
    }),
}))
