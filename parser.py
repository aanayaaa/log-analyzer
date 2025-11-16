import os
import re

# Regex pattern to match log lines
LOG_PATTERN = re.compile(
    r'^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) '
    r'(?P<level>INFO|WARNING|ERROR|CRITICAL) '
    r'(?P<message>.*)'
)

def read_log_file(filepath):
    """
    Reads log file and returns all raw lines.
    """
    if not os.path.exists(filepath):
        print("Log file not found:", filepath)
        return []

    with open(filepath, "r") as file:
        return file.readlines()


def parse_log_lines(lines):
    """
    Parses log lines into structured data using regex.
    Handles multiline stack traces.
    """
    parsed_logs = []
    current_entry = None

    for line in lines:

        match = LOG_PATTERN.match(line)

        if match:
            # If we had a previous log entry, push it
            if current_entry:
                parsed_logs.append(current_entry)

            # Start new log entry
            current_entry = {
                "timestamp": match.group("timestamp"),
                "level": match.group("level"),
                "message": match.group("message").strip(),
                "stacktrace": []
            }

        else:
            # This is a continuation line (stack trace or indent)
            if current_entry:
                current_entry["stacktrace"].append(line.rstrip())

    # Push last entry
    if current_entry:
        parsed_logs.append(current_entry)

    return parsed_logs
