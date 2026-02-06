#!/bin/bash
# NASCAR Poller Management Script
# Easy commands to start/stop/monitor the live data poller

POLLER_SCRIPT="tools/livePoller.py"
LOG_FILE="logs/poller.log"

case "$1" in
    start)
        echo "Starting NASCAR live data poller..."
        python3 $POLLER_SCRIPT &
        echo "Poller started in background (PID: $!)"
        echo "View logs: tail -f $LOG_FILE"
        ;;

    stop)
        echo "Stopping NASCAR live data poller..."
        pkill -f "livePoller.py"
        echo "Poller stopped"
        ;;

    restart)
        echo "Restarting NASCAR live data poller..."
        pkill -f "livePoller.py"
        sleep 2
        python3 $POLLER_script &
        echo "Poller restarted (PID: $!)"
        ;;

    status)
        if pgrep -f "livePoller.py" > /dev/null; then
            PID=$(pgrep -f "livePoller.py")
            echo "✅ Poller is running (PID: $PID)"
            echo ""
            echo "Recent activity:"
            tail -10 $LOG_FILE
        else
            echo "⏹️  Poller is not running"
        fi
        ;;

    logs)
        echo "Tailing poller logs (Ctrl+C to stop)..."
        tail -f $LOG_FILE
        ;;

    install)
        echo "Installing as systemd service..."
        sudo cp nascar-poller.service /etc/systemd/system/
        sudo systemctl daemon-reload
        sudo systemctl enable nascar-poller.service
        sudo systemctl start nascar-poller.service
        echo "✅ Service installed and started"
        echo "   Status: sudo systemctl status nascar-poller"
        echo "   Logs: journalctl -u nascar-poller -f"
        ;;

    uninstall)
        echo "Uninstalling systemd service..."
        sudo systemctl stop nascar-poller.service
        sudo systemctl disable nascar-poller.service
        sudo rm /etc/systemd/system/nascar-poller.service
        sudo systemctl daemon-reload
        echo "✅ Service uninstalled"
        ;;

    *)
        echo "NASCAR Live Data Poller Management"
        echo ""
        echo "Usage: ./poller.sh {start|stop|restart|status|logs|install|uninstall}"
        echo ""
        echo "Commands:"
        echo "  start      - Start poller in background"
        echo "  stop       - Stop poller"
        echo "  restart    - Restart poller"
        echo "  status     - Check if poller is running"
        echo "  logs       - View live logs"
        echo "  install    - Install as systemd service (auto-start on boot)"
        echo "  uninstall  - Remove systemd service"
        exit 1
        ;;
esac
