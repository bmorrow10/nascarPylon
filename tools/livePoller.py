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
import traceback
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.loader import load_all_schedules
from src.state import is_race_scheduled_now
from tools.nascarAPIclient import NascarApiClient, Series

# Configuration
DATA_DIR = Path("data")
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

POLL_INTERVAL_RACE = 5
POLL_INTERVAL_IDLE = 30
MAX_CONSECUTIVE_ERRORS = 10
RESTART_DELAY = 60  # Seconds to wait after max errors before trying again

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_DIR / "poller.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class RobustPoller:
    """Bulletproof NASCAR data poller"""

    def __init__(self):
        self.client = None
        self.is_polling = False
        self.current_series = Series.CUP
        self.consecutive_errors = 0
        self.last_successful_poll = None
        self.race_info = None
        self.total_polls = 0
        self.successful_polls = 0

    def initialize_client(self):
        """Initialize or reinitialize the API client"""
        try:
            self.client = NascarApiClient()
            logger.info("API client initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize API client: {e}")
            return False

    def check_race_status(self):
        """Check if race should be active"""
        try:
            schedules = load_all_schedules()
            race_info = is_race_scheduled_now(schedules)

            if race_info:
                series_name = race_info.get("series", "CUP")
                if series_name == "CUP":
                    self.current_series = Series.CUP
                elif series_name == "OREILLY":
                    self.current_series = Series.OREILLY
                elif series_name == "TRUCKS":
                    self.current_series = Series.TRUCKS

                self.race_info = race_info
                return True

            self.race_info = None
            return False

        except Exception as e:
            logger.error(f"Error checking race status: {e}")
            logger.debug(traceback.format_exc())
            return False

    def poll_live_data(self):
        """Poll NASCAR API and save data"""
        self.total_polls += 1

        try:
            # Ensure client exists
            if not self.client:
                if not self.initialize_client():
                    return False

            # Fetch data
            data = self.client.get_live_feed(self.current_series, use_cacher=True)

            if data and len(data.get("cars", [])) > 0:
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
                    f"✅ Poll #{self.total_polls}: Lap {lap}/{total} - {flag} - {cars} cars"
                )

                self.consecutive_errors = 0
                self.last_successful_poll = datetime.now()
                self.successful_polls += 1
                return True
            else:
                logger.warning(f"⚠️  Poll #{self.total_polls}: No data returned")
                self.consecutive_errors += 1
                return False

        except Exception as e:
            logger.error(f"❌ Poll #{self.total_polls} failed: {e}")
            logger.debug(traceback.format_exc())
            self.consecutive_errors += 1

            # Try to reinitialize client on error
            self.client = None

            return False

    def start_polling(self):
        """Enter active polling mode"""
        if not self.is_polling:
            logger.info(f"🏁 Starting live polling for {self.current_series.name}")
            if self.race_info:
                race_name = self.race_info["race"].get("raceName", "Unknown")
                logger.info(f"   Race: {race_name}")
            self.is_polling = True
            self.consecutive_errors = 0

    def stop_polling(self):
        """Exit active polling mode"""
        if self.is_polling:
            logger.info(f"⏹️  Stopping live polling")
            logger.info(f"   Session stats: {self.successful_polls} successful polls")
            self.is_polling = False
            self.consecutive_errors = 0
            self.successful_polls = 0

    def run(self):
        """Main polling loop with error recovery"""
        logger.info("=" * 60)
        logger.info("NASCAR LIVE DATA POLLER - ROBUST VERSION")
        logger.info("=" * 60)
        logger.info("Features: Auto-recovery, detailed logging, never gets stuck")
        logger.info("Press Ctrl+C to stop\n")

        # Initialize client
        self.initialize_client()

        try:
            while True:
                try:
                    # Check race status
                    race_active = self.check_race_status()

                    if race_active and not self.is_polling:
                        self.start_polling()
                    elif not race_active and self.is_polling:
                        self.stop_polling()

                    # Poll if active
                    if self.is_polling:
                        success = self.poll_live_data()

                        # Check for too many errors
                        if self.consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
                            logger.error(
                                f"❌ {MAX_CONSECUTIVE_ERRORS} consecutive errors"
                            )
                            logger.info(
                                f"⏸️  Pausing for {RESTART_DELAY}s before retry..."
                            )
                            time.sleep(RESTART_DELAY)

                            # Reset and try again
                            self.consecutive_errors = 0
                            self.client = None
                            self.initialize_client()
                            continue

                        time.sleep(POLL_INTERVAL_RACE)
                    else:
                        # Not polling - check schedule periodically
                        logger.debug("⏸️  Idle - checking schedule...")
                        time.sleep(POLL_INTERVAL_IDLE)

                except Exception as e:
                    logger.error(f"Error in main loop: {e}")
                    logger.debug(traceback.format_exc())
                    logger.info("Recovering in 10 seconds...")
                    time.sleep(10)

        except KeyboardInterrupt:
            logger.info("\n" + "=" * 60)
            logger.info("🏁 Shutting down poller...")
            logger.info(f"Total polls: {self.total_polls}")
            logger.info(f"Successful: {self.successful_polls}")
            logger.info("=" * 60)
            self.stop_polling()


def main():
    """Entry point"""
    poller = RobustPoller()
    poller.run()


if __name__ == "__main__":
    main()
