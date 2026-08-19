# Phase 1 Draw-Size & Gap Audit — claude_2 branch (CLEAN)

**Status: claude_2 contains ONLY fully closed, individually-verified, in-scope records.**
**For work-in-progress, unresolved, and out-of-scope-but-sourced entries, see the `claude_1` branch.**

This branch is a curated subset of `claude_1`, migrated 2026-08-19. It is intentionally kept
separate from `data/tennis/master_store_tennis_SSoT.json` and its approval-card process — nothing
here should be treated as validated against that store's Gate 4 standard until it goes through
equivalent review.

## Migration criteria (all three required)

An entry was migrated into this branch only if it met all of:
1. Individually VERIFIED with a named, checkable citation (not "carried from prior session, not re-verified").
2. Confirmed present in `master_store_tennis_SSoT.json` under the matching tour/tier/tournament/year
   (so it can actually support Phase 1D gap detection - the workorder's stated purpose).
3. No unresolved flags.

## Files

- `WORKORDER_Phase1_DrawSize_Gap_Audit.md` — the governing workorder.
- `draw_size_reference_m1000.json` — Phase 1A, M1000 draw sizes, 73 editions. Carried from `claude_1`
  unchanged. **Not yet independently re-audited by the Engineer this session** - do not treat as
  closed under the criteria above until that spot-audit is done.
- `m1000_r32_onward_gaps.json` + `reproduce_m1000_gaps.py` — Phase 1B, 92 gap instances across
  50/73 M1000 editions. Independently reproduced via script, entry-for-entry, against the pinned
  commit. Fully closed.
- `draw_size_reference_500_250.json` — Phase 1D draw sizes. **20 of 159 required editions migrated
  here as fully closed**: ATP Rotterdam, ATP Dubai, ATP Halle, ATP Queen's Club, all 2021-2025,
  all ATP500 tier. 129 editions remain unattempted (tracked in `claude_1`, not this branch).

## Explicitly excluded from this branch (sourced but not migrated - see `claude_1`)

- **Barcelona (5), Washington (5)** — carried from a prior session, not independently re-verified
  this session. Likely accurate but not certified under this branch's criteria.
- **Acapulco (5), Rio de Janeiro (5)** — individually source-verified against Wikipedia, but these
  tournaments are **completely absent from `master_store_tennis_SSoT.json`** under any name. Out
  of scope: they cannot support Phase 1D gap detection because there is no match data to check
  gaps against.
- **Hamburg ATP+WTA (10)** — individually source-verified, but Hamburg has **zero rows** in the
  master store under any tour or tier. Out of scope for the same reason as Acapulco/Rio.
- **WTA Dubai (5), WTA Queen's Club (1)** — individually source-verified, but only the ATP side of
  these two events exists in the master store; the WTA side is absent. Out of scope.

Do not treat anything on this branch as final until it's been reviewed the same way the master
store's approval cards are reviewed.
