import time
import random
from datetime import datetime

LOG_FILE = "logs/sample.log"

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

while True:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    level = random.choice(levels)
    msg = random.choice(messages)

    with open(LOG_FILE, "a") as f:
        f.write(f"{ts} | {level} | {msg}\n")

    print("Written:", ts, level, msg)
    time.sleep(1)
