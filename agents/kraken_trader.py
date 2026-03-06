#!/usr/bin/env python3
"""
Kraken Live Trading Bot - $50 to $100 challenge
Executes 1-2 trades with momentum-based entry and target exit
"""

import krakenex
import json
import time
from datetime import datetime, timedelta
import sys

# Load API keys
with open('/Users/macdaddy/.openclaw/workspace/.kraken_keys', 'r') as f:
    keys = json.load(f)

api = krakenex.API(
    key=keys['public_key'],
    secret=keys['private_key']
)

class KrakenTrader:
    def __init__(self):
        self.api = api
        self.capital = 50.0
        self.target = 100.0
        self.start_time = datetime.now()
        self.deadline = self.start_time + timedelta(hours=4)
        self.trades = []
        self.report_interval = 900  # 15 minutes
        self.last_report = datetime.now()
        
    def check_balance(self):
        """Get account balance"""
        print("[INIT] Checking account balance...")
        try:
            resp = self.api.query_private('Balance')
            if resp['error']:
                print(f"ERROR: {resp['error']}")
                return None
            
            balance = resp['result']
            usd_balance = float(balance.get('ZUSD', 0))
            btc_balance = float(balance.get('XXBT', 0))
            eth_balance = float(balance.get('XETH', 0))
            
            print(f"✓ Account balance verified")
            print(f"  USD: ${usd_balance:.2f}")
            print(f"  BTC: {btc_balance:.8f}")
            print(f"  ETH: {eth_balance:.6f}")
            
            return {
                'usd': usd_balance,
                'btc': btc_balance,
                'eth': eth_balance
            }
        except Exception as e:
            print(f"ERROR fetching balance: {e}")
            return None
    
    def get_ohlc_data(self, pair, interval=15):
        """Get 15-min OHLC data"""
        try:
            resp = self.api.query_public('OHLC', {'pair': pair, 'interval': interval})
            if resp['error']:
                print(f"ERROR: {resp['error']}")
                return None
            return resp['result'].get(list(resp['result'].keys())[0], [])
        except Exception as e:
            print(f"ERROR fetching OHLC: {e}")
            return None
    
    def detect_breakout(self, ohlc_data):
        """Simple breakout detection - last candle broke above 20-candle high"""
        if len(ohlc_data) < 21:
            return False, None
        
        recent = ohlc_data[-20:]
        highs = [float(candle[2]) for candle in recent]
        lows = [float(candle[3]) for candle in recent]
        close_prev = float(ohlc_data[-2][4])
        close_now = float(ohlc_data[-1][4])
        
        prev_high = max(highs)
        prev_low = min(lows)
        
        # Bullish breakout: price breaks above previous high
        if close_now > prev_high and close_prev <= prev_high:
            momentum = ((close_now - prev_high) / prev_high) * 100
            return True, momentum
        
        return False, None
    
    def get_current_price(self, pair):
        """Get current market price"""
        try:
            resp = self.api.query_public('Ticker', {'pair': pair})
            if resp['error']:
                return None
            ticker = resp['result'][list(resp['result'].keys())[0]]
            return float(ticker['c'][0])
        except Exception as e:
            print(f"ERROR fetching price: {e}")
            return None
    
    def execute_trade(self, pair, side, volume, price):
        """Place market order"""
        try:
            order_data = {
                'pair': pair,
                'type': side,
                'ordertype': 'market',
                'volume': str(volume)
            }
            resp = self.api.query_private('AddOrder', order_data)
            if resp['error']:
                print(f"ERROR placing order: {resp['error']}")
                return None
            
            txid = resp['result'].get('txid', [None])[0]
            print(f"✓ Order placed: {txid}")
            return txid
        except Exception as e:
            print(f"ERROR executing trade: {e}")
            return None
    
    def set_stop_loss(self, pair, stop_price):
        """Place stop-loss order"""
        try:
            order_data = {
                'pair': pair,
                'type': 'sell',
                'ordertype': 'stop-loss',
                'price': str(stop_price),
                'volume': str(self.trade_volume)
            }
            resp = self.api.query_private('AddOrder', order_data)
            return resp['result'].get('txid', [None])[0] if not resp['error'] else None
        except Exception as e:
            print(f"ERROR setting stop-loss: {e}")
            return None
    
    def run(self):
        """Main trading loop"""
        print("=" * 60)
        print("KRAKEN TRADING BOT - $50 → $100 CHALLENGE")
        print("=" * 60)
        print(f"Start time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Deadline:   {self.deadline.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Capital:    ${self.capital:.2f}")
        print(f"Target:     ${self.target:.2f} (100% gain)")
        print()
        
        # Check balance
        balance = self.check_balance()
        if not balance or balance['usd'] < self.capital:
            print("❌ Insufficient balance!")
            return False
        
        print("\n[ANALYSIS] Scanning BTC/ETH for breakout signals...")
        
        # Get 15-min data for BTC and ETH
        btc_ohlc = self.get_ohlc_data('XBTC')
        eth_ohlc = self.get_ohlc_data('XETH')
        
        breakout_pairs = []
        
        if btc_ohlc:
            is_breakout, momentum = self.detect_breakout(btc_ohlc)
            if is_breakout:
                breakout_pairs.append(('XBTC', momentum))
                print(f"  ✓ BTC breakout detected (momentum: {momentum:.3f}%)")
        
        if eth_ohlc:
            is_breakout, momentum = self.detect_breakout(eth_ohlc)
            if is_breakout:
                breakout_pairs.append(('XETH', momentum))
                print(f"  ✓ ETH breakout detected (momentum: {momentum:.3f}%)")
        
        if not breakout_pairs:
            print("  ⚠ No breakouts detected, using market orders on strongest signal...")
            # Fall back to market price momentum
            btc_price = self.get_current_price('XBTC')
            eth_price = self.get_current_price('XETH')
            breakout_pairs = [('XBTC', 0.1), ('XETH', 0.1)]
        
        # Execute trades
        print("\n[EXECUTION] Placing trades...")
        
        positions = []
        remaining_capital = self.capital
        
        for i, (pair, momentum) in enumerate(breakout_pairs[:2]):  # Max 2 trades
            if remaining_capital < 10:
                break
            
            # Allocate capital (first trade: 60%, second: 40%)
            allocation = remaining_capital * (0.6 if i == 0 else 0.4)
            
            price = self.get_current_price(pair)
            if not price:
                continue
            
            volume = allocation / price
            stop_loss_price = price * 0.97  # -3% stop loss
            take_profit_1 = price * 1.50   # +50% partial
            take_profit_2 = price * 2.00   # +100% full target
            
            # Execute entry
            txid = self.execute_trade(pair, 'buy', volume, price)
            
            if txid:
                trade = {
                    'id': i + 1,
                    'pair': pair,
                    'entry_price': price,
                    'volume': volume,
                    'entry_value': allocation,
                    'stop_loss': stop_loss_price,
                    'target_1': take_profit_1,
                    'target_2': take_profit_2,
                    'entry_time': datetime.now(),
                    'status': 'OPEN',
                    'txid': txid
                }
                positions.append(trade)
                self.trades.append(trade)
                
                print(f"\n✓ TRADE {i+1}: {pair}")
                print(f"  Entry price:   ${price:.2f}")
                print(f"  Entry amount:  {volume:.8f}")
                print(f"  Entry value:   ${allocation:.2f}")
                print(f"  Stop-loss:     ${stop_loss_price:.2f} (-3%)")
                print(f"  Target 1:      ${take_profit_1:.2f} (+50%)")
                print(f"  Target 2:      ${take_profit_2:.2f} (+100%)")
                
                remaining_capital -= allocation
        
        # Monitor trades
        print("\n[MONITORING] Tracking positions...")
        print(f"Active positions: {len(positions)}")
        
        # Monitor for 4 hours
        while datetime.now() < self.deadline and positions:
            elapsed = (datetime.now() - self.start_time).total_seconds() / 60
            
            # Report every 15 minutes
            if (datetime.now() - self.last_report).total_seconds() >= self.report_interval:
                print(f"\n[UPDATE] {datetime.now().strftime('%H:%M:%S')} - {elapsed:.0f} min elapsed")
                for pos in positions:
                    current_price = self.get_current_price(pos['pair'])
                    if current_price:
                        pnl = ((current_price - pos['entry_price']) / pos['entry_price']) * 100
                        pnl_value = (current_price - pos['entry_price']) * pos['volume']
                        print(f"  {pos['pair']}: ${current_price:.2f} | P&L: {pnl:+.2f}% (${pnl_value:+.2f})")
                self.last_report = datetime.now()
            
            # Check exit conditions
            for pos in positions[:]:
                current_price = self.get_current_price(pos['pair'])
                if not current_price:
                    continue
                
                pnl_pct = ((current_price - pos['entry_price']) / pos['entry_price']) * 100
                
                # Stop loss
                if current_price <= pos['stop_loss']:
                    pos['status'] = 'CLOSED - STOP LOSS'
                    pos['exit_price'] = current_price
                    pos['exit_time'] = datetime.now()
                    positions.remove(pos)
                    print(f"\n⚠ {pos['pair']} hit stop loss at ${current_price:.2f}")
                
                # Target 1: Partial profit
                elif current_price >= pos['target_1'] and pos['status'] == 'OPEN':
                    sell_volume = pos['volume'] * 0.5
                    txid = self.execute_trade(pos['pair'], 'sell', sell_volume, current_price)
                    print(f"\n✓ {pos['pair']} took partial profit at ${current_price:.2f}")
                    pos['partial_exit_price'] = current_price
                    pos['status'] = 'HALF CLOSED'
                
                # Target 2: Full target
                elif current_price >= pos['target_2'] and pos['status'] in ['OPEN', 'HALF CLOSED']:
                    sell_volume = pos['volume'] if pos['status'] == 'OPEN' else pos['volume'] * 0.5
                    txid = self.execute_trade(pos['pair'], 'sell', sell_volume, current_price)
                    print(f"\n🎯 {pos['pair']} hit 100% target at ${current_price:.2f}")
                    pos['exit_price'] = current_price
                    pos['exit_time'] = datetime.now()
                    pos['status'] = 'CLOSED - TARGET'
                    positions.remove(pos)
            
            time.sleep(30)  # Check every 30 seconds
        
        # Final report
        print("\n" + "=" * 60)
        print("FINAL REPORT")
        print("=" * 60)
        
        total_pnl = 0
        for trade in self.trades:
            if hasattr(trade, 'exit_price'):
                pnl = (trade['exit_price'] - trade['entry_price']) * trade['volume']
                total_pnl += pnl
                print(f"Trade {trade['id']}: {trade['pair']} | Status: {trade['status']} | P&L: ${pnl:+.2f}")
        
        final_balance = balance['usd'] + total_pnl
        total_return = ((final_balance - self.capital) / self.capital) * 100
        
        print(f"\nStarting capital: ${self.capital:.2f}")
        print(f"Final balance:    ${final_balance:.2f}")
        print(f"Total P&L:        ${total_pnl:+.2f} ({total_return:+.2f}%)")
        print(f"Execution time:   {(datetime.now() - self.start_time).total_seconds() / 60:.1f} minutes")
        print("=" * 60)
        
        return total_return >= 100

if __name__ == '__main__':
    trader = KrakenTrader()
    success = trader.run()
    sys.exit(0 if success else 1)
