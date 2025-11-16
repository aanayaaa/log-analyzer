from collections import Counter
from datetime import datetime

def count_by_level(parsed_logs):
    """
    Count INFO, WARNING, ERROR, CRITICAL logs.
    """
    levels = [entry["level"] for entry in parsed_logs]
    return Counter(levels)


def top_repeated_errors(parsed_logs, n=5):
    """
    Find the most common ERROR messages.
    """
    error_messages = [
        entry["message"]
        for entry in parsed_logs
        if entry["level"] in ["ERROR", "CRITICAL"]
    ]
    return Counter(error_messages).most_common(n)


def errors_by_hour(parsed_logs):
    """
    Group errors by hour for trend analysis.
    """
    hour_counts = Counter()

    for entry in parsed_logs:
        if entry["level"] in ["ERROR", "CRITICAL"]:
            dt = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
            hour = dt.strftime("%Y-%m-%d %H:00")
            hour_counts[hour] += 1

    return hour_counts


def keyword_search(parsed_logs, keyword):
    """
    Find all logs containing a specific keyword.
    """
    return [
        entry for entry in parsed_logs
        if keyword.lower() in entry["message"].lower()
    ]
