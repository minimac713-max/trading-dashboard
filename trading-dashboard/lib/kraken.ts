import axios from 'axios'
import { PriceData } from './store'

const KRAKEN_API_URL = 'https://api.kraken.com/0/public'

interface KrakenTickerResponse {
  [key: string]: {
    a: [string, number] // Ask price, whole lot volume
    b: [string, number] // Bid price, whole lot volume
    c: [string, number] // Last trade closed price, lot volume
    h: [string, string] // High price, High price (last 24h)
    l: [string, string] // Low price, Low price (last 24h)
    o: [string, string] // Opening price, Opening price (last 24h)
    p: [string, string] // Volume weighted average price, Volume weighted average price (last 24h)
    t: [number, number] // Number of trades, Number of trades (last 24h)
    v: [string, string] // Volume, Volume (last 24h)
  }
}

interface KrakenOHLCResponse {
  [key: string]: Array<
    [number, string, string, string, string, string, string, number]
  >
  last?: number
}

export async function fetchKrakenPrice(): Promise<PriceData> {
  try {
    const response = await axios.get<{ result: KrakenTickerResponse; error: string[] }>(
      `${KRAKEN_API_URL}/Ticker`,
      {
        params: {
          pair: 'XBTUSDT',
        },
      }
    )

    if (response.data.error && response.data.error.length > 0) {
      throw new Error(response.data.error[0])
    }

    const tickerData = response.data.result['XBTUSDT']
    const price = parseFloat(tickerData.c[0])
    const high24h = parseFloat(tickerData.h[1])
    const low24h = parseFloat(tickerData.l[1])
    const open24h = parseFloat(tickerData.o[1])

    const change24h = price - open24h

    return {
      price,
      timestamp: Date.now(),
      change24h,
      high24h,
      low24h,
    }
  } catch (error) {
    console.error('Error fetching Kraken price:', error)
    // Return mock data for demo purposes
    return {
      price: 42500 + Math.random() * 1000,
      timestamp: Date.now(),
      change24h: Math.random() * 1000 - 500,
      high24h: 43000,
      low24h: 42000,
    }
  }
}

export async function fetchKrakenOHLC(
  pair: string = 'XBTUSDT',
  interval: number = 60
): Promise<Array<[number, string, string, string, string, string, string, number]>> {
  try {
    const response = await axios.get<{
      result: KrakenOHLCResponse
      error: string[]
    }>(`${KRAKEN_API_URL}/OHLC`, {
      params: {
        pair,
        interval,
      },
    })

    if (response.data.error && response.data.error.length > 0) {
      throw new Error(response.data.error[0])
    }

    return response.data.result[pair] || []
  } catch (error) {
    console.error('Error fetching Kraken OHLC:', error)
    return []
  }
}

export async function fetchKrakenCandles(
  pair: string = 'XBTUSDT',
  interval: number = 60
): Promise<
  Array<{
    timestamp: number
    open: number
    high: number
    low: number
    close: number
    volume: number
  }>
> {
  try {
    const ohlcData = await fetchKrakenOHLC(pair, interval)

    return ohlcData.map((candle) => ({
      timestamp: candle[0] * 1000, // Convert to milliseconds
      open: parseFloat(candle[1]),
      high: parseFloat(candle[2]),
      low: parseFloat(candle[3]),
      close: parseFloat(candle[4]),
      volume: parseFloat(candle[7]),
    }))
  } catch (error) {
    console.error('Error processing candles:', error)
    return []
  }
}

// WebSocket connection for real-time price updates
export function subscribeToKrakenPriceUpdates(
  callback: (data: PriceData) => void
): WebSocket | null {
  try {
    const ws = new WebSocket('wss://ws.kraken.com')

    ws.onopen = () => {
      const subscription = {
        event: 'subscribe',
        pair: ['XBT/USD'],
        subscription: {
          name: 'ticker',
        },
      }
      ws.send(JSON.stringify(subscription))
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)

        // Handle subscription confirmation
        if (data.event === 'subscriptionStatus') {
          console.log('Subscribed to ticker updates')
          return
        }

        // Handle ticker data
        if (Array.isArray(data) && data.length >= 2 && data[data.length - 1] === 'ticker') {
          const tickerData = data[1]
          if (tickerData) {
            const currentPrice = parseFloat(tickerData.c[0])
            const change24h = parseFloat(tickerData.o[1]) ? currentPrice - parseFloat(tickerData.o[1]) : 0

            callback({
              price: currentPrice,
              timestamp: Date.now(),
              change24h,
              high24h: parseFloat(tickerData.h[1]),
              low24h: parseFloat(tickerData.l[1]),
            })
          }
        }
      } catch (error) {
        console.error('Error processing WebSocket message:', error)
      }
    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    ws.onclose = () => {
      console.log('WebSocket closed')
    }

    return ws
  } catch (error) {
    console.error('Error creating WebSocket:', error)
    return null
  }
}

export function subscribeToKrakenOHLC(
  interval: number = 1,
  callback: (data: any) => void
): WebSocket | null {
  try {
    const ws = new WebSocket('wss://ws.kraken.com')

    ws.onopen = () => {
      const subscription = {
        event: 'subscribe',
        pair: ['XBT/USD'],
        subscription: {
          name: 'ohlc',
          interval,
        },
      }
      ws.send(JSON.stringify(subscription))
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)

        if (data.event === 'subscriptionStatus') {
          console.log('Subscribed to OHLC updates')
          return
        }

        if (Array.isArray(data) && data.length >= 2) {
          callback(data)
        }
      } catch (error) {
        console.error('Error processing OHLC WebSocket message:', error)
      }
    }

    ws.onerror = (error) => {
      console.error('OHLC WebSocket error:', error)
    }

    return ws
  } catch (error) {
    console.error('Error creating OHLC WebSocket:', error)
    return null
  }
}
