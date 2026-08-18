# APPROVAL CARD — TENNIS MASTER STORE (GATE 4 FINAL, POST-MERGE)

**Artifact:** `data/Data_Sports/data/tennis/master_store_tennis_SSoT.json`

- **Master MD5:** `06ceabb665c26e55b727f9d2aebac06b`
- **Master SHA-256:** `68f408a8adeeabc8b30e46d5c90f81a90fb9eaadfffa7bb8dad92bd01710b54a`
- **Bytes:** 14,004,153
- **Rows:** 17,151 (`count` field verified equal to `len(matches)`)
- **Distinct player names:** 932 (was 933 — one identity unified)
- **Date of approval:** 2026-08-17
- **Issuing engineer:** branch `arena/01a00db1-the-creation`
- **Authority:** Director GATE 4 FINAL CLOSURE & "CLEAN HOUSE" COMMENCE 2026-08-17 §2.

## Transaction chain

| Stage | MD5 | Rows |
|---|---|---:|
| 190-name run (held, untouched) | `137d3cc729989474bb8d5ae568d7f68f` | 17,151 |
| Gate 4 respell (Dedura-Palomero, 1 row) | `5e1526331b19715443b10f1d708568ef` | 17,151 |
| **Gate 4 identity merge (Shang, 45 rows)** | **`06ceabb665c26e55b727f9d2aebac06b`** | **17,151** |

## What changed in this approval

**Identity merge:** `Juncheng Shang` (45 rows) → `Shang Juncheng` (2 rows) = **47 rows unified**
under the verified canonical join-key. The retired key `junchengshang` is **kept, not deleted**,
marked `RETIRED_MERGED` with `merged_into: shangjuncheng`, preserving join history for any
consumer holding the old spelling.

## ⚠️ IDENTITY EVIDENCE — DIRECTOR'S CITED ID WAS WRONG

The directive cited **ATP `S0MZ`**. Fetched ID-addressed by the author, `S0MZ` renders:

> `{"LastName":"Serrano","FirstName":"Jorge","BirthDate":"1997-01-05","NatlId":"ESP","CareerPrizeFormatted":"$186"}`

**Jorge Serrano, Spain, born 1997 — not this player.** The merge was **not** executed on the cited
id. A second hypothesis, `S0V6` (from the atptour.com slug `juncheng-shang`), renders **Indrek
Soome, FIN, b.2003** — re-confirming the standing project finding that *the ATP URL slug is not
authoritative; the id is.* Both were logged `REJECTED_IDENTITY` and discarded.

**Accepted identity — ATP `S0RE`** (Class A, ID-addressed, author-fetched):

> `{"LastName":"Shang","FirstName":"Juncheng","BirthCity":"Beijing, China","BirthDate":"2005-02-02","NatlId":"CHN","PlayHand":"Left-Handed","SglHiRank":47,"SglCareerTitles":1}`

Single-human confirmation: b.2005-02-02 Beijing, left-handed, career-high No. 47, 1 title —
consistent with both spellings carrying rank 89 in the same 2024 Atlanta week and a single
2021–2026 activity span.

**A-ITF caveat, disclosed:** the ITF URL recorded in `batch_8` for id `800559106` returned
**HTTP 404** on re-fetch across `jt`/`mt` paths. A search index still lists that exact URL with the
correct player, but **search-engine snippets are never acceptable as primary evidence**, so it was
not relied upon. The merge rests on Class A ATP `S0RE`. **Auditor action: re-resolve the A-ITF
profile for `800559106`.**

## Merge guards (new tool `apply_identity_merge.py`)

A merge is higher-risk than a respell — it is unrecoverable if the two are different humans — so
merge-specific guards were built and **fault-injection tested before use**:

| Guard | Check | Result |
|---|---|---|
| G1 | No row contains BOTH spellings (would prove distinct humans) | 0 rows — **pass** |
| G2 | No row becomes self-play | 0 — pass |
| G3 | No composite-key collisions | 0 — pass |
| G4 | No byte-identical rows | 0 — pass |
| G5 | Row-count invariant | 17,151 = 17,151 — pass |
| G6 | Base-hash precondition | matched — pass |

**Fault injection:** a fabricated row where both spellings meet, a forced self-play case, a wrong
base hash and a violated row invariant were each injected into sandboxed copies. **All were
refused; no sandbox store was written.**

## Self-audit results

- Rows changed: **45**, all a single transition `Juncheng Shang → Shang Juncheng` (19 `playerA`, 26 `playerB`).
- Row count 17,151 → 17,151. `count` field consistent. 0 self-play, 0 duplicate composite keys.
- `Shang Juncheng` 47 rows · `Juncheng Shang` **0 rows**.
- Gates: `verify_data` **25/25** · `validate_batch --all` **PASS** · ruling tests **ALL PASS**.

## Supersedes

`APPROVAL-CARD-TENNIS-GATE4-2026-08-17.md` (MD5 `5e152633…`). `PIN.txt` and `data/MANIFEST.json`
updated in the same commit.
