# PHASE 0 — MATCH RATING ENGINE (what it is, everything done)

**Engine:** Sport Engine (`engine/`) — pluggable sport data-processing engine for the
app/UI. **Phase 0** is the match-rating phase: it converts stored tennis match data
into per-player ratings.
**Author:** Engineer 1 · **Branch:** `arena/01a019b3-the-creation-2` · **Date:** 2026-08-19
**Audit status:** independently auditable — every number in this document is
reproducible from the branch bytes (data files + engine code + config), none from memory.

---

## 1. What Phase 0 is

Phase 0 rates a tennis match `pA vs pB` from its per-set game scores. The spec was
given by the Director on 2026-08-19 and is implemented exactly as specified:

1. **Normalise each set:** subtract 1 from BOTH sides until the higher side has
   **6 games** (`7-5` resolves to `6-4`). Side orientation is preserved so points go
   to the correct player.
2. **Points per player per set** (from games won after normalisation):

   | Games won | Points | Section |
   |---|---|---|
   | 0–2 | 2 | 1x |
   | 3–4 | 4 | 2x |
   | 5 | 7 | 3x |
   | 6 | 10 | 4x |

   `1x / 2x / 3x / 4x` are **section identifiers of the score**, not multipliers
   (Director answer, 2026-08-19).
3. **Match totals** = sum of per-set points for each player.
4. **Rating:** `pA = totalA − totalB` · `pB = totalB − totalA`.

