# HANDOFF-01 — Auditor 1 — Data Category Index

| Field | Value |
|---|---|
| **Handoff No** | **01** (absolute order) |
| **Task ID** | `T-001` |
| **From** | Director 1 |
| **To** | Auditor 1 |
| **Role (sign-off)** | Director 1 |
| **Branch ID (sign-off)** | `arena/01a01588-the-creation-2` |
| **Date** | 2026-08-18 |
| **Priority** | Normal |

---

⏳ **Submission Protocol**

Log your completed findings inside the repository's hand-off folder for your role (e.g. `hand_offs/auditor/REPLY-01-…`). Present your clean list directly to this control loop.

📢 **RELAY MESSAGE & CORE TEAM MANDATE**

**Status:** **ACTIVE / PROTOCOL INITIALIZED**
**Security Level:** **CRITICAL**
**Enforcement:** **BINDING ON ALL AGENTS (AUDITOR 3 & ENGINEER 5)**

🚨 **CRITICAL SECURITY & TRUTH NOTICE**

- • **Absolute Forensic Accountability:** **ALL WORK WILL BE INVESTIGATED FOR FALSEHOODS AND ASSERTIONS.** Every commit trail, trace file, and code structure will undergo rigorous multi-layered validation. False claims or unverified assumptions will result in immediate termination of the agent workspace.
- • **Handoff Isolation Rule:** **ALL HANDOFFS GO TO THE `hand_offs/` FOLDER IN THE REPOSITORY.** Every role's handoffs are committed there — including the director's folder (`hand_offs/director/`). Handoff structures, logs, and reports are shared in the repo, not kept local-only.
- • **Branch Commit Restriction:** **NOTHING SHOULD BE COMMITTED TO THE BRANCH EXCEPT CODE WORK FOR VERIFICATION AND ONLY IF YOU ARE ASKED TO SEND / COMMIT TO BRANCH.** Handoffs under `hand_offs/` are the designated exception and follow the Handoff Isolation Rule. Rogue commits or unrequested uploads will fail validation immediately.
- • **Sign-off Metadata Requirement:** **EVERY TEAM MEMBER MUST ATTACH THEIR ROLE AND BRANCH ID IN THEIR SUMMARY AND HANDOFFS.**

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

## Objective

An index of **data categories**:

1. **Tennis** — which tournaments exist, etc.
2. **Football** — which leagues/competitions exist, etc.

**Category level only.** No in-depth player-level (tennis) or team-level
(football) detail.

## Scope IN

- **Tennis** (from `data/tennis/master_store_tennis_SSoT.json` bytes): tournament names present, with `tour` (ATP/WTA), `tier`, `surface`, edition years, row counts per tournament. Cite `KNOWN-GAPS.md` markers (e.g. US Open 2026 absent) — reference, don't re-audit.
- **Football** (from `data/football/master_store_15767.json` bytes): `competitionName` list with `compType`, country, date range, row counts per competition, plus admission status (ADMITTED / HOLD / BLOCKED-BY-INPUT) per `APPROVAL-CARD-FULLFOOTBALL-2026-08-11.md`.

## Scope OUT

- No per-player rankings, records, or name tables.
- No per-team detail (identities, ratings, venues).
- No odds/model commentary.

## Source pointers

| Artifact | Path |
|---|---|
| Tennis store (17,285 rows) | `data/tennis/master_store_tennis_SSoT.json` |
| Football store (15,767 matches) | `data/football/master_store_15767.json` |
| Manifest | `data/MANIFEST.json` |
| Tennis pin/gaps | `data/tennis/PIN.txt`, `data/tennis/KNOWN-GAPS.md` |
| Football gaps/checksums | `data/football/KNOWN-GAPS.md`, `data/football/checksums.json` |
| Approval cards | `data/tennis/APPROVAL-CARD-TENNIS-GATE4-FINAL-2026-08-17.md`, `data/football/APPROVAL-CARD-FULLFOOTBALL-2026-08-11.md` |

## Deliverable & submission

1. Write the clean category list to **`hand_offs/auditor/REPLY-01-2026-08-18-AUD1.md`** — committed to the repo under `hand_offs/` (Handoff Isolation Rule).
2. **Present it directly to the Director (this control loop).**
3. Attach **Role** and **Branch ID** to your summary and hand-off (Sign-off Metadata Requirement).

## Rules

- Compute every count from the artifact bytes. Do not quote this hand-off's numbers as evidence.
- Do **not** modify the stores, `MANIFEST.json`, `PIN.txt`, or approval cards.
- Category-level only. Anything that looks like a category-level anomaly → flag it in the reply, don't expand scope.

---

**Sign-off — Role: Director 1 · Branch ID: `arena/01a01588-the-creation-2`**
