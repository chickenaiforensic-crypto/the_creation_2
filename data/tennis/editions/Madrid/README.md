# Madrid (WTA 1000, clay, Spain) — 2021–2026

Six editions pulled from the claude_1 pinned store (md5 `a280b2fb56e64f64724473e767d90485`) and gap-fixed under T-032b (2026-08-19, Auditor 1, PLAN-T032 Phases C+D, executed under the pre-audit → work → post-audit cycle). All 8 gaps (MA001–MA008) closed: 6 retirements + 2 walkovers. With T-032a (ATP, 21), the **Madrid event is COMPLETE: 12 slices, 29 restorations**.

## Draw-era mix (byte-asserted per edition)
- **2021–2022: 64-draw** — 63 matches = R64:32, R32:16, R16:8, QF:4, SF:2, F:1; **ZERO byes** (the bye-assert flips to 0 in this era, so any entry-at-R32 without an R64 row is a genuine anomaly — this is exactly how the Kvitova 2021 and Yastremska 2022 missing R64 rows were caught).
- **2023–2026: 96-draw** — 95 matches, 32 seed byes (R64-not-in-R128).
- **Verify-only slices**: 2023 and 2025 arrived count-clean (95/95) and passed full structural + spine verification before being declared gapless — no fixes, no assumptions.

## Headline — Swiatek's missing Madrid 2026 exit
**R32: Ann Li d. Iga Swiatek 7-6(4) 2-6 3-0 ret** (MA007) was absent entirely. Swiatek won set 2 (sets 2-1 truthful, games 12-12) and retired ill — "I had zero energy… felt really bad physically" — during the **Madrid 2026 tournament-wide virus outbreak**, which wire-links three restorations across both tours: this retirement, the Samsonova W/O (MA008), and the Cilic ATP W/O (MAM020, food poisoning).

## Walkover reasons (both wire-corroborated)
| Gap | Year | W/O | Reason | Source |
|-----|------|-----|--------|--------|
| MA002 | 2021 R32 | Pegula d. Azarenka | Lower back (singles + doubles withdrawal) | WTA-official (wtatennis.com/news/2126711) + own statement |
| MA008 | 2026 R32 | Noskova d. Samsonova | Illness (tournament-wide outbreak; out of doubles first) | tennistonic 2026-04-26 + Samsonova's own account (tennistemple 2026-05-10) |

## All 8 fixes
| Gap | Year | Round | Result | Note |
|-----|------|-------|--------|------|
| MA001 | 2021 | R64 | Kvitova d. Bouzkova 6-2 2-3 ret | Bouzkova ahead 3-2 in set 2; sets 1-1 truthful; id 1939206 |
| MA002 | 2021 | R32 | Pegula d. Azarenka W/O | id 1939710 |
| MA003 | 2021 | R16 | Bencic d. Jabeur 7-6(2) 4-3 ret | id 1940115 |
| MA004 | 2022 | R64 | Yastremska d. Minnen 6-3 0-2 ret | Minnen ahead 2-0 in set 2; sets 1-1 truthful; id 2081481 |
| MA005 | 2022 | R32 | Rybakina d. Siniakova 6-0 1-0 ret | id 2082091 |
| MA006 | 2024 | R64 | Putintseva d. Qinwen Zheng 7-5 2-0 ret | Zheng (seed 6, bye) played only this match; id 2599435 |
| MA007 | 2026 | R32 | Ann Li d. Swiatek 7-6(4) 2-6 3-0 ret | Virus-outbreak retirement; id 3185018 |
| MA008 | 2026 | R32 | Noskova d. Samsonova W/O | id 3185286 |

Pre-existing ret rows in the claude_1 slice (NOT raw-pipeline survivors): 2021 QF Sabalenka d. Mertens 6-1 4-0 ret (date-source-CSV path); 2023 R128 Sherif d. Giorgi 4-6 6-4 ret (tennisabstract-extraction path).

Status per edition: `closed_verified_gapless` (era-correct template, byes, exhaustive spine).
