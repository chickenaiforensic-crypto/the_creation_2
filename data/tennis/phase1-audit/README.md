# Phase 1 Draw-Size & Gap Audit — claude_1 branch

**Status: IN PROGRESS. Not reviewed. Not merged into the Gate-4-approved master store.**

This branch is a working area for the Phase 1 draw-size reference + gap audit described in
`WORKORDER_Phase1_DrawSize_Gap_Audit.md`. It is intentionally kept separate from
`data/tennis/master_store_tennis_SSoT.json` and its approval-card process — nothing here
should be treated as validated against that store's Gate 4 standard until it goes through
equivalent review.

## Files

- `WORKORDER_Phase1_DrawSize_Gap_Audit.md` — the governing workorder.
- `draw_size_reference_m1000.json` — Phase 1A, M1000 draw sizes, 73 editions. Reported DONE
  in a prior session; 5 entries independently spot-audited this session against edition-specific
  sources and held up (see commit history). Not re-verified in full.
- `m1000_r32_onward_gaps.json` — Phase 1B, 92 genuine gap instances across 50/73 M1000 editions.
  Reported DONE with 3 logged self-corrections in a prior session. Not re-run this session.
- `draw_size_reference_500_250.json` — Phase 1D, ATP500/WTA500/ATP250/WTA250 draw sizes.
  **13 of 159 editions verified this session** (Rotterdam 2022–2025, Dubai 2021–2025 ATP,
  Dubai WTA 2021/2023–2025). 2 entries explicitly flagged unresolved (Rotterdam 2021, WTA
  Dubai 2022). The remaining ~145 editions across ~36 tournaments are NOT STARTED.

## Not yet touched

- Phase 1C (M1000 real seeding/bye verification, 73 editions) — not started.
- Phase 1D gap detection (once draw sizes are complete) — not started.
- Remaining ATP500/WTA500/ATP250/WTA250 tournaments — not started.

## Known trap flagged during this work

WTA official "Overview" pages (`wtatennis.com/tournaments/{id}/{name}/{year}`) sometimes serve
generic/evergreen current-state copy on old-edition URLs rather than edition-specific figures.
Confirmed cases: WTA Rome 2022, WTA Toronto 2022. Use the edition-specific Wikipedia article or
the WTA/ATP draws archive instead.

Do not treat anything on this branch as final until it's been reviewed the same way the master
store's approval cards are reviewed.
