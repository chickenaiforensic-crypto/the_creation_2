# KNOWN GAPS — `master_store_tennis_SSoT.json`

- **Artifact:** `master_store_tennis_SSoT.json`
- **MD5:** `ad0b261dedc1ba58aea988f763f8f641`
- **SHA-256:** `dc2fd01873e5b7ab25611913ed45fd18ee02dad809b958e75c612614e74696eb`
- **Rows:** 17,285
- **Naming layer:** v5 canonical + Phase B remediation 2026-08-16 + GS134 completeness 2026-08-17
- **Measured from:** the artifact bytes, 2026-08-17

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

Consumers that require a date must quarantine or explicitly allow these rows. Do not invent dates.

## 4. Incomplete terminal sets and source-status inconsistency

Within the AO scope, 30 numeric score pairs are incomplete terminal sets. Twenty-one occur on records marked `retired`; nine occur on recovered records whose status metadata says `completed`. Phase Zero scores only physically completed sets and lists all 30 source rows in `phase_zero/AO_Phase_Zero_Run_Report.json`.

## 5. `winner` is `"A"` on every row

All 17,285 records are winner-first normalized. `playerA` is therefore a storage convention, not a predictive feature. Randomize or symmetrize player orientation before any predictive training.

## 6. Known score/default defects outside AO remain

- Wimbledon 2021 R128, Otte vs Rinderknech, contains `13-12(2)` and is marked completed, although that set score does not match the tournament's final-set format.
- Washington 2024 QF, Shelton vs Shapovalov, has score `7-6 6-6` and `defaulted: true` but no default marker in the score string. Marker casing is inconsistent elsewhere (`Def.` / `DEF`).

## 7. Field-level nulls remain

| Field | Empty rows |
|---|---:|
| `duration_min` | 2,520 |
| `rankA` | 426 |
| `rankB` | 452 |

No odds fields are present.

## 8. Naming scope

The v5 store applies the adjudicated canonical-name corrections and identity merges. The accompanying `player_canonical_names.json` contains **1,069 entries** (874 adjudicated + 195 Phase B additions). The 190-name verification queue closed **190/190 verified, 0 needs_verification, 0 disputed** (certified by the auditor, 2026-08-17); Gate 4 applied the resulting store respells and the `Juncheng Shang → Shang Juncheng` identity merge (45 rows rewritten, 47 rows unified, ATP `S0RE` Class A evidence). This does not turn unverified non-AO spellings into official-name assertions; future name evidence must extend the table without silently forking identities.

### 8.1 Evidence provenance caveats (2026-08-17, repair)

- **Shang evidence record repaired** (§2.3): ATP `S0RE` is the primary live source (Class A, ID-addressed); the ITF `800559106` endpoint is retained as historical evidence only — it returns HTTP 404 and is stale. The record's `name_as_displayed`/`match_result` now agree with the captured evidence: the ITF page displayed the Western order `Juncheng Shang` (`display_order_variant`, not `exact`), while the canonical keeps the Director's legal-name order `Shang Juncheng`, composed exactly from the ATP structured fields `LastName="Shang"`/`FirstName="Juncheng"`.
- **Evidence timestamps are local wall-clocks:** the fetching agent did not record a timezone and 74 values were mislabeled with a `Z` (UTC) suffix. Commit-bounded analysis proves they cannot be UTC (all were committed no later than 2026-08-17T09:08:09Z). The false `Z` suffixes were removed on 2026-08-17 with the wall-clock digits preserved; no offset is asserted without a record. Batch and transaction evidence carrying these values was relocated to `quarantine/evidence/`.
