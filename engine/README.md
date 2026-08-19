# SPORT ENGINE — pluggable data-processing engine (for the app / UI)

Processes sport data (tennis, football, expandable) into ratings and derived outputs
consumed by the UI. Sport adapters are registered in a pluggable registry — adding a new
sport means adding one adapter, no engine changes.

## Layout

```text
engine/
├── README.md
├── PHASE-0.md               # Phase 0 document — what it is + everything done
├── config/                 # ALL values/names live here (zero-hardcoding)
│   ├── rating_rules.json   # Phase 0 points table, sections, resolution rules
│   ├── tennis_schema.json  # tennis match-row field names, score grammar
│   ├── football_schema.json# football adapter identity (stub)
│   ├── sports.json         # active adapter list (the plug point)
│   ├── compute.json        # data root, manifest file, feed scope, default mutes
│   ├── manifest_schema.json# MANIFEST.json + edition-file field names
│   ├── position_rules.json # round → actual position/label mapping
│   └── test_data.json      # test fixtures + expected outcomes
├── reports/                # engine-rendered outputs
│   ├── ratings_table_cincinnati_masters_2021.md
│   └── ratings_tables_by_year.txt
├── sport_engine/
│   ├── __init__.py
│   ├── config.py           # config loader (fails loudly)
│   ├── registry.py         # pluggable sport registry
│   ├── adapters/
│   │   ├── __init__.py     # auto-registers adapters from sports.json
│   │   ├── base.py         # SportAdapter contract
│   │   ├── tennis.py       # tennis match -> per-set game scores
│   │   └── football.py     # STUB — football phase not specified yet
│   ├── rating/
│   │   └── phase0.py       # Phase 0 match-rating math (sport-agnostic)
│   └── compute/
│       ├── __init__.py
│       ├── selection.py    # Filters + Mutes (pure selection logic)
│       ├── data_source.py  # manifest-verified edition loading
│       ├── compute.py      # compute_ratings() orchestrator
│       └── ratings_table.py# per-year tables + render_table_text
└── tests/
    ├── __init__.py
    ├── test_phase0.py
    ├── test_tennis_adapter.py
    ├── test_config.py
    ├── test_compute.py
    └── test_ratings_table.py
```

## Phase map

| Phase | Status |
|---|---|
| Phase 0 — match rating | IMPLEMENTED + tests green (2026-08-19) |
| Computational layer — filters + mutes + live compute | IMPLEMENTED + tests green (2026-08-19) |
| Ratings table view — per-year tournament tables + selectable filters | IMPLEMENTED + tests green (2026-08-19) |
| Phase 1 — Head-to-Head (H2H) module | IMPLEMENTED + tests green (2026-08-19) |
| Phase 1 SaaS UI presentation layer (zero-hardcoded) | IMPLEMENTED — live dev server (2026-08-19) |
| Football mapping | NOT SPECIFIED — adapter stubbed, raises NotImplementedError |
| Rating accumulation (career/season) | NOT SPECIFIED — later phase |
| UI-facing outputs | NOT SPECIFIED — later phase |

## Computational layer (Director spec, 2026-08-19)

`compute_ratings(filters=None, mutes=None)` computes Phase 0 ratings **live** from the
edition files (never precomputed, never writes to the data tree). Every edition is
verified against `MANIFEST.json` (SHA-256 + match count) before use — any mismatch
raises `DataIntegrityError`, nothing is silently skipped.

**Feed scope (config `compute.json`):** for now the engine is fed **Cincinnati Masters
only** (2021–2025). Explicit filters compose with the feed: a category the caller
leaves empty falls back to the feed's value.

**Filters** (`Filters(tournaments, years, players, tiers)`): empty category = all;
non-empty = OR within a category, AND across categories.

**Mutes** (`Mutes(mute_years, mute_tournaments)`): designated years/tournaments are
removed from the selected set before computation and never appear in output results.
Caller mutes union config defaults.

**Output:** `scope` (filters, mutes, `loaded_editions` = the verified universe of all
manifest editions, `feed_editions` = the editions the computation actually drew from,
data root), `summary` (selected / rated / refused / players), `matches` (every selected
match — rated rows carry rating/points/sections, refused rows carry
`rateable: false` + `reason`), `players` (rating = sum of match ratings, matches,
average, refused; sorted by rating desc).

Void matches (retired / walkover / defaulted / unfinished) are **refused, never
guessed** — they appear in the report with their reason.

## Ratings table view (per year, selectable filters)

`build_ratings_table(filters=None, mutes=None)` produces **one tabulated ratings table
per (year, tournament)** in the selected set — each year's tournament listed like the
2021 table, top to bottom by engine rating, every player on its own row with the
actual-performance position beside it. The UI's year + tournament filters map directly
to `Filters(years=[...])` / `Filters(tournaments=[...])`; the feed scope from config
still applies underneath.

