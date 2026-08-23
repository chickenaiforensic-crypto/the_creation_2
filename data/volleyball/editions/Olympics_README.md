# Olympics (volleyball) — family README — WO-VB-3 CLOSED 2026-08-23 — Auditor 1

**4 editions / 128 rows, all `closed_verified_gapless`. Zero forfeits, zero golden sets (verified absent).**

| Edition | File | Matches | Format | Gold | Silver | Bronze |
|---|---|---|---|---|---|---|
| Tokyo-2020 M (played 2021) | `Olympics_M/2021.json` | 38 | 2 pools of 6 → QF/SF/3P/F | **France** (1st — first medal ever) | ROC | Argentina |
| Tokyo-2020 W (played 2021) | `Olympics_W/2021.json` | 38 | 2 pools of 6 → QF/SF/3P/F | **USA** (1st after 3 silvers) | Brazil | Serbia |
| Paris-2024 M | `Olympics_M/2024.json` | 26 | 3 pools of 4 → QF/SF/3P/F | **France** (back-to-back; MVP N'Gapeth repeats) | Poland | USA |
| Paris-2024 W | `Olympics_W/2024.json` | 26 | 3 pools of 4 → QF/SF/3P/F | **Italy** (1st in history) | USA | Brazil |

## Capture & verification
- Wikipedia edition-page wikitext via `action=raw` (fetch_page, 6–7 chunks/page); per-row official sources:
  - Tokyo: **FIVB vis2009 Results PDFs** (`getdocument.asmx?no=NNNN`, 38 unique ids per edition; M page prints `http://`, W page `https://` — stored as-printed) + archived olympics.com statistics PDFs.
  - Paris: **olympics.com P2 PDFs** (`OG2024_VVO_C73_...GPA-000100--.pdf` style, 26 unique per edition) + olympics.com result pages. As-printed quirks disclosed: M-page POL–EGY *Report* href duplicate-link typo (routed around via P2 PDF); W-page TUR–DOM P2 prints `C83` where all others print `C73`.
- **FIDELITY lock**: per-team pool points recomputed from set tokens == standings `spw/spl` for **all 48 team-pool entries** across 10 pools (Tokyo 2×6 ×2, Paris 3×4 ×2). Paris standings use the newer `win3s/win4s/win5s` table style — absorbed.
- **Spine locks**: SF participants == QF winners; F == SF winners; 3P == SF losers; champions == infobox gold. Paris adds the **teams-combined-ranking assert**: QF pairings 1v8/2v7/3v6/4v5 checked against the combined table exactly (M: ITA-JPN/USA-BRA/SLO-POL/FRA-GER, Serbia out as worst third; W: BRA-DOM/ITA-SRB/CHN-TUR/USA-POL, Japan out as worst third).

## Edition-specific adjudications & notes
- **edition_year for Tokyo = "2021"** (year actually played; COVID postponement byte-cited; DATA-RULES date-startswith rule holds).
- **ROC** stored as-printed (`{{vb|RUS|roc-olympics|name=ROC}}`) — distinct canon string from "Russia"; adjudication in DATA-RULES-VB naming policy.
- Tokyo: single venue Ariake Arena, behind closed doors (attendance fields empty in the bytes). Paris: single venue South Paris Arena 1.
- **Home flags** (Director rule: host-in-hosting-venue = home): Japan on all 2021 JPN rows (M: QF run; W: 5th-in-pool exit); France on all 2024 FRA rows (M: gold at home; W: 0 wins, combined 11th).
- **Format reform** Paris-2024: first 3-pools-of-4 Olympic tournament since 1968-style fields; paris2024.org "NEW VOLLEYBALL FORMAT" ref byte-cited in both pages.
- **Vandalism strike** (source-hygiene log): Paris M-page statistics-leaders tables carry fake names (CHN flagicon in a field with no China) — rejected as source class; match rows unaffected; awards table retained on volleyballworld MVP citation.
- **Tandara doping suspension** (Tokyo W, pre-SF, Enobosarm, Reuters ref) — roster event only; no forfeit.

## Notable rows preserved
France d. Brazil 39-37 set 2 (Tokyo M pools, 76 pts — store #2=); Brazil d. Poland 38-36 set 2 (Paris W pools, 74 pts); JPN-IRI 29-31 third set + 15-13 fifth (Tokyo M); Kim Yeon-koung farewell: KOR QF 3-2 TUR (28-26, 15-13-in-5th) + 3-2 JPN 16-14-in-5th (Tokyo W); France QF escape vs Germany 15-13-in-5th from 0-2 (Paris M); Japan's 17-15 extended-fifth QF loss to Italy (Paris M); USA bronze 3-0 with all sets at deuce 25-23/30-28/26-24 (Paris M); Italy's zero-sets-dropped knockout run to gold (Paris W); ROC 3-0 over eventual champions USA in pools (Tokyo W).

*Auditor 1 · arena/01a015bb-the-creation-2 · commits 2a152fa, 8cea5d2, 1fbaeac, +closure*
