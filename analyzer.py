from collections import Counter
from datetime import datetime


def count_by_level(entries):
    levels = [e["level"] for e in entries if "level" in e]
    return Counter(levels)


def top_repeated_errors(entries, top_n=5):
    messages = [e["message"] for e in entries if e["level"] in ("ERROR", "CRITICAL")]
    return Counter(messages).most_common(top_n)


def errors_by_hour(entries):
    counts = {}

    for entry in entries:
        try:
            dt = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
            hour_key = dt.strftime("%Y-%m-%d %H:00")
            counts[hour_key] = counts.get(hour_key, 0) + 1
        except:
            continue

    return counts


def keyword_search(entries, keyword):
    keyword = keyword.lower()
    results = []

    for e in entries:
        msg = e.get("message", "")
        stack = e.get("stacktrace", "")

        if keyword in msg.lower() or keyword in str(stack).lower():
            results.append(e)

    return results
