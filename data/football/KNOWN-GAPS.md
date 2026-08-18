# KNOWN GAPS — football master store (15,767)

**Artifact:** `master_store_15767.json` · md5 `bf2dd9b40e1dda6a4546394107f44a5a`
**Established by:** independent audit, 2026-08-14, branch `arena/019fff7a-the-bettor-1`
**Method:** every figure below recomputed from the file's own bytes. No figure is quoted from a report.

---

## 1. Only 5,381 of 15,767 rows are approved for use

The package README is titled **"15,767 Verified Matches"**. The governing approval card
(`APPROVAL-CARD-FULLFOOTBALL-2026-08-11.md`, stored alongside) records
**PARTIAL ADMISSION — NOT WHOLE-PACK APPROVAL**:

| Status | Rows |
|---|---:|
| ADMITTED | 5,381 |
| HOLD | 8,217 |
| BLOCKED-BY-INPUT | 2,169 |
| **Total** | **15,767** |

Verified against the bytes: the admitted slices total exactly 5,381 and the non-admitted
remainder is exactly 10,386 (8,217 + 2,169). Both figures reproduce.

**Admitted slices only:**

| Slice | Rows |
|---|---:|
| England Premier League | 1,900 |
| Italy Serie A | 1,900 |
| Germany Bundesliga | 1,530 |
| Czech Relegation Playoffs | 20 |
| Russian Relegation Playoffs | 20 |
| Germany Relegation Playoffs | 10 |
| Italy Relegation Playoffs | 1 |

**All UEFA slices remain BLOCKED** (Champions League 786, Europa League 772,
Conference League 611). The package's "zero synthetic" claim was **not adopted** by the card.

**Consequence:** the README headline overstates what is usable by 10,386 rows. Do not treat
the 15,767 figure as an approved row count.

## 2. Russian Premier League 2026-27 is a partial season in progress

16 rows on file against a 240-row full season. This is expected for an in-flight season, not a
defect — but it must not be read as a complete season.

## 3. France Ligue 1 season-size change is genuine, not a gap

380 rows/season for 2021-22 and 2022-23, then 306 rows/season from 2023-24. This reflects the
league's reduction from 20 to 18 clubs. Recorded here so it is not later mistaken for data loss.

---

## What is verified clean

15,767 rows · 0 duplicate ids · 0 duplicate (date, competition, home, away) tuples ·
0 malformed dates · 0 null/negative/non-integer goals · 0 empty team names · 0 self-play rows ·
0 muted rows · date range 2021-07-09 to 2026-08-09.

The README's 23-competition breakdown and its stated date range were recomputed and match the
data exactly (0 mismatches). Master md5 and sha256 match the approval card.

The defect is one of **authorisation scope**, not data integrity: the rows are sound, but two
thirds of them are not cleared for use.
