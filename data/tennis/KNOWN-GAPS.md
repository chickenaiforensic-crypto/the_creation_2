# KNOWN GAPS — `master_store_tennis_SSoT.json`

- **Artifact:** `master_store_tennis_SSoT.json`
- **MD5:** `fa273ca4d54563866e370a7178edc4fc`
- **SHA-256:** `dfdd6dfdb7152052b19be4cd31df6c8ac0f133b9d48632608754d4766e6057fc`
- **Rows:** 17,286
- **Naming layer:** v5 canonical + Phase B remediation 2026-08-16 + GS134 completeness 2026-08-17
- **Measured from:** the artifact bytes, 2026-08-18 (T-003 remediation)

The pin proves file identity. Residual defects below remain visible to downstream users.

---

## 1. Intra-edition Grand Slam draws in this store are complete

All **46** Grand Slam event-editions present in the store (AO / RG / Wimbledon 2021–2026 ATP+WTA; US Open 2021–2025 ATP+WTA) contain 127 matches. Intra-edition shortfall is **0 matches absent**.

| Tournament | Matches absent (intra-edition) |
|---|---:|
| Australian Open | 0 |
| Roland Garros | 0 |
| Wimbledon | 0 |
| US Open (editions present) | 0 |
| **Total** | **0** |

**US Open 2026 ATP and WTA** are still **absent entire editions** (not part of the closed 134).

## 2. Semi-final census — historical SF: 5; current unresolved SF: 0

The independent v3 audit correction was **SF: 5**. The GS134 merge restores the four remaining non-AO single-SF editions (RG 2022/2025/2026 ATP, Wimbledon 2022 ATP). Current unresolved SF shortfall: **0**.

## 3. Thirty-two recovered AO rows have forensic-null dates

Exactly **32 rows** have `date == ""`. All 32 are recovered Australian Open records, all carry `provenance.forensic_null == true`, and none were imputed. Breakdown:

- Year: 2021 = 7, 2022 = 6, 2024 = 4, 2025 = 9, 2026 = 6
- Tour: ATP = 27, WTA = 5
- Status: retired = 19, completed = 9, walkover = 4

**T-003 update (2026-08-18):** the nine `completed`-status rows in this set were externally evidenced as retirements and relabeled `retired` (per-row source URLs in `provenance.retirement_evidence`, see §4). Current status mix: **retired 28 / completed 0 / walkover 4**. Year and tour breakdowns unchanged.

**External-date resolution path (audit flight 2026-08-18, Auditor 1):** real-world dates for §3 rows exist in an accessible external source. Verified example: Tennis-Data.co.uk `2021/ausopen.csv` dates the forensic-null row Tomic–Sugita (AO 2021 R128, `3-6 6-1 4-1`, retired) at **08/02/2021**; the same source family is already cited per-row in the store (`tennis-data.co.uk results index`). **No dates were filled** — policy stands: never invent, never fill without a Director-authorized, per-row evidenced transaction in a future cycle. This paragraph documents the safe path only.

Consumers that require a date must quarantine or explicitly allow these rows. Do not invent dates.

## 4. Incomplete terminal sets and source-status inconsistency

Within the AO scope, 30 numeric score pairs are incomplete terminal sets. Twenty-one occur on records marked `retired`; nine occur on recovered records whose status metadata says `completed`. Phase Zero scores only physically completed sets and lists all 30 source rows in `phase_zero/AO_Phase_Zero_Run_Report.json`.

**T-003 update (2026-08-18):** all nine completed-status rows were externally evidence-checked and relabeled `retired` (per-row source URLs recorded in `provenance.retirement_evidence`). The store now contains **0** completed-status incomplete terminal sets; the 30 rows remain listed in the Phase Zero report for history.

## 5. `winner` is `"A"` on every row

All 17,286 records are winner-first normalized. `playerA` is therefore a storage convention, not a predictive feature. Randomize or symmetrize player orientation before any predictive training.

## 6. Score-marker history and the Otte–Rinderknech set score (resolved/clarified 2026-08-18)

