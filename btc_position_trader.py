#!/usr/bin/env python3
"""
Bitcoin Position Trader - Execute $50 long position
Mission: Convert BTC balance to position, target 100% gain with -8% stop loss
"""

import requests
import json
import time
import hashlib
import hmac
import base64
from datetime import datetime, timedelta
from urllib.parse import urlencode

# Kraken API Configuration
API_URL = "https://api.kraken.com"
API_KEY = "tuWRMuJOa4RxQfjaPkXBfubIKUfXtqDkSa9lH5v2qjahK/A6kFsfXYPQ"
API_SECRET = "2H85dro7ismiOHEQeEcJBknmK37Nv2/ls9xwrUp+tDEiFFt/+x1zvcSFhI0Cz67m0nNOc1NbH9lDKVaUq5Qugg=="

# Mission Parameters
CAPITAL_USD = 50.0
TARGET_USD = 100.0
STOP_LOSS_PCT = -8.0
TAKE_PROFIT_PCT = 100.0
DEADLINE_MINUTES = 60

mission_start = datetime.now()

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
    """Execute Kraken API request"""
    if data is None:
        data = {}
    
    try:
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
    except Exception as e:
        print(f"[ERROR] API request failed: {e}")
        return {'error': [str(e)]}

def get_balance():
    """Get full account balance"""
    try:
        resp = kraken_request('Balance', {})
        if 'result' in resp:
            return resp['result']
        return {}
    except Exception as e:
        print(f"[ERROR] Balance check failed: {e}")
        return {}

def get_btc_price():
    """Get current BTC/USD price"""
    try:
        resp = kraken_request('Ticker', {'pair': 'BTCUSD'}, private=False)
        if 'result' in resp and 'BTCUSD' in resp['result']:
            ticker = resp['result']['BTCUSD']
            price = float(ticker['c'][0])  # Last close price
            return price
    except Exception as e:
        print(f"[ERROR] BTC price fetch failed: {e}")
    return None

def check_momentum():
    """Check for uptrend momentum in BTC"""
    try:
        # Get OHLC data for last 4 hours
        resp = kraken_request('OHLC', {'pair': 'BTCUSD', 'interval': 60}, private=False)
        if 'result' not in resp:
            return False, "No OHLC data"
        
        ohlc = resp['result'].get('BTCUSD', [])
        if len(ohlc) < 2:
            return False, "Insufficient OHLC data"
        
        # Check if price is trending up (last close > previous close)
        prev_close = float(ohlc[-2][4])  # Close of previous candle
        curr_close = float(ohlc[-1][4])  # Close of current candle
        
        uptrend = curr_close > prev_close
        change_pct = ((curr_close - prev_close) / prev_close) * 100
        
        return uptrend, f"Momentum: {change_pct:.2f}%"
    except Exception as e:
        return False, f"Momentum check failed: {e}"

def place_market_order(side, volume):
    """Place market order"""
    try:
        data = {
            'pair': 'BTCUSD',
            'type': side,  # buy or sell
            'ordertype': 'market',
            'volume': str(f'{volume:.8f}')
        }
        
        resp = kraken_request('AddOrder', data)
        if 'result' in resp:
            return True, resp['result']
        else:
            return False, resp.get('error', ['Unknown error'])
    except Exception as e:
        return False, str(e)

def place_limit_order(side, volume, price):
    """Place limit order"""
    try:
        data = {
            'pair': 'BTCUSD',
            'type': side,
            'ordertype': 'limit',
            'price': str(f'{price:.2f}'),
            'volume': str(f'{volume:.8f}')
        }
        
        resp = kraken_request('AddOrder', data)
        if 'result' in resp:
            return True, resp['result']
        else:
            return False, resp.get('error', ['Unknown error'])
    except Exception as e:
        return False, str(e)

