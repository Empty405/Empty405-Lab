#!/usr/bin/env python

import csv
import subprocess
import sys

if len(sys.argv) != 2:
    print("Usage: fetch-batch.py <CSV>")
    raise SystemExit(1)

csv_path = sys.argv[1]

with open(csv_path, newline="", encoding="utf-8") as f:
    rows = csv.DictReader(f)

    for row in rows:
        source_id = row["source_id"].strip()
        category = row["category"].strip()
        url = row["url"].strip()

        print(f"\n=== {source_id} ===")

        result = subprocess.run([
            "./scripts/fetch-source.py",
            source_id,
            url,
            "--category",
            category,
        ])

        if result.returncode != 0:
            print(f"FAILED: {source_id}")