- Position column is derived from the stored result tree (winner + round fields);
  round → position mapping lives in `config/position_rules.json`
  (F 1st/2nd, SF 3rd, QF 5th, R16 9th, R32 17th, R64 33rd, R128 65th). Joint finishes
  share the position number but are listed on separate rows — never combined.
- `render_table_text(table)` renders one table as fixed-width tabulated text for
  display/copy.
- Zero-hardcoding: years, tournaments, players, round names and positions all come
  from data + config. `engine/reports/ratings_tables_by_year.txt` shows all years
  rendered by the engine.

## Phase 1 — Head-to-Head (H2H) module (Director spec, 2026-08-19)

`run_h2h(filters=None, mutes=None)` is a **stand-alone, decoupled subsystem** that
computes the **direct game score difference** between pA and pB — the margin —
while the primary Phase 0 rating tracks absolute points (no margins).

- **Point allocation:** points awarded per game of score difference
  (`config/h2h.json`, `points_per_game_difference = 1`). Normalised sets are the
  source: every set goes through the pre-built Phase 0 normalisation (7-5 → 6-4,
  7-6 → 6-4, orientation preserved), then per-set game differences are summed.
  Example `6-2 6-4` → +6 games → pA +6 H2H, pB −6 (vs Phase 0 +14/−14 — different
  metric by design).
- **Decoupled architecture:** own package `sport_engine/h2h/`, own data model
  (no points/rating fields), own pipeline (load → filter/mute → extract →
  normalise → difference → aggregate), own state. Reuses only the pre-built
  difference machinery (`TennisAdapter.extract_sets`, Phase 0 `normalize_set`)
  and the shared manifest-verified loader + pure Filters/Mutes selection. Never
  imports the absolute-point routines (`rate_sets`, `compute_ratings`).
- **Same feed scope** as the primary layer (config `compute.json` — Cincinnati
  Masters only), same filters/mutes semantics.
- **Tournament-aware tracking (Phase 1 extension):** every player carries a
  per-tournament context (matches, games_for, games_against, game_difference,
  average per tournament) alongside all-tournament totals — the module traces
  the specific tournament context for each individual player. The tournaments
  filter supports **multi-tournament ingestion** (e.g.
  `Filters(tournaments=["Cincinnati Masters", "Dubai"])`) so future engine
  expansions can evaluate cross-tournament player matchups.
- **Future per-tournament calibration hook:** `sport_engine/h2h/conversion_hook.py`
  is an abstraction for a conversion subsystem that will normalize separate raw
  tournament ratings for cross-tournament H2H comparison when two players arrive
  from different tournament data pools. Config `h2h_tournament.json`
  (`conversion_hook.enabled: false`, `method: not_specified`); the report exposes
  `conversion_hook.available` — currently `false`, never applied, `convert()`
  raises `NotImplementedError` until the Director specifies the conversion.
- **Output:** `summary` (selected/rated/refused/players), `matches` (per-match
  games_a/games_b, game_difference, h2h_a/h2h_b, per-set breakdown), `players`
  (games_for, games_against, game_difference, average, refused; ranked by
  difference desc). Void matches refused with reason, same policy as Phase 0.

Verified by hand: Zverev 2021 +29 (7-6(3) 6-2 +6 · 6-2 6-3 +7 · 6-1 6-3 +8 ·
6-4 3-6 7-6(4) +1 · 6-2 6-3 +7), Sinner 2021 +4 (6-2 7-5 +6, R32 loss −2),
Medvedev 2021 +22. Feed: 315 selected / 298 rated / 17 refused / 145 players.

## Phase 1 SaaS UI presentation layer (Director spec, 2026-08-19)

`python3 sport_engine/ui/server.py 8080` — professional reactive SaaS UI with
functional placeholders mapped to dynamic data hooks (strictly zero hardcoding:
every label, list, and default renders from the `/api/ui` manifest, which is
driven by `config/ui.json`, `config/sports.json`, and live engine data).

- **Selectable sports type control:** top-level Tennis / Football selector.
  The engine enforces a **development lock** (`config/sports.json`
  `development_lock`): no new sport may be exposed until the Tennis module is
  fully stabilized and verified with prediction accuracy exceeding 80%.
- **Matchup selector:** dual-entity dropdowns — Player A vs Player B (Tennis) /
  Team A vs Team B (Football), options from live data.
- **Prediction vector (master stat):** central live vector block for the
  predictive balance (pA % | pB %). Predictive logic is unbuilt, so it renders
  a **zeroed/connecting state** (`state: "zeroed"`, pA/pB null).
- **System rating data:** dynamic container rendering the live system rating per
  player (Phase 0 rating) + H2H game difference.
- **H2H analysis summation module:** aggregation component tracking historical
  H2H encounters within a user-defined date boundary; outputs the net H2H
  balance and an interactive action icon opening a chronological drill-down
  table (date, players, score, per-side H2H, winner).
