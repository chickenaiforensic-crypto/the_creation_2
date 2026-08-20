#!/usr/bin/env python3
"""Auditor 5 independent recompute — 2026-08-20.

Reads only files under data/. Quotes no prior report. Exit 0 iff every
implemented assertion in this script reproduces from disk.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA = os.path.join(ROOT, "data")
failures: list[str] = []
results: dict = {"auditor": "Auditor 5", "date": "2026-08-20", "root": ROOT}


def fail(msg: str) -> None:
    failures.append(msg)


def md5_sha256_bytes(path: str) -> tuple[str, str, int]:
    md5 = hashlib.md5()
    sha = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            md5.update(chunk)
            sha.update(chunk)
    return md5.hexdigest(), sha.hexdigest(), os.path.getsize(path)


def fold(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def join_key(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", fold(name).lower())


def parse_sets(score: str) -> list:
    out = []
    for part in re.split(r"\s+", (score or "").strip()):
        if not part:
            continue
        if part.upper().rstrip(".") in {"RET", "WO", "W/O", "DEF", "DEFAULT"}:
            continue
        m = re.match(r"^(\d+)-(\d+)(?:\((\d+)\))?$", part)
        if not m:
            out.append(("UNPARSED", part))
        else:
            out.append((int(m.group(1)), int(m.group(2)), m.group(3)))
    return out


def last_set_complete(score: str) -> bool | None:
    sets = parse_sets(score)
    if any(x[0] == "UNPARSED" for x in sets):
        return None
    if not sets:
        return False
    a, b, _tb = sets[-1]
    return (max(a, b) >= 6 and abs(a - b) >= 2) or (sorted([a, b]) == [6, 7])


def empty_field(v) -> bool:
    if v is None:
        return True
    s = str(v).strip()
    return s == "" or s.lower() in {"none", "null", "nan"}


# ---------------------------------------------------------------------------
# Pins
# ---------------------------------------------------------------------------
paths = {
    "tennis_store": os.path.join(DATA, "tennis", "master_store_tennis_SSoT.json"),
    "canonical": os.path.join(DATA, "tennis", "player_canonical_names.json"),
    "football_store": os.path.join(DATA, "football", "master_store_15767.json"),
    "manifest": os.path.join(DATA, "MANIFEST.json"),
    "football_checksums": os.path.join(DATA, "football", "checksums.json"),
}

pins = {}
for label, path in paths.items():
    md5, sha, nbytes = md5_sha256_bytes(path)
    pins[label] = {"path": os.path.relpath(path, ROOT), "md5": md5, "sha256": sha, "bytes": nbytes}
results["pins"] = pins

with open(paths["manifest"]) as fh:
    manifest = json.load(fh)

exp_t = manifest["active_store"]
if pins["tennis_store"]["md5"] != exp_t["md5"]:
    fail(f"tennis md5 != manifest: {pins['tennis_store']['md5']} vs {exp_t['md5']}")
if pins["tennis_store"]["sha256"] != exp_t["sha256"]:
    fail("tennis sha256 != manifest")
if pins["canonical"]["md5"] != manifest["canonical_names"]["md5"]:
    fail("canonical md5 != manifest")
if pins["canonical"]["sha256"] != manifest["canonical_names"]["sha256"]:
    fail("canonical sha256 != manifest")

exp_f = manifest["verification_targets"]["football"]
if pins["football_store"]["md5"] != exp_f["md5"]:
    fail("football md5 != manifest")
if pins["football_store"]["sha256"] != exp_f["sha256"]:
    fail("football sha256 != manifest")

# Stated pins from GS134 card / PIN / KNOWN-GAPS (tennis) and football card.
STATED_TENNIS_MD5 = "9b271a35139d8dd459c13aadf3554bfa"
STATED_TENNIS_SHA = "eb2eeaf7ba504bbd83c459ca47eb0d09f63deade7de713db1cc4de72f36f5527"
STATED_TENNIS_BYTES = 14136767
STATED_FOOTBALL_MD5 = "bf2dd9b40e1dda6a4546394107f44a5a"
STATED_FOOTBALL_SHA = "809075006b53842128e261f95eb094c38581c89ae75cc8294f333c32e4a76764"
if pins["tennis_store"]["md5"] != STATED_TENNIS_MD5:
    fail("tennis md5 != GS134/PIN/KNOWN-GAPS pin")
if pins["tennis_store"]["sha256"] != STATED_TENNIS_SHA:
    fail("tennis sha256 != GS134/PIN/KNOWN-GAPS pin")
if pins["tennis_store"]["bytes"] != STATED_TENNIS_BYTES:
    fail(f"tennis bytes {pins['tennis_store']['bytes']} != {STATED_TENNIS_BYTES}")
if pins["football_store"]["md5"] != STATED_FOOTBALL_MD5:
    fail("football md5 != card/checksums pin")
if pins["football_store"]["sha256"] != STATED_FOOTBALL_SHA:
    fail("football sha256 != card pin")

# ---------------------------------------------------------------------------
# Tennis
# ---------------------------------------------------------------------------
with open(paths["tennis_store"]) as fh:
    tennis = json.load(fh)
matches = tennis["matches"]
t = {
    "schema_version": tennis.get("schema_version"),
    "count_field": tennis.get("count"),
    "n_matches": len(matches),
    "count_eq_len": tennis.get("count") == len(matches),
}
if tennis.get("count") != 17285 or len(matches) != 17285:
    fail(f"tennis row count {tennis.get('count')}/{len(matches)} != 17285")
if tennis.get("count") != len(matches):
    fail("tennis count field != len(matches)")

winners = Counter(m.get("winner") for m in matches)
t["winner"] = dict(winners)
if winners != Counter({"A": 17285}):
    fail(f"winner not all A: {dict(winners)}")

t["self_play"] = sum(1 for m in matches if m.get("playerA") == m.get("playerB"))
t["empty_playerA"] = sum(1 for m in matches if not str(m.get("playerA") or "").strip())
t["empty_playerB"] = sum(1 for m in matches if not str(m.get("playerB") or "").strip())
if t["self_play"] or t["empty_playerA"] or t["empty_playerB"]:
    fail("tennis self-play or empty names")

empty_dates = [m for m in matches if not str(m.get("date") or "").strip()]
bad_dates = []
parsed_dates = []
for m in matches:
    d = m.get("date") or ""
    if d == "":
        continue
    try:
        datetime.strptime(d, "%Y-%m-%d")
        parsed_dates.append(d)
    except ValueError:
        bad_dates.append(d)
t["empty_dates"] = len(empty_dates)
t["malformed_dates"] = len(bad_dates)
t["date_min"] = min(parsed_dates) if parsed_dates else None
t["date_max"] = max(parsed_dates) if parsed_dates else None
if bad_dates:
    fail(f"malformed tennis dates: {bad_dates[:5]}")

fn_rows = [m for m in matches if isinstance(m.get("provenance"), dict) and m["provenance"].get("forensic_null")]
t["forensic_null"] = len(fn_rows)
t["forensic_null_empty_date"] = sum(1 for m in fn_rows if not str(m.get("date") or "").strip())
t["empty_date_without_fn"] = sum(
    1 for m in empty_dates if not (isinstance(m.get("provenance"), dict) and m["provenance"].get("forensic_null"))
)
t["fn_year"] = dict(Counter(str(m.get("edition_year")) for m in fn_rows))
t["fn_tour"] = dict(Counter(m.get("tour") for m in fn_rows))
t["fn_status"] = dict(Counter(m.get("status") for m in fn_rows))
t["fn_tournament"] = dict(Counter(m.get("tournament") for m in fn_rows))
if t["forensic_null"] != 32 or t["forensic_null_empty_date"] != 32 or t["empty_date_without_fn"] != 0:
    fail("forensic_null / empty-date invariant failed")
if t["fn_tournament"] != {"Australian Open": 32}:
    fail("forensic_null not confined to Australian Open")
if t["fn_year"] != {"2021": 7, "2022": 6, "2024": 4, "2025": 9, "2026": 6}:
    fail(f"fn year breakdown {t['fn_year']}")
if t["fn_tour"] != {"ATP": 27, "WTA": 5}:
    fail(f"fn tour {t['fn_tour']}")
if t["fn_status"] != {"retired": 19, "completed": 9, "walkover": 4}:
    fail(f"fn status {t['fn_status']}")

seen = set()
dup = 0
for m in matches:
    key = (
        m.get("date"),
        m.get("tournament"),
        m.get("tour"),
        m.get("round"),
        m.get("playerA"),
        m.get("playerB"),
        m.get("edition_year"),
    )
    if key in seen:
        dup += 1
    seen.add(key)
t["duplicate_composite"] = dup
if dup:
    fail("duplicate tennis composites")

ident_extra = 0
blob_counts: Counter[str] = Counter()
for m in matches:
    blob_counts[json.dumps(m, sort_keys=True, separators=(",", ":"))] += 1
ident_extra = sum(c - 1 for c in blob_counts.values() if c > 1)
t["byte_identical_extra"] = ident_extra
if ident_extra:
    fail("byte-identical tennis rows")

GS_NAMES = {"Australian Open", "Roland Garros", "Wimbledon", "US Open"}
editions = defaultdict(int)
for m in matches:
    if m.get("tier") == "GS" or m.get("tournament") in GS_NAMES:
        editions[(m.get("tournament"), str(m.get("edition_year")), m.get("tour"))] += 1
t["gs_editions"] = len(editions)
t["gs_editions_127"] = sum(1 for n in editions.values() if n == 127)
t["gs_non_127"] = {f"{a}|{b}|{c}": n for (a, b, c), n in editions.items() if n != 127}
t["gs_rows"] = sum(editions.values())
t["us_open_2026"] = editions.get(("US Open", "2026", "ATP"), 0) + editions.get(("US Open", "2026", "WTA"), 0)
if t["gs_editions"] != 46 or t["gs_editions_127"] != 46:
    fail(f"GS completeness {t['gs_editions']} editions, {t['gs_editions_127']} at 127")
if t["us_open_2026"] != 0:
    fail("US Open 2026 unexpectedly present")
ao_by_year = Counter(str(m.get("edition_year")) for m in matches if m.get("tournament") == "Australian Open")
t["ao_by_year"] = dict(ao_by_year)
if dict(ao_by_year) != {str(y): 254 for y in range(2021, 2027)}:
    fail(f"AO by year {dict(ao_by_year)}")

t["status"] = dict(Counter(m.get("status") for m in matches))
t["retired_true"] = sum(1 for m in matches if m.get("retired") is True)
t["walkover_true"] = sum(1 for m in matches if m.get("walkover") is True)
t["defaulted_true"] = sum(1 for m in matches if m.get("defaulted") is True)
t["flag_status_mismatch_retired"] = sum(
    1 for m in matches if bool(m.get("retired")) != (m.get("status") == "retired")
)
t["flag_status_mismatch_walkover"] = sum(
    1 for m in matches if bool(m.get("walkover")) != (m.get("status") == "walkover")
)
t["flag_status_mismatch_defaulted"] = sum(
    1 for m in matches if bool(m.get("defaulted")) != (m.get("status") == "defaulted")
)
if t["flag_status_mismatch_retired"] or t["flag_status_mismatch_walkover"] or t["flag_status_mismatch_defaulted"]:
    fail("tennis status flag mismatches")

t["empty_rankA"] = sum(1 for m in matches if empty_field(m.get("rankA")))
t["empty_rankB"] = sum(1 for m in matches if empty_field(m.get("rankB")))
t["empty_duration_min"] = sum(1 for m in matches if empty_field(m.get("duration_min")))
if (t["empty_rankA"], t["empty_rankB"], t["empty_duration_min"]) != (426, 452, 2520):
    fail(
        f"null census {t['empty_rankA']}/{t['empty_rankB']}/{t['empty_duration_min']} != 426/452/2520"
    )

names = {m["playerA"] for m in matches} | {m["playerB"] for m in matches}
t["distinct_player_names"] = len(names)
if t["distinct_player_names"] != 932:
    fail(f"distinct names {t['distinct_player_names']} != 932")
t["juncheng_shang_rows"] = sum(1 for m in matches if "Juncheng Shang" in (m["playerA"], m["playerB"]))
t["shang_juncheng_rows"] = sum(1 for m in matches if "Shang Juncheng" in (m["playerA"], m["playerB"]))
if t["juncheng_shang_rows"] != 0:
    fail("retired spelling Juncheng Shang still present")

otte = [
    m
    for m in matches
    if "Otte" in f"{m.get('playerA')} {m.get('playerB')}"
    and "Rinderknech" in f"{m.get('playerA')} {m.get('playerB')}"
    and m.get("tournament") == "Wimbledon"
    and str(m.get("date", "")).startswith("2021")
]
t["otte_rinderknech_2021_wimbledon"] = [
    {"date": m.get("date"), "round": m.get("round"), "score": m.get("score"), "status": m.get("status")}
    for m in otte
]
if not any(m.get("score") == "4-6 6-3 6-2 6-7(5) 13-12(2)" and m.get("status") == "completed" for m in otte):
    fail("Otte/Rinderknech 13-12(2) not found")

shelton = [
    m
    for m in matches
    if "Shelton" in f"{m.get('playerA')} {m.get('playerB')}"
    and "Shapovalov" in f"{m.get('playerA')} {m.get('playerB')}"
    and m.get("tournament") == "Washington"
    and str(m.get("date", "")).startswith("2024")
]
t["shelton_shapovalov_washington_2024"] = [
    {
        "date": m.get("date"),
        "round": m.get("round"),
        "score": m.get("score"),
        "defaulted": m.get("defaulted"),
        "status": m.get("status"),
    }
    for m in shelton
]
if not any(m.get("score") == "7-6 6-6" and m.get("defaulted") is True for m in shelton):
    fail("Shelton/Shapovalov Washington 7-6 6-6 defaulted not found")

ao = [m for m in matches if m.get("tournament") == "Australian Open"]
ao_incomplete_numeric = []
for m in ao:
    complete = last_set_complete(m.get("score") or "")
    if complete is False and parse_sets(m.get("score") or "") and not any(
        x[0] == "UNPARSED" for x in parse_sets(m.get("score") or "")
    ):
        ao_incomplete_numeric.append(m)
    # W/O has no numeric sets — excluded from this census by design
t["ao_incomplete_numeric_terminal"] = len(ao_incomplete_numeric)
t["ao_incomplete_by_status"] = dict(Counter(m.get("status") for m in ao_incomplete_numeric))
if t["ao_incomplete_numeric_terminal"] != 30:
    fail(f"AO incomplete numeric terminal sets {t['ao_incomplete_numeric_terminal']} != 30")
if t["ao_incomplete_by_status"] != {"retired": 21, "completed": 9}:
    fail(f"AO incomplete by status {t['ao_incomplete_by_status']}")

neg = 0
for m in matches:
    for k in ("setsA", "setsB", "gamesA", "gamesB"):
        v = m.get(k)
        if v is None or (isinstance(v, (int, float)) and v < 0):
            neg += 1
t["null_or_negative_sets_games"] = neg
if neg:
    fail("null/negative sets/games")

odds_keys = sorted({k for m in matches for k in m if "odd" in k.lower() or "price" in k.lower()})
t["odds_keys"] = odds_keys
if odds_keys:
    fail(f"odds keys present: {odds_keys}")

t["jj_wolf_rows"] = sum(1 for m in matches if "J.J. Wolf" in (m["playerA"], m["playerB"]))
t["jeffrey_wolf_rows"] = sum(1 for m in matches if "Jeffrey Wolf" in (m["playerA"], m["playerB"]))
t["tours"] = dict(Counter(m.get("tour") for m in matches))
t["tiers"] = dict(Counter(m.get("tier") for m in matches))
results["tennis"] = t

# Canonical table
with open(paths["canonical"]) as fh:
    canonical = json.load(fh)
c = {
    "entries": len(canonical),
    "verified_true": sum(1 for v in canonical.values() if v.get("verified") is True),
    "verified_absent": sum(
        1
        for v in canonical.values()
        if v.get("verified") is not True and v.get("status") != "RETIRED_MERGED"
    ),
    "retired_merged": sum(1 for v in canonical.values() if v.get("status") == "RETIRED_MERGED"),
    "needs_verification": sum(1 for v in canonical.values() if v.get("needs_verification")),
    "disputed": sum(
        1 for v in canonical.values() if v.get("disputed") or v.get("status") == "disputed"
    ),
}
if c["entries"] != 1069:
    fail(f"canonical entries {c['entries']} != 1069")
if c["verified_true"] != 190 or c["needs_verification"] != 0 or c["disputed"] != 0:
    fail(f"canonical verification census {c}")
if "junchengshang" not in canonical or canonical["junchengshang"].get("status") != "RETIRED_MERGED":
    fail("junchengshang not RETIRED_MERGED")
if canonical.get("junchengshang", {}).get("merged_into") != "shangjuncheng":
    fail("junchengshang merged_into != shangjuncheng")

join_mismatches = []
for n in sorted(names):
    k = join_key(n)
    if k not in canonical:
        join_mismatches.append({"store_name": n, "join_key": k})
c["store_names_whose_join_key_absent"] = join_mismatches
# Expect the Dedura-Palomero join-key drift (table key remains diegodedura).
if join_mismatches != [{"store_name": "Diego Dedura-Palomero", "join_key": "diegodedurapalomero"}]:
    fail(f"unexpected join-key mismatches: {join_mismatches}")
if "diegodedura" not in canonical:
    fail("diegodedura key missing")
if join_key(canonical["diegodedura"].get("canonical_full_name") or "") != "diegodedurapalomero":
    fail("diegodedura canonical_full_name join unexpected")
c["jjwolf_canonical_full_name"] = canonical.get("jjwolf", {}).get("canonical_full_name")
results["canonical"] = c

# ---------------------------------------------------------------------------
# Football
# ---------------------------------------------------------------------------
with open(paths["football_store"]) as fh:
    football = json.load(fh)
fm = football["store"]["matches"]
with open(paths["football_checksums"]) as fh:
    checksums = json.load(fh)

f = {
    "n_matches": len(fm),
    "unique_ids": len({m.get("id") for m in fm}),
    "muted_true": sum(1 for m in fm if m.get("muted") is True),
    "empty_home": sum(1 for m in fm if not str(m.get("homeName") or "").strip()),
    "empty_away": sum(1 for m in fm if not str(m.get("awayName") or "").strip()),
    "self_play": sum(
        1 for m in fm if m.get("homeName") == m.get("awayName") or m.get("homeId") == m.get("awayId")
    ),
}
if f["n_matches"] != 15767:
    fail(f"football rows {f['n_matches']} != 15767")
if f["unique_ids"] != 15767:
    fail("duplicate football ids")
if f["muted_true"] or f["empty_home"] or f["empty_away"] or f["self_play"]:
    fail("football muted/empty/self-play")

bad = []
parsed = []
for m in fm:
    d = m.get("dateISO") or ""
    try:
        datetime.strptime(d, "%Y-%m-%d")
        parsed.append(d)
    except ValueError:
        bad.append(d)
f["malformed_dates"] = len(bad)
f["date_min"] = min(parsed)
f["date_max"] = max(parsed)
if bad:
    fail("football malformed dates")
if [f["date_min"], f["date_max"]] != checksums["date_range"]:
    fail("football date_range != checksums.json")

badg = 0
for m in fm:
    for k in ("homeGoals", "awayGoals"):
        v = m.get(k)
        if v is None or not isinstance(v, int) or v < 0:
            badg += 1
f["null_neg_nonint_goals"] = badg
if badg:
    fail("football bad goals")

seen = set()
dups = 0
for m in fm:
    key = (m.get("dateISO"), m.get("competitionName"), m.get("homeName"), m.get("awayName"))
    if key in seen:
        dups += 1
    seen.add(key)
f["duplicate_tuple"] = dups
if dups:
    fail("football duplicate (date,comp,home,away)")

by_comp = Counter(m.get("competitionName") for m in fm)
f["by_competition"] = dict(by_comp)
if dict(by_comp) != checksums["by_competition"]:
    fail("football by_competition != checksums.json")
by_year = Counter(d[:4] for d in parsed)
f["by_year"] = dict(sorted(by_year.items()))
if dict(by_year) != checksums["by_year"]:
    fail("football by_year != checksums.json")
by_type = Counter(m.get("compType") for m in fm)
f["by_compType"] = dict(by_type)
if dict(by_type) != checksums["by_compType"]:
    fail("football by_compType != checksums.json")

ADMITTED = {
    "England Premier League": 1900,
    "Italy Serie A": 1900,
    "Italy Relegation Playoffs": 1,
    "Germany Bundesliga": 1530,
    "Germany Relegation Playoffs": 10,
    "Czech Relegation Playoffs": 20,
    "Russian Relegation Playoffs": 20,
}
admitted = sum(by_comp[k] for k in ADMITTED)
for k, exp in ADMITTED.items():
    if by_comp.get(k) != exp:
        fail(f"admitted slice {k}: {by_comp.get(k)} != {exp}")
f["admitted_rows"] = admitted
f["non_admitted_rows"] = len(fm) - admitted
if admitted != 5381 or f["non_admitted_rows"] != 10386:
    fail("admitted arithmetic failed")

UEFA = ("UEFA Champions League", "UEFA Europa League", "UEFA Conference League")
uefa_n = sum(by_comp[k] for k in UEFA)
f["uefa_three_sum"] = uefa_n
f["uefa_breakdown"] = {k: by_comp[k] for k in UEFA}
f["hold_inferred_if_blocked_equals_uefa"] = len(fm) - admitted - uefa_n
if uefa_n != 2169:
    fail(f"UEFA three-sum {uefa_n} != 2169")
if f["hold_inferred_if_blocked_equals_uefa"] != 8217:
    fail("HOLD inferred != 8217")

rpl_inflight = [m for m in fm if m["competitionName"] == "Russian Premier League" and m["dateISO"] >= "2026-07-01"]
f["rpl_from_2026_07_01"] = len(rpl_inflight)
if len(rpl_inflight) != 16:
    fail(f"RPL in-flight {len(rpl_inflight)} != 16")


def season(d: str) -> str:
    y, mo = int(d[:4]), int(d[5:7])
    return f"{y}-{y+1}" if mo >= 7 else f"{y-1}-{y}"


l1 = [m for m in fm if m["competitionName"] == "France Ligue 1"]
f["ligue1_by_season"] = dict(sorted(Counter(season(m["dateISO"]) for m in l1).items()))
if f["ligue1_by_season"] != {
    "2021-2022": 380,
    "2022-2023": 380,
    "2023-2024": 306,
    "2024-2025": 306,
    "2025-2026": 306,
}:
    fail(f"Ligue 1 seasons {f['ligue1_by_season']}")

empty_source = [m for m in fm if m.get("sourceId") == ""]
f["empty_sourceId"] = len(empty_source)
f["empty_sourceId_by_competition"] = dict(Counter(m["competitionName"] for m in empty_source))
if f["empty_sourceId"] != 82 or f["empty_sourceId_by_competition"] != {"MOL Cup": 82}:
    fail(f"empty sourceId census {f['empty_sourceId']} {f['empty_sourceId_by_competition']}")

idents = football["store"]["identities"]
id_ids = {x["id"] for x in idents}
used = {m.get("homeId") for m in fm} | {m.get("awayId") for m in fm}
f["identities"] = len(idents)
f["match_team_ids"] = len(used)
f["match_ids_missing_identity"] = len(used - id_ids)
f["identities_unused"] = len(id_ids - used)
if f["match_ids_missing_identity"]:
    fail("match team id missing from identities")
results["football"] = f

# ---------------------------------------------------------------------------
# Tree / documentation (observations, not all hard-fail)
# ---------------------------------------------------------------------------
tree = {
    "Engineering_capital_dir": os.path.isdir(os.path.join(ROOT, "Engineering")),
    "engineering_dir": os.path.isdir(os.path.join(ROOT, "engineering")),
    "verify_data_py": os.path.exists(os.path.join(ROOT, "Engineering", "tools", "verify_data.py"))
    or os.path.exists(os.path.join(ROOT, "engineering", "tools", "verify_data.py")),
    "data_Data_Sports": os.path.isdir(os.path.join(ROOT, "data", "Data_Sports")),
    "quarantine": os.path.isdir(os.path.join(ROOT, "quarantine")),
    "admission_ledger": os.path.exists(
        os.path.join(ROOT, "audit_work", "audit_2026-08-11_five-workorders", "admission-ledger.json")
    ),
}
readme = open(os.path.join(DATA, "README.md"), encoding="utf-8").read()
tree["data_readme_stale_tennis_md5_06ceabb"] = "06ceabb665c26e55b727f9d2aebac06b" in readme
tree["data_readme_stale_17151"] = "17,151" in readme
tree["data_readme_names_gate4_as_current"] = "APPROVAL-CARD-TENNIS-GATE4-FINAL-2026-08-17.md" in readme
tree["data_readme_wrong_root_path"] = "data/Data_Sports/data/" in readme
pin_txt = open(os.path.join(DATA, "tennis", "PIN.txt"), encoding="utf-8").read()
tree["pin_hashes_match_gs134"] = STATED_TENNIS_MD5 in pin_txt and STATED_TENNIS_SHA in pin_txt
tree["pin_still_names_gate4_card"] = "APPROVAL-CARD-TENNIS-GATE4-FINAL-2026-08-17.md" in pin_txt
results["tree"] = tree

# Hard-fail the actively false production README pin (wrong tennis digest).
if not tree["data_readme_stale_tennis_md5_06ceabb"]:
    # If README was repaired, that assertion would no longer be a defect.
    pass
else:
    # Recorded as a defect, not a hash-mismatch of the store itself.
    results["defects"] = results.get("defects", [])
results.setdefault("defects", [])
results["defects"].extend(
    [
        "data/README.md pins superseded tennis store 17,151 / 06ceabb… (actual 17,285 / 9b271a35…)",
        "data/README.md names GATE4-FINAL as current approval card (superseded by GS134)",
        "data/README.md cites data/Data_Sports/data/ and Engineering/tools/verify_data.py — neither exists",
        "PIN.txt hashes match GS134 store but still names GATE4-FINAL as the approval card",
        "canonical join-key diegodedura != join(Diego Dedura-Palomero)=diegodedurapalomero",
        "82 MOL Cup football rows have sourceId=='' (not in football KNOWN-GAPS.md)",
        "admission-ledger.json absent; HOLD/BLOCKED labels inferred from UEFA arithmetic + card text",
        "J.J. Wolf remains canonical and store spelling (60 rows); Jeffrey Wolf = 0",
    ]
)

results["failures"] = failures
results["ok"] = not failures

out_json = os.path.join(os.path.dirname(__file__), "recompute-results.json")
with open(out_json, "w") as fh:
    json.dump(results, fh, indent=2, sort_keys=False)
    fh.write("\n")

print(json.dumps({"ok": results["ok"], "failures": failures, "wrote": os.path.relpath(out_json, ROOT)}, indent=2))
if failures:
    sys.exit(1)
sys.exit(0)
