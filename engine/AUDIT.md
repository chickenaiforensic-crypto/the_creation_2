# ENGINE AUDIT — findings & fixes (session branch `arena/01a01b5f-the-creation-2`)

Audit of the work ported from `arena/01a019b3-the-creation-2` (Engineer 1),
carried out by Engineer 2. Every claim below was confirmed by reading the source
and config in full and by re-running the engine live — none from memory.

**Baseline at audit:** 88 tests green, feed 315 selected / 298 rated / 17 refused /
145 players. All documented headline numbers (leaderboard, per-year #1, ratings %,
performance %) re-derived and matched exactly.

---

## Findings

### A. `years` parameter was dead (FIXED)
- **What:** `/api/matchup` accepted `years` but `matchup_report()` never read it —
  the year selection was always taken from `years_from/years_to` (ratings range).
  Verified: `years=['2021']` returned byte-identical output to no `years`.
- **Fix:** `matchup_report()` now honours an explicit `years` list
  (`effective_years = years if years else range_years`).

### B. "Mute" controls were not wired to the engine's Mutes (FIXED)
- **What:** the Configurations tab labelled three controls "Mute years /
  tournaments / tours", but they were sent as inclusion *Filters*; `matchup_report()`
  hardcoded `mutes = Mutes()` (empty). The real mute mechanism was never exercised.
  "Mute years" did nothing at all (see A).
- **Fix:**
  - `matchup_report()` / `performance_report()` / `ratings_report()` now accept
    `mute_years` / `mute_tournaments` and pass a real `Mutes(...)` through to the
    compute / H2H / performance subsystems.
  - `run_performance()` / `tournament_performance()` thread mutes through (muted
    matches excluded from windows and from baseline ratings).
  - Frontend: "Mute years" → `mute_years`, "Mute tournaments" → `mute_tournaments`
    (true exclusion, matching their labels). "Mute tours" relabelled to
    "Tours (ATP / WTA)" — it is an inclusion filter for the US Open ATP/WTA split,
    not a mute.

### C. Zero-hardcoding violations (FIXED)
- `compute.py:_rate_match` read `match.get("date")` / `match.get("round")` with
  literal keys instead of config field names (worked only because config names them
  the same). → now uses `f["date"]` / `f["round"]`.
- `app.js` hardcoded UI strings: `"Team A vs Team B"`, `"Points per game difference"`,
  `"Feed tournaments"`, `"Sports exposed"`, `"Development lock"`, the ratings no-data
  sentence, and the `"H2H "` stat prefix. → all moved to `config/ui.json`
  (`matchup_selector.team_vs_title`, `parameters_labels.*`,
  `ratings_percentage.no_data_text`, `h2h.system_rating_prefix`).

### D. Stale test count in PHASE-0.md (FIXED)
- §2.6 said "41 tests green" (Phase-0 scope only). Branch now carries 96. Updated.

### E. Minor documentation drift (FIXED)
- `convert/ratio.py` docstring said `%B = pointsB/total`; the code computes
  `100 - %A` (equivalent — no bug). Docstring corrected.
- `server.py` endpoint list omitted `/api/performance` and `/api/ratings`. Updated.

### F. Multi-select query values were not split (FIXED — latent bug)
- The frontend joins multi-select controls with commas (`"a,b,c"`); the server's
  `parse_qs` kept each joined string as a single item, so any multi-select filter
  (years, tournaments, tours) silently matched nothing.
- Fix: new `_csv()` helper in `server.py` splits comma-joined values for all list
  params.

### G. Two normalisations of a 7-6 set inside H2H (NOT CHANGED — Director note)
- H2H game-difference normalises 7-6 → 6-4 (Phase 0 rule); H2H region-points /
  percentage normalises 7-6 → 6-5 (conversion-layer theory table). Both are
  documented, but the two different normalisations coexist inside one module and
  should be re-confirmed by the Director. No change made without sign-off.

### H. Ratings range also restricts H2H match selection (NOT CHANGED — behaviour note)
- `years_from/years_to` (ratings range) is used both as the ratings-percentage
  scope AND as the year filter for the H2H match selection. This is the existing
  tested behaviour; flagged for the Director in case H2H should instead be bounded
  only by the date boundary (`from`), not the ratings range.

---

## New feature added this session

**Ratings-only page** (new "Ratings" tab + `/api/ratings` endpoint).
- Definition (config `ratings.json`): a player's rating is the **accumulation of
  their own Phase 0 points per match, without subtracting the opponent's points**
  (distinct from the Phase 0 delta rating `pA = totalA − totalB`).
- Filters: tournament (single, from the full dataset), year or year period
  (`years_from` / `years_to`), plus optional `tours`, `mute_years`,
  `mute_tournaments`.
- Output: total rating, matches rated, points by year, points by tournament, and a
  chronological per-match breakdown (date, round, opponent, score, points).
- Subsystem: `sport_engine/ratings/ratings.py` (`run_ratings`), reusing the
  manifest-verified loader + Filters/Mutes selection + live `compute_ratings`.

**Verification (live, this session):**
- Sinner, Cincinnati Masters (all years): rating **274**, 14 matches,
  per-year {2021:38, 2022:40, 2023:8, 2024:88, 2025:100}.
- Sinner, 2024 only: **88**.
- Mute `2024` on Sinner vs Alcaraz: ratings points 274→186, 302→284.
- Tests: **96 green** (88 prior + 8 new in `tests/test_ratings.py`).
