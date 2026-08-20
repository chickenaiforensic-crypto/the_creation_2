# AUDITOR 5 — ORIENTATION AND INDEPENDENT RECOMPUTE

**Role:** Auditor 5  
**Date:** 2026-08-20  
**Branch:** `arena/01a01f58-the-creation-2`  
**Authority:** role assignment “Auditor_5 / orientproceed”  
**Method:** every figure below was recomputed from the file’s own bytes. No figure is quoted from a prior report. A matching hash proves that bytes are unchanged; it does not prove that the dataset is complete, nor that accompanying prose is current.

**Reproduction:** from the repository root:

```bash
python3 hand_offs/auditor/recompute.py
```

Exit `0` means every implemented assertion in that script reproduced. Transcript: `hand_offs/auditor/recompute-results.json`.

---

## 0. Orientation — what this tree is

This repository is a **stripped production snapshot**, not a working engineering tree.

| Path | On disk |
|---|---|
| `data/tennis/master_store_tennis_SSoT.json` | Present. Active tennis SSoT. |
| `data/tennis/player_canonical_names.json` | Present. 1,069 entries. |
| `data/football/master_store_15767.json` | Present. Football verification target. |
| `data/MANIFEST.json` | Present. Tennis active-store + football verification-target + canonical-names pins. |
| `data/Data_Sports/data/` | **Absent.** Cited by `data/README.md` as the production root. |
| `Engineering/tools/verify_data.py` | **Absent.** Cited by `data/README.md` as the verifier. |
| `engineering/phase_{zero,one,two,three,four}/` | Present as empty stubs. Every README is the identical two-line placeholder `# the_creation_2` / `Analyse`. |
| `quarantine/evidence/` | **Absent.** Cited by `data/README.md` as the custody tree. |
| `audit_work/…/admission-ledger.json` | **Absent.** Cited by the football approval card as the admission ledger. |
| `ui_build/`, `others/`, `hand_offs/{engineer,others}/` | Placeholder READMEs only. |

Eleven README files are byte-identical stubs (`README.md` at repo root, five engineering phases, three handoff folders, `others/`, `ui_build/`). They carry no phase contract.

**Consequence of orientation:** Auditor 5 can certify **file identity and row-level integrity** of the two stores and the canonical table. Auditor 5 cannot certify a verifier run that this tree does not contain, cannot reopen Class A ATP/ITF fetches, and cannot read an admission ledger that is not here.

---

## 1. Package verdict

| Object | Verdict |
|---|---|
| Tennis SSoT bytes vs MANIFEST / PIN / GS134 card / KNOWN-GAPS pins | **AUTHENTIC** |
| Tennis row-level integrity (duplicates, self-play, dates, names, winner-first, GS intra-edition census) | **PASS** |
| Tennis residual defects listed in `KNOWN-GAPS.md` | **REPRODUCED** |
| Football store bytes vs MANIFEST / checksums.json / approval card | **AUTHENTIC** |
| Football row-level integrity | **PASS** |
| Football admitted-slice arithmetic (5,381 / 10,386) | **REPRODUCED** |
| Football HOLD 8,217 / BLOCKED-BY-INPUT 2,169 as **ledger labels** | **NOT INDEPENDENTLY READ** (ledger absent). Arithmetic identity with UEFA three-sum **does** reproduce — see §4.3. |
| `data/README.md` as an authority on the active tennis pin | **REJECT — actively false** |
| Whole-pack “locked / clean house / tools present” | **REJECT** |

The stores may be consumed under the constraints in each sport’s `KNOWN-GAPS.md` plus the additional defects in §5. The production README must not be.

---

## 2. File identity (recomputed)

| File | Bytes | MD5 | SHA-256 |
|---|---:|---|---|
| `data/tennis/master_store_tennis_SSoT.json` | 14,136,767 | `9b271a35139d8dd459c13aadf3554bfa` | `eb2eeaf7ba504bbd83c459ca47eb0d09f63deade7de713db1cc4de72f36f5527` |
| `data/tennis/player_canonical_names.json` | 277,134 | `845e6f398196abdee78444c35d5b4b77` | `94ed4e45381ef529fb19e88a0f7921e873663aa3421bf4f72503490e36189225` |
| `data/football/master_store_15767.json` | 7,130,079 | `bf2dd9b40e1dda6a4546394107f44a5a` | `809075006b53842128e261f95eb094c38581c89ae75cc8294f333c32e4a76764` |

