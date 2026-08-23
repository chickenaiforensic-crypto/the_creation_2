# REPLY-VB-3 — WO-VB-3 (Olympics 2021+2024, M+W) — CLOSED — 2026-08-23 — Auditor 1

**Scope delivered:** 4/4 editions, 128 rows, all `closed_verified_gapless`. Store after closure: **12 editions / 712 rows / ISSUES:0**.

| # | Edition | Rows | Commit | Gold (byte-verified) |
|---|---|---|---|---|
| 1 | Olympics_M 2021 (Tokyo-2020) | 38 | 2a152fa | France d. ROC 3-2 — first FRA gold/medal ever |
| 2 | Olympics_W 2021 (Tokyo-2020) | 38 | 8cea5d2 | USA d. Brazil 3-0 — first after 3 silvers |
| 3 | Olympics_M 2024 (Paris) | 26 | 1fbaeac | France d. Poland 3-0 — back-to-back, host gold |
| 4 | Olympics_W 2024 (Paris) | 26 | closure commit | Italy d. USA 3-0 — first in history |

## Verification summary (3-phase every cycle)
- **Census-first held all four builds**: Tokyo 38 (2×15 RR + 8 KO), Paris 26 (3×6 RR + 8 KO) — the Paris format
  reform (first 3-pools-of-4 since the 2-pools era began 1972) byte-documented from the paris2024.org ref both pages.
- **FIDELITY**: 48/48 team-pool entries sealed (recomputed points == spw/spl); program cumulative 280 team-entries.
- **Spine locks** exact ×4; Paris adds the combined-ranking QF-pairing assert (1v8/2v7/3v6/4v5) — both genders exact.
- **Per-row sources all distinct**: Tokyo FIVB vis2009 PDFs (38+38 unique ids), Paris olympics.com P2 PDFs (26+26).
- **Zero forfeits / zero golden sets** across the family (verified absent).

## Adjudications & disclosures filed
1. **ROC canon** (DATA-RULES naming policy, commit 2a152fa): stored as-printed "ROC", distinct from "Russia".
2. **edition_year 2021 for Tokyo-2020** — year actually played; postponement byte-cited.
3. As-printed quirks: M-2021 `http://` vs W-2021 `https://` fivb.org links; Paris-M POL–EGY Report-href typo
   (routed to P2 PDF); Paris-W TUR–DOM `C83` vs `C73` prefix.
4. **Vandalism strike**: Paris-M statistics-leaders tables fake-named — rejected class for narrative; rows unaffected.
5. **Tandara suspension** (Tokyo-W): roster event, no forfeit, disclosed in provenance.
6. One sandbox reset absorbed mid-WO (before cycle 3): recovered to 8cea5d2, harness rebuilt from spec, baseline
   re-proven before work. All four pushes rev-parse-verified.

## New artifacts this closure
- `data/volleyball/editions/Olympics_README.md` (family README)
- `hand_offs/auditor/CALENDAR-MATRIX-VB-2026-08-23-AUD1.md` — **Director-requested existence grid**: proves every
  absent year in 2021–2025 is an absent EVENT (Olympics quadrennial, WCh 2022+2025 only, EuroVolley 2021+2023 with
  NO 2025 edition) — only VNL is annual. Updated same-commit with any existence/built change.
- New canon first-writes this WO: Venezuela, ROC (team ledger 55 entries).

## Next
**WO-VB-4 (continental championships AVC/NORCECA/CSV/CAVB 2021–2025)** — first deliverable: per-event byte-census
of what actually happened per confederation (COVID moves/cancellations expected), matrix updated in same commit.
Then WO-VB-5 VNL (the big block), WO-VB-6 qualifiers, WO-VB-7 club, WO-VB-8 rolling 2026.

*Auditor 1 · arena/01a015bb-the-creation-2*
