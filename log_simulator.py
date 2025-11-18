import os
import time
import random
from datetime import datetime

# Always write logs to the correct directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "sample.log")

# Create logs folder if missing
os.makedirs(LOG_DIR, exist_ok=True)

# Create log file if not present
if not os.path.exists(LOG_FILE):
    open(LOG_FILE, "w").close()

messages = [
    "Starting system initialization",
    "Loading configuration file /etc/app/config.yaml",
    "Disk usage at 85% on /dev/sda1",
    "Database connection failed: timeout after 30s",
    "Failed to authenticate user: invalid token",
    "Retrying database connection",
    "System crash detected in Module X",
    "Unauthorized access attempt from IP 192.168.1.45",
    "Memory usage crossed 90%",
    "Stack trace: File 'app.py', line 42, in <module>"
]

levels = ["INFO", "WARNING", "ERROR", "CRITICAL"]

print("🔥 Log simulator running... writing logs to:", LOG_FILE)
print("-----------------------------------------------------------")

while True:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    level = random.choice(levels)
    msg = random.choice(messages)

    log_line = f"{ts} | {level} | {msg}\n"

    with open(LOG_FILE, "a") as f:
        f.write(log_line)

    print("Written:", log_line.strip())

    time.sleep(1)
