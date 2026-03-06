#!/usr/bin/env python3
"""
Verify BTC balance using krakenex library
"""

import krakenex
from pprint import pprint
from datetime import datetime

def main():
    print("="*60)
    print("🔗 KRAKEN BTC VERIFICATION")
    print("="*60)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
    
    # Load API keys
    try:
        with open('/Users/macdaddy/.openclaw/workspace/kraken_public_key.txt', 'r') as f:
            api_key = f.read().strip()
        
        with open('/Users/macdaddy/.openclaw/workspace/kraken_private_key.txt', 'r') as f:
            api_secret = f.read().strip()
        
        print(f"✅ Keys loaded")
        print(f"   Public: {api_key[:20]}...")
        print(f"   Secret: {api_secret[:20]}...\n")
        
    except Exception as e:
        print(f"❌ Failed to load keys: {e}")
        return
    
    # Initialize Kraken API
    try:
        k = krakenex.API()
        k.set_key(api_key, api_secret)
        print(f"✅ Kraken API initialized\n")
        
    except Exception as e:
        print(f"❌ Failed to initialize API: {e}")
        return
    
    # Get account balance
    print("📍 Fetching Account Balance...\n")
    try:
        balance = k.query_private('Balance')
        
        if balance['error']:
            print(f"❌ API Error: {balance['error']}")
            print(f"Response: {balance}")
            return
        
        result = balance.get('result', {})
        print("✅ Balance Retrieved Successfully\n")
        
        # Find BTC balance
        btc_balance = None
        btc_key = None
        
        for key in ['XXBT', 'XBT', 'BTC']:
            if key in result:
                btc_balance = float(result[key])
                btc_key = key
                break
        
        if btc_balance is None:
            print("❌ No BTC balance found in account")
            print(f"Available balances: {list(result.keys())}")
            print(f"Full result: {result}")
            return
        
        print(f"💰 BTC Balance: {btc_balance:.8f} BTC (key: {btc_key})")
        
        # Get current price
        print("\n📍 Fetching Current Price...\n")
        ticker = k.query_public('Ticker', {'pair': 'XXBTZUSD'})
        
        if ticker['error']:
            print(f"❌ Ticker Error: {ticker['error']}")
            return
        
        btc_price = float(ticker['result']['XXBTZUSD']['c'][0])
        usd_value = btc_balance * btc_price
        
        print(f"✅ Current Price Retrieved")
        print(f"   BTC Price: ${btc_price:.2f}")
        print(f"   Account Value: {btc_balance:.8f} BTC × ${btc_price:.2f} = ${usd_value:.2f} USD")
        
        # Get OHLC for signal
        print("\n📍 Analyzing Price Action...\n")
        ohlc = k.query_public('OHLC', {'pair': 'XXBTZUSD', 'interval': 1})
        
        if not ohlc['error'] and 'XXBTZUSD' in ohlc['result']:
            candles = ohlc['result']['XXBTZUSD']
            if len(candles) >= 3:
                recent = candles[-3:]
                closes = [float(c[4]) for c in recent]
                
                if closes[-1] > closes[-2] > closes[-3]:
                    signal = "📈 UPTREND - BUY SIGNAL CONFIRMED"
                elif closes[-1] < closes[-2] < closes[-3]:
                    signal = "📉 DOWNTREND - SELL SIGNAL"
                else:
                    if closes[-1] > closes[-2]:
                        signal = "📈 BULLISH MOMENTUM"
                    else:
                        signal = "📉 BEARISH MOMENTUM"
                
                print(f"{signal}")
                for i, c in enumerate(recent):
                    ts, o, h, l, close, vwap, vol, count = c
                    print(f"  1m[{i}]: O:{float(o):.2f} H:{float(h):.2f} L:{float(l):.2f} C:{float(close):.2f}")
        
        # Summary
        print("\n" + "="*60)
        print("✅ VERIFICATION COMPLETE - READY TO TRADE")
        print("="*60)
        print(f"✓ BTC Balance: {btc_balance:.8f} BTC")
        print(f"✓ Current Price: ${btc_price:.2f}")
        print(f"✓ Account Value: ${usd_value:.2f} USD")
        print(f"✓ Goal: Double holdings (${usd_value:.2f} → ${usd_value*2:.2f})")
        print(f"✓ Max per trade: $50 USD")
        print(f"✓ Strategy: Momentum following with tight stops")
        print(f"✓ Asset: Bitcoin only")
        print("="*60)
        
        return {
            'confirmed': True,
            'btc_balance': btc_balance,
            'btc_price': btc_price,
            'account_value': usd_value,
            'goal_value': usd_value * 2
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    main()
