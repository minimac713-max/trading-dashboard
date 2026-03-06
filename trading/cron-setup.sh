#!/bin/bash
#
# Kraken Trading Bot - Cron Setup Script
# Automates periodic trading runs 24/7
#
# Usage:
#   bash cron-setup.sh --install   (set up cron jobs)
#   bash cron-setup.sh --remove    (remove all cron jobs)
#   bash cron-setup.sh --status    (show current jobs)
#   bash cron-setup.sh --logs      (show recent trading logs)
#

set -e

# ============================================================================
# CONFIGURATION
# ============================================================================

TRADING_DIR="/Users/macdaddy/.openclaw/workspace/trading"
TRADER_SCRIPT="${TRADING_DIR}/kraken_trader.py"
LOG_DIR="${TRADING_DIR}/logs"
CRON_LOG="${LOG_DIR}/cron.log"
ERROR_LOG="${LOG_DIR}/errors.log"

# Mode: 'simulator' or 'trader'
# Change this before install if you want paper trading
MODE="trader"

# Frequency options (choose one)
FREQUENCY="10-minutes"  # Options: "10-minutes", "hourly", "daily"

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

create_log_dir() {
    mkdir -p "$LOG_DIR"
}

print_header() {
    echo ""
    echo "========================================================================"
    echo "$1"
    echo "========================================================================"
    echo ""
}

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$CRON_LOG"
    echo "$1"
}

# ============================================================================
# CRON JOB SETUP
# ============================================================================

