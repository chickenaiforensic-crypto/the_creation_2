# UI REBUILD — PROVENANCE & AUDIT RECORD

**Branch:** `arena/01a01c7b-the-creation-2` · **Role:** Engineer_4 · **Date:** 2026-08-20
**Directive:** pull content from the engine branch only; create a new UI — blank; Task 1 = tournament
filter selector that filters the tournaments and its players. Nothing else was done.

## 1. Data source (engine — content-only pull, NO merge)

- **Source branch:** `arena/01a015bb-the-creation-2`
- **Source tip commit:** `3ee36eb1574e908086ce84c82e419092d7a90655` (confirmed via `git rev-parse FETCH_HEAD`)
- **Method:** `git fetch origin arena/01a015bb-the-creation-2`, then
  `git archive FETCH_HEAD data/tennis | tar -x -C ui_build/engine --strip-components=2`.
  Content extraction only — the engine branch was **not merged**, no local engine branch was created,
  and `main` was **not pulled or touched** (per directive: contaminated).
- **Pulled tree:** the engine's `data/tennis/` verbatim → `ui_build/engine/`
  (187 files, 7.0 MB: `DATA-RULES.md`, `MANIFEST.json`, `WORKORDER-tennis-gap-closure.md`,
  `build.py`, `generate_summaries.py`, `gap_report.json`, `master_store_tennis_SSoT.json`,
  `editions/` (18 tournaments × editions + per-edition summaries + READMEs), `phase1-audit/`).

## 2. Integrity verification of the pulled content (recomputed from bytes)

| Check | Result |
|---|---|
| 78/78 edition files sha256 vs engine `MANIFEST.json` `checksum_sha256` | **PASS** (0 mismatches) |
| 78/78 edition files `match_count` vs actual `len(matches)` | **PASS** (0 mismatches) |
| Total rows across editions | **3,828** |
| Engine `build.py` rerun in a scratch copy (`/tmp`, engine's own script) | `Build OK: 78 editions, 3828 matches` |
| Rebuilt compiled store vs pulled compiled store | **byte-identical** |
| Compiled store sha256 (both) | `20b21c91b67958d238c88906b66ede1b3782ddf2290359d0aa8b40ea20ab27f7` |
| Engine `MANIFEST.json` sha256 | `51efa302e2bf6519d88a448d0a97582d61fcfb1e48f0a88020afcf7053f29762` |

## 3. UI build (blank rebuild — no old UI code reused)

- `ui_build/build_index.py` — fail-loud index builder: re-verifies every edition file's sha256 +
  match count against the engine `MANIFEST.json`; exits non-zero and writes nothing on any mismatch.
  No value in the index is invented; every field is read from the edition files.
- `ui_build/app/index.json` (generated, 1,070,119 bytes) —
  **sha256 `23bdc86ba27855e7baaf303b26e1e6d1d9b48462e94d8d72baee58bc5c229ca2`**.
  Derived counts: **78 editions · 3,828 matches · 18 tournaments (name+tour keys) · 634 players**.
- `ui_build/app/index.html` + `app.css` + `app.js` — new blank UI, no framework.
  Tournament identity is `(tournament, tour)` from the data (Tokyo and US Open each exist as ATP and
  WTA editions — disambiguated, not merged). Row rendering reads the `winner` field; status badges
  come from `walkover`/`retired`/`defaulted` flags. No data-derived number is hardcoded in the UI.
- `ui_build/serve.py` — static server, `0.0.0.0:8080`, no-store caching.

## 4. Task 1 — tournament filter selector (scope)

Implemented: tournament selector (All + 18), dependent player selector per tournament, player
text-filter, player→match filter, reset, live exact counts, match table. Table rendering is capped at
400 visible rows with an explicit on-screen note; counts remain exact.

Not implemented (out of directive): year/round/surface filters, search over scores, anything else.

## 5. Functional audit of the filter logic

A DOM-stub harness (Node) loaded the real `app.js`, drove every control, and cross-checked all counts
and player lists against the **raw engine edition files** (independent recomputation, not the index):

- data strip, option counts, full-dataset render cap: **PASS**
- all 18 tournament keys: player list + match count + rendered rows vs raw bytes: **PASS**
- 5 tournament × 3 player combinations vs raw bytes: **PASS**
- global player filter, text-filter narrowing with selection retention,
  player reset on tournament switch, full reset: **PASS**

Result: `ALL UI FILTER TESTS PASSED` (ground truth: 3,828 matches, 18 tournaments, 634 players).

## 6. Dataset facts as pulled (from bytes; for auditor reference)

- `winner` = `A` on all 3,828 rows (winner-first normalization).
- `status`: completed 3,672 · retired 127 · walkover 28 · defaulted 1.
- Rounds present: R128 (800) · R64 (686) · R32 (1,172) · R16 (624) · QF (312) · SF (156) · F (78).
- Empty dates: 0. Rank fields: 0 (engine Rule 4).

## 7. Deliberately NOT touched (out of scope)

- `main` branch — not pulled (contaminated per directive).
- This branch's `data/` tree (17,285-row tennis SSoT, football store, `data/MANIFEST.json`,
  approval cards) — left byte-identical; the UI consumes only `ui_build/engine/`.
- Known engine anomaly observed during orientation (Basel 2024 `gap_count:1` / Basel 2025
  `gap_count:2` in engine `MANIFEST.json` while statuses read `closed_verified_gapless`):
  reported, not fixed — directive was Task 1 only.

## 8. Re-run

```bash
python3 ui_build/build_index.py   # fails loud on any edition/manifest drift
python3 ui_build/serve.py         # http://0.0.0.0:8080
```
