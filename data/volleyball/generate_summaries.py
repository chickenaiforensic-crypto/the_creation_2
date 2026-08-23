"""
Renders editions/{Competition}/summaries/{Year}.txt for every edition in MANIFEST.json.
Pure rendering from edition JSON + manifest row — nothing fetched or inferred (Director text-account requirement).
Usage: python3 generate_summaries.py  (run after build.py)
"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
ROUND_ORDER = ["RR", "PO", "R16", "QF", "SF", "3P", "F", "5P", "7P", "9P", "11P"]

def main():
    man = json.load(open(os.path.join(BASE, "MANIFEST.json")))
    n = 0
    for ed in man["editions"]:
        d = json.load(open(os.path.join(BASE, ed["file_path"])))
        comp_dir = os.path.dirname(os.path.join(BASE, ed["file_path"]))
        sdir = os.path.join(comp_dir, "summaries"); os.makedirs(sdir, exist_ok=True)
        L = []
        L.append(f"{d['competition']} {d['edition_year']} — {d.get('label','')}".rstrip(" —"))
        L.append(f"tier {d['tier']} | gender {d['gender']} | teams {d.get('team_count','?')} | matches {d['match_count']} | status {ed['status']}")
        L.append(f"hosts: {d.get('hosts','')}")
        L.append(f"source policy: {ed.get('source','')[:200]}")
        L.append("")
        ms = d["matches"]
        phases = []
        for m in ms:
            if m["phase"] not in phases: phases.append(m["phase"])
        for ph in phases:
            L.append(f"== {ph} ==")
            sub = [m for m in ms if m["phase"] == ph]
            sub.sort(key=lambda m: (ROUND_ORDER.index(m["round"]) if m["round"] in ROUND_ORDER else 99, m["date"]))
            for m in sub:
                flags = []
                if m["forfeit"]: flags.append("FORFEIT")
                if m.get("golden_set"): flags.append("GOLDEN SET")
                if m.get("leg"): flags.append(f"leg {m['leg']}")
                if m["home"] in ("A", "B"): flags.append(f"home: {'winner' if m['home']=='A' else 'loser'}")
                f = (" [" + ", ".join(flags) + "]") if flags else ""
                L.append(f"{m['date']} {m['round']:>3} {m['teamA']} d. {m['teamB']} {m['setsA']}-{m['setsB']} ({m['set_scores']}) @ {m['venue_city']}{f}")
            L.append("")
        year = str(d["edition_year"])
        open(os.path.join(sdir, f"{year}.txt"), "w").write("\n".join(L) + "\n")
        n += 1
    print(f"Summaries OK: {n}")

if __name__ == "__main__":
    main()