**Worked example (Director's, verified):** sets `6-2`, `6-4` → pA 10+10 = 20 pts,
pB 2+4 = 6 pts → **pA rating +14, pB −14**.

**Tiebreak rule (Director answer, 2026-08-19):** any set won by more than 6 games
(`7-5`, `7-6`, `8-6`, `9-7`, …) resolves to **6-4 for the winner, regardless of how
long a tiebreak lasted** (never `6-5`). Example: sets `6-4`, `7-6` → the `7-6` set
resolves to `6-4` → totals 20 / 8 → rating `+12 / −12`.

---

## 2. Everything done for Phase 0

### 2.1 Data

- **Source:** `data/tennis/` pulled from `arena/01a015bb-the-creation-2` (tip
  `d8b951f`): **53 fully-audited editions across 11 tournaments** — Cincinnati (WTA
  M1000), Cincinnati Masters (ATP M1000), Cleveland (WTA 250), Dubai (ATP 500),
  Halle (ATP 500), Metz (ATP 250), Monastir (WTA 250), Queen's Club (ATP 500),
  Rotterdam (ATP 500), US Open (ATP GS), US Open WTA (WTA GS), 2021–2025 — +
  `MANIFEST.json` + `DATA-RULES.md` + per-edition `.txt` summaries. (The source
  branch also carries Tokyo ATP/WTA — 8 editions, 232 rows — not in the Director's
  completed-data list; not pulled.)
- **Verified on pull (read-only):** 53/53 manifest entries — SHA-256 checksums and
  match counts match the files, **0 errors**; master store `count == len(matches)`
  (2,917); all 53 per-edition `.txt` summaries present; `build.py` runs clean.
- **Branch scope is 2021–2025 only.** No 2026 or unplayed events are treated as gaps.
- **Feed (config `compute.json`):** for now the engine is fed **Cincinnati Masters
  only** — 5 editions, 315 matches.

### 2.2 Engine build (structure only — zero hardcoding)

- **`sport_engine/rating/phase0.py`** — the Phase 0 math (sport-agnostic). All spec
  values load from `config/rating_rules.json` (points table, sections, max winner
  games, resolved loser games); config validated at import, fails loudly.
- **`sport_engine/adapters/`** — pluggable sport adapters. `tennis.py` parses the
  stored score strings (`6-4 7-6(4)` → sets) and **refuses** any match that is not
  fully rateable; `football.py` is a stub (raises `NotImplementedError` until the
  Director specifies the football mapping — nothing invented).
- **`sport_engine/registry.py`** — pluggable registry; active sports list from
  `config/sports.json` (auto-discovery, no sport names in code).
- **`sport_engine/compute/`** — computational layer:
  - `data_source.py`: loads edition files **verified against the manifest**
    (SHA-256 + match count); any drift raises `DataIntegrityError`.
  - `selection.py`: `Filters` (tournaments, years, players, tiers) + `Mutes`
    (mute_years, mute_tournaments) — muted data is removed before computation and
    never appears in results.
  - `compute.py`: `compute_ratings()` — live computation with filters/mutes; feed
    scope from config composes underneath.
  - `ratings_table.py`: `build_ratings_table()` + `render_table_text()` — per-year
    tournament tables, every player individually ranked by rating with the
    actual-performance position column (positions from `config/position_rules.json`).
- **Zero-hardcoding rule (binding, applied):** all spec values, schema names,
  years, tournaments, players, round names, positions live in `engine/config/*.json`
  or the data — never in code. Grep-audited; only deliberate literal is the engine
  version string.

### 2.3 Void-match policy (refused, never guessed)

A match is rateable only when `status == completed`, not retired/walkover/defaulted,
and every set has a winner. Void rows are **refused** (`None`) and appear in engine
output with their reason — never guessed or imputed. The full register of every
non-rateable / missing-data row is in `data/tennis/DATA-INACCURACIES.md` (single
file): 58 void matches (47 retired, 10 walkover, 1 defaulted) + 114 completed rows
with the optional `duration_min` absent (optional field, not required by the schema).
The data is gapless: 53/53 editions `closed_verified_gapless`, `gap_count 0`.

### 2.4 Results — Cincinnati Masters 2021–2025 (engine output)

Feed totals: **315 matches selected · 298 rated · 17 refused** · 145 players rated.

| Year | Matches | Rated | Refused | Players rated | Engine #1 (rating) | Champion (rating) |
|---|---|---:|---:|---:|---|---:|
| 2021 | 55 | 55 | 0 | 56 | Zverev (+62) | Zverev (+62) |
| 2022 | 55 | 54 | 1 | 56 | Coric (+70) | Coric (+70) |
| 2023 | 55 | 50 | 5 | 55 | Djokovic (+46) | Djokovic (+46) |
| 2024 | 55 | 52 | 3 | 56 | Sinner (+38) | Sinner (+38) |
| 2025 | 95 | 87 | 8 | 94 | Sinner (+72) | Alcaraz (+50) |

All-year leaderboard (top 10 by rating): Zverev +152 · Sinner +106 · Alcaraz +70 ·
Coric +64 · Rublev +58 · Medvedev +58 · Auger-Aliassime +56 · Hurkacz +52 ·
Tsitsipas +52 · Tiafoe +46.

**Deliverables rendered by the engine:**
- `engine/reports/ratings_table_cincinnati_masters_2021.md` — 2021, all 56 players,
  tabulated, top to bottom by rating, actual position beside each.
- `engine/reports/ratings_tables_by_year.txt` — all 5 years rendered.
- The ratings-table view is selectable by **year and tournament** filters
  (`Filters(years=[...])`, `Filters(tournaments=[...])`) for the UI.

### 2.5 Score Calibrator — built, analyzed, dropped (Director decision)

Per the Director's ambition to align ratings with the leaderboard, a Score
Calibrator was built (regional analysis 1st→last, isotonic/PAVA). Central
cross-year analysis over all 320 players (2021–2025) showed the pooled region means
are already ordered (1st 53.20 > 2nd 30.80 = 3rd 30.80 > 5th 14.10 > 9th 10.05 >
17th 0.15 > 33rd −8.42 > 65th −10.81), so the central adjustments are **all 0.00**
and raw accuracy equals calibrated accuracy exactly (**90.31% = 90.31%**).
**Director decision (2026-08-19): the calibration changes nothing, so it is
dropped — the engine uses the raw Phase 0 points.** All calibrator code, config,
tests, and documentation were removed from the branch.

### 2.6 Verification (how the auditors can check)

- **Tests:** `cd engine && python3 -m unittest discover -s tests` → **41 tests green**
  (phase 0 math, adapter, compute, config, ratings table; fixtures in
  `config/test_data.json`, data-driven, no literals).
- **Data integrity:** `MANIFEST.json` — 53 editions, 0 checksum/count errors.
- **Independent recomputation:** Sinner 2021 = +8, Sinner 2021–2024 = +34, full
  2021 leaderboard, per-year ratings — all re-derived with a separate plain-python
  implementation of the spec; identical results.
- **Hand-verified:** Zverev 2021 +62 (R32 +14, R16 +14, QF +14, SF +6, F +14);
  Djokovic 2023 +46 (4 rated matches, R32 retirement refused); calibration 2021
  2nd +6.5 / 3rd −6.5 (pre-drop).

---

## 3. Commit record (this branch)

- `39ab1e6` Phase 0 rating core + pluggable registry (orientation bug found via real
  data and fixed in the same build).
- `25a24e6` Purged inherited main files; pulled clean tennis data from the data branch.
- `398caed` Zero-hardcoding: spec values/schema names → `engine/config/*.json`.
- `c54e4f6` + `9db8701` Zero-hardcoding complete: test fixtures externalized.
- `561cd03` Director answers applied: 7-6 → 6-4; sections are identifiers.
- `0998a1c` Computational layer: filters + mutes + live compute (Cincinnati feed).
- `65f49e0`, `c3f3f0c`, `a4ff379` Ratings table view + 2021 table (all 56 players).
- `4cec136` Ratings table view engine feature (per-year, selectable filters).
- `bbc154f` Score Calibrator (built).
- `bc19f29` Calibrator → central analysis, calibration dropped (raw points used).
- `7515afd`, `486a1c2`, `e0c0357` Data-inaccuracies register + context cleanup.
- `8e6310c` Calibrator fully removed; this Phase 0 document added.