install_cron_10min() {
    print_header "Installing cron job: Every 10 minutes"
    
    # Create wrapper script for 10-minute interval
    WRAPPER="${TRADING_DIR}/run_trader.sh"
    
    cat > "$WRAPPER" << 'EOF'
#!/bin/bash
source ~/.zprofile 2>/dev/null || true
cd /Users/macdaddy/.openclaw/workspace/trading

# Check if already running (prevent overlaps)
LOCK_FILE="/tmp/trading_bot.lock"
LOCK_TIMEOUT=600  # 10 minutes

if [ -f "$LOCK_FILE" ]; then
    LOCK_AGE=$(($(date +%s) - $(stat -f%m "$LOCK_FILE" 2>/dev/null || echo 0)))
    if [ $LOCK_AGE -lt $LOCK_TIMEOUT ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Previous trade still running, skipping..." >> logs/cron.log
        exit 0
    fi
fi

# Set lock
touch "$LOCK_FILE"

# Run trading bot
python3 kraken_trader.py >> logs/cron.log 2>> logs/errors.log
EXIT_CODE=$?

# Clean lock
rm -f "$LOCK_FILE"

# Log result
if [ $EXIT_CODE -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Trade cycle completed successfully" >> logs/cron.log
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Trade cycle failed with code $EXIT_CODE" >> logs/errors.log
fi

exit $EXIT_CODE
EOF
    
    chmod +x "$WRAPPER"
    
    # Install cron job (every 10 minutes)
    (crontab -l 2>/dev/null | grep -v "run_trader.sh"; echo "*/10 * * * * $WRAPPER") | crontab -
    
    log_message "✓ Cron job installed: Every 10 minutes"
    log_message "  Script: $WRAPPER"
}

install_cron_hourly() {
    print_header "Installing cron job: Hourly"
    
    WRAPPER="${TRADING_DIR}/run_trader.sh"
    
    cat > "$WRAPPER" << 'EOF'
#!/bin/bash
source ~/.zprofile 2>/dev/null || true
cd /Users/macdaddy/.openclaw/workspace/trading
python3 kraken_trader.py >> logs/cron.log 2>> logs/errors.log
EOF
    
    chmod +x "$WRAPPER"
    
    # Install cron job (every hour)
    (crontab -l 2>/dev/null | grep -v "run_trader.sh"; echo "0 * * * * $WRAPPER") | crontab -
    
    log_message "✓ Cron job installed: Every hour"
    log_message "  Script: $WRAPPER"
}

install_cron_daily() {
    print_header "Installing cron job: Daily at 9:00 AM"
    
    WRAPPER="${TRADING_DIR}/run_trader.sh"
    
    cat > "$WRAPPER" << 'EOF'
#!/bin/bash
source ~/.zprofile 2>/dev/null || true
cd /Users/macdaddy/.openclaw/workspace/trading
python3 kraken_trader.py >> logs/cron.log 2>> logs/errors.log
EOF
    
    chmod +x "$WRAPPER"
    
    # Install cron job (daily at 9:00 AM)
    (crontab -l 2>/dev/null | grep -v "run_trader.sh"; echo "0 9 * * * $WRAPPER") | crontab -
    
    log_message "✓ Cron job installed: Daily at 09:00"
    log_message "  Script: $WRAPPER"
}

remove_cron() {
    print_header "Removing cron jobs"
    
    crontab -l 2>/dev/null | grep -v "run_trader.sh" | crontab -
    
    echo "✓ Cron jobs removed"
    echo ""
}

show_cron() {
    print_header "Current cron jobs"
    
    crontab -l 2>/dev/null | grep -i trader || echo "No trading cron jobs found"
    
    echo ""
}

show_logs() {
    print_header "Recent cron execution logs (last 50 lines)"
    
    if [ -f "$CRON_LOG" ]; then
        tail -50 "$CRON_LOG"
    else
        echo "No cron logs yet"
    fi
    
    echo ""
}

show_errors() {
    print_header "Recent error logs (last 20 lines)"
    
    if [ -f "$ERROR_LOG" ]; then
        tail -20 "$ERROR_LOG"
    else
        echo "No errors logged"
    fi
    
    echo ""
}

# ============================================================================
# PREREQUISITES CHECK
# ============================================================================

check_prerequisites() {
    print_header "Checking prerequisites"
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 not found. Install with: brew install python3"
        exit 1
    fi
    echo "✓ Python 3: $(python3 --version)"
    
    # Check trading bot file
    if [ ! -f "$TRADER_SCRIPT" ]; then
        echo "❌ Trading bot not found: $TRADER_SCRIPT"
        exit 1
    fi
    echo "✓ Trading bot: $TRADER_SCRIPT"
    
    # Check ccxt library
    if ! python3 -c "import ccxt" 2>/dev/null; then
        echo "⚠ ccxt library not found. Installing..."
        pip3 install ccxt python-dotenv requests
    fi
    echo "✓ CCXT library installed"
    
    # Check API credentials
    if [ ! -f ~/.kraken/api.json ]; then
        echo "⚠ API credentials not found: ~/.kraken/api.json"
        echo "  Create with: {"
        echo "    \"apiKey\": \"your-kraken-api-key\","
        echo "    \"secret\": \"your-kraken-private-key\""
        echo "  }"
        echo ""
        read -p "Continue anyway? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        echo "✓ API credentials found"
    fi
    
    # Create log directory
    create_log_dir
    echo "✓ Log directory ready: $LOG_DIR"
    
    echo ""
}

# ============================================================================
# MAIN
# ============================================================================

case "${1:-}" in
    --install)
        check_prerequisites
        case "$FREQUENCY" in
            "10-minutes")
                install_cron_10min
                ;;
            "hourly")
                install_cron_hourly
                ;;
            "daily")
                install_cron_daily
                ;;
            *)
                echo "Unknown frequency: $FREQUENCY"
                exit 1
                ;;
        esac
        
        echo "============================================"
        echo "✓ Cron jobs installed!"
        echo "============================================"
        echo ""
        echo "Monitor logs:"
        echo "  tail -f $CRON_LOG"
        echo ""
        echo "View errors:"
        echo "  tail -f $ERROR_LOG"
        echo ""
        ;;
    
    --remove)
        remove_cron
        ;;
    
    --status)
        show_cron
        ;;
    
    --logs)
        show_logs
        show_errors
        ;;
    
    *)
        print_header "Kraken Trading Bot - Cron Setup"
        
        cat << EOF
Usage:
  bash cron-setup.sh --install     Install cron jobs (frequency: $FREQUENCY)
  bash cron-setup.sh --remove      Remove all cron jobs
  bash cron-setup.sh --status      Show active cron jobs
  bash cron-setup.sh --logs        Show recent logs and errors

Configuration:
  Trading script: $TRADER_SCRIPT
  Log directory: $LOG_DIR
  Frequency: $FREQUENCY
  Mode: $MODE

To change frequency, edit FREQUENCY in this script and run --install again.

Frequency options:
  - 10-minutes    Run every 10 minutes (for active trading)
  - hourly        Run once per hour
  - daily         Run once per day at 09:00

Examples:

1. Install cron job (every 10 minutes):
   bash cron-setup.sh --install

2. Check what cron jobs are active:
   bash cron-setup.sh --status

3. View recent logs:
   bash cron-setup.sh --logs

4. Remove all cron jobs:
   bash cron-setup.sh --remove

5. Stream logs in real-time:
   tail -f $CRON_LOG

EOF
        ;;
esac
