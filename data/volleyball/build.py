"""
Compiles data/volleyball/editions/**/*.json into data/volleyball/master_store_volleyball_SSoT.json.
Checksum-gated: any MANIFEST/file mismatch aborts the build. Run after any edition/MANIFEST change.
Usage: python3 build.py
"""
import json, hashlib, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(BASE, "MANIFEST.json")
OUT = os.path.join(BASE, "master_store_volleyball_SSoT.json")

def main():
    with open(MANIFEST) as f:
        man = json.load(f)
    matches, errors = [], []
    for ed in man["editions"]:
        fp = os.path.join(BASE, ed["file_path"])
        if not os.path.exists(fp):
            errors.append(f"MISSING FILE: {ed['file_path']}"); continue
        raw = open(fp).read()
        if hashlib.sha256(raw.encode()).hexdigest() != ed["checksum_sha256"]:
            errors.append(f"CHECKSUM MISMATCH: {ed['file_path']}"); continue
        data = json.loads(raw)
        ms = data.get("matches", [])
        if len(ms) != ed["match_count"] or data.get("match_count") != len(ms):
            errors.append(f"COUNT MISMATCH: {ed['file_path']}"); continue
        matches.extend(ms)
    if errors:
        for e in errors: print("ERROR:", e)
        sys.exit(1)
    if man["total_editions"] != len(man["editions"]):
        print("ERROR: manifest total_editions mismatch"); sys.exit(1)
    store = {
        "schema_version": "vb-1.1",
        "description": "Compiled volleyball master store — built from data/volleyball/editions/ via build.py. Do not edit directly; edit source files in editions/ and rerun build.py.",
        "count": len(matches),
        "matches": matches,
    }
    with open(OUT, "w") as f:
        json.dump(store, f, indent=1, ensure_ascii=False); f.write("\n")
    print(f"Build OK: {len(man['editions'])} editions, {len(matches)} matches -> {OUT}")

if __name__ == "__main__":
    main()
