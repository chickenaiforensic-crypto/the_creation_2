# CENSUS-VB-4 — Continental championships existence census (AVC/NORCECA/CSV/CAVB, 2021–2025) — 2026-08-23 — Auditor 1

**WO-VB-4 opening deliverable (Director-ordered census-first).** Every line dated-sourced this session via web survey;
Grokipedia surfaced in results and was used for ZERO claims (rejected class — program strike #5 logged in tennis/VB era).
Each edition still gets its own byte-census (official match count from the edition page wikitext) BEFORE any row is built.

## The headline finding
**NO confederation held a continental championship in 2025.** All four moved to even years under the FIVB 2025–28
calendar reform; the 2026 editions (all ten, LIVE now or September) are the LA28 qualifiers already censused in
CENSUS-VB. 2025 continental-looking events (NORCECA Final Six/Final Four, Pan-Am Cup, AVC Nations Cups) are
SEPARATE second-tier annual competitions — not championships, not in WO-VB-4 scope.

## Existence grid → build queue (15 editions)
| # | Edition | Host (city) | Champion (to verify at build) | Source (dated) |
|---|---------|-------------|-------------------------------|----------------|
| 1 | AVC Asian Ch M 2021 (21st) | Japan (Chiba + Funabashi), 12–19 Sep | Iran | en.wikipedia 2023-Asian-M-Ch quals table (crawl 2026-07-26) |
| 2 | AVC Asian Ch M 2023 (22nd) | Iran (Urmia), 19–26 Aug | Japan (10th) | en.wikipedia edition page (crawl 2026-07-26) |
| — | AVC Asian Ch W 2021 | ~~Philippines (San Fernando/Angeles/Olongapo)~~ | **CANCELLED — COVID-19** | en.wikipedia/wikiwand series page (crawl 2026-06-18) |
| 3 | AVC Asian Ch W 2023 (21st) | Thailand (Nakhon Ratchasima) | Thailand (3rd) | series page + CENSUS-VB |
| 4 | NORCECA Ch M 2021 | Mexico (Durango City) | **Puerto Rico (1st title ever)** d. Canada | norceca survey; VERIFY on edition wikitext |
| 5 | NORCECA Ch M 2023 | USA (Charleston) | USA d. Canada | norceca survey; VERIFY on edition wikitext |
| 6 | NORCECA Ch W 2021 | Mexico (TBV at build) | Dominican Republic (3rd) | 2023 edition page cross-refs (PUR silver, CAN bronze) |
| 7 | NORCECA Ch W 2023 | Canada (Quebec City), 29 Aug – 3 Sep | Dominican Republic (4th) d. USA 3-2 | en.wikipedia edition page (crawl 2025-06-26) |
| 8 | CSV South American Ch M 2021 | Brazil (Brasília) | Brazil | series survey; VERIFY at build |
| 9 | CSV South American Ch M 2023 | Brazil (Recife), 26–30 Aug | **Argentina d. Brazil 3-0 — first title in 59 years** | series survey + CSV wiki title-holders (crawl 2026-07-29) |
| 10 | CSV South American Ch W 2021 | Colombia (Barrancabermeja), 15–19 Sep | Brazil (22nd); 5 teams / 10 RR matches (full table already surfaced) | wikiwand edition page |
| 11 | CSV South American Ch W 2023 | Brazil (Recife), 19–23 Aug | Brazil (23rd, 15th straight); 5 teams / 10 RR | en.wikipedia edition page (crawl 2026-03-20) |
| 12 | CAVB African Nations M 2021 (23rd) | Rwanda (Kigali) — TBV | Tunisia (11th; three-peat 2017/19/21) | series survey; VERIFY at build |
| 13 | CAVB African Nations M 2023 (24th) | Egypt (Cairo), Sep | Egypt (9th) d. Algeria 3-1; **15 teams** — biggest build of the WO | en.wikipedia edition page (crawl 2025-05-26) |
| 14 | CAVB African Nations W 2021 | Rwanda (Kigali) | Cameroon (3rd straight); 9 teams | en.wikipedia edition page (crawl 2026-07-26) |
| 15 | CAVB African Nations W 2023 | Cameroon (Yaoundé) | Kenya (10th); 12 teams, 2 pools of 6 | en.wikipedia edition page (crawl 2026-07-26) |

## Scope adjudications (Director veto welcome)
1. **2025 = NO-EDITION across all four confederations** — CALENDAR-MATRIX updated this commit (was `?-WO4`).
2. **Second-tier events excluded from WO-VB-4**: AVC Challenge/Nations Cups (M 2022–25, W 2022–25), NORCECA Final
   Four/Final Six + Pan-Am Cup, CSV Copa Sudamericana. They are real, annual, and buildable — parked as a
   WO-VB-6-adjacent menu line for a Director call (they are development/ranking events, not championships).
3. **Estimated volume**: ~15 editions ≈ 400–500 rows (CAVB-M-2023 alone ~40+; CSV editions tiny at 10 each).
4. **Build order** (cadence of one edition per commit, README+REPLY at close): AVC M 2021→2023, AVC W 2023,
   NORCECA M 2021→2023, NORCECA W 2021→2023, CSV M+W 2021→2023, CAVB W 2021→2023, CAVB M 2021→2023 (largest last).
5. Sources at build: Wikipedia edition wikitext (action=raw) as completeness template + official per-match links
   where carried (AVC pages carry asianvolleyball.net / FIVB VIS; NORCECA pages carry norceca.net boxscores;
   CAVB/CSV vary — hierarchy per DATA-RULES applies, gaps disclosed per-row if official links are thin).

*Auditor 1 · arena/01a015bb-the-creation-2*
