#!/usr/bin/env python3
"""
Bot Activity Monitor - Real-Time Dashboard Backend
Tracks all bot activities, trades, and system status
Outputs JSON for dashboard consumption
"""

import json
import os
import glob
from datetime import datetime
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
TRADING_DIR = os.path.join(WORKSPACE, "trading")
LOG_DIR = os.path.join(TRADING_DIR, "logs")
MONITOR_FILE = os.path.join(TRADING_DIR, "MONITOR.json")

# ============================================================================
# MONITOR ALL BOT ACTIVITY
# ============================================================================

def scan_active_bots():
    """Scan for currently running bot processes"""
    import subprocess
    
    try:
        result = subprocess.run(
            ["pgrep", "-f", "kraken_.*hunter.py"],
            capture_output=True,
            text=True
        )
        pids = result.stdout.strip().split('\n')
        return [int(p) for p in pids if p]
    except:
        return []

def parse_trading_logs():
    """Extract trade data from log files"""
    trades = []
    
    if not os.path.exists(LOG_DIR):
        return trades
    
    log_files = glob.glob(os.path.join(LOG_DIR, "*.log"))
    
    for log_file in log_files:
        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()
                
            current_trade = None
            for line in lines[-100:]:  # Last 100 lines
                if "TRADE #" in line and "HUNTING" in line:
                    if current_trade:
                        trades.append(current_trade)
                    current_trade = {
                        'file': os.path.basename(log_file),
                        'timestamp': None,
                        'status': 'hunting'
                    }
                elif "BUY:" in line and current_trade:
                    current_trade['status'] = 'long'
                    current_trade['entry'] = extract_price(line)
                elif "SELL:" in line and current_trade:
                    current_trade['status'] = 'closed'
                    current_trade['exit'] = extract_price(line)
                elif "PROFIT:" in line and current_trade:
                    current_trade['profit'] = extract_profit(line)
            
            if current_trade:
                trades.append(current_trade)
        except:
            pass
    
    return trades

def extract_price(line):
    """Extract price from log line"""
    try:
        parts = line.split('$')
        if len(parts) > 1:
            price_str = parts[1].split()[0]
            return float(price_str)
    except:
        pass
    return 0

def extract_profit(line):
    """Extract profit from log line"""
    try:
        if '$' in line:
            parts = line.split('$')
            if len(parts) > 1:
                profit_str = parts[1].split()[0]
                return float(profit_str)
    except:
        pass
    return 0

def get_account_balance():
    """Get current account balance from Kraken API"""
    try:
        import ccxt
        creds_file = os.path.expanduser("~/.kraken/api.json")
        with open(creds_file) as f:
            creds = json.load(f)
        
        kraken = ccxt.kraken({
            'apiKey': creds['apiKey'],
            'secret': creds['secret'],
            'enableRateLimit': True,
        })
        
        balance = kraken.fetch_balance()
        return {
            'btc': balance.get('BTC', {}).get('free', 0),
            'usd': balance.get('USD', {}).get('free', 0),
            'total_btc': balance.get('BTC', {}).get('total', 0),
            'total_usd': balance.get('USD', {}).get('total', 0)
        }
    except:
        return None

def get_btc_price():
    """Get current BTC price"""
    try:
        import ccxt
        kraken = ccxt.kraken()
        ticker = kraken.fetch_ticker('BTC/USD')
        return {
            'price': ticker['last'],
            'high_24h': ticker['high'],
            'low_24h': ticker['low'],
            'change_24h': ticker['percentage']
        }
    except:
        return None

# ============================================================================
# BUILD MONITOR JSON
# ============================================================================

def build_monitor():
    """Build complete monitor status JSON"""
    
    active_pids = scan_active_bots()
    trades = parse_trading_logs()
    balance = get_account_balance()
    btc_price = get_btc_price()
    
    monitor = {
        'timestamp': datetime.now().isoformat(),
        'status': 'operational',
        'active_bots': len(active_pids),
        'pids': active_pids,
        'recent_trades': trades[-5:] if trades else [],
        'total_trades_today': len(trades),
        'account': balance or {},
        'market': btc_price or {},
        'dashboard_url': 'https://trading-dashboard-minimac713-max.vercel.app/'
    }
    
    return monitor

# ============================================================================
# MAIN
# ============================================================================

def main():
    monitor = build_monitor()
    
    # Write to file
    with open(MONITOR_FILE, 'w') as f:
        json.dump(monitor, f, indent=2)
    
    # Also print to stdout
    print(json.dumps(monitor, indent=2))
    
    print(f"\n✅ Monitor updated: {MONITOR_FILE}")

if __name__ == "__main__":
    main()
