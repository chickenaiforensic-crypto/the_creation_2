# WORKORDER — Phase 1 Draw-Size Reference & Gap Audit
**Parent document:** WORKORDER_Tennis_Defect_Resolution.md (Phase 1: Scope Lock)
**Repo:** chickenaiforensic-crypto/the_creation_2, branch `arena/01a015bb-the-creation-2`
**Store commit pinned:** `b40331246285c7b88f364c13ea2a71ac26921ae6`
**Purpose:** Build the per-edition draw-size table required to classify R32-level shortfalls as real gaps vs. structural byes, and produce a first, checkable list of genuine missing matches.
**Audit standard:** every claim below carries either a reproducible script + input file, or a named external source. Nothing here should be taken on say-so — re-run the scripts, re-check the sources.

---

## 0. What "done" means for this workorder

A claim only counts as closed if a second person, given only the repo + this document, can reproduce the same number without asking the author anything. Three things are explicitly logged below as **self-caught errors** rather than hidden, because the review process matters as much as the result — if the team re-runs the scripts and gets different numbers than stated here, that's a real finding, not a formatting issue.

---

## Phase 1A — M1000 draw-size table (2021–2025) — STATUS: DONE

**Task:** Determine actual singles draw size (56 vs 96) for every M1000 tournament-edition, since Madrid/Rome/Canada/Cincinnati/Shanghai all changed size mid-window and a static assumption would misclassify results.

**Method:** Web search against tournament-edition-specific sources (Wikipedia edition pages, ATP Tour / WTA Tour official tournament pages), not category defaults. Each entry independently confirmed by at least one edition-specific citation (e.g. "2023 Mutua Madrid Open... Draw: 96S").

**Result:** 73 tournament-editions covered. Deliverable: `draw_size_reference_m1000.json`.

| Tournament | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Indian Wells | 96 | 96 | 96 | 96 | 96 |
| Miami | 96 | 96 | 96 | 96 | 96 |
| Monte Carlo (ATP only) | 56 | 56 | 56 | 56 | 56 |
| Madrid | 56 | 56 | 96 | 96 | 96 |
| Rome | 56 | 56 | 96 | 96 | 96 |
| Canada (Toronto/Montreal) | 56 | 56 | 56 | 56 | 96 |
| Cincinnati | 56 | 56 | 56 | 56 | 96 |
| Shanghai (ATP only, not held '21–'22) | — | — | 96 | 96 | 96 |
| Paris Masters (ATP only) | 56 | 56 | 56 | 56 | 56 |

**Acceptance check for reviewer:** open `draw_size_reference_m1000.json`, pick any 5 entries at random, verify against the cited Wikipedia edition page independently.

**Not yet done:** ATP500/WTA500/ATP250/WTA250 draw sizes (159 more tournament-editions). Two spot-checked so far (Barcelona: 48→32 in 2025; Washington: 48-draw throughout 2021–2025) — the rest of that tier set is asserted from general category knowledge (32-draw standard), not yet individually source-verified per edition the way M1000 was. **This is the largest remaining chunk of Phase 1.**

---

## Phase 1B — Round-of-32-onward gap detection (M1000) — STATUS: DONE, with self-corrections logged

**Task:** Identify genuine missing matches (not byes) by checking that every player who appears in round N+1 has a traceable win in round N.

**Method (reproducible):**
```
For each M1000 tournament-edition 2021-2025:
  for each round transition in [R32->R16, R16->QF, QF->SF, SF->F]:
    winners_in_round_N = { winner_name(match) for match in round N }
    players_in_round_N+1 = { playerA, playerB for match in round N+1 }
    ghosts = players_in_round_N+1 NOT IN winners_in_round_N
    each ghost = one missing match, logged with player name + tournament + edition + exact round transition
```
R64→R32 is deliberately excluded from this pass — see error log below for why.

