# SPORT ENGINE — pluggable data-processing engine (for the app / UI)

Processes sport data (tennis, football, expandable) into ratings and derived outputs
consumed by the UI. Sport adapters are registered in a pluggable registry — adding a new
sport means adding one adapter, no engine changes.

## Layout

```text
engine/
├── README.md
├── sport_engine/
│   ├── __init__.py
│   ├── registry.py          # pluggable sport registry
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── base.py          # SportAdapter contract
│   │   ├── tennis.py        # tennis match -> per-set game scores
│   │   └── football.py      # STUB — football phase not specified yet
│   └── rating/
│       ├── __init__.py
│       └── phase0.py        # Phase 0 match-rating math (sport-agnostic)
└── tests/
    ├── __init__.py
    ├── test_phase0.py
    └── test_tennis_adapter.py
```

## Phase map

| Phase | Status |
|---|---|
| Phase 0 — match rating | IMPLEMENTED + tests green (2026-08-19) |
| Football mapping | NOT SPECIFIED — adapter stubbed, raises NotImplementedError |
| Rating accumulation (career/season) | NOT SPECIFIED — later phase |
| UI-facing outputs | NOT SPECIFIED — later phase |

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

## Open questions — answered (Director, 2026-08-19)

1. `7-6` tiebreak sets: **answered** — they resolve to `6-4` for the winner (never
   `6-5`), regardless of how long a tiebreak lasted.
2. `1x / 2x / 3x / 4x`: **answered** — they are section identifiers of the score,
   **not multipliers**. They are recorded per set but never applied as multipliers.

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
