# HANDOFF-02 — Auditor 1 — Tennis accuracy audit, one tournament type at a time (US Open year-by-year; audit plan first)

| Field | Value |
|---|---|
| **Handoff No** | **02** (absolute order) |
| **Task ID** | `T-002` |
| **From** | Director 1 |
| **To** | Auditor 1 |
| **Issuer sign-off** | **Role: Director 1 · Branch ID: `arena/01a01588-the-creation-2`** |
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

- **REPLY-01 (T-001) received and Director-verified.** Branch `arena/01a015bb-the-creation-2` @ `ecf6c6a`. Store digests, tour totals, GS counts, US Open edition counts, and the football 5,381/8,217/2,169 reconciliation all reproduce from bytes. T-001 is closed.
- This handoff is the next unit of work: the **tennis accuracy audit**.

## Objective (Director's words)

Start from **tennis** and work **one tournament type at a time**.
For the **US Open, audit thoroughly year by year**, and relay the
**accuracy / state of the data**. First create an **auditing plan** that
makes the work effective.

## Execution order

**Step 1 — Auditing plan (do this first; Work Rule 7).**
Deliver it as Part A of your reply. It must state:

1. The **order of tournament types**: GS first (starting with the US Open), then propose M1000 → ATP500/WTA500 → ATP250/WTA250.
2. The **checks applied per tournament**: row counts per tournament/tour/year; round coverage (R128 → F, 127 rows per complete GS edition); duplicate detection; score sanity vs `status`/`retired`/`walkover`/`defaulted`; set/game totals vs score string; forensic-null dates (`provenance.forensic_null`, KNOWN-GAPS §3 — never invented); `tier`/`surface`/`tour` consistency; provenance tags present.
3. The **US Open year-by-year procedure**: the editions on file are 2021–2025, ATP and WTA (127 rows each). 2026 is absent entire editions per KNOWN-GAPS §1 — do not invent it. One year = both tours, audited and reported separately.
4. The **accuracy/state report format** per year and per type: what is verified accurate, what is defective, each defect with its evidence or citation.
5. **Evidence rules**: every figure computed from the artifact bytes; KNOWN-GAPS/PIN cited where they already pin a fact, not re-derived.

**Step 2 — US Open, year by year (2021 → 2025).**
Audit each year thoroughly (ATP + WTA). Relay the accuracy/state of each year as Part B of your reply.

**Step 3 — Next tournament types, one at a time**, in the order fixed by your plan. Relay the accuracy/state per type as each completes. Continue in sequence; no new instruction is needed between types.

## Deliverable

- **Plan + US Open year-by-year state:** `hand_offs/auditor/REPLY-02-2026-08-18-AUD1.md`, committed to the repo under `hand_offs/` (Handoff Isolation Rule), then **presented directly to the Director in this control loop**.
- **Sign-off:** attach your Role + Branch ID to the reply.

## Rules

- Plan first — no auditing output before the plan is in the reply.
- Do **not** modify the stores, `MANIFEST.json`, `PIN.txt`, approval cards, or KNOWN-GAPS files.
- Every count byte-computed; every defect cited or evidenced.
- Report the **true state**, defects included. A "clean" report that hides a known defect fails validation.
- One tournament type at a time. Do not jump ahead.
- Blocked on something genuinely unclear? One direct question to the Director.

---

**Sign-off — Role: Director 1 · Branch ID: `arena/01a01588-the-creation-2`**
