import time
import os
from log_parser import read_log_file, parse_log_lines
from analyzer import keyword_search
from utils import send_email_alert   # from utils.py

LOG_FILE = "logs/sample.log"

# --- YOUR EMAIL CONFIG ---
SENDER = "v.aanaya01@gmail.com"
APP_PASSWORD = "btab ieyq kpli tdtl"   # <- MUST BE APP PASSWORD
RECEIVER = "aanaya.v01@gmail.com"


def monitor_logs():
    print("🔔 Alert system running... watching logs in real time.\n")

    last_size = 0

    while True:
        if not os.path.exists(LOG_FILE):
            time.sleep(1)
            continue

        lines = read_log_file(LOG_FILE)

        # Check new logs only
        new_lines = lines[last_size:]
        last_size = len(lines)

        entries = parse_log_lines(new_lines)

        for e in entries:
            level = e["level"]
            msg = e["message"]
            ts = e["timestamp"]

            if level in ("ERROR", "CRITICAL"):
                print(f"\n⚠ ALERT TRIGGERED → {ts} | {level} | {msg}")

                body = f"Timestamp: {ts}\nLevel: {level}\nMessage: {msg}\n\nThis alert was auto-generated."
                send_email_alert(SENDER, APP_PASSWORD, RECEIVER, f"LOG ALERT: {level}", body)

        time.sleep(1)


if __name__ == "__main__":
    monitor_logs()
