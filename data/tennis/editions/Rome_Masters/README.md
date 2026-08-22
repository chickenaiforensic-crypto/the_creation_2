# Rome Masters (ATP M1000, clay, Italy) — 2021–2026

Six editions pulled from the claude_1 pinned store (md5 `a280b2fb56e64f64724473e767d90485`) and gap-fixed under T-033a (2026-08-19, Auditor 1, pre-audit → work → post-audit cycle). All 13 gaps (RM001–RM013) closed: 10 retirements + 3 walkovers. **2022 is a VERIFY-ONLY slice** (zero gaps; full structural + spine verification passed before gapless declaration). The claude_1 Rome ATP slice carried ZERO pre-existing ret/wo rows — a clean 100% drop with no CSV-path survivors.

## Draw-era mix (byte-asserted)
- 2021–2022: 56-draw (55 matches, 8 byes). 2023–2026: 96-draw (95 matches, 32 byes).

## Pre-audit catch (before any writes)
The hygiene sweep found **4× "J.J. Wolf"** in the pulled 2023 (×3) and 2024 (×1) slices; renamed to **Jeffrey Wolf** at pull-time with per-row `name_fix` provenance (Rule 1, precedent ddb6019). The defect class T-032a caught post-write is now screened pre-write.

## Walkover reasons (all 3 wire-corroborated)
| Gap | Year | W/O | Reason | Source |
|-----|------|-----|--------|--------|
| RM002 | 2021 R32 | Nishikori d. Carreno Busta | Lower back pain | ATP-official (atptour.com Rome 2021 Tuesday report) |
| RM010 | 2025 R64 | Nakashima d. Thompson | Back (also missed Madrid); own quote | tennistemple 2025-05-09; FoxSports |
| RM012 | 2026 R64 | Medvedev d. Machac | Illness, ATP-confirmed morning-of | IANS 2026-05-09 ×2 |

## Structural adjudications
- **Seed-played-only-the-missing-match ×3**: Musetti 2024 (seed 26 — ZERO rows in the pulled slice; Atmane d. Musetti 7-5 1-0 ret), Humbert 2025 (seed 21; Moutet 6-3 4-0 ret), Fils 2026 (seed 15; Pellegrino 4-0 ret).
- **LL-into-bye (4th of program)**: 2024 Juncheng Shang [LL] occupies a bye slot per TE draw-bracket bytes and PLAYED his R64 (in-store Napolitano d. Shang 6-7(3) 6-1 6-0). Replaced-seed identity not wire-verified — no row impact; recorded as-is per no-guessing rule.
- **Champion rung restored**: Ruud d. Berrettini 7-5 2-0 ret (2025 R32) opened his title run.
- Recurring figures: Berrettini ret/W-O loser in restorations at 3 events (MC 2023, Madrid 2025, Rome 2025); Carballes Baena beneficiary 2024 → retiree 2025; Djere winner of both 2023 restorations.

## All 13 fixes
| Gap | Year | Round | Result |
|-----|------|-------|--------|
| RM001 | 2021 | R64 | Musetti d. Hurkacz 6-4 2-0 ret |
| RM002 | 2021 | R32 | Nishikori d. Carreno Busta W/O |
| RM003 | 2023 | R128 | Djere d. Lestienne 6-1 ret |
| RM004 | 2023 | R128 | Kokkinakis d. Munar 4-2 ret |
| RM005 | 2023 | R32 | Djere d. Garin 6-3 2-1 ret |
| RM006 | 2024 | R128 | Carballes Baena d. O'Connell 6-7(7) 5-0 ret (sets 1-1) |
| RM007 | 2024 | R64 | Atmane d. Musetti 7-5 1-0 ret |
| RM008 | 2025 | R128 | Ofner d. Carballes Baena 6-3 0-0 ret (tied-token) |
| RM009 | 2025 | R64 | Moutet d. Humbert 6-3 4-0 ret |
| RM010 | 2025 | R64 | Nakashima d. Thompson W/O |
| RM011 | 2025 | R32 | Ruud d. Berrettini 7-5 2-0 ret (champion rung) |
| RM012 | 2026 | R64 | Medvedev d. Machac W/O |
| RM013 | 2026 | R64 | Pellegrino d. Fils 4-0 ret |

Status per edition: `closed_verified_gapless`.
