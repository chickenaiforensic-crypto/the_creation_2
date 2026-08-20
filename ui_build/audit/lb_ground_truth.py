#!/usr/bin/env python3
"""Shipped audit harness — independent Phase 0 ground truth. Version: v1.4
Reads the RAW engine edition files (not index.json), implements the directive
math from scratch, exports expected leaderboards per scope as JSON.

Usage: python3 ui_build/audit/lb_ground_truth.py <out.json>
"""
import json, re, decimal, os, sys

ENGINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine")
TOKEN = re.compile(r"^(\d+)-(\d+)(\(\d+\))?$")
ROUND_ORDER = {"R128": 0, "R64": 1, "R32": 2, "R16": 3, "QF": 4, "SF": 5, "F": 6}
ROUND_BY_ORDER = {v: k for k, v in ROUND_ORDER.items()}


def is_complete(a, b):
    hi, lo = max(a, b), min(a, b)
    return (hi == 6 and lo <= 4) or (hi == 7 and lo in (5, 6))


def js_fixed1(x):
    """Emulate JS Number.prototype.toFixed(1): ties go to the algebraically larger n."""
    d = decimal.Decimal(x)  # exact expansion of the binary double JS also computes
    rounding = decimal.ROUND_HALF_UP if d >= 0 else decimal.ROUND_HALF_DOWN
    return str(d.quantize(decimal.Decimal("0.1"), rounding=rounding))


def fmt_signed_int(n):
    return f"+{n}" if n > 0 else (str(n) if n < 0 else "0")


def fmt_signed_avg(x):
    s = js_fixed1(abs(x))
    return f"+{s}" if x > 0 else (f"-{s}" if x < 0 else "0.0")


manifest = json.load(open(os.path.join(ENGINE, "MANIFEST.json")))
matches = []
for e in manifest["editions"]:
    d = json.load(open(os.path.join(ENGINE, e["file_path"])))
    assert len(d["matches"]) == e["match_count"], f"count drift {e['file_path']}"
    for r in d["matches"]:
        matches.append({
            "tkey": f"{r['tournament']}|{r['tour']}", "year": r["edition_year"],
            "round": r["round"], "playerA": r["playerA"], "playerB": r["playerB"],
            "score": r["score"], "winner": r["winner"],
        })
print("raw matches loaded:", len(matches))


def scope_rows(tkey, year):
    return [m for m in matches if (not tkey or m["tkey"] == tkey) and (not year or m["year"] == year)]


def leaderboard(rows):
    agg = {}
    sets_counted = sets_excluded = walkovers = 0

    def entry(p):
        return agg.setdefault(p, {"rating": 0, "matches": 0, "best": -1, "champ": False})

    for m in rows:
        eA, eB = entry(m["playerA"]), entry(m["playerB"])
        eA["matches"] += 1
        eB["matches"] += 1
        order = ROUND_ORDER[m["round"]]
        for p, e in ((m["playerA"], eA), (m["playerB"], eB)):
            e["best"] = max(e["best"], order)
            if m["round"] == "F" and ((m["winner"] == "A" and p == m["playerA"]) or (m["winner"] == "B" and p == m["playerB"])):
                e["champ"] = True

        score = (m["score"] or "").strip()
        if score == "W/O":
            walkovers += 1
            continue
        if not score:
            continue
        for tok in score.split():
            mm = TOKEN.match(tok)
            assert mm, f"unexpected token {tok!r} in {score!r}"
            a, b = int(mm.group(1)), int(mm.group(2))
            if not is_complete(a, b):
                sets_excluded += 1
                continue
            hi, lo = max(a, b), min(a, b)
            w, l = (6, 4) if hi == 7 else (hi, lo)
            diff = w - l
            if a > b:
                eA["rating"] += diff; eB["rating"] -= diff
            else:
                eB["rating"] += diff; eA["rating"] -= diff
            sets_counted += 1

    lst = []
    for p, e in agg.items():
        lst.append({
            "player": p, "rating": e["rating"], "matches": e["matches"],
            "avg": e["rating"] / e["matches"] if e["matches"] else 0.0,
            "best": ROUND_BY_ORDER[e["best"]] if e["best"] >= 0 else "—",
            "champ": e["champ"],
        })
    lst.sort(key=lambda r: (-r["rating"], -r["matches"], r["player"]))
    out_rows = []
    for i, r in enumerate(lst):
        out_rows.append([
            i + 1, r["player"], fmt_signed_int(r["rating"]), r["matches"],
            fmt_signed_avg(r["avg"]), "CHAMPION" if r["champ"] else r["best"],
        ])
    return out_rows, {"matches": len(rows), "players": len(lst),
                      "setsCounted": sets_counted, "setsExcluded": sets_excluded,
                      "walkovers": walkovers}


scopes = [
    ("ALL|", "", ""),
    ("ALL|2025", "", "2025"),
    ("Basel|ATP|2025", "Basel|ATP", "2025"),
    ("Basel|ATP|", "Basel|ATP", ""),
    ("US Open|WTA|2023", "US Open|WTA", "2023"),
    ("Cincinnati|WTA|", "Cincinnati|WTA", ""),
    ("Dubai|ATP|2024", "Dubai|ATP", "2024"),
    ("Zhengzhou|WTA|2023", "Zhengzhou|WTA", "2023"),
]

truth = {}
for key, tkey, year in scopes:
    rows, meta = leaderboard(scope_rows(tkey, year))
    truth[key] = {"rows": rows, "meta": meta}
    print(f"{key}: {meta['matches']} matches -> {meta['players']} players, "
          f"sets scored {meta['setsCounted']}, excluded {meta['setsExcluded']}, walkovers {meta['walkovers']}")

out = sys.argv[1] if len(sys.argv) > 1 else "lb_truth.json"
json.dump(truth, open(out, "w"), indent=1)
print("wrote", out)
