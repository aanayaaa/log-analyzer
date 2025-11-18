import re

# Regex pattern to parse logs like:
# 2025-01-01 12:00:55 | ERROR | Something wrong | Stacktrace
LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\S+\s+\S+)\s+\|\s+(?P<level>[A-Z]+)\s+\|\s+(?P<message>.*?)(?:\s*\|\s*(?P<stacktrace>.*))?$"
)


def read_log_file(path):
    """Read log file safely."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        return []


def parse_log_lines(lines):
    """Convert raw log lines into structured dictionaries."""
    parsed = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = LOG_PATTERN.match(line)
        if match:
            entry = match.groupdict()

            # Make sure stacktrace exists
            if entry.get("stacktrace") is None:
                entry["stacktrace"] = ""

            parsed.append(entry)

    return parsed
