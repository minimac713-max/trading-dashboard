#!/usr/bin/env python3
"""
Kraken Bitcoin Paper Trading Simulator
Tests strategy without risking capital
"""

import ccxt
import json
import logging
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

# ============================================================================
# CONFIGURATION
# ============================================================================

SYMBOL = "BTC/USD"
POSITION_SIZE = 50  # USD
PROFIT_TARGET = 1.00  # 100% profit
STOP_LOSS_PERCENT = -0.08  # -8%
STARTING_BALANCE = 1000  # Paper trading balance
LOG_DIR = os.path.expanduser("~/.openclaw/workspace/trading/logs")
SIM_LOG = os.path.join(LOG_DIR, "simulator.log")

MOMENTUM_WINDOW = 20
MOMENTUM_THRESHOLD = 0.02

# ============================================================================
# LOGGING
# ============================================================================

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [SIM] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(SIM_LOG),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


# ============================================================================
# PAPER TRADING ENGINE
# ============================================================================

class PaperTradeSimulator:
    """Simulate trades with live price data."""
    
    def __init__(self, starting_balance: float = STARTING_BALANCE):
        self.exchange = ccxt.kraken()
        self.balance = starting_balance
        self.usd = starting_balance
        self.btc = 0
        self.trades: List[Dict] = []
        self.position_open = False
        self.entry_price = 0
        self.entry_time = None
    
    def get_balance_snapshot(self) -> Dict:
        """Get current portfolio value."""
        ticker = self.exchange.fetch_ticker(SYMBOL)
        current_price = ticker['last']
        
        btc_value = self.btc * current_price
        total = self.usd + btc_value
        pnl = total - STARTING_BALANCE
        pnl_pct = pnl / STARTING_BALANCE if STARTING_BALANCE else 0
        
        return {
            'usd': self.usd,
            'btc': self.btc,
            'btc_value': btc_value,
            'total': total,
            'pnl': pnl,
            'pnl_pct': pnl_pct,
            'price': current_price
        }
    
    def get_ohlcv(self, timeframe: str = '1h', limit: int = 100) -> list:
        """Fetch live OHLCV data."""
        try:
            return self.exchange.fetch_ohlcv(SYMBOL, timeframe, limit=limit)
        except Exception as e:
            logger.error(f"Failed to fetch data: {e}")
            return []
    
    def calculate_momentum(self, closes: list) -> float:
        """Calculate momentum over window."""
        if len(closes) < 2:
            return 0.0
        return (closes[-1] - closes[0]) / closes[0]
    
    def check_entry_signal(self) -> Tuple[bool, float, str]:
        """Check if entry signal triggered."""
        ohlcv = self.get_ohlcv('1h', MOMENTUM_WINDOW)
        if not ohlcv or len(ohlcv) < MOMENTUM_WINDOW:
            return False, 0, "Insufficient data"
        
        closes = [x[4] for x in ohlcv]
        current_price = closes[-1]
        momentum = self.calculate_momentum(closes)
        
        if momentum > MOMENTUM_THRESHOLD:
            return True, current_price, f"Uptrend (momentum: {momentum:.2%})"
        
        return False, current_price, f"No signal (momentum: {momentum:.2%})"
    
    def buy(self, price: float) -> bool:
        """Simulate buy order."""
        if self.position_open:
            logger.warning("Position already open")
            return False
        
        if self.usd < POSITION_SIZE:
            logger.warning(f"Insufficient USD: ${self.usd:.2f}")
            return False
        
        qty = POSITION_SIZE / price
        self.btc += qty
        self.usd -= POSITION_SIZE
        self.position_open = True
        self.entry_price = price
        self.entry_time = datetime.now()
        
        logger.info(f"BUY SIMULATED: {qty:.8f} BTC @ ${price:.2f}")
        return True
    
    def sell(self, price: float, reason: str) -> Dict:
        """Simulate sell order."""
        if not self.position_open or self.btc <= 0:
            logger.warning("No position to close")
            return {}
        
        sale_value = self.btc * price
        self.usd += sale_value
        pnl_usd = (price - self.entry_price) * self.btc
        pnl_pct = (price - self.entry_price) / self.entry_price
        
        trade = {
            'entry_price': self.entry_price,
            'exit_price': price,
            'entry_time': self.entry_time.isoformat() if self.entry_time else None,
            'exit_time': datetime.now().isoformat(),
            'qty': self.btc,
            'pnl_usd': pnl_usd,
            'pnl_pct': pnl_pct,
            'reason': reason
        }
        
        self.trades.append(trade)
        self.btc = 0
        self.position_open = False
        
        logger.info(f"SELL SIMULATED: ${price:.2f} - P&L: ${pnl_usd:.2f} ({pnl_pct:.2%}) [{reason}]")
        return trade
    
    def monitor_position(self) -> None:
        """Monitor open position for targets/stops."""
        if not self.position_open:
            return
        
        profit_target = self.entry_price * (1 + PROFIT_TARGET)
        stop_loss = self.entry_price * (1 + STOP_LOSS_PERCENT)
        
        logger.info(f"Position open: {self.btc:.8f} BTC @ ${self.entry_price:.2f}")
        logger.info(f"Targets: Profit=${profit_target:.2f}, Stop=${stop_loss:.2f}")
        
        # Fetch current price
        ticker = self.exchange.fetch_ticker(SYMBOL)
        current_price = ticker['last']
        
        if current_price >= profit_target:
            logger.info(f"PROFIT TARGET HIT: ${current_price:.2f}")
            self.sell(current_price, "profit_target")
        
        elif current_price <= stop_loss:
            logger.warning(f"STOP LOSS HIT: ${current_price:.2f}")
            self.sell(current_price, "stop_loss")
    
    def run_cycle(self) -> None:
        """Run single simulation cycle."""
        logger.info("=" * 70)
        logger.info("SIMULATION CYCLE")
        logger.info("=" * 70)
        
        snapshot = self.get_balance_snapshot()
        logger.info(f"Portfolio: ${snapshot['total']:.2f} (USD: ${snapshot['usd']:.2f}, BTC: {snapshot['btc']:.8f})")
        
        # Check open positions
        if self.position_open:
            self.monitor_position()
        else:
            # Check entry signal
            should_buy, price, reason = self.check_entry_signal()
            logger.info(f"Signal check: {reason}")
            
            if should_buy:
                self.buy(price)
        
        logger.info("")
    
    def print_stats(self) -> None:
        """Print simulation statistics."""
        logger.info("=" * 70)
        logger.info("SIMULATION STATISTICS")
        logger.info("=" * 70)
        
        snapshot = self.get_balance_snapshot()
        
        logger.info(f"Starting Balance: ${STARTING_BALANCE:.2f}")
        logger.info(f"Current Balance: ${snapshot['total']:.2f}")
        logger.info(f"Total P&L: ${snapshot['pnl']:.2f} ({snapshot['pnl_pct']:.2%})")
        logger.info(f"Completed Trades: {len(self.trades)}")
        
        if self.trades:
            wins = sum(1 for t in self.trades if t['pnl_usd'] > 0)
            losses = sum(1 for t in self.trades if t['pnl_usd'] < 0)
            total_pnl = sum(t['pnl_usd'] for t in self.trades)
            
            logger.info(f"Wins: {wins}, Losses: {losses}")
            logger.info(f"Win Rate: {wins/len(self.trades):.1%}")
            logger.info(f"Total Trade P&L: ${total_pnl:.2f}")
            
            for i, trade in enumerate(self.trades, 1):
                logger.info(f"  Trade {i}: {trade['reason']} - ${trade['pnl_usd']:.2f} ({trade['pnl_pct']:.2%})")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import time
    
    sim = PaperTradeSimulator(STARTING_BALANCE)
    
    # Run multiple cycles
    num_cycles = 10
    for i in range(num_cycles):
        sim.run_cycle()
        time.sleep(2)  # Brief pause between cycles
    
    sim.print_stats()