def execute_trade():
    """Main trade execution"""
    print("\n" + "="*70)
    print("🚀 BITCOIN POSITION TRADER - EXECUTION START")
    print("="*70)
    print(f"⏰ Start: {mission_start.strftime('%I:%M:%S %p CT')}")
    print(f"📋 Mission: Enter $50 BTC position → Target $100 (+100%)")
    print(f"🛑 Stop Loss: -8% | 🎯 Take Profit: +100%")
    print(f"⏱️  Deadline: {(mission_start + timedelta(minutes=DEADLINE_MINUTES)).strftime('%I:%M:%S %p CT')}")
    print("="*70)
    
    # Step 1: Check balance
    print("\n[STEP 1] Checking account balance...")
    balance = get_balance()
    
    btc_balance = float(balance.get('XXBT', {}).get('availability', 0) or balance.get('XXBT', {}).get('free', 0) or 0)
    usd_balance = float(balance.get('ZUSD', {}).get('availability', 0) or balance.get('ZUSD', {}).get('free', 0) or 0)
    
    print(f"   BTC Available: {btc_balance:.8f}")
    print(f"   USD Available: ${usd_balance:.2f}")
    
    if btc_balance < 0.001 and usd_balance < CAPITAL_USD:
        print(f"[ERROR] Insufficient balance. Need $50 USD or 0.001 BTC minimum")
        return False
    
    # Step 2: Get BTC price and check momentum
    print("\n[STEP 2] Checking market conditions...")
    btc_price = get_btc_price()
    if not btc_price:
        print("[ERROR] Could not get BTC price")
        return False
    
    print(f"   BTC/USD Price: ${btc_price:.2f}")
    
    uptrend, momentum_msg = check_momentum()
    print(f"   Uptrend Status: {uptrend}")
    print(f"   {momentum_msg}")
    
    # Step 3: Calculate position sizing
    print("\n[STEP 3] Position sizing...")
    
    if usd_balance >= CAPITAL_USD:
        # Use USD to buy BTC
        btc_to_buy = CAPITAL_USD / btc_price
        position_source = "USD"
        position_amount = btc_to_buy
        position_value_usd = CAPITAL_USD
    else:
        # Use existing BTC
        btc_to_buy = 0
        position_source = "Existing BTC"
        position_amount = btc_balance
        position_value_usd = btc_balance * btc_price
    
    print(f"   Source: {position_source}")
    print(f"   Position Size: {position_amount:.8f} BTC")
    print(f"   Position Value (USD): ${position_value_usd:.2f}")
    print(f"   Entry Price: ${btc_price:.2f}")
    
    # Calculate levels
    stop_loss_price = btc_price * (1 + STOP_LOSS_PCT/100)
    take_profit_price = btc_price * (1 + TAKE_PROFIT_PCT/100)
    
    print(f"\n[STEP 4] Risk/Reward Levels:")
    print(f"   Entry:       ${btc_price:.2f}")
    print(f"   Stop Loss:   ${stop_loss_price:.2f} (-8% risk)")
    print(f"   Take Profit: ${take_profit_price:.2f} (+100% target)")
    
    # Step 5: Place entry order (only if we need to buy BTC)
    print(f"\n[STEP 5] Placing entry order...")
    if btc_to_buy > 0.0001:
        success, result = place_market_order('buy', btc_to_buy)
        if success:
            print(f"   ✅ BUY order placed!")
            print(f"      Order ID(s): {result.get('txid')}")
            entry_price = btc_price
        else:
            print(f"   ❌ Order failed: {result}")
            return False
    else:
        print(f"   ℹ️  Using existing BTC position (no buy order needed)")
        entry_price = btc_price
    
    # Step 6: Monitor position
    print(f"\n[STEP 6] Position monitoring active...")
    monitor_position(entry_price, position_amount, stop_loss_price, take_profit_price)
    
    return True

def monitor_position(entry_price, position_size, stop_loss, take_profit):
    """Monitor position until exit condition"""
    print(f"\n   Monitoring {position_size:.8f} BTC position")
    print(f"   Checks every 30 seconds, updates every 5 minutes\n")
    
    last_update = time.time()
    check_count = 0
    
    while datetime.now() < mission_start + timedelta(minutes=DEADLINE_MINUTES):
        check_count += 1
        current_price = get_btc_price()
        
        if not current_price:
            time.sleep(30)
            continue
        
        current_value = position_size * current_price
        entry_value = position_size * entry_price
        pnl = current_value - entry_value
        pnl_pct = (pnl / entry_value) * 100 if entry_value > 0 else 0
        
        # Update display every 5 minutes
        if time.time() - last_update >= 300:
            time_left = (mission_start + timedelta(minutes=DEADLINE_MINUTES) - datetime.now()).total_seconds() / 60
            print(f"   [{datetime.now().strftime('%H:%M:%S')}] Price: ${current_price:.2f} | P&L: ${pnl:.2f} ({pnl_pct:.2f}%) | Time left: {time_left:.0f}m")
            last_update = time.time()
        
        # Check exit conditions
        if current_price >= take_profit:
            print(f"\n✅ TAKE PROFIT HIT! Price reached ${take_profit:.2f}")
            print(f"   Final Value: ${current_value:.2f}")
            print(f"   Profit: ${pnl:.2f} ({pnl_pct:.2f}%)")
            print(f"   Status: MISSION SUCCESS ✅")
            close_position(position_size, "Take profit")
            return True
        
        if current_price <= stop_loss:
            print(f"\n🛑 STOP LOSS HIT! Price hit ${stop_loss:.2f}")
            print(f"   Current Value: ${current_value:.2f}")
            print(f"   Loss: ${pnl:.2f} ({pnl_pct:.2f}%)")
            print(f"   Status: STOP LOSS TRIGGERED ⚠️")
            close_position(position_size, "Stop loss")
            return False
        
        time.sleep(30)
    
    # Deadline reached
    current_price = get_btc_price()
    if current_price:
        current_value = position_size * current_price
        entry_value = position_size * entry_price
        pnl = current_value - entry_value
        pnl_pct = (pnl / entry_value) * 100 if entry_value > 0 else 0
        print(f"\n⏰ DEADLINE REACHED")
        print(f"   Final Price: ${current_price:.2f}")
        print(f"   Final Value: ${current_value:.2f}")
        print(f"   P&L: ${pnl:.2f} ({pnl_pct:.2f}%)")
        close_position(position_size, "Deadline")
        return pnl >= CAPITAL_USD

def close_position(position_size, reason):
    """Close position with market order"""
    print(f"\n[ACTION] Closing position - {reason}")
    # In production, would place actual sell order
    # For now, log the intention
    print(f"   Would execute: SELL {position_size:.8f} BTC @ market")
    print("="*70)

if __name__ == '__main__':
    execute_trade()
