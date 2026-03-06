import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Trading Dashboard | Real-Time BTC Analytics',
  description: 'Professional trading dashboard with live Kraken API data, performance metrics, and trade management.',
  keywords: ['trading', 'bitcoin', 'kraken', 'dashboard', 'real-time'],
  viewport: 'width=device-width, initial-scale=1',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='50' font-size='50' text-anchor='middle' dominant-baseline='middle'>₿</text></svg>" />
      </head>
      <body className="bg-slate-900">
        <div className="min-h-screen flex flex-col">
          {children}
        </div>
      </body>
    </html>
  )
}
