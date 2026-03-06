#!/usr/bin/env python3
"""
Verify BTC balance using krakenex library - FINAL
"""

import krakenex
from datetime import datetime
import json

def main():
    print("="*60)
    print("🔗 KRAKEN BTC VERIFICATION")
    print("="*60)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
    
    # Initialize Kraken API
    try:
        k = krakenex.API()
        # Load keys from separate files
        k.key = open('/Users/macdaddy/.openclaw/workspace/kraken_public_key.txt').read().strip()
        k.secret = open('/Users/macdaddy/.openclaw/workspace/kraken_private_key.txt').read().strip()
        
        print(f"✅ API Keys loaded")
        print(f"   Public: {k.key[:20]}...")
        print(f"   Secret: {k.secret[:20]}...\n")
        
    except Exception as e:
        print(f"❌ Failed to load keys: {e}")
        return
    
    # Get account balance
    print("📍 Fetching Account Balance...\n")
    try:
        balance = k.query_private('Balance')
        
        if balance.get('error'):
            print(f"❌ API Error: {balance['error']}")
            print(f"\nFull response: {json.dumps(balance, indent=2)}")
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
            print("❌ No BTC balance found")
            print(f"Available keys: {list(result.keys())}\n")
            print(f"Full balances:\n{json.dumps(result, indent=2)}")
            return
        
        print(f"💰 BTC BALANCE: {btc_balance:.8f} BTC (Kraken key: {btc_key})")
        
        # Get current price
        print("\n📍 Fetching Current Price...\n")
        ticker = k.query_public('Ticker', {'pair': 'XXBTZUSD'})
        
        if ticker.get('error'):
            print(f"❌ Ticker Error: {ticker['error']}")
            return
        
        btc_data = ticker['result']['XXBTZUSD']
        btc_price = float(btc_data['c'][0])  # Last trade close
        bid = float(btc_data['b'][0])
        ask = float(btc_data['a'][0])
        
        usd_value = btc_balance * btc_price
        
        print(f"✅ Price Retrieved")
        print(f"   Last Price: ${btc_price:.2f}")
        print(f"   Bid: ${bid:.2f}")
        print(f"   Ask: ${ask:.2f}")
        print(f"\n💵 Account Value: {btc_balance:.8f} BTC × ${btc_price:.2f} = ${usd_value:.2f} USD")
        
        # Get OHLC for momentum signal
        print("\n📍 Analyzing Momentum Signal...\n")
        ohlc = k.query_public('OHLC', {'pair': 'XXBTZUSD', 'interval': 1})
        
        signal = "🔄 NEUTRAL"
        if not ohlc.get('error') and 'XXBTZUSD' in ohlc['result']:
            candles = ohlc['result']['XXBTZUSD']
            if len(candles) >= 3:
                recent = candles[-3:]
                closes = [float(c[4]) for c in recent]
                times = [datetime.fromtimestamp(float(c[0])) for c in recent]
                
                print("Recent 1-minute candles:")
                for i, c in enumerate(recent):
                    ts, o, h, l, close, vwap, vol, count = c
                    print(f"  [{times[i].strftime('%H:%M:%S')}] O:{float(o):.2f} H:{float(h):.2f} L:{float(l):.2f} C:{float(close):.2f}")
                
                print()
                if closes[-1] > closes[-2] > closes[-3]:
                    signal = "📈 UPTREND - STRONG BUY SIGNAL"
                elif closes[-1] < closes[-2] < closes[-3]:
                    signal = "📉 DOWNTREND - STRONG SELL SIGNAL"
                elif closes[-1] > closes[-2]:
                    if closes[-2] > closes[-3]:
                        signal = "📈 BULLISH - UPTREND CONTINUING"
                    else:
                        signal = "📈 BULLISH REVERSAL - BUY SIGNAL"
                else:
                    if closes[-2] < closes[-3]:
                        signal = "📉 BEARISH - DOWNTREND CONTINUING"
                    else:
                        signal = "📉 BEARISH REVERSAL"
        
        print(f"{signal}")
        
        # Summary - READY TO TRADE
        print("\n" + "="*60)
        print("✅ VERIFICATION COMPLETE - READY TO TRADE")
        print("="*60)
        print(f"✓ BTC Balance Confirmed: {btc_balance:.8f} BTC")
        print(f"✓ Current Price: ${btc_price:.2f}")
        print(f"✓ Account Value: ${usd_value:.2f} USD")
        print(f"✓ Doubling Goal: ${usd_value:.2f} → ${usd_value*2:.2f}")
        print(f"✓ Max per trade: $50 USD ({50/btc_price:.8f} BTC)")
        print(f"✓ Trade Signal: {signal}")
        print(f"✓ Ready to Execute: YES")
        print("="*60)
        
        return {
            'confirmed': True,
            'btc_balance': btc_balance,
            'btc_price': btc_price,
            'account_value': usd_value,
            'goal_value': usd_value * 2,
            'signal': signal
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    result = main()
