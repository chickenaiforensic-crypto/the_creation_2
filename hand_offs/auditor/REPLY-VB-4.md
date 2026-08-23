# REPLY-VB-4 — WO-VB-4 (Continental championships 2021–2025) — CLOSED — 2026-08-23 — Auditor 1

**Scope delivered:** 15/15 existing editions, 412 rows, all `closed_verified_gapless`. Store after closure:
**27 editions / 1,124 rows / ISSUES:0** (7 forfeit rows, 0 golden sets).

## Commits
census `03c280e` · AVC `e5382dd`,`c7abd88`,`c38cc93` · batch-of-6 `6a9f0ff` · batch-of-5 `605f2e1` · closer+closure (this).

## What the auditing team should know
1. **The existence census IS the deliverable's spine**: 2025 = zero continental championships in ANY confederation
   (calendar reform — dated negative proofs in CENSUS-VB-4); AVC-W-2021 cancelled (COVID). CALENDAR-MATRIX carries the
   full grid, every cell now BUILT / CANCELLED / NO-EDITION.
2. **The FIDELITY lock earned its keep — 5 printed-standings defects caught and corrected WITH arithmetic proof**
   (details per-edition in Continental_README and in each edition's source note; printed values preserved alongside).
3. **First forfeit rows in the store (7)** — Tanzania's mid-tournament removal and Morocco's 7P walkover; DATA-RULES
   forfeit hygiene validated end-to-end by the harness.
4. **Two disclosed schema migrations** (13P/15P, 6P) — enum extensions only, zero legacy regressions.
5. **Source-granularity honesty**: two 2021 CAVB editions carry the Wikipedia edition page as per-row source because the
   confederation published no per-match links; disclosed on every affected row. All other editions carry unique official
   per-match links (AVC/FIVB/norceca/voleysur/Live Center).
6. **Batching (Director-approved)** used for the 11 small editions — one commit per batch, per-edition asserts intact,
   manifest dupe-guard verified after mid-batch abort/rerun.
7. **Qualification lattice closed**: all WCh-2022/2025 continental berths trace to in-store editions, both directions.

## Next
**WO-VB-5 — VNL 2021–2026, M+W, 12 season-editions, ~1,500+ matches** — the program's largest block. Standing plan:
weekly-batch commits per season, census-first per season (formats changed 2021 bubble → 2022+ weeks format),
FIDELITY via prelim standings, Finals spine asserts. Then WO-VB-6 qualifiers, WO-VB-7 club, WO-VB-8 rolling 2026.

*Auditor 1 · arena/01a015bb-the-creation-2*
