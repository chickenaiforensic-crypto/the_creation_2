# BRANCH-VS-MAIN-TENNIS-DIFF — full inventory + proposed work orders — 2026-08-19 — AUD1

**Purpose:** the Director will hand branch files to the auditing team directly; this document is the byte-derived map of exactly what differs between `main`'s legacy tennis artifact and this branch's curated corpus, and the proposed work orders to pull + audit known AND unknown gaps before any fixing.

**Measured from bytes this session:** branch `arena/01a015bb-the-creation-2` @ `5967c0d` (202 editions / 14,892 rows / full audit ISSUES:0) vs `origin/main` @ `7f104e7` (`data/tennis/master_store_tennis_SSoT.json`, 17,285 rows / 305 (tournament,tour,year) editions; pinned 2026-08-17, "v5 canonical + Phase B"). Diff regenerated fresh after a sandbox reset — nothing below is from memory.

## Self-corrections logged with this filing (prose-level, zero data impact)
1. My earlier reply said "2026 is not included" — **false**: the branch contains 15 completed early-2026 editions (AO/IW/Miami/MC/Madrid/Rome/RG/Wimbledon = 1,577 rows), harness-verified. A coverage-matrix print also hard-coded columns 2021–2025 and silently hid the 2026 column. Display/prose only.
2. Prior message said 23 out-of-scope families and 110 shared-delta editions; bytes say **24** (Auckland and Stuttgart each split ATP/WTA) and **111**.

## The four quadrants

### A) In MAIN only — OUT-OF-SCOPE event families: 24 families / 113 editions / ~3,411 rows — NEVER AUDITED
Adelaide (WTA 21-26) · Atlanta (ATP 21-24) · Auckland (ATP 23-26) · Auckland (WTA 23-26) · Barcelona (ATP 21-26) · Berlin (WTA 21-26) · Birmingham (WTA 21-24) · Bogota (WTA 21-26) · Brisbane (WTA 24-26) · Eastbourne (WTA 21-24) · Estoril (ATP 21-24,26) · Hobart (WTA 23-26) · Lyon (WTA 21-23) · Marseille (ATP 21-25) · Montpellier (ATP 21-26) · Munich (ATP 21-24) · Newport (ATP 21-24) · Nottingham (WTA 21-26) · Palermo (WTA 21-24) · Rabat (WTA 22-26) · San Jose (WTA 21-22) · Stuttgart (ATP 21-26) · Stuttgart (WTA 21-26) · Washington (ATP 21-26).
**Status: entirely unverified** — never passed through any gap program; they live in the artifact that still carries 60 Wolf field-hits + 60 initials-style names (byte-measured this session). Gap profile UNKNOWN (these are the "unknown gaps").

### B) In MAIN only — IN-SCOPE events, completed 2026 editions: 4 editions / 122 rows
Rotterdam 2026 (31) · Dubai ATP 2026 (30) · Halle 2026 (31) · Queen's Club 2026 (31). Events finished; main's rows unverified; branch has the 2021–2025 runs of all four verified.

### C) In BRANCH only: 14 editions / 854 rows
The WTA-only-1000 coverage build (Doha 3, Dubai_WTA 4, Beijing 3, Wuhan 2, Guadalajara 2) — main has NOTHING for these. 100% TE-byte-built, 39/39 ret-wo header re-read, retro-audited (RETRO-AUDIT-T036-T038).

### D) SHARED editions with row-count deltas: 111 editions — branch longer in ALL 111, shorter in ZERO
main 6,761 rows vs branch 7,047 across these editions (+286 = exactly the 286 closed gaps: rets, walkovers, and missing completed rows restored across the Masters/gap programs). **Branch is a strict superset of main on all shared ground.**

## Proposed work orders (pull → census → audit → then fix; nothing pre-authorized)
- **WO-1 (T-039) — In-scope 2026 tail:** build/verify Rotterdam/Dubai-ATP/Halle/Queen's 2026 from TE bytes (main's 122 rows used only as cross-reference, never as source); ~4 editions, 1 cycle. Extends naturally to the post-event queue (Cincinnati 2026 ends this week, then US Open etc.).
- **WO-2 (T-040) — Out-of-scope family adjudication:** Director decision first — adopt the 24 families into scope (then: census like CENSUS-T036, per-family draw survey, gap audit of main's ~3,411 rows against TE bytes, fix/build) or formally declare them out-of-scope and record main's slice as superseded-unverified. If adopted: largest program yet (~113 editions), recommend phased by tour/tier.
- **WO-3 — Main-store defect ledger handover:** the 60/60 Wolf-initials hits in main's artifact map onto rows the branch already fixed (shared ground) or never adopted (Category A); auditing team can use branch `player_canonical_names`/editions as the reference truth.

*Filed read-only: no data bytes changed. Next assignment acknowledged: volleyball championships data gathering (European Championship Women et al., ongoing) — awaiting the work order.*

*Role: AUDITOR 1 · Branch ID: arena/01a015bb-the-creation-2*
