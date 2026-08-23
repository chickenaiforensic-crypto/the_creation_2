# DATA-RULES-VB.md — Volleyball store law (schema v1.1, Director-approved 2026-08-23)

Binding for every row in `data/volleyball/`. Changes require a disclosed migration note here + in the commit.

## Row schema v1.1 (key order canonical for built rows)
| Key | Type / domain | Rule |
|---|---|---|
| date | "YYYY-MM-DD" | local calendar date of the match; must startwith edition_year |
| competition | string | folder-stable id, e.g. "EuroVolley_W", "World_Championship_M", "VNL_W", "Olympics_M" |
| tier | enum | "OG" · "WORLD-CH" · "CONT-CH" · "VNL" · "QUAL" · "LEAGUE" · "CLUB-WORLD" · "CLUB-CONT" |
| gender | "M" / "W" | |
| phase | string | "Pool A".."Pool F", "Final round", "Classification 5-8", etc. |
| round | enum | "RR" (round-robin) · "R16" · "QF" · "SF" · "F" · "3P" · "5P".."15P" incl. "6P" (placement; **13P/15P + 6P added 2026-08-23 WO-VB-4 migrations** — first 16-team full-classification edition, Asian-M-2021; placement-bracket semifinals typed "PO") · "PO" (playoff) |
| teamA | string | **ALWAYS the match winner** (tennis convention; app relies on it) |
| teamB | string | loser |
| bestOf | 5 | all senior indoor internationals; golden-set exception flagged separately |
| home | "A"/"B"/"N" | **MANDATORY (Director 2026-08-23).** Which side enjoyed home advantage. Two-legged cup/qualifier ties: per-leg truth. Championships on neutral ground: "N" — EXCEPT a host nation playing in the hosting venue = home |
| leg | "" / "1" / "2" | non-empty only for two-legged (home-and-away) cup/qualifier ties |
| winner | "A" | constant |
| edition_year | string | e.g. "2023"; for seasons crossing years (club), the label year defined in the edition census |
| setsA / setsB | int | setsA==3, setsB∈{0,1,2} (forfeit rows follow the federation-recorded scoreline, normally 3-0) |
| pointsA / pointsB | int | derived sums of set tokens; harness-checked |
| set_scores | string | authoritative tokens "25-20 23-25 25-16 25-19", winner's points first in each token |
| duration_min | "" or int-string | "" when source lacks it |
| forfeit | bool | true → status "forfeit", wire-sourced narrative in provenance |
| golden_set | bool | CEV aggregate-tie golden sets only; token appended as "G15-12"-style, excluded from setsA/B |
| venue_city | string | **MANDATORY non-empty (Director 2026-08-23)**; city name in English |
| source | URL | named checkable page for THIS match (official match centre preferred) |
| status | "completed" / "forfeit" | |
| provenance | object | capture_agent "Auditor 1 - arena/01a015bb-the-creation-2", capture_date, ssot_write true, note "WO-VB-N build per PLAN-VB", merge "WO-VB-N-<EVENT>-<YYYY-MM-DD>", raw_source byte-narrative |

## Harness rules (rebuild /tmp/vb_harness.py from this spec after every sandbox reset)
1. winner=="A"; teamA!=teamB; setsA==3 unless golden-set-decided tie (then per-census note), setsB∈{0,1,2}.
2. Token count == setsA+setsB (golden-set token excluded, prefixed "G").
3. Set validity, sets 1–4: winner side w, loser l → (w==25 and l<=23) or (w>25 and w-l==2). Set 5: (w==15 and l<=13) or (w>15 and w-l==2). Each token's first number must be the SET winner's points — sets won by the MATCH loser have l>w impossible; instead tokens are written from match-winner perspective: a token teamA lost reads e.g. "23-25" (a<b). Set-count check: tokens with a>b == setsA, a<b == setsB; per-set validity applied to max/min accordingly. Ties (a==b) forbidden.
4. pointsA == Σ first numbers, pointsB == Σ second numbers.
5. Forfeit hygiene: forfeit→status "forfeit"; scoreline as federation-recorded; provenance narrative mandatory.
6. home∈{A,B,N}; venue_city non-empty; leg∈{"",1,2}; leg non-empty → home != "N".
7. date startswith edition_year (club seasons: window declared in census); duplicate (phase, round, pair, leg) guard; completeness == official match count byte-derived at census (pool of 6 = 15, pool of 4 = 6, KO rounds counted from bracket).
8. MANIFEST sha256/count/status sync; store count == Σ edition matches; PROGRESS-VB.md updated in same commit as any WO state change.

## Naming policy (locked)
- Country teams: English exonyms, one spelling forever, first write wins. Locked now: **"Turkiye"** (no diacritics — store-wide ASCII team names for app safety; people names in future volleyball rosters would keep native diacritics per tennis precedent, but v1.1 rows carry team names only).
- "Korea" = South Korea ("Korea Republic" not used); "Iran", "USA", "Dominican Republic", "Czechia", "North Macedonia", "Great Britain" if ever. Ambiguities adjudicated in census, recorded here.
- **"ROC" adjudication (WO-VB-3, 2026-08-23):** at Tokyo-2020 (played 2021) the Russian team competed as the Russian Olympic Committee under the WADA-ban naming ruling; the edition page prints it `{{vb|RUS|roc-olympics|name=ROC}}` everywhere. Stored **as-printed "ROC"** — a distinct canon string from "Russia" (reserved for rows where the team competed under its own name/flag, e.g. EuroVolley-2021). Rationale: per-row byte truth beats retro-normalisation; a consumer joining across editions can map ROC→Russia knowingly, but the store never asserts a flag the bytes deny.

## Sources (locked hierarchy)
1. CEV.eu / volleyballworld.com official match pages → 2. confederation sites → 3. Wikipedia edition pages (corroboration + completeness template) → 4. wire for forfeit narratives. Grokipedia: rejected class.

## File conventions (identical to tennis)
Edition files `json.dumps(indent=1, ensure_ascii=False)+'\n'`; MANIFEST/gap_report `indent=2`+'\n'; build.py checksum-gated compile; generate_summaries.py renders per-edition text accounts (Director cross-check requirement); git identity `Auditor 1 <auditor1@arena.local>`; long single-line narrative commits.
