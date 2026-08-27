# PROGRESS-VB — Volleyball program ledger (cold-start resume point)

**Read this first on any fresh session.** Recovery ritual: `git fetch origin arena/01a015bb-the-creation-2 && git reset --hard FETCH_HEAD`, rebuild `/tmp/vb_harness.py` from `data/volleyball/DATA-RULES-VB.md`, re-run baseline, resume the row marked IN-FLIGHT.

Program law: `hand_offs/auditor/PLAN-VB-2026-08-23-AUD1.md` · Landscape census: `CENSUS-VB-2026-08-23-AUD1.md`.

| WO | Scope | Status | Editions built | Commits | REPLY |
|----|-------|--------|----------------|---------|-------|
| WO-VB-0 | Foundations (rules/schema/harness/pipeline) | **DONE** (schema v1.1 w/ Director additions: home A/B/N mandatory, venue_city mandatory; harness self-test 21/21) | infra | this commit | — |
| WO-VB-1 | EuroVolley M+W 2021, 2023 | **DONE** (FIDELITY 96/96; README + REPLY-VB-1) | 4/4 (304 rows) | 28b6e7b, ccad013, dff24ff, this | REPLY-VB-1 |
| WO-VB-2 | World Championship M+W 2022, 2025 | **DONE** (FIDELITY 104 team-entries; README + REPLY-VB-2) | 4/4 (280 rows) | 1be16c0, 3530fcf, 527cfb6, this | REPLY-VB-2 |
| WO-VB-3 | Olympics M+W 2021(Tokyo-2020), 2024 | **DONE** (FIDELITY 48/48; ROC adjudication; Olympics_README + REPLY-VB-3 + CALENDAR-MATRIX) | 4/4 (128 rows) | 2a152fa, 8cea5d2, 1fbaeac, this | REPLY-VB-3 |
| WO-VB-4 | AVC/NORCECA/CSV/CAVB championships 2021–2025 | **DONE** (15/15; 5 FIDELITY catches proven; 7 forfeit rows; Continental_README + REPLY-VB-4) | 15/15 (412 rows) | 03c280e…this | REPLY-VB-4 |
| WO-VB-5 | VNL M+W 2021–2026 | **CLOSED 12/12** (1,336 rows == census grid; REPLY-VB-5 + VNL_README filed; catches #6/#7/#8) | 12/12 (1336 rows) | census c41ea05, 4fd0585, 2086276, 2472b58, fcd3d8f, d9ce397, 4e9d5ec, 65b43ea, closure this | — |
| WO-VB-6 | Qualifiers: OQT-2023, Challenger Cups 2022-24, EuroVolley quals, European League | **IN-FLIGHT — CENSUS-VB-6 FILED; Phase A CLOSED 8/8** (216 + 32 = 248 rows; all four 2023/2024 Challenger Cups built and locked; discontinuation adjudicated byte-proven; ranking-entry wrinkles 2024 UKR-M / BEL-W documented; no new forfeits; ledger steady 95) | 8/8 Phase A (248 rows) | Phase B PLANNED (Golden League 2022-2024 first, Director sizing call needed for Silver/all-year) | census 12ea58e, 86a2ece, 4cb21c8, this (final 32) | — |
| WO-VB-7 | Club: Club World Ch 2021–2025 (+CL depth = Director call) | QUEUED | 0/~10 | — | — |
| WO-VB-8 | 2026 post-event queue (10 continentals + Club WCh as they finish; EuroVolley-W final 2026-09-06) | ROLLING | 0/~11 | — | — |

**Store state:** 47 editions / 2676 rows / ISSUES:0 (10 forfeit rows unchanged; zero golden sets; team ledger 95 nations; VNL family CLOSED 12/12; WO-VB-6 Phase A CLOSED 8/8 — 248 qualifier rows). ALL Tier-1 families CLOSED incl. VNL 12/12 (`VNL_README.md`). Record sets: POL-ARG 48-50 (98 pts, M-2026), GER-TUR 42-44 (86, M-2024), ARG-USA 43-41 (84, M-2023), then the 78-pt 40-38 band. Longest fifth: 27-25 tie band (SLO-NED M-2024, CZE-USA W-2025 — corrects the sole-record claim in the 65b43ea commit). Next: WO-VB-6 qualifiers (census-first per event). Families CLOSED: EuroVolley (4), World_Championship (4), Olympics (4), Asian_Championship (3), NORCECA_Championship (4), South_American_Championship (4), African_Nations_Championship (4). Tier-1+2 window COMPLETE except VNL. Existence grid: `CALENDAR-MATRIX-VB-2026-08-23-AUD1.md` (update same-commit as any existence/built change).
**Tennis program:** closed at `5967c0d` (202 editions / 14,892 rows / ISSUES:0); diff doc `BRANCH-VS-MAIN-TENNIS-DIFF` filed; tennis WO-1/WO-2/WO-3 await separate authorization.

*Update this table in the SAME COMMIT as any WO state change. — Auditor 1 · arena/01a015bb-the-creation-2*