All three match `data/MANIFEST.json`. Tennis also matches `PIN.txt`, `APPROVAL-CARD-TENNIS-GS134-2026-08-17.md`, and `tennis/KNOWN-GAPS.md`. Football also matches `football/checksums.json` and `APPROVAL-CARD-FULLFOOTBALL-2026-08-11.md`.

`APPROVAL-CARD-TENNIS-GATE4-FINAL-2026-08-17.md` pins a **different** tennis digest (`06ceabb665c26e55b727f9d2aebac06b`, 17,151 rows). That card is superseded. It is still sitting in the production tennis directory.

---

## 3. Tennis — independent recompute

**Artifact:** `master_store_tennis_SSoT.json`  
**Schema:** 3.0. `count` field = `len(matches)` = **17,285**.

### 3.1 Integrity

| Check | Result |
|---|---|
| Duplicate composite `(date, tournament, tour, round, playerA, playerB, edition_year)` | **0** |
| Byte-identical rows | **0** |
| Self-play | **0** |
| Empty `playerA` / `playerB` | **0 / 0** |
| Malformed dates | **0** |
| Null / negative `setsA|setsB|gamesA|gamesB` | **0** |
| `winner` | **`A` on all 17,285 rows** |
| `retired` / `walkover` / `defaulted` flags vs `status` | **0 mismatches** (202 / 30 / 3) |
| Odds fields | **none** |
| Date range (non-empty) | 2021-02-08 … 2026-08-03 |
| Distinct player names | **932** |
| Tours | ATP 9,419 · WTA 7,866 |

`winner == "A"` on every row is a storage convention, not a predictive feature. Randomize or symmetrize orientation before any model training. This reproduces KNOWN-GAPS §5.

### 3.2 Grand Slam intra-edition census

**46** GS editions are present. **46 / 46** contain **127** matches. Intra-edition shortfall: **0**.

| Tournament | Editions | Matches |
|---|---:|---:|
| Australian Open | 12 (ATP+WTA × 2021–2026) | 1,524 (254 × 6 years) |
| Roland Garros | 12 | 1,524 |
| Wimbledon | 12 | 1,524 |
| US Open | 10 (ATP+WTA × 2021–2025) | 1,270 |
| **US Open 2026 ATP and WTA** | **0** | **absent entire editions** |

This reproduces KNOWN-GAPS §1.

### 3.3 Forensic-null dates

Exactly **32** rows have `date == ""`. All 32 carry `provenance.forensic_null == true`. Zero empty dates lack the tag. All 32 are Australian Open.

| | 2021 | 2022 | 2024 | 2025 | 2026 | Total |
|---|---:|---:|---:|---:|---:|---:|
| ATP | — | — | — | — | — | 27 |
| WTA | — | — | — | — | — | 5 |
| **Year** | **7** | **6** | **4** | **9** | **6** | **32** |

Status: retired 19 · completed 9 · walkover 4. Reproduces KNOWN-GAPS §3.

### 3.4 Incomplete terminal sets (AO)

Numeric last-set incomplete (last pair not a completed set; walkovers excluded because they are not numeric): **30**.

- `retired`: **21**
- `completed`: **9**

Reproduces KNOWN-GAPS §4.

### 3.5 Named score defects

- Wimbledon 2021-06-29 R128, Otte vs Rinderknech: score `4-6 6-3 6-2 6-7(5) 13-12(2)`, status `completed`. Present.
- Washington 2024-08-02 QF, Shelton vs Shapovalov: score `7-6 6-6`, `defaulted: true`, status `defaulted`. Present.

Reproduces KNOWN-GAPS §6.

### 3.6 Field-level nulls

