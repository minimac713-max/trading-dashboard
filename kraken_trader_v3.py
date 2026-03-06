#!/usr/bin/env python3
"""
Kraken Trading Bot v3 - Fixed API Authentication
"""

import json
import time
import hmac
import hashlib
import base64
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

class KrakenTraderV3:
    def __init__(self, api_key, private_key):
        self.api_key = api_key
        self.private_key = private_key
        self.api_url = "https://api.kraken.com"
        self.capital = 50.0
        self.deadline = datetime.now() + timedelta(hours=1)
        
    def sign_request(self, urlpath, data, secret):
        """Correct Kraken signature"""
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = hashlib.sha256(encoded).digest()
        
        signature = hmac.new(
            base64.b64decode(secret),
            message,
            hashlib.sha512
        )
        return base64.b64encode(signature.digest()).decode()
    
    def get_balance(self):
        """Get balance"""
        try:
            print("[LOG] Checking balance...")
            endpoint = "/0/private/Balance"
            data = {"nonce": str(int(time.time() * 1000))}
            
            postdata = urllib.parse.urlencode(data)
            signature = self.sign_request(endpoint, data, self.private_key)
            
            headers = {
                "API-Key": self.api_key,
                "API-Sign": signature
            }
            
            req = urllib.request.Request(
                self.api_url + endpoint,
                data=postdata.encode(),
                headers=headers,
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode())
            
            if result.get('error'):
                print(f"[ERROR] {result['error']}")
                return None
            
            print(f"[SUCCESS] Balance retrieved ✓")
            return result.get('result', {})
            
        except Exception as e:
            print(f"[ERROR] Balance check failed: {e}")
            return None
    
    def get_ticker(self, pair="BTCUSD"):
        """Get price"""
        try:
            endpoint = f"/0/public/Ticker?pair={pair}"
            
            with urllib.request.urlopen(self.api_url + endpoint, timeout=10) as response:
                result = json.loads(response.read().decode())
            
            if result.get('error'):
                print(f"[ERROR] {result['error']}")
                return None
            
            ticker = result['result'].get(pair, {})
            price = float(ticker['c'][0])
            return price
            
        except Exception as e:
            print(f"[ERROR] Ticker failed: {e}")
            return None
    
    def execute(self):
        """Main execution"""
        print("\n" + "="*60)
        print("KRAKEN BOT v3 - FIXED AUTHENTICATION")
        print("="*60)
        print(f"[MISSION] Double $50 → $100")
        print(f"[DEADLINE] {self.deadline.strftime('%I:%M %p CT')}")
        print("="*60 + "\n")
        
        # Test authentication
        balance = self.get_balance()
        if not balance:
            print("\n[CRITICAL] Authentication failed - check API key status in Kraken")
            print("[DEBUG] Verify kraken 04 is ACTIVE in Settings → Connections & API")
            return False
        
        # Get price
        price = self.get_ticker("BTCUSD")
        if not price:
            print("[ABORT] Cannot get price")
            return False
        
        print(f"\n[MARKET] BTC/USD: ${price:.2f}")
        print(f"[POSITION] ${self.capital} = {self.capital/price:.6f} BTC")
        print("\n[SUCCESS] Bot authenticated and ready to trade!")
        print("[NOTE] Would place order here - awaiting Kraken API confirmation")
        
        return True


def main():
    try:
        with open('/Users/macdaddy/.openclaw/workspace/kraken_public_key.txt') as f:
            api_key = f.read().strip()
        with open('/Users/macdaddy/.openclaw/workspace/kraken_private_key.txt') as f:
            private_key = f.read().strip()
        
        print(f"[AUTH] Keys loaded ✓")
    except Exception as e:
        print(f"[ERROR] Failed to load keys: {e}")
        return
    
    trader = KrakenTraderV3(api_key, private_key)
    trader.execute()


if __name__ == "__main__":
    main()
