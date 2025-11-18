from parser import read_log_file, parse_log_lines
from analyzer import count_by_level, top_repeated_errors, errors_by_hour, keyword_search
from alert import send_email_alert
import os

# -----------------------------
# EMAIL ALERT CONFIG
# -----------------------------
SENDER_EMAIL = "v.aanaya01@gmail.com"          # <-- Replace with YOUR Gmail
APP_PASSWORD = "fdla tgmn ifsr nbpa"       # <-- Replace with 16-char App Password
RECEIVER_EMAIL = "aanaya.v01@gmail.com"        # <-- Can use the same email for testing

# -----------------------------
# READ AND PARSE LOGS
# -----------------------------
log_path = os.path.join(os.getcwd(), "logs", "sample.log")

lines = read_log_file(log_path)
parsed = parse_log_lines(lines)

print("\n=== LOG SUMMARY ===")
print("Total Entries:", len(parsed))

# -----------------------------
# ANALYSIS SECTION
# -----------------------------
# Count by severity
level_counts = count_by_level(parsed)
print("\nLog Level Counts:", level_counts)

# Top repeated errors
print("\nTop Errors:")
for msg, count in top_repeated_errors(parsed):
    print(f"  {count}x - {msg}")

# Errors by hour
print("\nErrors by Hour:")
for hour, count in errors_by_hour(parsed).items():
    print(f"  {hour}: {count}")

# Keyword search example
print("\nSecurity-related Logs (keyword = 'unauthorized'):")
for entry in keyword_search(parsed, "unauthorized"):
    print(" ", entry["timestamp"], "-", entry["message"])

# -----------------------------
# ALERT RULES
# -----------------------------
error_count = level_counts.get("ERROR", 0)
critical_count = level_counts.get("CRITICAL", 0)

alert_message = None

# Rule 1: If ANY critical issue → immediate alert
if critical_count > 0:
    alert_message = f"⚠️ CRITICAL ALERT: {critical_count} critical issues found!"

# Rule 2: If too many errors → send alert
elif error_count > 10:
    alert_message = f"⚠️ High Error Volume: {error_count} errors detected!"

# -----------------------------
# SEND EMAIL ALERT (if triggered)
# -----------------------------
if alert_message:
    print("\n=== SENDING EMAIL ALERT ===")
    send_email_alert(
        SENDER_EMAIL,
        APP_PASSWORD,
        RECEIVER_EMAIL,
        "Log Analyzer Alert",
        alert_message
    )
else:
    print("\nNo alerts triggered.")