| Field | Empty rows |
|---|---:|
| `duration_min` | 2,520 |
| `rankA` | 426 |
| `rankB` | 452 |

Reproduces KNOWN-GAPS §7.

### 3.7 Identity merge (Shang)

- `Juncheng Shang` rows now: **0**
- `Shang Juncheng` rows now: **48**
- Canonical key `junchengshang`: `status: RETIRED_MERGED`, `merged_into: shangjuncheng`
- Canonical key `shangjuncheng`: Class A, ATP `S0RE`, canonical_full_name `Shang Juncheng`

The superseded Gate 4 card recorded **47** unified rows. The extra row is consistent with the GS134 append (17,151 → 17,285) and is not a fork: the retired spelling is absent. Gate 4’s “47” figure is historical and must not be re-used as a current census.

### 3.8 Canonical table census

| | |
|---|---:|
| Entries | 1,069 |
| `verified: true` (with `player_id_official`) | 190 |
| `needs_verification` | 0 |
| `disputed` | 0 |
| `RETIRED_MERGED` | 1 (`junchengshang`) |
| Remaining entries with no `verified` flag | 878 |

The 190/190 certified queue is a **subset** of the table, not a statement that 1,069 names are Class A. KNOWN-GAPS §8 already says this; the bytes agree.

### 3.9 Claims that cannot be reproduced from this tree

- GS134 composition “109 Retired + 25 Walkovers” of the **134 appended rows**. Whole-store retired/walkover flags are 202 / 30. Isolating the 134 requires the pre-append store (`06ceabb…`, 17,151 rows), which is not in this tree.
- Live ATP/ITF identity fetches (Auditor 3’s Class A re-fetch of `S0RE`, ITF 404 on `800559106`). Not re-opened by Auditor 5.
- Source-grade split “12 Official / 122 Press-Grade” on the 134. Per-row `source` strings exist; the grade taxonomy is not on the rows.

---

## 4. Football — independent recompute

**Artifact:** `master_store_15767.json`  
**Wrapper:** `format=pitch-rating-full`, `version=3.6.3`, `schemaVersion=v3.0.0`, `exportedAt=2026-08-05T06:03:26.773Z`.  
**Matches:** `store.matches` length **15,767**.

### 4.1 Integrity

| Check | Result |
|---|---|
| Unique `id` | 15,767 / 15,767 |
| Duplicate `(dateISO, competitionName, homeName, awayName)` | **0** |
| `muted: true` | **0** |
| Empty home / away names | **0 / 0** |
| Self-play (name or id) | **0** |
| Malformed `dateISO` | **0** |
| Null / negative / non-integer goals | **0** |
| Date range | **2021-07-09 … 2026-08-09** (matches `checksums.json`) |
| Match `homeId`/`awayId` missing from `store.identities` | **0** |

`football/checksums.json` `total`, `by_competition` (23 competitions), `by_year`, and `by_compType` all reproduce exactly.

### 4.2 Admitted slices (authorization scope, from the card)

The card is **PARTIAL ADMISSION — NOT WHOLE-PACK APPROVAL**. Slice sizes on disk:

| Slice | Rows | Matches card |
|---|---:|---|
| England Premier League | 1,900 | yes |
| Italy Serie A | 1,900 | yes |
| Italy Relegation Playoffs | 1 | yes |
| Germany Bundesliga | 1,530 | yes |
| Germany Relegation Playoffs | 10 | yes |
| Czech Relegation Playoffs | 20 | yes |
| Russian Relegation Playoffs | 20 | yes |
| **Admitted** | **5,381** | yes |
| **Remainder** | **10,386** | yes |

Do not treat 15,767 as an approved row count. Reproduces football KNOWN-GAPS §1.

### 4.3 HOLD 8,217 / BLOCKED-BY-INPUT 2,169

No row carries an admission-status field. The ledger cited by the card is not in this tree.

The three UEFA competitions sum to **exactly 2,169**:

| Competition | Rows |
|---|---:|
| UEFA Champions League | 786 |
| UEFA Europa League | 772 |
| UEFA Conference League | 611 |
| **Sum** | **2,169** |

