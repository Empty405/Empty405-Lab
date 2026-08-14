#!/usr/bin/env python

import csv
import sys
from pathlib import Path

FILE = Path("data/response-quality.csv")

FIELDS = [
    "test_id",
    "completeness",
    "specificity",
    "legal_grounding",
    "source_transparency",
    "actionability",
    "accessibility",
    "referral_only",
    "contradiction_detected",
    "notes",
]

def load():
    if not FILE.exists():
        return []
    with FILE.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def save(rows):
    with FILE.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

def upsert(rows, item):
    for i, row in enumerate(rows):
        if row["test_id"] == item["test_id"]:
            rows[i] = item
            return
    rows.append(item)

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  response-quality.py list")
        print("  response-quality.py score TEST_ID")
        raise SystemExit(1)

    rows = load()
    cmd = sys.argv[1]

    if cmd == "list":
        if not rows:
            print("No response-quality records yet.")
            return
        for r in rows:
            print(
                f"{r['test_id']:8} "
                f"complete={r['completeness']} "
                f"legal={r['legal_grounding']} "
                f"sources={r['source_transparency']} "
                f"contradiction={r['contradiction_detected']}"
            )
        return

    if cmd != "score" or len(sys.argv) < 3:
        print("Usage: response-quality.py score TEST_ID")
        raise SystemExit(1)

    test_id = sys.argv[2]

    print("Score each field from 0 to 5.")
    print("0 = absent / unusable")
    print("5 = complete / strong")

    completeness = input("Completeness [0-5]: ").strip()
    specificity = input("Specificity [0-5]: ").strip()
    legal_grounding = input("Legal grounding [0-5]: ").strip()
    source_transparency = input("Source transparency [0-5]: ").strip()
    actionability = input("Actionability [0-5]: ").strip()
    accessibility = input("Accessibility [0-5]: ").strip()

    referral_only = input("Referral only? [yes/no]: ").strip().lower()
    contradiction = input("Contradiction detected? [yes/no]: ").strip().lower()
    notes = input("Notes: ").strip()

    item = {
        "test_id": test_id,
        "completeness": completeness,
        "specificity": specificity,
        "legal_grounding": legal_grounding,
        "source_transparency": source_transparency,
        "actionability": actionability,
        "accessibility": accessibility,
        "referral_only": referral_only,
        "contradiction_detected": contradiction,
        "notes": notes,
    }

    upsert(rows, item)
    save(rows)

    print(f"Saved quality assessment for {test_id}")

if __name__ == "__main__":
    main()
