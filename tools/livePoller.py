#!/usr/bin/env python3
"""
NASCAR Live Data Poller
Automatically polls NASCAR API during races and saves to data/liveRace.json

This runs as a background service:
- Checks every 30 seconds if a race should be active (based on schedule)
- When race is active, polls every 5 seconds
- Automatically starts/stops polling based on race status
- Logs all activity for debugging
"""

import json
import logging
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path so we can import from src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.loader import load_all_schedules
from src.state import is_race_scheduled_now
from tools.nascarAPIclient import NascarApiClient, Series

# Configuration
DATA_DIR = Path("data")
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

POLL_INTERVAL_RACE = 5  # Seconds between polls during active race
POLL_INTERVAL_IDLE = 30  # Seconds between schedule checks when idle
MAX_CONSECUTIVE_ERRORS = 10  # Stop polling after this many errors in a row

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "poller.log"),
        logging.StreamHandler(),  # Also print to console
    ],
)
logger = logging.getLogger(__name__)


class LiveDataPoller:
    """Automated NASCAR live data polling service"""

    def __init__(self):
        self.client = NascarApiClient()
        self.is_polling = False
        self.current_series = None
        self.consecutive_errors = 0
        self.last_successful_poll = None
        self.race_info = None

    def check_race_status(self):
        """Check if a race should be active right now"""
        try:
            schedules = load_all_schedules()
            race_info = is_race_scheduled_now(schedules)

            if race_info:
                # Map series name to enum
                series_name = race_info.get("series", "CUP")
                if series_name == "CUP":
                    self.current_series = Series.CUP
                elif series_name == "OREILLY":
                    self.current_series = Series.OREILLY
                elif series_name == "TRUCKS":
                    self.current_series = Series.TRUCKS
                else:
                    self.current_series = Series.CUP  # Default

                self.race_info = race_info
                return True

            self.race_info = None
            return False

        except Exception as e:
            logger.error(f"Error checking race status: {e}")
            return False

    def poll_live_data(self):
        """Poll NASCAR API and save data"""
        try:
            # Fetch live data
            data = self.client.get_live_feed(self.current_series, use_cacher=True)

            if data:
                # Save to file
                filepath = DATA_DIR / "liveRace.json"
                DATA_DIR.mkdir(exist_ok=True)

                with open(filepath, "w") as f:
                    json.dump(data, f, indent=2)

                # Log success
                lap = data.get("lap", 0)
                total = data.get("lapsTotal", 0)
                flag = data.get("flag", "UNKNOWN")
                cars = len(data.get("cars", []))

                logger.info(
                    f"✅ {self.current_series.name}: Lap {lap}/{total} - {flag} - {cars} cars"
                )

                self.consecutive_errors = 0
                self.last_successful_poll = datetime.now()
                return True
            else:
                logger.warning("⚠️  API returned no data")
                self.consecutive_errors += 1
                return False

        except Exception as e:
            logger.error(f"❌ Error polling data: {e}")
            self.consecutive_errors += 1
            return False

    def start_polling(self):
        """Enter active polling mode"""
        if not self.is_polling:
            logger.info(f"🏁 Starting live polling for {self.current_series.name}")
            if self.race_info:
                race_name = self.race_info["race"].get("raceName", "Unknown")
                logger.info(f"   Race: {race_name}")
            self.is_polling = True

    def stop_polling(self):
        """Exit active polling mode"""
        if self.is_polling:
            logger.info(f"⏹️  Stopping live polling")
            self.is_polling = False
            self.consecutive_errors = 0

    def run(self):
        """Main polling loop"""
        logger.info("=" * 60)
        logger.info("NASCAR LIVE DATA POLLER - STARTING")
        logger.info("=" * 60)
        logger.info("Press Ctrl+C to stop\n")

        try:
            while True:
                # Check if we should be polling
                race_active = self.check_race_status()

                if race_active and not self.is_polling:
                    # Race window opened - start polling
                    self.start_polling()

                elif not race_active and self.is_polling:
                    # Race window closed - stop polling
                    self.stop_polling()

                # If polling, fetch data
                if self.is_polling:
                    success = self.poll_live_data()

                    # Check for too many errors
                    if self.consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
                        logger.error(
                            f"❌ {MAX_CONSECUTIVE_ERRORS} consecutive errors - stopping polling"
                        )
                        self.stop_polling()

                    time.sleep(POLL_INTERVAL_RACE)
                else:
                    # Not polling - just check schedule periodically
                    if race_active:
                        logger.info(
                            f"⏳ Race window active but no data yet - retrying..."
                        )
                    else:
                        logger.debug("⏸️  No race active - checking schedule...")

                    time.sleep(POLL_INTERVAL_IDLE)

        except KeyboardInterrupt:
            logger.info("\n" + "=" * 60)
            logger.info("🏁 Shutting down poller...")
            logger.info("=" * 60)
            self.stop_polling()


def main():
    """Entry point"""
    poller = LiveDataPoller()
    poller.run()


if __name__ == "__main__":
    main()
