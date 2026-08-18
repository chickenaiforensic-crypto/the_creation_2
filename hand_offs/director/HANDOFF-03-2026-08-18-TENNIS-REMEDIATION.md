# HANDOFF-03 — Tennis Remediation Sweep (fix the errors from the audit; make tennis clean)

| Field | Value |
|---|---|
| **Handoff No** | **03** (absolute order) |
| **Task ID** | `T-003` |
| **From** | Director 1 |
| **To** | **ENGINEER 5** (per fixed relay roster; if you are not Engineer 5, sign with your actual Role + Branch ID and the Director will record it) |
| **Issuer sign-off** | **Role: Director 1 · Branch ID: `arena/01a01588-the-creation-2`** |
| **Date** | 2026-08-18 |
| **Priority** | **Director's one-sweep order — execute exactly, nothing extra** |

---

⏳ **Submission Protocol**

Log your completed findings inside the repository's hand-off folder for your role (e.g. `hand_offs/engineer/REPLY-03-…`). Present your clean list directly to this control loop.

📢 **RELAY MESSAGE & CORE TEAM MANDATE**

**Status:** **ACTIVE / PROTOCOL INITIALIZED**
**Security Level:** **CRITICAL**
**Enforcement:** **BINDING ON ALL AGENTS (AUDITOR 3 & ENGINEER 5)**

🚨 **CRITICAL SECURITY & TRUTH NOTICE**

- • **Absolute Forensic Accountability:** **ALL WORK WILL BE INVESTIGATED FOR FALSEHOODS AND ASSERTIONS.** Every commit trail, trace file, and code structure will undergo rigorous multi-layered validation. False claims or unverified assumptions will result in immediate termination of the agent workspace.
- • **Handoff Isolation Rule:** **ALL HANDOFFS GO TO THE `hand_offs/` FOLDER IN THE REPOSITORY.** Every role's handoffs are committed there — including the director's folder (`hand_offs/director/`). Handoff structures, logs, and reports are shared in the repo, not kept local-only.
- • **Branch Commit Restriction:** **NOTHING SHOULD BE COMMITTED TO THE BRANCH EXCEPT CODE WORK FOR VERIFICATION AND ONLY IF YOU ARE ASKED TO SEND / COMMIT TO BRANCH.** Handoffs under `hand_offs/` are the designated exception and follow the Handoff Isolation Rule. Rogue commits or unrequested uploads will fail validation immediately.
- • **Sign-off Metadata Requirement:** **EVERY TEAM MEMBER MUST ATTACH THEIR ROLE AND BRANCH ID IN THEIR SUMMARY AND HANDOFFS LOCALLY.**

📋 **MAIN**
**The Goal:** Writing 100% accurate code with strict controls so nobody can upload messy, duplicate, or unverified files again.

💬 **SESSION RULES (BINDING)**

1. **1. Clear** — No vague language. State exactly what was done, found, or needed.
2. **2. Brief** — No padding, no preamble, no trailing summaries. Say it once.
3. **3. Summarised** — Compress findings to their essential point. No walls of text.
3b. **Simplification Rule** — All information must be listed clearly and summarized as if the Director has no prior context.

🛠️ **WORK RULES (BINDING)**

1. **1. Never skim read** — Read every file fully before acting on it.
2. **2. Never assume** — If it is not confirmed in the file or output, it is not known.
3. **3. Never guess** — No inferences presented as facts.
4. **4. Always audit and confirm before touching anything** — Verify state first, act second.
5. **5. Do what the user wants** — Not what seems logical, not what seems better. What is asked.
6. **6. Ask when unclear** — One direct question. No proceeding blind.
7. **7. Before writing anything — plan first** — Think through the approach before producing any output.
8. **8. Audit before every question** — For every question you intend to ask, first perform a system audit (read the engine · code · config · deployment · DB · memory · docs) to check whether the answer is already there. Only ask if the answer is genuinely not resolvable from the system. A question that the system already answers is a failure of this rule.

---

## Context

- T-002 (tennis accuracy audit, Auditor 1) is CLOSED and Director-verified:
  **305 editions / 17,285 rows, zero arithmetic defects, zero verified result
  discrepancies.** Pinned defects and new defect classes were consolidated in the
  Director's register.
- The Director has now ordered the **one-sweep remediation**: fix the errors, on
  the repo. This workorder covers **tennis only**. Football and the canonical
  names table are **out of scope — do not touch them**.
- Current store digest (pre-sweep): md5 `ad0b261dedc1ba58aea988f763f8f641`,
  sha256 `dc2fd01873e5b7ab25611913ed45fd18ee02dad809b958e75c612614e74696eb`,
  rows **17,285**, bytes 14,135,427.

## The fixes (exactly these, in this order)

### D1 — Split the merged WTA Adelaide 2023 edition (F-1)

Store currently labels 53 WTA rows as `tournament="Adelaide"`, `edition_year=2023`.
They are two real tournaments merged. **Split by date — the boundary is clean:**

