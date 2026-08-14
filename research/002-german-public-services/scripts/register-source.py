#!/usr/bin/env python

import csv
import hashlib
import pathlib
import sys

if len(sys.argv) != 3:
    print("Usage: register-source.py <ID> <FILE>")
    raise SystemExit(1)

source_id = sys.argv[1]
path = pathlib.Path(sys.argv[2])

if not path.is_file():
    print(f"File not found: {path}")
    raise SystemExit(1)

digest = hashlib.sha256(path.read_bytes()).hexdigest()

print(f"ID:     {source_id}")
print(f"FILE:   {path}")
print(f"SHA256: {digest}")
