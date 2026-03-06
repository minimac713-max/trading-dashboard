#!/usr/bin/env python3
"""
Live Kraken Trading Executor - $50 to $100 in 2 hours
Mission: Execute 1-2 crypto positions with strict stop/limit management
"""

import requests
import json
import time
import hashlib
import hmac
import base64
from datetime import datetime
from urllib.parse import urlencode

# Kraken API Configuration
API_URL = "https://api.kraken.com"
API_KEY = "tuWRMuJOa4RxQfjaPkXBfubIKUfXtqDkSa9lH5v2qjahK/A6kFsfXYPQ"
API_SECRET = "2H85dro7ismiOHEQeEcJBknmK37Nv2/ls9xwrUp+tDEiFFt/+x1zvcSFhI0Cz67m0nNOc1NbH9lDKVaUq5Qugg=="

# Mission Parameters
CAPITAL = 50.0
TARGET = 100.0
DEADLINE_MINUTES = 120
STOP_LOSS_PCT = -3.0
TAKE_PROFIT_PCT = 100.0

# Trading State
mission_start = time.time()
positions = {}
entry_log = []

def get_kraken_signature(urlpath, data, secret):
    """Generate Kraken API signature"""
    postdata = urlencode(data)
    encoded = (str(data.get('nonce', '')) + postdata).encode()
    message = hashlib.sha256(encoded).digest()
    signature = base64.b64encode(
        hmac.new(base64.b64decode(secret), message, hashlib.sha512).digest()
    ).decode()
    return signature

def kraken_request(endpoint, data=None, private=True):
    """Execute authenticated Kraken API request"""
    if data is None:
        data = {}
    
    if private:
        data['nonce'] = str(int(time.time() * 1000))
        headers = {
            'API-Sign': get_kraken_signature(f'/0/private/{endpoint}', data, API_SECRET),
            'API-Key': API_KEY
        }
        response = requests.post(f'{API_URL}/0/private/{endpoint}', 
                                data=data, headers=headers, timeout=10)
    else:
        response = requests.get(f'{API_URL}/0/public/{endpoint}', 
                               params=data, timeout=10)
    
    return response.json()

def get_current_prices():
    """Fetch current BTC/ETH/XRP prices"""
    try:
        pairs = ['BTCUSD', 'ETHUSD', 'XRPUSD']
        result = {}
        for pair in pairs:
            resp = kraken_request('Ticker', {'pair': pair}, private=False)
            if 'result' in resp and pair in resp['result']:
                last_price = float(resp['result'][pair]['c'][0])
                result[pair] = last_price
        return result
    except Exception as e:
        print(f"❌ Error fetching prices: {e}")
        return {}

def get_account_balance():
    """Check available USD balance"""
    try:
        resp = kraken_request('Balance', {})
        if 'result' in resp and 'USD' in resp['result']:
            return float(resp['result']['USD'])
        return 0.0
    except Exception as e:
        print(f"❌ Error fetching balance: {e}")
        return 0.0

def place_order(pair, side, volume, price_type='market', limit_price=None, stop_price=None):
    """Place market or limit order with optional stop loss"""
    try:
        data = {
            'pair': pair,
            'type': side,  # buy or sell
            'ordertype': price_type,  # market, limit, etc
            'volume': str(volume)
        }
        
        if price_type == 'limit' and limit_price:
            data['price'] = str(limit_price)
        
        if stop_price:
            data['stopLossPrice'] = str(stop_price)
        
        resp = kraken_request('AddOrder', data)
        return resp
    except Exception as e:
        print(f"❌ Error placing order: {e}")
        return {'error': [str(e)]}

def execute_trading_strategy():
    """Execute the $50→$100 trading strategy"""
    global positions, entry_log
    
    print("=" * 60)
    print("🚀 MISSION START: $50 → $100 in 2 hours")
    print(f"⏰ Start: {datetime.now().strftime('%H:%M:%S CST')}")
    print("=" * 60)
    
    # Check balance
    balance = get_account_balance()
    print(f"💰 Available USD: ${balance:.2f}")
    
    if balance < CAPITAL:
        print(f"❌ Insufficient balance. Need ${CAPITAL}, have ${balance:.2f}")
        return False
    
    # Get current prices
    prices = get_current_prices()
    if not prices:
        print("❌ Could not fetch market prices")
        return False
    
    print(f"\n📊 Current Prices:")
    for pair, price in prices.items():
        print(f"   {pair}: ${price:.2f}")
    
    # Allocate capital: 50% BTC, 50% ETH (aggressive growth strategy)
    allocation = {
        'BTCUSD': 25.0,
        'ETHUSD': 25.0
    }
    
    print(f"\n📍 Position Allocation:")
    
    for pair, usd_amount in allocation.items():
        if pair not in prices:
            print(f"   ⚠️  Skipping {pair} - price unavailable")
            continue
        
        current_price = prices[pair]
        volume = usd_amount / current_price
        stop_loss_price = current_price * (1 + STOP_LOSS_PCT / 100)
        take_profit_price = current_price * (1 + TAKE_PROFIT_PCT / 100)
        
        print(f"\n   {pair}:")
        print(f"      Amount: ${usd_amount:.2f}")
        print(f"      Volume: {volume:.8f}")
        print(f"      Entry: ${current_price:.2f}")
        print(f"      Stop Loss: ${stop_loss_price:.2f} ({STOP_LOSS_PCT}%)")
        print(f"      Take Profit: ${take_profit_price:.2f} ({TAKE_PROFIT_PCT}%)")
        
        # Place buy order
        result = place_order(pair, 'buy', volume, 'market')
        
        if 'result' in result:
            order_data = result['result']
            txid = order_data.get('txid', ['unknown'])[0]
            entry_log.append({
                'pair': pair,
                'side': 'buy',
                'volume': volume,
                'entry_price': current_price,
                'stop_loss': stop_loss_price,
                'take_profit': take_profit_price,
                'timestamp': datetime.now().isoformat(),
                'order_id': txid
            })
            positions[pair] = {
                'volume': volume,
                'entry_price': current_price,
                'stop_loss': stop_loss_price,
                'take_profit': take_profit_price,
                'order_id': txid,
                'status': 'open'
            }
            print(f"      ✅ Order placed: {txid}")
        else:
            print(f"      ❌ Order failed: {result.get('error', ['unknown error'])}")
    
    print("\n" + "=" * 60)
    print("📝 ENTRY LOG:")
    print(json.dumps(entry_log, indent=2))
    return True

