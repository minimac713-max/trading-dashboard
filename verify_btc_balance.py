#!/usr/bin/env python3
"""
Verify BTC balance on Kraken and identify momentum signal
"""

import json
import time
import hmac
import hashlib
import base64
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime

class KrakenBalance:
    def __init__(self, api_key, private_key):
        self.api_key = api_key
        self.private_key = private_key
        self.api_url = "https://api.kraken.com"
    
    def sign_request(self, endpoint, data):
        """Sign request for Kraken API"""
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = hashlib.sha256(encoded).digest()
        
        signature = hmac.new(
            base64.b64decode(self.private_key),
            message,
            hashlib.sha512
        )
        
        return base64.b64encode(signature.digest()).decode()
    
    def get_balance(self):
        """Get account balance - BTC only"""
        try:
            endpoint = "/0/private/Balance"
            data = {"nonce": int(time.time() * 1000)}
            
            signature = self.sign_request(endpoint, data)
            
            headers = {
                "API-Key": self.api_key,
                "API-Sign": signature
            }
            
            postdata = urllib.parse.urlencode(data)
            url = self.api_url + endpoint
            
            req = urllib.request.Request(
                url,
                data=postdata.encode(),
                headers=headers,
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode())
            
            if result.get('error'):
                print(f"❌ API Error: {result['error']}")
                return None
            
            balance = result.get('result', {})
            
            # Look for XBT (Kraken's symbol for Bitcoin)
            btc_balance = balance.get('XXBT', {})
            if not btc_balance:
                # Try alternative symbol
                btc_balance = balance.get('XBT', {})
            
            available_btc = float(btc_balance.get('n', 0)) if 'n' in btc_balance else float(btc_balance.get('af', 0)) if 'af' in btc_balance else 0
            
            print(f"✅ Balance Retrieved Successfully")
            print(f"📊 Raw Balance Data: {json.dumps(balance, indent=2)}")
            
            return {
                'available': available_btc,
                'full_balance': balance
            }
            
        except Exception as e:
            print(f"❌ Failed to get balance: {e}")
            return None
    
    def get_ticker(self, pair="XXBTZUSD"):
        """Get current BTC price and recent history"""
        try:
            # Get ticker
            endpoint = f"/0/public/Ticker?pair={pair}"
            url = self.api_url + endpoint
            
            with urllib.request.urlopen(url, timeout=10) as response:
                result = json.loads(response.read().decode())
            
            if result.get('error'):
                print(f"❌ Ticker Error: {result['error']}")
                return None
            
            ticker = result['result'].get(pair, {})
            
            last_price = float(ticker['c'][0])  # Last trade close
            bid = float(ticker['b'][0])  # Best bid
            ask = float(ticker['a'][0])  # Best ask
            
            print(f"✅ Ticker Data Retrieved")
            print(f"  Current Price: ${last_price:.2f}")
            print(f"  Bid: ${bid:.2f}")
            print(f"  Ask: ${ask:.2f}")
            
            return {
                'price': last_price,
                'bid': bid,
                'ask': ask,
                'raw': ticker
            }
            
        except Exception as e:
            print(f"❌ Failed to get ticker: {e}")
            return None
    
    def get_ohlc(self, pair="XXBTZUSD", interval=1):
        """Get OHLC data for momentum analysis"""
        try:
            # interval 1 = 1 minute candles
            endpoint = f"/0/public/OHLC?pair={pair}&interval={interval}"
            url = self.api_url + endpoint
            
            with urllib.request.urlopen(url, timeout=10) as response:
                result = json.loads(response.read().decode())
            
            if result.get('error'):
                print(f"❌ OHLC Error: {result['error']}")
                return None
            
            ohlc = result['result'].get(pair, [])
            
            # Get last 5 candles for trend analysis
            recent = ohlc[-5:] if len(ohlc) >= 5 else ohlc
            
            print(f"✅ OHLC Data Retrieved ({len(ohlc)} total candles)")
            for candle in recent[-3:]:  # Show last 3
                ts, o, h, l, c, vwap, vol, count = candle
                print(f"  [Time {datetime.fromtimestamp(ts).strftime('%H:%M:%S')}] O:{float(o):.2f} H:{float(h):.2f} L:{float(l):.2f} C:{float(c):.2f}")
            
            return ohlc
            
        except Exception as e:
            print(f"❌ Failed to get OHLC: {e}")
            return None


def main():
    # Load keys
    with open('/Users/macdaddy/.openclaw/workspace/kraken_public_key.txt', 'r') as f:
        api_key = f.read().strip()
    
    with open('/Users/macdaddy/.openclaw/workspace/kraken_private_key.txt', 'r') as f:
        private_key = f.read().strip()
    
    print("="*60)
    print("🔗 KRAKEN BTC VERIFICATION & TRADE SIGNAL")
    print("="*60)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
    
    verifier = KrakenBalance(api_key, private_key)
    
    # Step 1: Get BTC balance
    print("📍 Step 1: Checking BTC Balance\n")
    balance_data = verifier.get_balance()
    
    if not balance_data:
        print("❌ Cannot proceed - balance check failed")
        return
    
    btc_available = balance_data['available']
    print(f"\n💰 BTC AVAILABLE: {btc_available:.6f} BTC\n")
    
    # Step 2: Get current ticker
    print("📍 Step 2: Checking Current Price\n")
    ticker = verifier.get_ticker()
    
    if not ticker:
        print("❌ Cannot proceed - price check failed")
        return
    
    current_price = ticker['price']
    usd_value = btc_available * current_price
    print(f"\n💵 CURRENT VALUE: {btc_available:.6f} BTC × ${current_price:.2f} = ${usd_value:.2f} USD\n")
    
    # Step 3: Get momentum signal
    print("📍 Step 3: Analyzing Momentum\n")
    ohlc = verifier.get_ohlc()
    
    signal = "🔄 NEUTRAL"  # Default
    if ohlc and len(ohlc) >= 3:
        recent = ohlc[-3:]
        closes = [float(c[4]) for c in recent]  # Get close prices
        
        if closes[-1] > closes[-2] > closes[-3]:
            signal = "📈 UPTREND - BUY SIGNAL"
        elif closes[-1] < closes[-2] < closes[-3]:
            signal = "📉 DOWNTREND - SELL SIGNAL"
        elif closes[-1] > closes[-2]:
            signal = "📈 BULLISH MOMENTUM"
        else:
            signal = "📉 BEARISH MOMENTUM"
    
    print(f"\n{signal}\n")
    
    # Summary
    print("="*60)
    print("VERIFICATION COMPLETE")
    print("="*60)
    print(f"✅ BTC Balance Confirmed: {btc_available:.6f} BTC")
    print(f"✅ Current Price: ${current_price:.2f} USD")
    print(f"✅ Account Value: ${usd_value:.2f} USD")
    print(f"✅ Trade Signal: {signal}")
    print(f"✅ Trading Parameters:")
    print(f"   - Goal: Double holdings (${usd_value:.2f} → ${usd_value*2:.2f})")
    print(f"   - Max per trade: $50 USD")
    print(f"   - Asset: Bitcoin only")
    print(f"   - Strategy: Momentum/Trend following with tight stops")
    print("="*60)
    
    return {
        'btc_balance': btc_available,
        'btc_price': current_price,
        'account_usd_value': usd_value,
        'signal': signal,
        'ready_to_trade': True
    }


if __name__ == "__main__":
    main()
