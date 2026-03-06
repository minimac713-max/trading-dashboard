#!/usr/bin/env python3
"""
Kraken Bitcoin Trading Bot - Production Version
Executes real trades with strict risk management
"""

import ccxt
import json
import logging
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple

# ============================================================================
# CONFIGURATION
# ============================================================================

SYMBOL = "BTC/USD"
POSITION_SIZE = 50  # USD
PROFIT_TARGET = 1.00  # 100% profit = 2x entry price
STOP_LOSS_PERCENT = -0.08  # -8%
API_CREDS_FILE = os.path.expanduser("~/.kraken/api.json")
LOG_DIR = os.path.expanduser("~/.openclaw/workspace/trading/logs")
TRADE_LOG = os.path.join(LOG_DIR, "trades.log")

# Momentum thresholds for entry signals
MOMENTUM_WINDOW = 20  # candles
MOMENTUM_THRESHOLD = 0.02  # 2% change = signal

# ============================================================================
# LOGGING SETUP
# ============================================================================

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(TRADE_LOG),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


# ============================================================================
# API & CREDENTIALS
# ============================================================================

def load_api_credentials() -> Dict[str, str]:
    """Load Kraken API credentials from secure file."""
    if not os.path.exists(API_CREDS_FILE):
        logger.error(f"API credentials file not found: {API_CREDS_FILE}")
        logger.error("Create ~/.kraken/api.json with: {\"apiKey\": \"...\", \"secret\": \"...\"}")
        sys.exit(1)
    
    try:
        with open(API_CREDS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load credentials: {e}")
        sys.exit(1)


def init_exchange() -> ccxt.kraken:
    """Initialize CCXT Kraken exchange with credentials."""
    creds = load_api_credentials()
    return ccxt.kraken({
        'apiKey': creds['apiKey'],
        'secret': creds['secret'],
        'enableRateLimit': True,
    })


# ============================================================================
# MARKET DATA & SIGNALS
# ============================================================================

def get_ohlcv(exchange: ccxt.kraken, symbol: str, timeframe: str = '1h', limit: int = 100) -> list:
    """Fetch OHLCV data from Kraken."""
    try:
        return exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    except Exception as e:
        logger.error(f"Failed to fetch OHLCV: {e}")
        return []


def calculate_momentum(closes: list) -> float:
    """Calculate momentum as % change over window."""
    if len(closes) < 2:
        return 0.0
    return (closes[-1] - closes[0]) / closes[0]


def get_entry_signal(exchange: ccxt.kraken, symbol: str) -> Tuple[bool, float, str]:
    """
    Generate entry signal based on momentum + trend.
    Returns: (should_buy, current_price, signal_reason)
    """
    ohlcv = get_ohlcv(exchange, symbol, '1h', MOMENTUM_WINDOW)
    if not ohlcv or len(ohlcv) < MOMENTUM_WINDOW:
        return False, 0, "Insufficient data"
    
    closes = [x[4] for x in ohlcv]
    current_price = closes[-1]
    momentum = calculate_momentum(closes)
    
    # Signal: Upward momentum above threshold
    if momentum > MOMENTUM_THRESHOLD:
        return True, current_price, f"Uptrend detected (momentum: {momentum:.2%})"
    
    return False, current_price, f"No signal (momentum: {momentum:.2%})"


# ============================================================================
# TRADE EXECUTION & MANAGEMENT
# ============================================================================

def get_account_balance(exchange: ccxt.kraken, currency: str = "USD") -> float:
    """Get available balance in specified currency."""
    try:
        balance = exchange.fetch_balance()
        return balance.get('free', {}).get(currency, 0)
    except Exception as e:
        logger.error(f"Failed to fetch balance: {e}")
        return 0


def calculate_position_qty(entry_price: float, position_size: float = POSITION_SIZE) -> float:
    """Calculate quantity to buy based on position size."""
    return position_size / entry_price


def execute_trade(exchange: ccxt.kraken, symbol: str, entry_price: float) -> Optional[Dict]:
    """Execute market buy order."""
    qty = calculate_position_qty(entry_price)
    
    logger.info(f"Executing BUY: {qty:.8f} BTC @ ${entry_price:.2f}")
    
    try:
        order = exchange.create_market_buy_order(symbol, qty)
        logger.info(f"Order executed: {order['id']}")
        return order
    except Exception as e:
        logger.error(f"Trade execution failed: {e}")
        return None


def calculate_target_stop(entry_price: float) -> Tuple[float, float]:
    """Calculate profit target and stop loss levels."""
    profit_target = entry_price * (1 + PROFIT_TARGET)
    stop_loss = entry_price * (1 + STOP_LOSS_PERCENT)
    return profit_target, stop_loss


def monitor_position(exchange: ccxt.kraken, symbol: str, entry_price: float, entry_time: datetime) -> None:
    """Monitor position until target or stop loss hit."""
    profit_target, stop_loss = calculate_target_stop(entry_price)
    
    logger.info(f"Position monitoring: Entry={entry_price:.2f}, Target={profit_target:.2f}, Stop={stop_loss:.2f}")
    
    while True:
        try:
            ticker = exchange.fetch_ticker(symbol)
            current_price = ticker['last']
            pnl_pct = (current_price - entry_price) / entry_price
            
            # Check profit target
            if current_price >= profit_target:
                logger.info(f"PROFIT TARGET HIT: ${current_price:.2f} (P&L: {pnl_pct:.2%})")
                execute_exit(exchange, symbol, current_price, entry_price, "profit_target")
                break
            
            # Check stop loss
            elif current_price <= stop_loss:
                logger.warning(f"STOP LOSS HIT: ${current_price:.2f} (P&L: {pnl_pct:.2%})")
                execute_exit(exchange, symbol, current_price, entry_price, "stop_loss")
                break
            
            logger.debug(f"Position open: {current_price:.2f} (P&L: {pnl_pct:.2%})")
        
        except Exception as e:
            logger.error(f"Monitoring error: {e}")
        
        # Sleep before next check
        import time
        time.sleep(60)


def execute_exit(exchange: ccxt.kraken, symbol: str, exit_price: float, entry_price: float, reason: str) -> None:
    """Execute market sell to close position."""
    try:
        balance = exchange.fetch_balance()
        btc_qty = balance.get('free', {}).get('BTC', 0)
        
        if btc_qty > 0.00001:  # Minimum to trade
            logger.info(f"Executing SELL: {btc_qty:.8f} BTC @ ${exit_price:.2f} ({reason})")
            order = exchange.create_market_sell_order(symbol, btc_qty)
            
            pnl_usd = (exit_price - entry_price) * btc_qty
            pnl_pct = (exit_price - entry_price) / entry_price
            
            logger.info(f"Exit successful - P&L: ${pnl_usd:.2f} ({pnl_pct:.2%})")
        else:
            logger.warning(f"No BTC to sell (balance: {btc_qty})")
    except Exception as e:
        logger.error(f"Exit failed: {e}")


# ============================================================================
# MAIN TRADING LOOP
# ============================================================================

def run_trading_cycle():
    """Single trading cycle: check signal, execute if triggered."""
    logger.info("=" * 70)
    logger.info("Starting trading cycle")
    logger.info("=" * 70)
    
    exchange = init_exchange()
    
    # Check balance
    balance = get_account_balance(exchange, "USD")
    logger.info(f"USD Balance: ${balance:.2f}")
    
    if balance < POSITION_SIZE:
        logger.warning(f"Insufficient balance. Required: ${POSITION_SIZE}, Available: ${balance:.2f}")
        return
    
    # Check entry signal
    should_buy, current_price, reason = get_entry_signal(exchange, SYMBOL)
    logger.info(f"Entry signal: {reason}")
    
    if should_buy:
        logger.info(f"SIGNAL TRIGGERED - Current price: ${current_price:.2f}")
        
        order = execute_trade(exchange, SYMBOL, current_price)
        if order:
            entry_time = datetime.now()
            # Monitor position (blocks until exit)
            monitor_position(exchange, SYMBOL, current_price, entry_time)
    else:
        logger.info("No entry signal - waiting for next cycle")
    
    logger.info("Trading cycle complete\n")


if __name__ == "__main__":
    run_trading_cycle()
