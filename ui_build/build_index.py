"""
build_index.py — verified UI index builder (new blank UI, Task 1).

Reads ONLY the engine content pulled verbatim from
arena/01a015bb-the-creation-2 @ 3ee36eb1574e908086ce84c82e419092d7a90655
into ui_build/engine/ (that tree's own MANIFEST.json + editions/**/*.json).

Discipline (mirrors engine build.py):
  * every edition file's sha256 and match count are re-verified against
    ui_build/engine/MANIFEST.json before any index byte is written;
  * on ANY mismatch the script exits non-zero and writes nothing;
  * nothing in the index is invented — every value is read from the files.

Output: ui_build/app/index.json
Usage:  python3 ui_build/build_index.py
"""
import datetime
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(HERE, "engine")
MANIFEST_PATH = os.path.join(ENGINE, "MANIFEST.json")
OUT_PATH = os.path.join(HERE, "app", "index.json")

SOURCE_BRANCH = "arena/01a015bb-the-creation-2"
SOURCE_COMMIT = "3ee36eb1574e908086ce84c82e419092d7a90655"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    manifest_raw = open(MANIFEST_PATH, "rb").read()
    manifest = json.loads(manifest_raw)

    errors = []
    tournaments = {}          # key -> info
    players_by_tournament = {}  # key -> set of names
    players = set()
    matches = []

    for edition in manifest["editions"]:
        file_path = os.path.join(ENGINE, edition["file_path"])
        if not os.path.exists(file_path):
            errors.append(f"MISSING FILE: {edition['file_path']}")
            continue
        raw = open(file_path, "rb").read()
        actual_sha = hashlib.sha256(raw).hexdigest()
        if actual_sha != edition["checksum_sha256"]:
            errors.append(
                f"CHECKSUM MISMATCH: {edition['file_path']} "
                f"(manifest={edition['checksum_sha256'][:12]}..., actual={actual_sha[:12]}...)"
            )
            continue
        data = json.loads(raw)
        rows = data.get("matches", [])
        if len(rows) != edition["match_count"]:
            errors.append(
                f"COUNT MISMATCH: {edition['file_path']} "
                f"(manifest={edition['match_count']}, actual={len(rows)})"
            )
            continue

        name = edition["tournament"]
        tour = edition["tour"]
        key = f"{name}|{tour}"
        info = tournaments.setdefault(key, {
            "key": key,
            "name": name,
            "tour": tour,
            "tier": edition["tier"],
            "years": [],
            "matches": 0,
        })
        info["years"].append(edition["year"])
        info["matches"] += len(rows)
        pset = players_by_tournament.setdefault(key, set())

        for r in rows:
            players.add(r["playerA"])
            players.add(r["playerB"])
            pset.add(r["playerA"])
            pset.add(r["playerB"])
            matches.append({
                "tkey": key,
                "year": r["edition_year"],
                "date": r["date"],
                "round": r["round"],
                "playerA": r["playerA"],
                "playerB": r["playerB"],
                "score": r["score"],
                "status": r["status"],
                "retired": r["retired"],
                "walkover": r["walkover"],
                "defaulted": r["defaulted"],
                "winner": r["winner"],
                "surface": r["surface"],
                "indoor": r["indoor"],
            })

    if errors:
        print("INDEX BUILD FAILED — integrity errors found:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    for info in tournaments.values():
        info["years"].sort()
        info["players"] = len(players_by_tournament[info["key"]])

    index = {
        "provenance": {
            "source_branch": SOURCE_BRANCH,
            "source_commit": SOURCE_COMMIT,
            "content_path": "ui_build/engine/ (verbatim data/tennis tree, pulled content-only via git archive; no merge)",
            "engine_manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
            "editions_in_manifest": len(manifest["editions"]),
            "editions_verified": len(manifest["editions"]),
            "verification": "sha256 + match_count re-checked for every edition file against the engine MANIFEST.json; builder exits non-zero on any mismatch",
            "matches": len(matches),
            "distinct_players": len(players),
            "built_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
        "tournaments": sorted(tournaments.values(), key=lambda t: (t["name"].lower(), t["tour"])),
        "playersByTournament": {k: sorted(v, key=str.lower) for k, v in players_by_tournament.items()},
        "players": sorted(players, key=str.lower),
        "matches": matches,
    }

    with open(OUT_PATH, "w") as f:
        json.dump(index, f, separators=(",", ":"))
    print(
        f"Index OK: {len(manifest['editions'])} editions verified, "
        f"{len(matches)} matches, {len(tournaments)} tournaments, "
        f"{len(players)} players -> {OUT_PATH}"
    )
    print(f"index.json sha256: {sha256_file(OUT_PATH)}")


if __name__ == "__main__":
    main()