| Split | Dates | Rows | Final (stays in store) |
|---|---|---|---|
| `"Adelaide International 1"` | `2023-01-01` … `2023-01-08` | 29 | Sabalenka d. Noskova `6-3 7-6(4)` (2023-01-08) |
| `"Adelaide International 2"` | `2023-01-09` … `2023-01-14` | 24 | Bencic d. Kasatkina `6-0 6-2` (2023-01-14) |

- Relabel `tournament` on all 53 rows accordingly. Keep `tour=WTA`,
  `tier=WTA500`, `surface=Hard`, `edition_year=2023` unchanged.
- After the split, assert per sub-edition: no duplicate matches, no
  self-play, every winner of round R appears in round R+1 where both rounds
  exist. Residual spine gaps (e.g. Int'l 2 has 0 SF rows) are **documented,
  not invented** — see D5.
- Do not create rows that do not exist.

### D2 — Add the missing Dubai 2026 ATP final as a walkover row (F-2)

The 2026 Dubai (ATP500) final was a walkover: **Medvedev d. Griekspoor W/O**,
2026-02-28 — externally confirmed (AP News 2026-02-28; Livemint; Director-verified).
Add one row:

- `date="2026-02-28"`, `tournament="Dubai"`, `tier="ATP500"`, `round="F"`,
  `surface="Hard"`, `indoor=false`, `tour="ATP"`, `playerA="Daniil Medvedev"`,
  `playerB="Tallon Griekspoor"`, `setsA=0`, `setsB=0`, `gamesA=0`, `gamesB=0`,
  `score="W/O"`, `bestOf=3`, `status="walkover"`, `walkover=true`,
  `retired=false`, `defaulted=false`, `winner="A"`, `edition_year="2026"`.
- `rankA`/`rankB`/`duration_min`: leave empty strings (counted as nulls — see D5).
- `provenance`: `raw_source` must cite the external confirmation (AP News URL,
  2026-02-28, verified by Director 2026-08-18); `capture_agent` = your Role +
  Branch ID.
- Store rows become **17,286**. Update the store's top-level `count` and any
  internal row-count mention to 17,286 (grep for "17285" inside the store and
  fix each occurrence consistently).

### D3 — Normalize score markers: strip `RET` / `Def.` / `DEF` (O-1 rev2, M-3, D-NEW-1, F-3)

**Policy (Director's decision):** score strings carry pure set scores only;
retirement and default are conveyed exclusively by `status` + flags
(`retired`, `defaulted`), never by tokens inside `score`.

- Strip the trailing `RET` token from **all 31 rows** that carry it:
  - Australian Open (26): 2021 R128 Tomic–Sugita, R32 Dimitrov–Carreno Busta,
    R16 Rublev–Ruud, WTA R128 Juvan–Konta; 2022 R64 van de Zandschulp–Gasquet,
    WTA R128 Brengle–Yastremska, WTA R64 Svitolina–Tan, WTA R64 Zhang–Rybakina;
    2024 R128 de Minaur–Raonic, WTA R16 Noskova–Svitolina, WTA R128
    Mertens–Sherif, WTA R128 Wozniacki–Linette; 2025 SF Zverev–Djokovic, R16
    Alcaraz–Draper, R64 Lehecka–Gaston, R64 Cerundolo–Diaz Acosta, R128
    Passaro–Dimitrov, R128 Davidovich Fokina–Shang, R128 Martinez–Darderi,
    WTA R32 Bencic–Osaka; 2026 QF Djokovic–Musetti, R32 Paul–Davidovich Fokina,
    R128 Sinner–Gaston, R128 Borges–Auger-Aliassime, WTA R128 Hon–Stakusic,
    WTA R128 Klimovicova–Jones.
  - Roland Garros (1): 2026 QF Arnaldi–Berrettini `7-5 5-2 RET`.
  - Cincinnati Masters (1): 2025 F Alcaraz–Sinner `5-0 RET`.
  - Basel (3, ATP500): 2025 QF Davidovich Fokina–Ruud `7-6(1) 0-0 RET`,
    QF Munar–Auger-Aliassime `6-3 0-0 RET`, QF Fonseca–Shapovalov `3-6 6-3 4-1 RET`.
- Strip the default tokens from the 2 rows that carry them:
  - Barcelona 2021 R32 Zapata Miralles–Fognini `6-0 4-4 Def.` → `6-0 4-4`.
  - Dubai 2024 SF Bublik–Rublev `6-7(4) 7-6(5) 6-5 DEF` → `6-7(4) 7-6(5) 6-5`.
- **Assertion required per edited row:** the parsed set-pair list of `score`
  is byte-identical before and after (only the trailing token disappears).
  No digits may change anywhere.

### D4 — The 9 AO §4 completed-status partial scores (evidence or note, never guess)

These 9 AO rows carry retirement-shaped scores under `status="completed"`:

1. 2021 R128 Ruud d. Thompson `6-3 6-3 2-1`
2. 2021 R128 Machac d. Vilella Martinez `6-7(5) 7-5 6-0 3-0`
3. 2024 R32 Alcaraz d. Shang `6-1 6-1 1-0`
4. 2024 R128 Medvedev d. Atmane `5-7 6-2 6-4 1-0`
5. 2024 R128 Baez d. Wolf `3-6 6-2 6-3 3-0`
6. 2025 R16 Shelton d. Monfils `7-6(3) 6-7(3) 7-6(2) 1-0`
7. 2025 R32 Humbert d. Fils `4-6 7-5 6-4 1-0`
8. 2026 R64 Moutet d. Zheng `3-6 6-1 6-3 2-0`
9. 2026 R128 Musetti d. Collignon `4-6 7-6(3) 7-5 3-2`

For **each** row: check an external source. If (and only if) the source
confirms a retirement, relabel `status="retired"`, `retired=true`, and put
the source URL in `provenance`. If not confirmable: **leave status untouched**
and add `provenance.note = "score-shape suggests retirement; status retained
pending evidence (T-003 remediation 2026-08-18)"`. Never relabel on inference.

### D5 — Re-pin every digest site + documentation (PA-02, PA-03, M-1/M-2 documentation)

After D1–D4, compute the new md5/sha256/bytes and update **every** pin:

1. `data/MANIFEST.json` → `active_store.rows` = 17,286, new md5 + sha256.
2. `data/tennis/PIN.txt` → new `md5`, `sha256`, `bytes`, `rows: 17286`; append a
   line: `T-003 remediation 2026-08-18: Adelaide 2023 WTA split into
   Adelaide International 1 (29) + 2 (24); Dubai 2026 ATP F walkover row added
   (17,286 rows); RET/Def./DEF tokens stripped from 33 scores (31 RET + 2 Def);
   §4 nine rows evidence-checked per D4. Director order.`
3. `data/tennis/KNOWN-GAPS.md`:
   - Header pins → new MD5/SHA-256, Rows 17,286.
   - §5 "All 17,285 records" → 17,286.
   - §7 recompute the three null censuses from bytes (the new Dubai row adds
     nulls; the marker strip changes none).
   - §6 wording fix (PA-03): state that Wimbledon 2019–2021 used the 12-12
     final-set tiebreak, so 2021 R128 Otte–Rinderknech `13-12(2)` marked
     completed **is format-consistent**; the residual §6 items are the
     Washington 2024 default-marker question (now resolved by D3 policy) and
     the marker-casing inconsistency (resolved by D3). Rewrite §6 accordingly.
   - Add a section **"Non-GS completeness (M-1/M-2)"**: no walkover rows
     outside GS except title matches now recorded per D2 (0 WO in the prior
     11,443 non-GS rows); spine coverage — M1000 28/82 complete, ATP/WTA500
     44/81, ATP/WTA250 51/96; **205 spine matches absent** across non-GS;
     late-entrant definition note (161 + 1,766 first-transition events);
     worst editions: WTA Miami 2022 (R32=12/R16=7), ATP Cincinnati 2023
     (R32=13/R16=6); season-start dates: 48 rows (Brisbane 30 + Auckland 18);
     Adelaide Int'l 2 2023 0 SF rows; Adelaide 2022 Int'l 2 absent.
   - Add a note: bare `7-6`/`6-7` tiebreak-less scores exist (17 AO QF rows +
     additional QF rows elsewhere, e.g. Adelaide 2023 QFs) — census them
     store-wide from bytes and record the count; digits are never invented.
4. `data/tennis/APPROVAL-CARD-TENNIS-GS134-2026-08-17.md` → header
   Master MD5/SHA-256/Bytes/Rows → new values; append one row to the
   transaction-chain table: `T-003 remediation sweep | <new md5> | 17,286`.
   Do not rewrite historical stage rows.
5. `data/README.md` → production-store table row for tennis: 17,286 rows, new
   md5. Fix any other tennis figure in that file that contradicts the new pins.

### Explicitly NOT to fix (document only — do not invent)

- §3 forensic-null dates: never invent dates.
- §5 `winner=="A"`: by design.
- O-3 2021-only long final sets: correct.
- O-5 / §7 rank+duration nulls: no sources to fill them.
- M-2 missing non-GS matches: no rows added except the D2 title match.
- Bare tiebreak digits: never invented.

## Before replying — self-verification (all assertions must appear in your reply)

1. New md5/sha256/bytes; `count` == `len(matches)` == 17,286.
2. Adelaide split: 29/24 partition, both finals present, bracket invariants
   hold per sub-edition, dates within windows.
3. Marker census store-wide: **0** occurrences of `RET`, `Def.`, `DEF` in any
   `score`; pairs preserved on all 33 edited rows (show the before/after pair
   list for each).
4. D4 table: per-row outcome — relabeled (with source URL) or noted (unchanged).
5. §7 recomputed values; every pin site lists the new digest.
6. Football store + canonical names table + all other files: **untouched**
   (show their digests unchanged).

## Deliverable

- `hand_offs/engineer/REPLY-03-2026-08-18.md` with the fix log + all assertions
  above, committed to the repo under `hand_offs/`, then **presented directly to
  the Director in this control loop**.
- **Sign-off: Role + Branch ID** on the reply.
- One commit story per logical fix group (D1…D5), or one well-documented
  commit if atomic — your call; every commit message must say what changed.

---

**Sign-off — Role: Director 1 · Branch ID: `arena/01a01588-the-creation-2`**
