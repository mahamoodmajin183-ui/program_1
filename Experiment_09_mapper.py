#!/usr/bin/env python3
"""
Experiment 9 - MAPPER (from the manual): reads CSV lines from stdin, turns each record into a JSON document and
prints  "null<TAB><json>"  for the Hadoop-MongoDB connector.

Change from the manual: the manual takes the header with next(sys.stdin).  In a real Hadoop job every input
split gets its own mapper, and only the first split contains the header line, so here any line equal to the
header is skipped instead.
"""
import csv
import json
import sys

HEADER = ["transaction_id", "user_id", "product_id", "quantity", "price", "timestamp"]
NUMERIC = ("quantity", "price")

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        values = next(csv.reader([line]))
    except Exception:
        continue
    if [v.strip() for v in values] == HEADER:
        continue

    document = {}
    for i, field in enumerate(HEADER):
        try:
            document[field] = float(values[i]) if field in NUMERIC else values[i]
        except (ValueError, IndexError):
            document[field] = values[i] if i < len(values) else None
    print(f"null\t{json.dumps(document)}")