- **H2H percentage aggregation (Phase 1 extension):** the standalone H2H module
  aggregates the total rating points gathered by each player across their
  DIRECT historical encounters and converts the absolute point totals into a
  relative balance out of 100%. Linear baseline for this iteration
  (`config/h2h.json` `percentage.scaling: "linear"`); the exponential scaling
  expansion factor (to prevent high-margin victories collapsing into 51%-49%)
  remains **disabled** (`exponential_enabled: false`).
- **Targeted player search input:** the horizontal matchup selector uses
  searchable inputs (datalist over the full 577-player dataset) — any explicit
  pair can be loaded directly to generate its isolated H2H percentage profile.
- **Tournament UI filter:** a global Tournament Filter dropdown on the active
  view constrains or broadens the dataset feeding the ratings and H2H
  computations — options are the full dataset (10 tournament names; US Open
  ATP/WTA separated via the tours filter). "All tournaments" falls back to the
  feed default (Cincinnati Masters).
- **API:** `/api/ui`, `/api/options`, `/api/matchup?a=..&b=..&tours=..&tournaments=..&years=..&from=..`.
- **Tour filter (approved):** US Open ATP/WTA are now selectable separately via
  the `tours` filter (e.g. `tours=ATP` vs `tours=WTA`), since both share the
  tournament name "US Open" and differ only by the `tour` field.

## Phase 0 — match rating (Director spec, 2026-08-19)

Rate a match `pA vs pB` from per-set game scores.

1. Normalise each set: `-1` on both sides until the higher side has 6 games.
   Any set won by more than 6 games (`7-5`, `7-6`, `8-6`, `9-7`, …) resolves to
   **6-4 for the winner, regardless of how long a tiebreak lasted**
   (Director answer, 2026-08-19). Side orientation is preserved.
2. Points per player per set, from games won (after normalisation):

   | Games won | Points | Section |
   |---|---|---|
   | 0–2 | 2 | 1x |
   | 3–4 | 4 | 2x |
   | 5 | 7 | 3x |
   | 6 | 10 | 4x |

   `1x / 2x / 3x / 4x` are **section identifiers of the score, not multipliers**
   (Director answer, 2026-08-19).

3. Match totals = sum of per-set points.
4. Rating: `pA = totalA - totalB`, `pB = totalB - totalA`.

### Worked example (verified)

Sets `6-2`, `6-4`:

| Set | pA games | pA pts | pB games | pB pts |
|---|---|---|---|---|
| 1 | 6 | 10 | 2 | 2 |
| 2 | 6 | 10 | 4 | 4 |
| **Total** | | **20** | | **6** |

`pA = 20 - 6 = +14` · `pB = 6 - 20 = -14` — matches the spec exactly.

Tiebreak set example (Director answer): sets `6-4`, `7-6` — the `7-6` set resolves
to `6-4` (winner 10 pts, loser 4 pts), so totals are 20 / 8, rating `+12 / -12`.

## Resolved — Phase 0 (Director answers + fixes)

1. `7-6` tiebreak sets: **resolved** — they resolve to `6-4` for the winner (never
   `6-5`), regardless of how long a tiebreak lasted (Director answer, `561cd03`).
2. `1x / 2x / 3x / 4x`: **resolved** — section identifiers of the score, **not
   multipliers**; recorded per set, never applied as multipliers (Director answer,
   `561cd03`).
3. Orientation bug: **fixed** — B-won sets were briefly credited to A (orientation
   loss in normalisation); found via real data, fixed with regression test
   (`39ab1e6`).

## Integrity rules (engine side)

- A match is only rateable when `status == completed` and not `retired / walkover /
  defaulted`, and every set has a winner (no unfinished sets like `6-6`). Anything else is
  refused (`None`), never guessed.
- Incomplete/void rows and contradictory set data are surfaced as `not rateable`, not rated.

## Zero-hardcoding rule (binding)

- Every spec value and schema name lives in `engine/config/*.json` — never in code:

  | File | Content |
  |---|---|
  | `rating_rules.json` | Phase 0 points table, sections, max winner games, resolved loser games |
  | `tennis_schema.json` | Tennis record field names, void flags, score grammar |
  | `football_schema.json` | Football adapter identity (stub) |
  | `sports.json` | Active adapter list (the plug point) |
  | `compute.json` | Data root, manifest file, feed scope, default mutes |
  | `manifest_schema.json` | MANIFEST.json + edition-file field names |
  | `position_rules.json` | Round → actual position/label mapping |
  | `test_data.json` | Test fixtures + expected outcomes (tests are data-driven, no literals) |

- Changing a rule = edit the config JSON, no code change.
- Config is validated at import (missing/invalid/empty config fails loudly — no silent
  defaults; the points/section tables must cover `0..max_winner_games` fully).
- Code contains structure only. The engine version string in
  `sport_engine/__init__.py` is the single deliberate literal (code metadata, not data).

## Run tests

```bash
cd engine && python3 -m unittest discover -s tests -v
```
