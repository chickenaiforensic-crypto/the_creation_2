# CENSUS-VB-5 — VNL 2021–2026 season census (M+W) — 2026-08-23 — Auditor 1

**WO-VB-5 opening deliverable (census-first).** Dated sources: fivb.com schedule announcement 2021 (248 matches/both
genders), en.wikipedia season + statistics pages (crawls 2026-07/08), volleycommunity format explainer (2026-08-02),
worldofvolley/insidethegames 2021 bubble pieces. Grokipedia: not used. Every per-edition count re-verified from the
edition page's own bytes at build (matches-played infobox + structural census) before any row.

## The three format eras (byte-anchored)
1. **2021 — the Rimini bubble**: 16 teams/gender, single round-robin (15 matches/team = 120) + FINAL FOUR (SF×2, 3P, F)
   = **124 matches/gender**; entire event behind closed doors in one city (attendance 0 printed); no promotion/relegation.
2. **2022–2024 — the Final-8 era**: 16 teams, 12 prelim matches/team over 3 travel weeks (96) + 8-team KO finals
   (QF×4, SF×2, 3P, F) = **104/gender**; finals host seeded into QF.
3. **2025–2026 — the 18-team era**: 18 teams, 12/team over 3 weeks in 3 pools-of-6 per week (108) + Final 8 = **116/gender**;
   direct relegation of 18th, promotion via ranking.

## Build queue (12 season-editions / 1,336 rows — the program's largest block)
| # | Edition | Prelim+Finals | Finals host | Podium (VERIFY at build) |
|---|---|---|---|---|
| 1 | VNL_W 2021 | 120+4=124 | Rimini | USA (3rd) d. Brazil; Turkiye bronze |
| 2 | VNL_M 2021 | 120+4=124 | Rimini | Brazil d. Poland; France bronze |
| 3 | VNL_W 2022 | 96+8=104 | Ankara | Italy d. Brazil; Serbia bronze |
| 4 | VNL_M 2022 | 96+8=104 | Bologna | France d. USA; Poland bronze |
| 5 | VNL_W 2023 | 96+8=104 | Arlington | Turkiye (1st) d. China; Poland bronze |
| 6 | VNL_M 2023 | 96+8=104 | Gdansk | Poland d. USA; Japan bronze |
| 7 | VNL_W 2024 | 96+8=104 | Bangkok | Italy d. Japan; Poland bronze |
| 8 | VNL_M 2024 | 96+8=104 | Lodz | France d. Japan; Poland bronze |
| 9 | VNL_W 2025 | 108+8=116 | Lodz | Italy d. Brazil; Poland bronze |
| 10 | VNL_M 2025 | 108+8=116 | Ningbo | Poland d. Italy; Brazil bronze |
| 11 | VNL_W 2026 | 108+8=116 | Macau | Turkiye (2nd) d. Brazil; Italy bronze |
| 12 | VNL_M 2026 | 108+8=116 | Ningbo | Poland (3rd) d. USA; Slovenia bronze |

## Capture & verification plan
- **Order**: chronological, W before M within a year (match the calendar). One edition per commit-cycle,
  content committed in WEEK BATCHES inside the cycle if context requires splitting (Director batching approval stands).
- **Wikipedia layout warning**: VNL season pages often externalise the preliminary round to a subpage
  ("...Nations League preliminary round" or per-week sections); the census at build must locate ALL result blocks and
  reconcile row-count == matches-played infobox before transcription. Venue/city per week varies (2022+): the
  week/pool-to-city map must be byte-read per edition (venue_city law).
- **FIDELITY**: prelim = one combined standings table (2022+) or single RR table (2021) — recompute per-team spw/spl
  == printed for ALL 16/18 teams; finals-era carry rules do NOT apply (fresh KO). Spine asserts: QF field == top-7 +
  host (2022+), F == SF winners, 3P == SF losers, champion == infobox.
- **ROC note**: 2021 VNL Russia competed as "Russia" (not ROC — FIVB event, not IOC); verify from bytes at build.
- **Withdrawal/forfeit watch**: 2021 bubble had COVID-era replacement quirks (e.g. W: some squads); 2022 Russia
  EXPELLED post-invasion (replaced); verify per edition, forfeit hygiene ready.
- Sources: volleyballworld.com schedule ids / vis2009 P2 PDFs carried per-row on season pages (verify per edition;
  granularity disclosed if thinner).
- Estimated context load is the driver: ~112-124 rows/edition ≈ 4-7 wikitext chunks per prelim page + finals.

*Auditor 1 · arena/01a015bb-the-creation-2*