def monitor_positions(check_interval=1800):  # 30 minute intervals
    """Monitor open positions and execute exits"""
    global positions, mission_start
    
    print("\n⏱️  Monitoring positions... (30-min updates)")
    
    while True:
        elapsed = time.time() - mission_start
        elapsed_minutes = elapsed / 60
        
        if elapsed_minutes >= DEADLINE_MINUTES:
            print("\n⏰ DEADLINE REACHED - Closing all positions")
            close_all_positions(reason="Deadline expired")
            return
        
        print(f"\n📍 Update: {elapsed_minutes:.1f} min / {DEADLINE_MINUTES} min")
        print(f"   Time: {datetime.now().strftime('%H:%M:%S CST')}")
        
        # Check each position
        prices = get_current_prices()
        total_value = 0
        
        for pair, pos in positions.items():
            if pos['status'] != 'open':
                continue
            
            current_price = prices.get(pair, pos['entry_price'])
            position_value = pos['volume'] * current_price
            entry_value = pos['volume'] * pos['entry_price']
            pnl = position_value - entry_value
            pnl_pct = (pnl / entry_value) * 100 if entry_value > 0 else 0
            
            print(f"\n   {pair}:")
            print(f"      Current Price: ${current_price:.2f}")
            print(f"      Position Value: ${position_value:.2f}")
            print(f"      P&L: ${pnl:.2f} ({pnl_pct:.2f}%)")
            
            total_value += position_value
            
            # Check exit conditions
            if current_price >= pos['take_profit']:
                print(f"      🎯 TAKE PROFIT HIT! Closing...")
                close_position(pair, reason="Take profit reached")
            elif current_price <= pos['stop_loss']:
                print(f"      🛑 STOP LOSS HIT! Closing...")
                close_position(pair, reason="Stop loss triggered")
        
        # Check total portfolio
        total_pnl = total_value - CAPITAL
        total_pnl_pct = (total_pnl / CAPITAL) * 100 if CAPITAL > 0 else 0
        
        print(f"\n   📊 Portfolio:")
        print(f"      Total Value: ${total_value:.2f}")
        print(f"      P&L: ${total_pnl:.2f} ({total_pnl_pct:.2f}%)")
        
        if total_value >= TARGET:
            print(f"      🎉 TARGET REACHED! Closing all...")
            close_all_positions(reason="Target reached")
            return
        
        # Check if all positions closed
        if all(pos['status'] == 'closed' for pos in positions.values()):
            print("\n✅ All positions closed")
            return
        
        time.sleep(check_interval)

def close_position(pair, reason=""):
    """Close a specific position"""
    try:
        pos = positions[pair]
        # Market sell
        result = place_order(pair, 'sell', pos['volume'], 'market')
        positions[pair]['status'] = 'closed'
        print(f"   ✅ {pair} closed - {reason}")
    except Exception as e:
        print(f"   ❌ Error closing {pair}: {e}")

def close_all_positions(reason=""):
    """Emergency close all open positions"""
    print(f"\n🔴 CLOSING ALL POSITIONS - {reason}")
    for pair in positions:
        if positions[pair]['status'] == 'open':
            close_position(pair, reason)
    
    # Final report
    final_value = 0
    for pair, pos in positions.items():
        if pair in get_current_prices():
            final_value += pos['volume'] * get_current_prices()[pair]
    
    final_pnl = final_value - CAPITAL
    print("\n" + "=" * 60)
    print("📊 MISSION FINAL REPORT")
    print("=" * 60)
    print(f"Starting Capital: ${CAPITAL:.2f}")
    print(f"Final Value: ${final_value:.2f}")
    print(f"P&L: ${final_pnl:.2f}")
    print(f"Return: {(final_pnl/CAPITAL)*100:.2f}%")
    print(f"Status: {'SUCCESS ✅' if final_value >= TARGET else 'TIMEOUT ⏰'}")
    print("=" * 60)

if __name__ == '__main__':
    if execute_trading_strategy():
        monitor_positions()
    else:
        print("\n❌ Mission failed to start")
