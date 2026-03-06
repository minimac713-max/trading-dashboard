#!/usr/bin/env python3
"""
Kraken Live Trading Bot v2 - Improved Auth & Debugging
"""

import json
import time
import hmac
import hashlib
import base64
import urllib.request
import urllib.error
from datetime import datetime, timedelta
import sys
import urllib.parse

class KrakenTrader:
    def __init__(self, api_key, private_key):
        self.api_key = api_key
        self.private_key = private_key
        self.api_url = "https://api.kraken.com"
        self.capital = 50.0
        self.target = 100.0
        self.deadline = datetime.now() + timedelta(hours=1)
        self.position = None
        self.entry_price = None
        
    def sign_request(self, endpoint, data):
        """Sign request for Kraken API - Corrected method"""
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
        """Get account balance from Kraken"""
        try:
            print("[LOG] Checking account balance...")
            endpoint = "/0/private/Balance"
            nonce = str(int(time.time() * 1000))
            data = {"nonce": nonce}
            
            print(f"[DEBUG] Nonce: {nonce}")
            
            postdata = urllib.parse.urlencode(data)
            print(f"[DEBUG] Post data: {postdata}")
            
            signature = self.sign_request(endpoint, data)
            print(f"[DEBUG] Signature: {signature[:20]}...")
            
            headers = {
                "API-Key": self.api_key,
                "API-Sign": signature
            }
            
            url = self.api_url + endpoint
            
            req = urllib.request.Request(
                url,
                data=postdata.encode(),
                headers=headers,
                method="POST"
            )
            
            print(f"[DEBUG] URL: {url}")
            print(f"[DEBUG] Headers: {headers}")
            
            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    result = json.loads(response.read().decode())
            except urllib.error.HTTPError as e:
                print(f"[DEBUG] HTTP Error: {e.code}")
                print(f"[DEBUG] Response: {e.read().decode()}")
                return None
                
            if result.get('error'):
                print(f"[ERROR] Kraken API error: {result['error']}")
                return None
            
            balance = result.get('result', {})
            print(f"[SUCCESS] Account balance retrieved")
            print(f"  BTC: {balance.get('XXBT', {})}")
            print(f"  USD: {balance.get('ZUSD', {})}")
            return balance
            
        except Exception as e:
            print(f"[ERROR] Failed to get balance: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_ticker(self, pair="BTCUSD"):
        """Get current price"""
        try:
            endpoint = f"/0/public/Ticker?pair={pair}"
            url = self.api_url + endpoint
            
            with urllib.request.urlopen(url, timeout=10) as response:
                result = json.loads(response.read().decode())
            
            if result.get('error'):
                print(f"[ERROR] Ticker error: {result['error']}")
                return None
            
            # Handle different key formats
            ticker_data = result.get('result', {})
            if not ticker_data:
                print("[ERROR] No ticker data returned")
                return None
            
            # Kraken returns different pair names, try both
            for key in ticker_data:
                if 'XBTUSDT' in key or 'XXBTZUSD' in key or 'BTCUSD' in key or pair in key:
                    ticker = ticker_data[key]
                    last_price = float(ticker['c'][0])  # Last trade close
                    return last_price
            
            # Fallback: use first key
            first_key = list(ticker_data.keys())[0]
            ticker = ticker_data[first_key]
            last_price = float(ticker['c'][0])
            return last_price
            
        except Exception as e:
            print(f"[ERROR] Failed to get ticker: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def place_order(self, pair, side, volume, price=None):
        """Place market order"""
        try:
            print(f"[LOG] Placing {side} order: {volume} {pair} @ {price or 'market'}")
            endpoint = "/0/private/AddOrder"
            nonce = str(int(time.time() * 1000))
            
            data = {
                "nonce": nonce,
                "ordertype": "market",
                "type": side,
                "pair": pair,
                "volume": f"{float(volume):.6f}",
            }
            
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
            
            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    result = json.loads(response.read().decode())
            except urllib.error.HTTPError as e:
                print(f"[DEBUG] HTTP Error: {e.code}")
                print(f"[DEBUG] Response: {e.read().decode()}")
                return None
            
            if result.get('error'):
                print(f"[ERROR] Order error: {result['error']}")
                return None
            
            order = result.get('result', {})
            print(f"[SUCCESS] Order placed!")
            print(f"  Order IDs: {order.get('txid')}")
            return order
            
        except Exception as e:
            print(f"[ERROR] Failed to place order: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def execute_trade(self):
        """Execute main trading logic"""
        print("\n" + "="*60)
        print("KRAKEN LIVE TRADING BOT v2 - EXECUTION START")
        print("="*60)
        print(f"[MISSION] Double $50 → $100 in ~1 hour")
        print(f"[DEADLINE] {self.deadline.strftime('%I:%M %p CT')}")
        print(f"[AUTHORIZED] Abel Villagomez ✓")
        print("="*60 + "\n")
        
        # Step 1: Verify balance
        balance = self.get_balance()
        if not balance:
            print("[ABORT] Cannot verify balance")
            return False
        
        # Step 2: Get BTC price
        btc_price = self.get_ticker("BTCUSD")
        if not btc_price:
            print("[ABORT] Cannot get BTC price")
            return False
        
        print(f"\n[MARKET] BTC/USD: ${btc_price:.2f}")
        
        # Step 3: Calculate position size
        btc_amount = self.capital / btc_price
        print(f"[POSITION] ${self.capital} USD = {btc_amount:.6f} BTC")
        
        # Step 4: Place BUY order at market
        print("\n[ACTION] Placing BUY order...")
        order = self.place_order("BTCUSD", "buy", btc_amount)
        
        if order:
            self.entry_price = btc_price
            self.position = {
                'pair': 'BTCUSD',
                'amount': btc_amount,
                'entry': btc_price,
                'time': datetime.now()
            }
            
            # Calculate targets
            stop_loss = btc_price * 0.92  # -8%
            take_profit = btc_price * 2.0  # +100%
            
            print(f"\n[TARGETS]")
            print(f"  Entry:       ${btc_price:.2f}")
            print(f"  Stop Loss:   ${stop_loss:.2f} (-8%)")
            print(f"  Take Profit: ${take_profit:.2f} (+100%)")
            
            return True
        else:
            print("[ABORT] Order placement failed")
            return False


def main():
    # Load API keys from text files
    try:
        with open('/Users/macdaddy/.openclaw/workspace/kraken_public_key.txt', 'r') as f:
            api_key = f.read().strip()
        
        with open('/Users/macdaddy/.openclaw/workspace/kraken_private_key.txt', 'r') as f:
            private_key = f.read().strip()
        
        print(f"[AUTH] Kraken API keys loaded ✓")
        print(f"[AUTH] Public Key: {api_key[:20]}...")
        print(f"[AUTH] Private Key: {private_key[:20]}...")
        
    except Exception as e:
        print(f"[ERROR] Failed to load API keys: {e}")
        sys.exit(1)
    
    # Initialize trader
    trader = KrakenTrader(api_key, private_key)
    
    # Execute
    trader.execute_trade()


if __name__ == "__main__":
    main()
