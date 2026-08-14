#!/usr/bin/env python

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

FILE = Path("data/comparison-wave-001.csv")

FIELDS = [
    "test_id",
    "institution_id",
    "request_template",
    "channel",
    "sent_at_utc",
    "ack_at_utc",
    "first_human_at_utc",
    "first_substantive_at_utc",
    "resolved_at_utc",
    "status",
]

def now():
    return datetime.now(timezone.utc).isoformat()

def load_rows():
    if not FILE.exists():
        print(f"Missing file: {FILE}")
        raise SystemExit(1)

    with FILE.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    normalized = []
    for row in rows:
        normalized.append({field: row.get(field, "") for field in FIELDS})
    return normalized

def save_rows(rows):
    with FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

def find(rows, test_id):
    for row in rows:
        if row["test_id"] == test_id:
            return row
    print(f"Unknown request: {test_id}")
    raise SystemExit(1)

def show(rows):
    for row in rows:
        print(
            f"{row['test_id']:8} "
            f"{row['institution_id']:12} "
            f"{row['status']:18} "
            f"sent={row['sent_at_utc'] or '-'}"
        )

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  request-tracker.py list")
        print("  request-tracker.py sent TEST_ID CHANNEL")
        print("  request-tracker.py ack TEST_ID")
        print("  request-tracker.py human TEST_ID")
        print("  request-tracker.py substantive TEST_ID")
        print("  request-tracker.py resolved TEST_ID")
        raise SystemExit(1)

    rows = load_rows()
    command = sys.argv[1]

    if command == "list":
        show(rows)
        return

    if len(sys.argv) < 3:
        print("TEST_ID required")
        raise SystemExit(1)

    test_id = sys.argv[2]
    row = find(rows, test_id)
    timestamp = now()

    if command == "sent":
        if len(sys.argv) < 4:
            print("Channel required")
            raise SystemExit(1)

        row["channel"] = sys.argv[3]
        row["sent_at_utc"] = timestamp
        row["status"] = "SENT"

    elif command == "ack":
        row["ack_at_utc"] = timestamp
        row["status"] = "ACKNOWLEDGED"

    elif command == "human":
        row["first_human_at_utc"] = timestamp
        row["status"] = "HUMAN_RESPONSE"

    elif command == "substantive":
        row["first_substantive_at_utc"] = timestamp
        row["status"] = "SUBSTANTIVE_RESPONSE"

    elif command == "resolved":
        row["resolved_at_utc"] = timestamp
        row["status"] = "RESOLVED"

    else:
        print(f"Unknown command: {command}")
        raise SystemExit(1)

    save_rows(rows)

    print(f"{test_id}")
    print(f"status: {row['status']}")
    print(f"time:   {timestamp}")

if __name__ == "__main__":
    main()