`15,767 − 5,381 − 2,169 = 8,217`.

The card text says “all UEFA slices remain blocked.” The arithmetic identity is therefore **consistent with** BLOCKED-BY-INPUT = the three UEFA slices and HOLD = the non-admitted non-UEFA remainder. Auditor 5 **adopts this as an inferred identity, not as a ledger read.** Anyone treating 8,217 / 2,169 as independently labelled statuses without the ledger is overclaiming.

### 4.4 Named residual facts

- Russian Premier League with `dateISO >= 2026-07-01`: **16** rows (2026-07-24 … 2026-08-02). Partial in-flight season, not a defect. Reproduces KNOWN-GAPS §2.
- France Ligue 1 by July-start season: 2021-22 **380**, 2022-23 **380**, 2023-24 **306**, 2024-25 **306**, 2025-26 **306**. League-size change, not data loss. Reproduces KNOWN-GAPS §3.

### 4.5 Identities vs matches (observation)

`store.identities` has **798** records; match rows use **463** distinct team ids; **335** identities are unused. Unused identities include clubs from leagues with **zero matches** in this store (Belgium, Turkey, Greece, Netherlands, MLS, …) and 239 records still carrying migrated Dixon-Coles `fittedRatings`. This does not break match-row integrity. It is leftover model-port material sitting inside the verification target.

---

## 5. Defects not already on the governing gap cards

These are **new relative to the KNOWN-GAPS files in this tree.** They were measured from the bytes.

### 5.1 CRITICAL — `data/README.md` pins the wrong tennis store

The production data README still states:

- tennis rows **17,151**
- tennis MD5 **`06ceabb665c26e55b727f9d2aebac06b`** (Gate 4 FINAL, pre-GS134)
- current approval card = `APPROVAL-CARD-TENNIS-GATE4-FINAL-2026-08-17.md`
- production root = `data/Data_Sports/data/`
- verifier = `python3 Engineering/tools/verify_data.py`

On this branch the active store is **17,285 / `9b271a35…`**, the current card is **GS134**, the path `data/Data_Sports/data/` does not exist, and the verifier does not exist.

A consumer that trusts `data/README.md` will reject the authentic file or look for a store that is not here. **The README is not a pin. It is a defect.**

### 5.2 HIGH — PIN.txt hash is current; PIN.txt card pointer is not

`PIN.txt` records md5 `9b271a35…`, sha256 `eb2eeaf7…`, rows 17,285, bytes 14,136,767 — all correct. In the same file it still names `APPROVAL-CARD-TENNIS-GATE4-FINAL-2026-08-17.md` as the approval card. GS134’s card says it supersedes GATE4-FINAL. Two authorities in the tennis directory disagree about which card governs.

### 5.3 HIGH — canonical join-key drift: Diego Dedura-Palomero

The store spelling is `Diego Dedura-Palomero` (Gate 4 respell). The table key remains `diegodedura` (join of the pre-respell `store_v3_spelling` `Diego Dedura`).

`join(canonical_full_name)` = `diegodedurapalomero`, which is **not a key** in the table.

This is the **only** store name whose accent-folded alphanumeric join-key is absent from the table. Every other hyphenated name joins cleanly (`felixaugeraliassime`, `ylenainalbon`, …). Shang was handled with an explicit `RETIRED_MERGED` alias key. Dedura was not.

A consumer that joins store bytes to the table by current-spelling join-key will drop this player.

### 5.4 MEDIUM — 82 MOL Cup rows with empty `sourceId`

Football `sourceId == ""` : **82** rows, all `competitionName == "MOL Cup"`, ids `m:5374` … `m:5455`, dates 2024-09-25 … 2026-05-20. Goals are well-typed integers; they are not muted.

The store wrapper `amended` entry D2 records an 82-row MOL Cup adoption (`5,000 -> 5,082`). The empty `sourceId` on exactly those 82 rows is not listed in `football/KNOWN-GAPS.md`. Provenance for those rows is not on the match object.

### 5.5 LOW — `J.J. Wolf` initials remain