**Self-caught errors during this work (kept visible, not scrubbed):**
1. **Winner-field bug:** the store's `winner` field holds the literal string `"A"` or `"B"`, not a player name. First-pass code compared names against `"A"`/`"B"` directly and produced a false result (every R16 player flagged as a "ghost"). Caught by manually inspecting one edition's raw rows before trusting the aggregate number. Fixed by resolving `winner` through `playerA`/`playerB` before comparison.
2. **Single-round-pair blind spot:** checking only R32→R16 missed a case where a player skipped a full round of records (WTA Montreal 2021: Coco Gauff won her R64 match, has no R32 match on file at all, reappears directly in the QF). Caught by manually tracing one flagged "clean" edition that had a raw-count anomaly (15 R32 rows, expected 16) but zero ghosts under the single-pair check — the anomaly should have produced a ghost and didn't, which was the tell. Fixed by checking the full round chain, not just adjacent pairs.
3. **Bye false-positive:** the full-chain check's R64→R32 transition initially looked like it was flagging 8-16 "gaps" per edition — these are top seeds who structurally receive first-round byes (8 seeds in a 56-draw, 32 in a 96-draw) and correctly have no R64 match. Confirmed via ATP ranking-points documentation on standard bye structure, then excluded R64→R32 from the "genuine gap" count. Round of 32 itself always has all 32 slots filled (byes are absorbed before that point), so R32-onward transitions are byefree and any ghost there is real.

**Result:** 92 genuine gap instances across 50 of 73 M1000 editions. Each instance names the exact player, tournament, edition year, and round transition. Deliverable: `m1000_r32_onward_gaps.json`.

**Acceptance check for reviewer:** re-run the method above against the raw store file at the pinned commit; the count should reproduce exactly. Spot-check 3–5 individual gap entries against an external result source (e.g. Wikipedia edition draw page) to confirm the named player really is missing a round from the store, not just from this analysis.

---

## Phase 1C — R64 bye-layer verification (M1000) — STATUS: NOT STARTED

**Task:** The bye-count sanity check (expected byes = draw_size − 2×R64_match_count) only matches for 13 of 73 M1000 editions; 60 are off. This means the R64 layer may contain additional real gaps indistinguishable from correct byes using round-transition logic alone — resolving it requires the actual per-edition seeding list (who was seeded, who received the bye), not inference from match counts.

**Method required:** source real draw sheets / seeding lists per edition (73 lookups), compare actual bye recipients against the store's R64-round data.

**Deliverable (not yet created):** `data/tennis/draw_seeding_reference.json` or equivalent, one entry per edition with seed list + confirmed bye recipients.

**Acceptance:** every M1000 edition's R64 layer has a disposition — either the bye count is confirmed correct against real seeding, or specific additional R64-level gaps are named (same format as Phase 1B's output).

---

## Phase 1D — ATP500/WTA500/ATP250/WTA250 draw sizes + gap detection — STATUS: NOT STARTED (2 of 159 editions spot-checked)

**Task:** Repeat Phase 1A + Phase 1B for the remaining 159 tournament-editions across 4 tiers (40 unique tournaments).

**Known so far:**
- Barcelona (ATP500): 48-draw 2021–2024, 32-draw 2025 — sourced
- Washington (ATP500): 48-draw throughout 2021–2025 — sourced
- Remaining ~38 unique tournaments: asserted from general category knowledge (32-draw is standard for ATP250/WTA250/most ATP500/WTA500), not yet individually verified per edition

**Deliverable (not yet created):** `draw_size_reference_500_250.json` + corresponding gap list in the same format as `m1000_r32_onward_gaps.json`.

---

## Deliverables checklist

- [x] `draw_size_reference_m1000.json` (Phase 1A)
- [x] `m1000_r32_onward_gaps.json` (Phase 1B)
- [ ] `draw_seeding_reference.json` — real seeding/bye data, M1000 (Phase 1C)
- [ ] `draw_size_reference_500_250.json` (Phase 1D)
- [ ] Gap list for 500/250 tiers, same format as Phase 1B (Phase 1D)
- [ ] Nothing here has been committed or pushed to the repo — per existing repo governance (gatekeeper approves all merges), these are local deliverables awaiting review/approval before any commit

## Reporting standard going forward

Every phase checkpoint states: what's reproducible right now (with the exact script/method), what's asserted-but-unverified, and what's simply not started. No phase gets marked done until a second party (or a second pass by the same author, explicitly re-deriving rather than re-reading their own prior output) reproduces the number.
