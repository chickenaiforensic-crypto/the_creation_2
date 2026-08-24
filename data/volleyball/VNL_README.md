# VNL_README.md — FIVB Volleyball Nations League family (store law summary)

**Status: FAMILY CLOSED — 12/12 season-editions, 1,336 rows, gapless vs official calendar (WO-VB-5, 2026-08-23/24).**

| Year | W champion | M champion | Format | Rows/gender |
|---|---|---|---|---|
| 2021 | USA (3rd straight) | Brazil (1st) | Rimini bubble, true single RR (120 pairs) + F4 | 124 |
| 2022 | Italy (1st) | France (1st) | First travel-weeks: 6 pools of 8 ×16, Final 8 | 104 |
| 2023 | Turkiye (1st) | Poland (1st, home) | Travel-weeks | 104 |
| 2024 | Italy (2nd) | France (2nd) | Travel-weeks; no relegation (expansion) | 104 |
| 2025 | Italy (3rd, 12-0) | Poland (2nd) | First 18-team: 9 pools of 6, algorithm slates | 116 |
| 2026 | Turkiye (2nd) | Poland (3rd, 2nd straight) | 18-team | 116 |

## Structural law captured from bytes
- **Id sequences:** every season is one volleyballworld schedule-id block, contiguous per edition, asserted per build (2021 W 11830-11953 / M 11700-11823; 2022 M 13650-13753 → W 13754-13857; 2023 W 16024-16127 → M 16128-16231; 2024 M 18853-18956 → W 18957-19060; 2025 M 21437-21552 → W 21553-21668; 2026 M 26434-26549 → W 26550-26665).
- **Host-seeding edge-cases (4):** W-2024 THA 13th bumped NED (8th); M-2025 CHN 17th bumped IRI; W-2026 CHN 9th bumped POL then WON their QF (3-2 v USA); M-2026 CHN 18th bumped BUL **and** the EX relegation fell on 17th CAN (host shield redirect).
- **Promotion/relegation lattice, closed both directions every cycle:** Challenger Cup winners in (CRO-W'23, CUB-M'23, FRA-W'24, TUR-M'24, CZE-W'25, CHN-M'25) + ranking entrants at expansion (BEL-W'25, UKR-M'25) and post-relegation (UKR-W'26, BEL-M'26); relegated: BEL-W'22, AUS-M'22, CRO-W'23, CHN-M'23, none 2024, KOR-W'25, NED-M'25, BUL-W'26, CAN-M'26.
- **Forfeits:** exactly two in the family — both Quezon City M-2022 COVID rows (CHN→FRA medical; GER→CHN refusal), federation-recorded 25-0 ×3, wire-cited.
- **Distinct-federation adjudication:** pools hosted by Hong Kong-China (W'23, W'24, W'25, W'26) and Macau-China (W'24) are all-N even when CHN plays there; the Macau **finals** of W-2026 print host=China with CHN holding the QH berth → CHN home flags, disclosed.
- **Record ledger (store-wide, VNL-heavy):** biggest set POL d. ARG **50-48** (98 pts, M-2026); then GER-TUR 44-42 (86, M-2024), ARG-USA 43-41 (84, M-2023), the 78-pt 40-38 band (BUL-GER WCh-25, SRB-KOR W-22, GER-FRA M-26). Longest fifth: **27-25 tie band** (SLO-NED M-2024; CZE-USA W-2025). Lowest fifth: CAN d. BUL 15-4 (W-2025). SLO's M-2026 QF vs TUR: 35-33 + 39-37 back-to-back.
- **FIDELITY catches in-family:** #6 W-2021 stale spw/spl table (rows govern); #7 (this WO, self) W-2026 draft WL cells cross-contaminated from M-2026 — caught by the lock pre-commit; **#8 M-2026 ARG-GER set 3: wiki row 25-21 vs official P2 PDF 25-15 — P2 governs** (vis 256881349; the printed standings were right, the wiki row token was the typo; inverse direction of catch #2).
- Source classes: explicit hrefs (2021-24) → `{{VNL game|id|2025}}` template → year-less `{{VNL game|id}}` + `Vb res 12` with attendance (2026, attendance not a schema field). All rows also cite FIVB vis2009 P2 PDFs (except the two forfeits, where none exist).

Per-row source = volleyballworld schedule page; builders re-derive per-edition combined standings (spw/spl AND full W/L-category profile) against the printed tables — **double lock exact for every one of the 12 editions**.

*Auditor 1 · arena/01a015bb-the-creation-2*
