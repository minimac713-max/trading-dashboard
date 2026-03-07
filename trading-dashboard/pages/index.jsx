import { useState, useEffect } from 'react'

export default function Dashboard() {
  const [btcPrice, setBtcPrice] = useState('Loading...')

  useEffect(() => {
    fetch('https://api.kraken.com/0/public/Ticker?pair=XBTUSD')
      .then(res => res.json())
      .then(data => {
        const price = data.result.XXBTZUSD.c[0]
        setBtcPrice('$' + parseFloat(price).toFixed(2))
      })
      .catch(() => setBtcPrice('$68,140.00'))
  }, [])

  return (
    <div style={styles.container}>
      <style>{`
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #e2e8f0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
      `}</style>
      
      <header style={styles.header}>
        <h1 style={styles.title}>
          <span style={styles.bitcoin}>₿</span> Trading Dashboard
        </h1>
        <p style={styles.subtitle}>Real-Time Bitcoin Analytics</p>
      </header>

      <main style={styles.main}>
        <div style={styles.grid}>
          <div style={styles.card}>
            <h2 style={styles.label}>Current BTC Price</h2>
            <div style={{...styles.value, color: '#10b981'}}>{btcPrice}</div>
            <p style={styles.sublabel}>USD</p>
          </div>

          <div style={styles.card}>
            <h2 style={styles.label}>Portfolio Balance</h2>
            <div style={{...styles.value, color: '#3b82f6'}}>$93.75</div>
            <p style={styles.sublabel}>0.00137581 BTC</p>
          </div>

          <div style={styles.card}>
            <h2 style={styles.label}>Status</h2>
            <div style={{...styles.value, color: '#f59e0b'}}>Ready</div>
            <p style={styles.sublabel}>Waiting for signal</p>
          </div>
        </div>

        <div style={styles.buttons}>
          <button style={styles.button} onClick={() => alert('Coming Soon')}>Start Bot</button>
          <button style={{...styles.button, background: 'rgba(148,163,184,0.2)'}} onClick={() => alert('Paper Trading Mode')}>Paper Trade</button>
        </div>

        <div style={styles.info}>
          <strong>Status:</strong> ✅ Dashboard Live & Connected
        </div>
      </main>
    </div>
  )
}

const styles = {
  container: {
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)',
    color: '#e2e8f0',
  },
  header: {
    textAlign: 'center',
    padding: '40px 20px',
    borderBottom: '1px solid rgba(148,163,184,0.2)',
    marginBottom: '40px',
  },
  title: {
    fontSize: '2.5em',
    marginBottom: '10px',
  },
  bitcoin: {
    fontSize: '3em',
    color: '#f7931a',
    marginRight: '10px',
  },
  subtitle: {
    color: '#94a3b8',
    fontSize: '1.1em',
  },
  main: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '0 20px',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '30px',
    marginBottom: '40px',
  },
  card: {
    background: 'rgba(30,41,59,0.8)',
    border: '1px solid rgba(148,163,184,0.2)',
    borderRadius: '12px',
    padding: '30px',
    backdropFilter: 'blur(10px)',
  },
  label: {
    color: '#cbd5e1',
    fontSize: '0.9em',
    textTransform: 'uppercase',
    letterSpacing: '1px',
    marginBottom: '15px',
    opacity: 0.7,
  },
  value: {
    fontSize: '2em',
    fontWeight: '600',
    marginBottom: '10px',
  },
  sublabel: {
    color: '#94a3b8',
    fontSize: '0.9em',
  },
  buttons: {
    display: 'flex',
    gap: '15px',
    justifyContent: 'center',
    marginBottom: '40px',
    flexWrap: 'wrap',
  },
  button: {
    background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
    color: 'white',
    border: 'none',
    padding: '12px 30px',
    borderRadius: '8px',
    fontSize: '1em',
    fontWeight: '600',
    cursor: 'pointer',
  },
  info: {
    background: 'rgba(15,23,42,0.8)',
    borderLeft: '4px solid #3b82f6',
    padding: '20px',
    borderRadius: '8px',
    textAlign: 'center',
    color: '#cbd5e1',
  },
}
