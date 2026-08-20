# UI REBUILD — PROVENANCE & AUDIT RECORD

**Current version: v1.6** (version ledger in §10; canonical marker `ui_build/VERSION`)

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

Not implemented in Task 1 (later superseded by the Phase 0 directive of 2026-08-20, which added
the Year/Edition filter): round and surface filters, search over scores, anything else.

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

## 8. Phase 0 Engine Ratings Verification View (Technical Directive 2026-08-20)

**Honesty note for auditors:** no Phase 0 ratings engine pre-existed on this branch
(`engineering/phase_zero/README.md` is a placeholder). The Phase 0 math below was implemented
fresh in `ui_build/app/app.js` (`computeRatings`), exactly per the directive, computed live
in-browser on every filter change. Zero hardcoded presentation values: every POS / PLAYER /
RATING / MATCHES / AVG / ACTUAL POSITION cell is derived at render time from `index.json`.

### 8.1 Rules implemented (verbatim from directive + dataset precedent)
- 7-5 set → normalized down via a **-1 reduction to a 6-4 point basis**.
- 7-6 tiebreak set → **normalized directly to a 6-4 point basis** for the winner.
- All other physically completed sets (6-0…6-4) count their actual game differential.
- Physically incomplete sets (retirement/default mid-set) are **never scored** — the standing
  Phase-Zero precedent already recorded in `data/tennis/KNOWN-GAPS.md` §4 ("Phase Zero scores
  only physically completed sets").
- Walkovers carry the literal score `W/O` in this dataset: counted as a **0-set appearance**
  (MATCHES +1, rating contribution 0).
- Tier labels are treated **strictly as identifiers, never multipliers**. Dataset scan:
  tiers present are GS / M1000 / ATP500 / ATP250 / WTA500 / WTA250 — **zero `1x/2x/3x/4x`
  labels exist in this dataset**, so that mandate is satisfied vacuously and structurally.
- Audit hook: any unparseable score token is excluded AND raises a visible red warning banner
  (element `leaderboard-warn`). Current dataset: **0 unparseable tokens**.

### 8.2 Column semantics (implemented definitions)
- **RATING** = net normalized game differential over all scored sets in scope (integer).
- **MATCHES** = appearances in scope (walkovers included as 0-set appearances).
- **AVG** = RATING ÷ MATCHES, 1 decimal, signed.
- **ACTUAL POSITION** = deepest round reached in scope; `CHAMPION` when the player won a final
  in scope (multi-edition scopes can therefore show several champions).
- **POS** = sequential rank after sorting by RATING desc, tie-breaks MATCHES desc then name asc.
- Filters: Tournament + Year dropdowns (Year options derived from the selected tournament's
  editions; all years otherwise). Both instantly recalculate + resort the leaderboard and the
  match log. The Task-1 player filter still applies to the match log only (stated on-screen).

### 8.3 Score-shape audit of the full dataset (3,828 rows, before any UI code was written)
- Completed-set shapes found: 6-0 (264) · 6-1 (885) · 6-2 (1,408) · 6-3 (2,223) · 6-4 (2,329) ·
  7-5 (862) · 7-6 (1,683). **No malformed or exotic scores exist on this branch** (no `13-12`,
  no `6-6`, no bare tiebreaks).
- 128 retired/defaulted rows end with exactly one incomplete final-set token (all excluded).
- 28 walkover rows carry score `W/O`. 1 defaulted row: Dubai 2024 SF `6-7(4) 7-6(5) 6-5` —
  only the incomplete `6-5` excluded.
- status-vs-flag consistency: 0 mismatches.

### 8.4 Verification of the ratings math (two independent implementations)
Ground truth recomputed in Python from the **raw edition files** (not the index), then the real
`app.js` driven through a DOM stub and compared **cell-by-cell** across 8 scopes
(full dataset; all-2025; Basel ATP 2025; Basel ATP all years; US Open WTA 2023;
Cincinnati WTA all years; Dubai ATP 2024; Zhengzhou WTA 2023):

- Every POS / PLAYER / RATING / MATCHES / AVG / ACTUAL POSITION cell: **PASS**
- Meta counters (matches, players rated, sets scored, incomplete excluded, walkovers): **PASS**
- Descending-sort invariant: **PASS** · audit-warning banner hidden (0 unparsed): **PASS**
- Task-1 regression (tournament + player filters) + full reset: **PASS**

Representative full-dataset outputs (computed, not hardcoded):
9,654 sets scored · 115 incomplete excluded · 28 walkovers ·
POS 1 Jannik Sinner +361 / 87 / +4.1 / CHAMPION · POS 2 Daniil Medvedev +332 / 84 / +4.0 ·
POS 3 Carlos Alcaraz +312 / 76 / +4.1 · POS 5 Novak Djokovic +235 / 46 / +5.1 (highest AVG in top-5) ·
POS 634 Pedro Martinez −67 / 25 / −2.7 (tie with Sebastian Baez −67 resolved by matches desc).

### 8.5 Defect found and fixed during this directive's testing
Reset left the Year filter at its previous value (the year dropdown rebuild preserved the
element's still-set value after state was cleared). Fixed by clearing the element before
rebuild; caught and re-verified by the harness.

## 9. Re-run

```bash
python3 ui_build/build_index.py   # fails loud on any edition/manifest drift
python3 ui_build/serve.py         # http://0.0.0.0:8080
```

Phase 0 ratings are computed live in the browser — no index rebuild is needed for rating
changes; they recompute on every Tournament/Year filter change.

## 10. Version history & versioning rules

**Rule (per user directive 2026-08-20):** every shipped update increments the version
(v1.1 → v1.2 → v1.3 …). The canonical marker is `ui_build/VERSION`; the shipped carrier is
`ui_build/app/version.js` (`window.APP_VERSION`), injected into the header badge and the
browser tab title at load time. Every shipped file also carries a `Version:` header marker.
The audit harness fails if `version.js`, `VERSION`, or any file-header marker drift apart.
**Preview server name rule (v1.5):** the live-preview process name also carries the version and
the page file name (`Tennis UI {version} · index.html`) and is restarted on every version bump,
so the panel label can never lag behind the shipped files. `serve.py` prints the same version
(read from `ui_build/VERSION`) in its startup log.

| Version | Commit | Change |
|---|---|---|
| v1.1 | `9eaf4d6` | Blank UI rebuild on engine content; Task 1 tournament + player filter selector |
| v1.2 | `c3acf05` | Phase 0 Engine Ratings Verification View; Tournament + Year filters; reset-year defect fixed |
| v1.3 | `aa133a8` | Versioning system: visible header badge + tab title, VERSION file, file-header markers, sync check in harness, this ledger |
| v1.4 | `d385d21` | File names surfaced in the UI: served document chip in header (`index.html`) + full shipped-file inventory and engine data-file paths in the footer; audit harness files added to the version sync check |
| v1.5 | `ab4e8de` | Preview server name now carries version + page file name and is restarted on each bump; `serve.py` prints the version from `VERSION` at startup; rule recorded in §10 |
| v1.6 | (this commit) | Usability defects fixed after user audit: Find player now auto-suggests names as you type (click / ↑↓ / Enter), explicit **Search** button (exact match, unique-partial resolution, honest no-match and ambiguous hints), live status banner describing the exact UI state, how-to panel, selected player highlighted on the leaderboard. Functional audit harness expanded to 11 user-flow groups (F1–F11) incl. a full reset proof; all cross-checked against raw engine bytes |
