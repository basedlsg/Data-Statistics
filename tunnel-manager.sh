#!/bin/bash

# Robust Tunnel Manager for VC Hype Simulation Dashboard
# Automatically tries multiple tunnel services and restarts on failure

PORT=8000
LOG_FILE="/tmp/tunnel-manager.log"
PID_FILE="/tmp/tunnel-manager.pid"

# Color output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" | tee -a "$LOG_FILE"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARN:${NC} $1" | tee -a "$LOG_FILE"
}

# Kill any existing tunnels
cleanup() {
    log "Cleaning up existing tunnels..."
    pkill -f "lt --port" 2>/dev/null
    pkill -f "localtunnel" 2>/dev/null
    pkill -f "bore local" 2>/dev/null
    pkill -f "tmole" 2>/dev/null
    rm -f "$PID_FILE"
}

# Check if HTTP server is running on port
check_local_server() {
    if curl -s -o /dev/null -w "%{http_code}" "http://localhost:$PORT/standalone-dashboard.html" | grep -q "200"; then
        return 0
    else
        error "Local server on port $PORT is not responding!"
        return 1
    fi
}

# Try localtunnel (most reliable in this environment)
try_localtunnel() {
    log "Attempting to start localtunnel..."

    # Kill any existing localtunnel processes
    pkill -f "lt --port $PORT" 2>/dev/null
    sleep 1

    # Start localtunnel in background
    lt --port $PORT > /tmp/lt-output.txt 2>&1 &
    LT_PID=$!
    echo $LT_PID > "$PID_FILE"

    # Wait for URL to be generated
    sleep 3

    if [ -f /tmp/lt-output.txt ]; then
        URL=$(grep -oP 'https://[^\s]+\.loca\.lt' /tmp/lt-output.txt | head -1)
        if [ ! -z "$URL" ]; then
            log "✓ Localtunnel started successfully!"
            echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${GREEN}🌐 Dashboard URL: ${YELLOW}$URL/standalone-dashboard.html${NC}"
            echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${YELLOW}📝 If prompted for IP verification, use:${NC}"
            echo -e "   • 104.155.129.177"
            echo -e "   • 34.30.49.235"
            echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            return 0
        fi
    fi

    error "Localtunnel failed to start"
    return 1
}

# Monitor tunnel health
monitor_tunnel() {
    log "Starting tunnel monitor..."
    RESTART_COUNT=0
    MAX_RESTARTS=10

    while true; do
        sleep 30  # Check every 30 seconds

        # Check if tunnel process is still running
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if ! ps -p $PID > /dev/null 2>&1; then
                warn "Tunnel process died! Attempting restart... (Attempt $((RESTART_COUNT+1))/$MAX_RESTARTS)"

                if [ $RESTART_COUNT -lt $MAX_RESTARTS ]; then
                    RESTART_COUNT=$((RESTART_COUNT+1))
                    try_localtunnel
                    sleep 5
                else
                    error "Max restart attempts reached. Exiting."
                    exit 1
                fi
            else
                log "Tunnel is healthy (PID: $PID)"
            fi
        else
            warn "PID file not found. Restarting tunnel..."
            try_localtunnel
        fi
    done
}

# Main execution
main() {
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log "  VC Hype Simulation - Robust Tunnel Manager"
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Cleanup any existing tunnels
    cleanup

    # Check local server
    log "Checking local HTTP server on port $PORT..."
    if ! check_local_server; then
        error "Please start the HTTP server first: python3 -m http.server $PORT"
        exit 1
    fi
    log "✓ Local server is running"

    # Start tunnel
    if try_localtunnel; then
        log "Tunnel started successfully. Monitoring for failures..."
        # Monitor in foreground (or background with & at the end)
        monitor_tunnel
    else
        error "Failed to start any tunnel service"
        exit 1
    fi
}

# Handle Ctrl+C gracefully
trap 'log "Received interrupt signal. Cleaning up..."; cleanup; exit 0' INT TERM

# Run main
main