- **Wimbledon 2021 R128, Otte vs Rinderknech, `13-12(2)`, marked completed: format-consistent, not a defect.** Wimbledon 2019–2021 played a 7-point tiebreak at **12-12** in the final set, so a `13-12(2)` fifth set is the correct rendering for the 2021 edition; the uniform 10-point tiebreak at 6-6 arrived only in 2022. The earlier §6 claim that this score "does not match the tournament's final-set format" was itself inaccurate and is withdrawn (PA-03).
- **Marker policy (T-003 D3, Director's decision):** score strings carry pure set scores only. Retirement and default are conveyed exclusively by `status` + flags (`retired`, `defaulted`), never by tokens inside `score`. The 31 trailing `RET` tokens and 2 default tokens (`Def.`/`DEF`) that previously existed were stripped with set digits byte-preserved; a store-wide census now finds **0** marker tokens. This resolves both residual §6 items (the Washington 2024 missing-marker question — no marker is now expected anywhere — and the marker-casing inconsistency).

## 7. Field-level nulls remain

| Field | Empty rows |
|---|---:|
| `duration_min` | 2,521 |
| `rankA` | 427 |
| `rankB` | 453 |

No odds fields are present. (T-003 note: the added Dubai 2026 walkover row contributes one null to each census; the D3 marker strip changed none.)

## 8. Naming scope

The v5 store applies the adjudicated canonical-name corrections and identity merges. The accompanying `player_canonical_names.json` contains **1,069 entries** (874 adjudicated + 195 Phase B additions). The 190-name verification queue closed **190/190 verified, 0 needs_verification, 0 disputed** (certified by the auditor, 2026-08-17); Gate 4 applied the resulting store respells and the `Juncheng Shang → Shang Juncheng` identity merge (45 rows rewritten, 47 rows unified, ATP `S0RE` Class A evidence). This does not turn unverified non-AO spellings into official-name assertions; future name evidence must extend the table without silently forking identities.

### 8.1 Evidence provenance caveats (2026-08-17, repair)

- **Shang evidence record repaired** (§2.3): ATP `S0RE` is the primary live source (Class A, ID-addressed); the ITF `800559106` endpoint is retained as historical evidence only — it returns HTTP 404 and is stale. The record's `name_as_displayed`/`match_result` now agree with the captured evidence: the ITF page displayed the Western order `Juncheng Shang` (`display_order_variant`, not `exact`), while the canonical keeps the Director's legal-name order `Shang Juncheng`, composed exactly from the ATP structured fields `LastName="Shang"`/`FirstName="Juncheng"`.
- **Evidence timestamps are local wall-clocks:** the fetching agent did not record a timezone and 74 values were mislabeled with a `Z` (UTC) suffix. Commit-bounded analysis proves they cannot be UTC (all were committed no later than 2026-08-17T09:08:09Z). The false `Z` suffixes were removed on 2026-08-17 with the wall-clock digits preserved; no offset is asserted without a record. Batch and transaction evidence carrying these values was relocated to `quarantine/evidence/`.

## 9. Non-GS completeness (M-1/M-2) — measured 2026-08-18

- **Walkover rows:** the 11,443 non-GS rows recorded **0 walkovers** before T-003; unplayed matches are silently absent outside GS. The single exception now on file is the **Dubai 2026 ATP final** (Medvedev d. Griekspoor W/O), added per T-003 D2 because a title match must be derivable from the bytes. All other non-GS walkovers remain unrecorded.
- **Spine coverage** (R32→F where applicable; R16/QF/SF/F=8/4/2/1): M1000 **28/82** editions complete, ATP/WTA500 **45/82**, ATP/WTA250 **51/96**; **208 spine matches absent** across non-GS (103 + 54 + 51). No rows were invented. *(Post-T-003 recompute 2026-08-18: the Adelaide split adds one 500-level edition and four gaps — Int'l 2 lacks 2 R16 and 2 SF rows — while the added Dubai 2026 final closes one F gap: 81→82 editions, 51→54 absent, 205→208 total.)*
- **Late-entrant metric definition:** counting all present-round transitions except each edition's first (bye entry point), M1000 late entrants = **161**; including first transitions adds 1,766 bye events (= 1,927 total); spine-only counting gives 99. Record all three with this note to avoid re-derivation disputes.
- **Worst editions:** WTA Miami 2022 (R32=12/R16=7), ATP Cincinnati 2023 (R32=13/R16=6).
- **Season-start dates:** 48 rows carry a date in the calendar year before their `edition_year` (WTA Brisbane 2024: 8, Brisbane 2025: 22, WTA Auckland 2024: 1, Auckland 2025: 17). Correct reality for December starts — do not "fix".
- **Adelaide:** the 2023 WTA rows are now correctly split into `Adelaide International 1` (29 rows, full R32→F) and `Adelaide International 2` (24 rows). Int'l 2 residual gaps, documented not invented: 2 R16 rows absent (R32 winners Alexandrova, Kvitova, Q. Zheng, V. Kudermetova have no R16 rows) and **0 SF rows** (QF winners Badosa and V. Kudermetova do not reappear before the F). **Adelaide International 2 2022 is absent entirely** (only Int'l 1 2022 is on file).

## 10. Bare tiebreak notation (digits never invented)

**419 rows** store-wide contain a `7-6`/`6-7` set with no tiebreak digits. **415 are QF rows** — consistent with the "restored QF round" provenance (17 of them Australian Open QFs) — plus 4 non-QF rows: Bogota 2026 WTA R32 (Riera–Janicijevic), Roland Garros 2026 WTA R128 (Frech–Ruse, retired), US Open 2022 ATP R128 (Moutet–Wawrinka, retired), US Open 2022 WTA R128 (Davis–Bronzetti, retired). Tiebreak point digits are unknown for these rows and must never be imputed.

## 11. External reference source status (audit flight 2026-08-18)

Recorded per the Senior Forensic Advisor directive so future verification cycles do not silently assume source availability:

| Source | Status 2026-08-18 | Notes |
|---|---|---|
| Tennis Explorer | ✅ accessible | Corroborated the Adelaide 2023 split slice (final/SFs/QFs/R16 all match store bytes). |
| Tennis-Data.co.uk | ✅ accessible | Per-competition CSVs; AO 2021 sample 5/5 exact vs store; carries dates for §3 rows (see §3 resolution path) and betting odds (store carries none, per PIN). |
| Jeff Sackmann GitHub (`JeffSackmann/tennis_atp`) | ⛔ offline (404) | Repo and raw CSVs gone; community forks exist but are **not admissible** as reference without a Director ruling — a fork's integrity cannot be verified against the vanished original. **Official source limitation for this audit flight.** |
| TennisViz | ⛔ not usable | Licensed B2B product, no public per-match dataset; additionally this store carries no shot-level fields, so shot-data checks are inapplicable to this schema. |
