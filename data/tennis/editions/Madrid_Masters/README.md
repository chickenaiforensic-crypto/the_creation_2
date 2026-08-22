# Madrid Masters (ATP M1000, clay, Spain) — 2021–2026

Six editions pulled from the claude_1 pinned store (md5 `a280b2fb56e64f64724473e767d90485`) and gap-fixed under T-032a (2026-08-19, Auditor 1, per PLAN-T032 Phases A+B). All 21 gaps (MAM001–MAM021) closed: 16 retirements + 5 walkovers — the raw M1000 pipeline had dropped 100% of ret/wo rows in this slice-set (6th consecutive), matching the byte-derived gap map exactly.

## Draw-era mix (byte-asserted per edition)
- **2021–2022: 56-draw** — 55 matches = R64:24, R32:16, R16:8, QF:4, SF:2, F:1; 8 seed byes (R32-not-in-R64).
- **2023–2026: 96-draw** — 95 matches = R128:32, R64:32, R32:16, R16:8, QF:4, SF:2, F:1; 32 seed byes (R64-not-in-R128).

## Headline restoration — Auger-Aliassime's 2024 run to the final
Every rung of FAA's 2024 path beyond R16 was missing from the raw store and is now restored:
- R32: FAA d. Mensik 6-1 1-0 ret (MAM006)
- QF: FAA d. Sinner W/O — right hip, tournament-official + Sinner's own post (AP/AFP) (MAM007)
- SF: FAA d. Lehecka 3-3 ret — **the program's first missing semifinal**; tied-token 3-3 credits nobody (MAM008)

## Walkover reasons (all 5 wire-corroborated)
| Gap | Year | W/O | Reason | Source |
|-----|------|-----|--------|--------|
| MAM004 | 2022 R16 | Djokovic d. Murray | Illness (food poisoning) | Tournament-official; Reuters 2022-05-05; Guardian via ABC |
| MAM007 | 2024 QF | Auger-Aliassime d. Sinner | Right hip | Tournament-official + own post; AP/WaPo, AFP/Sportstar 2024-05-01 |
| MAM013 | 2025 R64 | Rublev d. Monfils | Illness | ATP-official (atptour.com 2025-04-25) + own Snapchat |
| MAM014 | 2025 R64 | Medvedev d. Djere | Left shoulder | ATP-official (atptour.com 2025-04-25) |
| MAM020 | 2026 R64 | Fonseca d. Cilic | Food poisoning | Cilic's own Instagram (puntodebreak/tennistemple 2026-04-24) |

## Structural adjudications (no rows fabricated)
- **Seed-played-only-the-missing-match** (explains a 31-apparent-byes anomaly): 2023 Griekspoor (seed 30, bye; only match = the missing R64 vs Munar, 7-6(3) ret); 2025 Rune (seed 8, bye; only match = the missing R64 vs Cobolli, 6-2 ret).
- **LL-into-bye (3rd of the program, Monte Carlo precedent)**: 2025 — Alcaraz (seed 2, bye) withdrew 2025-04-24 with a right adductor tear (Barcelona final) + left hamstring discomfort (own press conference; olympics.com). LL **Kamil Majchrzak** took the slot and PLAYED R64 (in-store Diallo d. Majchrzak). Alcaraz correctly has NO row. Wire corroboration matches bracket bytes: his scheduled 2R opponent was the Bergs–Diallo winner — exactly Majchrzak's actual R64 opponent.
- **Name-canon artifacts (NOT gaps)**: 2025 R128 diff initially flagged "Bu Yunchaokete"/"Pablo Landaluce" — store canon is "Yunchaokete Bu" and "Martin Landaluce"; both rows present.

## All 21 fixes
| Gap | Year | Round | Result |
|-----|------|-------|--------|
| MAM001 | 2021 | R64 | Sinner d. Pella 6-2 4-4 ret (tied-token) |
| MAM002 | 2021 | R32 | de Minaur d. Harris 6-2 3-0 ret |
| MAM003 | 2022 | R16 | Zverev d. Musetti 6-3 1-0 ret |
| MAM004 | 2022 | R16 | Djokovic d. Murray W/O |
| MAM005 | 2023 | R64 | Munar d. Griekspoor 7-6(3) ret |
| MAM006 | 2024 | R32 | Auger-Aliassime d. Mensik 6-1 1-0 ret |
| MAM007 | 2024 | QF | Auger-Aliassime d. Sinner W/O |
| MAM008 | 2024 | SF | Auger-Aliassime d. Lehecka 3-3 ret |
| MAM009 | 2025 | R128 | Mayot d. Moutet 6-3 4-2 ret |
| MAM010 | 2025 | R128 | Muller d. Goffin 6-3 3-6 1-0 ret |
| MAM011 | 2025 | R128 | Struff d. van de Zandschulp 7-5 2-6 4-1 ret |
| MAM012 | 2025 | R64 | Cobolli d. Rune 6-2 ret |
| MAM013 | 2025 | R64 | Rublev d. Monfils W/O |
| MAM014 | 2025 | R64 | Medvedev d. Djere W/O |
| MAM015 | 2025 | R64 | Tiafoe d. Darderi 7-5 3-1 ret |
| MAM016 | 2025 | R32 | Fritz d. Bonzi 4-6 7-5 0-0 ret (sets 1-1, games 11-11) |
| MAM017 | 2025 | R32 | Draper d. Berrettini 7-6(2) ret |
| MAM018 | 2026 | R128 | Budkov Kjaer d. Opelka 5-3 ret |
| MAM019 | 2026 | R64 | Moller d. Diallo 7-5 3-3 ret (tied-token) |
| MAM020 | 2026 | R64 | Fonseca d. Cilic W/O |
| MAM021 | 2026 | R32 | Kopriva d. Rinderknech 6-4 3-6 ret (loser ahead on games 10-9) |

Status per edition: `closed_verified_gapless` (era-correct template, byes, exhaustive spine).
