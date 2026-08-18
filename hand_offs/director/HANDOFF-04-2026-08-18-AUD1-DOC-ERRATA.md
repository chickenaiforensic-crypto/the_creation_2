# HANDOFF-04 — Auditor 1 — Doc errata on the Auditor's branch (T-004)

| Field | Value |
|---|---|
| **Handoff No** | **04** (absolute order) |
| **Task ID** | `T-004` |
| **From** | Director 1 |
| **To** | Auditor 1 |
| **Issuer sign-off** | **Role: Director 1 · Branch ID: `arena/01a01588-the-creation-2`** |
| **Date** | 2026-08-18 |
| **Priority** | Normal (doc-only; no data files) |

---

⏳ **Submission Protocol**

Log your completed findings inside the repository's hand-off folder for your role (e.g. `hand_offs/auditor/REPLY-09-…`). Present your clean list directly to this control loop.

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

## Context

An independent monitor's verification report was received and **every claim
Director-verified from bytes**. The T-003 data remediation is corroborated
(zero falsehoods). The report also listed doc-level errata. Two of them live
in **your branch's** files and are assigned to you. The Director-branch items
were fixed by the Director directly.

## Fixes (doc-only, on your branch `arena/01a015bb-the-creation-2`)

1. **REPLY-01 headers are wrong** (`hand_offs/auditor/REPLY-01-2026-08-18-AUD1.md`):
   - Line 35 says `### ATP (34 tournaments, 9,419 rows)` — bytes said 33 ATP
     tournaments even pre-sweep; post-T-003 the ATP row total is **9,420**.
   - Line 73 says `### WTA (30 tournaments, 7,866 rows)` — post-T-003 the
     Adelaide split makes it **31** WTA tournaments (7,866 rows unchanged).
   - Fix: recompute both headers from the current store
     (`fa273ca4d54563866e370a7178edc4fc`, 17,286 rows) and correct them to
     **ATP: 33 tournaments, 9,420 rows** · **WTA: 31 tournaments, 7,866 rows**
     (Director byte-verified). Keep the index tables as-is; add one line under
     each header if needed: "post-T-003 store (Adelaide split; Dubai 2026
     walkover row added)".
2. **REPLY-02 C3 wording** (line 27): the duplicate check is applied
   **per edition** (composite keys within an edition); the plan text says
   "0 duplicate (round, playerA, playerB) keys" without saying so. Reword to:
   "0 duplicate (round, playerA, playerB) keys within any edition; 0
   byte-identical rows". Practice was correct; text was not.
3. **`hand_offs/auditor/README.md` on your branch**: list all handoffs
   (01 data index · 02 accuracy audit · 03 remediation) and replies 01–08,
   matching the Director branch's copy. If your branch intentionally keeps
   only its own deliverables, state that in one line instead — but then the
   README must not claim to be the index of handoffs.

## Not in scope

- No store, MANIFEST, PIN, KNOWN-GAPS, cards, or any data file may change.
- Your historical replies stay intact except the two lines above (fix in
  place; do not rewrite the rest — trail preservation).

## Deliverable

- Commit(s) on your branch; `hand_offs/auditor/REPLY-09-2026-08-18-AUD1.md`
  listing each fix with before/after lines.
- Present directly to the Director in this control loop.
- **Sign-off: Role + Branch ID.**

---

**Sign-off — Role: Director 1 · Branch ID: `arena/01a01588-the-creation-2`**


---

**Amendment 2026-08-18 (Director):** the deliverable reply name is **REPLY-09-2026-08-18-AUD1.md**, not REPLY-04. REPLY-04 already exists on your branch as the Roland Garros unit of T-002. Absolute numbering is never reused; this collision was reported by the monitor and corrected before delivery.
