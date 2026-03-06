import { useEffect, useState } from 'react'

export default function Home() {
  const [btcPrice, setBtcPrice] = useState('68,140.00')

  useEffect(() => {
    const updatePrice = async () => {
      try {
        const response = await fetch('https://api.kraken.com/0/public/Ticker?pair=XBTUSD')
        const data = await response.json()
        const price = data.result.XXBTZUSD.c[0]
        setBtcPrice(parseFloat(price).toFixed(2))
      } catch (error) {
        console.error('Price fetch error:', error)
      }
    }

    updatePrice()
    const interval = setInterval(updatePrice, 10000)
    return () => clearInterval(interval)
  }, [])

  return (
    <>
      <style>{`
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }
        html, body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
          color: #e2e8f0;
          min-height: 100vh;
        }
        .container {
          max-width: 1200px;
          margin: 0 auto;
          padding: 20px;
        }
        header {
          text-align: center;
          padding: 40px 20px;
          border-bottom: 1px solid rgba(148, 163, 184, 0.2);
          margin-bottom: 40px;
        }
        header h1 {
          font-size: 2.5em;
          margin-bottom: 10px;
        }
        .bitcoin {
          font-size: 3em;
          color: #f7931a;
          margin-right: 10px;
        }
        header p {
          color: #94a3b8;
          font-size: 1.1em;
        }
        .dashboard {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 30px;
          margin-bottom: 40px;
        }
        .card {
          background: rgba(30, 41, 59, 0.8);
          border: 1px solid rgba(148, 163, 184, 0.2);
          border-radius: 12px;
          padding: 30px;
          backdrop-filter: blur(10px);
        }
        .card h2 {
          color: #cbd5e1;
          font-size: 0.9em;
          text-transform: uppercase;
          letter-spacing: 1px;
          margin-bottom: 15px;
          opacity: 0.7;
        }
        .card .value {
          font-size: 2em;
          font-weight: 600;
          margin-bottom: 10px;
        }
        .card .subtext {
          color: #94a3b8;
          font-size: 0.9em;
        }
        .price { color: #10b981; }
        .balance { color: #3b82f6; }
        .status { color: #f59e0b; }
        .controls {
          display: flex;
          gap: 15px;
          justify-content: center;
          margin-bottom: 40px;
          flex-wrap: wrap;
        }
        button {
          background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
          color: white;
          border: none;
          padding: 12px 30px;
          border-radius: 8px;
          font-size: 1em;
          font-weight: 600;
          cursor: pointer;
        }
        button:hover {
          transform: translateY(-2px);
          box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
        }
        .button-secondary {
          background: rgba(148, 163, 184, 0.2);
          color: #cbd5e1;
        }
        .info-box {
          background: rgba(15, 23, 42, 0.8);
          border-left: 4px solid #3b82f6;
          padding: 20px;
          border-radius: 8px;
          margin-top: 30px;
          text-align: center;
        }
        .info-box p {
          color: #cbd5e1;
          line-height: 1.6;
        }
      `}</style>

      <div className="container">
        <header>
          <h1><span className="bitcoin">₿</span>Trading Dashboard</h1>
          <p>Real-Time Bitcoin Analytics & Trading</p>
        </header>
        
        <div className="dashboard">
          <div className="card">
            <h2>Current BTC Price</h2>
            <div className="value price">${btcPrice}</div>
            <div className="subtext">USD</div>
          </div>
          
          <div className="card">
            <h2>Portfolio Balance</h2>
            <div className="value balance">$93.75</div>
            <div className="subtext">0.00137581 BTC</div>
          </div>
          
          <div className="card">
            <h2>Trading Status</h2>
            <div className="value status">Ready</div>
            <div className="subtext">Waiting for signal</div>
          </div>
        </div>
        
        <div className="controls">
          <button onClick={() => alert('Coming soon: Start Trading Bot')}>Start Bot</button>
          <button className="button-secondary" onClick={() => alert('Simulator mode - Risk free testing')}>Paper Trade</button>
          <button className="button-secondary" onClick={() => alert('View your trading strategy')}>View Strategy</button>
        </div>
        
        <div className="info-box">
          <p>
            <strong>Dashboard Status:</strong> ✅ Live & Connected<br/>
            All systems operational. Ready to start trading.
          </p>
        </div>
      </div>
    </>
  )
}
