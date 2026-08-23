# Continental championships — family README — WO-VB-4 CLOSED 2026-08-23 — Auditor 1

**15/15 existing editions built / 412 rows, all `closed_verified_gapless`. AVC-W-2021 = CANCELLED (COVID; censused).
2025 = ZERO editions confederation-wide (FIVB 2025–28 calendar reform; byte-censused in CENSUS-VB-4).**

| Edition | Rows | Champion | Notes |
|---|---|---|---|
| Asian_Championship_M/2021 (Chiba+Funabashi) | 56 | Iran (4th) d. Japan | 16 teams; carry-over pools E–H; SRI COVID withdrawal → UZB |
| Asian_Championship_M/2023 (Urmia) | 41 | Japan (10th) d. Iran | Mongolia withdrew (2-team Pool D); Qatar 1st-ever medal |
| Asian_Championship_W/2023 (Nakhon Ratchasima) | 43 | Thailand (3rd, home, undefeated) d. China 16-14-in-5th | FIDELITY caught spw typo (238→248 proven) |
| NORCECA_Championship_M/2021 (Durango) | 22 | **Puerto Rico — 1st ever** d. Canada | FIDELITY caught CAN standings typo (proven) |
| NORCECA_Championship_M/2023 (Charleston) | 17 | USA (10th, home) d. Canada | 6P schema migration |
| NORCECA_Championship_W/2021 (Guadalajara) | 16 | Dominican Republic (3rd) d. PUR 3-2 | |
| NORCECA_Championship_W/2023 (Quebec City) | 17 | Dominican Republic (4th, b2b) d. USA 3-2 | after 0-3 pool loss to USA |
| South_American_Championship_M/2021 (Brasília) | 10 | Brazil (33rd) | closed doors; Venezuela COVID withdrawal; 1-pt row-vs-table conflict resolved |
| South_American_Championship_M/2023 (Recife) | 10 | **Argentina — 1st in 59 years** d. Brazil 3-0 | final's set-2 row-vs-standings conflict resolved (29-27 row governs) |
| South_American_Championship_W/2021 (Barrancabermeja) | 10 | Brazil (22nd) — lost decider to best-ever-silver Colombia | |
| South_American_Championship_W/2023 (Recife) | 10 | Brazil (23rd, 15th straight) | |
| African_Nations_Championship_M/2021 (Kigali) | 48 | Tunisia (11th) d. Cameroon | **first forfeit rows** (Tanzania removed ×6); bracket-graphic code confusion adjudicated |
| African_Nations_Championship_M/2023 (Cairo) | 49 | Egypt (9th, home) d. Algeria | Libya bronze; ALG-LBA 33-35 set; Morocco 7P forfeit |
| African_Nations_Championship_W/2021 (Kigali) | 17 | Cameroon (3-peat) d. Kenya | Rwanda forfeited by FIVB; Senegal withdrew; 4 matches cancelled; 35-33 set |
| African_Nations_Championship_W/2023 (Yaoundé) | 46 | Kenya (10th) d. Egypt | ended hosts' reign |

## Verification & forensic ledger
- **Census-first** held ×15 (official counts byte-derived; infobox `matches=` where printed, structural census otherwise).
- **FIDELITY**: recomputed pool points == printed spw/spl everywhere, including carry-over pools (AVC) and forfeit
  arithmetic (CAVB). **5 catches corrected-with-proof**: AVC-W-2023 THA spw; NORCECA-M-2021 CAN row (pool arithmetically
  broken); CSV-M-2021 1-point row-vs-table; CSV-M-2023 final set-2 (29-27 row governs); all documented in-data both ways.
- **7 forfeit rows** (first in store): Tanzania ×6 (removed, financial), Morocco ×1 (7P walkover) — hygiene law
  (status/scoreline/narrative) validated end-to-end.
- **Schema migrations**: rounds `13P`/`15P` (16-team classification) and `6P` (NORCECA's 6th-place match) — disclosed in DATA-RULES.
- **Source classes**: AVC P2 PDFs (asianvolleyball.net) · FIVB vis2009 · AVC daily bulletins (day-level, disclosed) ·
  norceca.net P2 PDFs (URL-drift as-printed) · voleysur.org IDjogo · FIVB Live Center · Wikipedia-page-as-source for the
  two Kigali-2021 editions (CAVB printed no per-match links — disclosed on every affected row). Wiki defects routed
  around: duplicated vis id, www-less URL, bracket-graphic team codes.
- **Qualification lattice complete**: every WCh-2022 and WCh-2025 continental berth awarded in these 15 editions lands on
  an edition already in the store (incl. Vietnam's pass-down and Libya's debut).
- New canon this WO: 31 nations → **team ledger 91**. Store-record curios: 35-33 & 33-35 sets (68 pts), TTO 4-25, BDI 2-25, USA 25-3.

*Auditor 1 · arena/01a015bb-the-creation-2 · commits e5382dd → this*
