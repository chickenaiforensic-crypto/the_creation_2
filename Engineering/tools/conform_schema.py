#!/usr/bin/env python3
"""Conform master_store_tennis_SSoT.json to schema.json.
Currently: strips rankA/rankB per removed_fields in schema.
Idempotent - safe to re-run.
"""
import json
import sys

STORE_PATH = sys.argv[1] if len(sys.argv) > 1 else "master_store_tennis_SSoT.json"
SCHEMA_PATH = sys.argv[2] if len(sys.argv) > 2 else "schema.json"
OUT_PATH = sys.argv[3] if len(sys.argv) > 3 else STORE_PATH

with open(SCHEMA_PATH) as f:
    schema = json.load(f)

with open(STORE_PATH) as f:
    store = json.load(f)

removed = list(schema.get("removed_fields", {}).keys())
allowed = set(schema["fields"].keys())

before_count = len(store["matches"])
stripped = 0
for row in store["matches"]:
    for field in removed:
        if field in row:
            del row[field]
            stripped += 1
    extra = set(row.keys()) - allowed
    if extra:
        print(f"WARNING: row has undeclared fields not in schema: {extra}")

store["schema_version"] = schema["schema_version"]

with open(OUT_PATH, "w") as f:
    json.dump(store, f, indent=2)

print(f"Rows processed: {before_count}")
print(f"Field-instances stripped: {stripped}")
print(f"Output written to: {OUT_PATH}")