Canonical `jjwolf.canonical_full_name` = `J.J. Wolf`. Store rows: **60**. `Jeffrey Wolf`: **0**. This tree does not contain a binding DATA-RULES file, so Auditor 5 does not treat initials as a rule violation here. It is a residual abbreviated spelling that any later naming standard will have to confront. Not on tennis KNOWN-GAPS.

### 5.6 LOW — GATE4-FINAL card left in the production tennis directory

The file is historically useful. Sitting next to the live store with a different MD5, while `data/README.md` still points at it, is how a consumer pins the wrong artifact. Custody convention in the README itself says staging/historical material belongs under `quarantine/evidence/`, which does not exist.

### 5.7 INFO — verifier, quarantine, and admission ledger are not in this snapshot

Absence is a fact about the snapshot, not a hash failure of the stores. It does mean:

- `data/README.md` admission rule 2 (“keep executable tools under `Engineering/`”) is vacuously unmet.
- Football authorization labels cannot be ledger-read.
- Evidence batches referenced by PIN.txt (wall-clock repairs, ITF 404, etc.) are not inspectable here.

---

## 6. What Auditor 5 is **not** claiming

- Not a live source audit. ATP `S0RE`, ITF `800559106`, RSSSF, tennisabstract, and Wikipedia URLs were not re-fetched.
- Not a slice-hash audit of the football admitted SHA-256 values on the 2026-08-11 card (those are hashes of extracted slices, not of the whole file; the slice extractor is not in this tree).
- Not an approval of UEFA, La Liga, Ligue 1, Scottish, Czech league, or cup rows for use.
- Not an approval of `data/README.md`.
- Not a reconstruction of HOLD vs BLOCKED as labelled statuses.
- Not a claim that 1,069 canonical entries are Class A verified. 190 are.

---

## 7. Actions

For the **Director**

1. Treat `data/README.md` as failed custody, not as a pin.
2. Decide whether GATE4-FINAL remains in `data/tennis/` or is moved out of the production directory.
3. Decide whether the Dedura join-key is repaired by adding alias key `diegodedurapalomero` (Shang pattern) or by renaming the existing key (breaks any consumer holding `diegodedura`).
4. Confirm that BLOCKED-BY-INPUT is defined as the three UEFA competitions. If yes, the 2,169 figure is reproducible without the missing ledger. If no, the 2,169 figure is currently unreproducible.

For **Engineer** (do not touch store bytes unless directed)

1. Rewrite `data/README.md` against MANIFEST: tennis 17,285 / `9b271a35…`, football 15,767 / `bf2dd9b40e…`, current tennis card = GS134, production root = `data/` (not `data/Data_Sports/data/`). Stop citing a verifier that is not in the tree, or restore the verifier.
2. Point `PIN.txt` at `APPROVAL-CARD-TENNIS-GS134-2026-08-17.md`.
3. Add `diegodedurapalomero` as an alias/join key for Dedura-Palomero, Shang-style, **without** rewriting store bytes.
4. Record the 82 empty-`sourceId` MOL Cup rows on `football/KNOWN-GAPS.md`.
5. Replace the eleven stub READMEs with real phase/handoff contracts, or delete the empty phase directories so they are not mistaken for scoped work.

For **downstream consumers**

- Read `data/MANIFEST.json`, not `data/README.md`, for the active tennis pin.
- Read each sport’s `KNOWN-GAPS.md` plus §5 of this report before use.
- Football: only the 5,381 admitted-slice rows are in-scope unless a later card says otherwise.
- Tennis: do not train on `winner` as a feature; do not impute the 32 forensic-null dates; do not treat US Open 2026 as missing-from-an-edition (the editions are absent).

---

## 8. Pin of this report’s inputs

| Input | MD5 |
|---|---|
| tennis SSoT | `9b271a35139d8dd459c13aadf3554bfa` |
| canonical names | `845e6f398196abdee78444c35d5b4b77` |
| football store | `bf2dd9b40e1dda6a4546394107f44a5a` |
| MANIFEST.json | `ec172b9578edefd9dd20eee7bf3f0d16` |

Auditor 5 did not modify any file under `data/`.
