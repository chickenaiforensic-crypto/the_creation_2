# HANDOFF-06 — Auditor 1 — Cincinnati (WTA 1000) Audit, 2021–2025, within the `claude_1` branch

| Field | Value |
|---|---|
| **Handoff No** | **06** (absolute order) |
| **Task ID** | `T-006` |
| **From** | Director 1 (relaying a direct ADMIN order) |
| **To** | Auditor 1 |
| **Issuer sign-off** | **Role: Director 1 · Branch ID: `arena/01a01588-the-creation-2`** |
| **Date** | 2026-08-19 |
| **Priority** | **HIGH — Admin-ordered. Start immediately; one year at a time.** |

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

## THE ADMIN DIRECTIVE (verbatim)

> Create a workorder for Auditor_1 to audit Cincinnati (WTA 1000) within the
> `Claude_1` branch. The audit must cover years 2021 through 2025, processed one
> year at a time. Auditor_1 must identify all known gaps and newly discovered
> errors, adhering strictly to the requirements in Auditor_1's branch. The final
> delivery must be a consolidated report for the full 2021–2025 period.

## Step 0 — place this workorder in the workspace (immediately)

1. Read this file fully. Then copy it into the `claude_1` branch workspace as
   **`data/tennis/phase1-audit/WORKORDER_Cincinnati_WTA_Audit.md`** (the Admin
   ordered the audit "within the Claude_1 branch"; the Director session is
   branch-locked to `arena/01a01588-the-creation-2`, so carrying the workorder
   file into the workspace is your first commit there).
2. **Binding requirements — read these in full before any audit step:**
   - `data/tennis/DATA-RULES.md` on **your branch**
     (`arena/01a015bb-the-creation-2`) — the 7 rules are the audit standard.
     Where DATA-RULES conflicts with this workorder, **DATA-RULES wins** —
     flag the conflict to the Director, do not silently resolve it either way.
   - `data/tennis/phase1-audit/WORKORDER_Phase1_DrawSize_Gap_Audit.md` and
     `data/tennis/phase1-audit/README.md` on **`claude_1`** — the Phase 1
     context, method, and error log. Your work extends it.

## Scope (exactly this, nothing else)

- **Tournament:** Cincinnati, **WTA 1000** only (tour = `WTA`, tier = `M1000`).
  The ATP `Cincinnati Masters` slice is out of scope.
- **Years:** 2021, 2022, 2023, 2024, 2025 — **processed one year at a time**,
  in order, with a per-year checkpoint presented to the Director before moving
  to the next year.
- **Deliverables:** per-year checkpoints + a **consolidated report for the full
  2021–2025 period** at the end.

## Audit standard — what every year's pass must produce

For each year (on `claude_1`'s own bytes — pinned store commit
`b40331246285c7b88f364c13ea2a71ac26921ae6`, store digest on that branch
`a280b2fb…`; **re-derive every figure from those bytes, do not reuse
Director-branch figures except as orientation**):

1. **Draw size, edition-specifically confirmed** (DATA-RULES Rule 2; Phase 1A
   method): the Phase 1 table says Cincinnati 56-draw 2021–2024, 96-draw 2025 —
   verify each year for the **WTA** edition from an edition-specific source
   (Wikipedia edition page or WTA draws archive — mind the known WTA evergreen
   "Overview" trap recorded in the phase1 README). A confirmed draw size is
   what makes a missing match a **real gap** vs a **structural bye**.
2. **Round-census vs draw size:** count rows per round; list every round short
   of its draw-derived target with the exact missing count.
3. **Gap detection, R32→F chain** (Phase 1B method, reproducible):
   winners of round N vs players in round N+1; every "ghost" named with
   player, round transition, disposition. R64→R32 is bye-affected — classify,
   don't count blindly (Phase 1B self-corrections 2 and 3 are your guide).
4. **Known gaps from Phase 1B** — these WTA Cincinnati instances are already
   on file in `m1000_r32_onward_gaps.json` as **UNRESOLVED** (Director
   re-verified from that file): 2021 ×3 (Ostapenko R32→R16, Pegula R32→R16,
   Bencic R16→QF) · 2022 ×4 (Riske-Amritraj, Sabalenka, Rogers, Kudermetova,
   all R32→R16) · 2023 ×2 (Paolini R16→QF, Jabeur R16→QF) · 2025 ×1 (Gauff
   R32→R16). For each: confirm against the bytes, then resolve it with an
   external source or keep it open — every one must end with a disposition.
5. **Newly discovered errors:** anything beyond the Phase 1B list — per
   DATA-RULES: full player names (Rule 1 — flags for initials/abbreviations),
   per-row provenance genuineness (Rule 3), score/status/flag coherence,
   score arithmetic vs games/sets, duplicate/self-play rows, date validity,
   and any `rankA`/`rankB` presence (Rule 4: rank fields are excluded from the
   dataset schema — report their presence as a rule violation, do not
   silently keep or silently drop them).
6. **Accuracy spot-check (finals minimum, deeper where feasible):** verify the
   year's final (and as many earlier rounds as your sources allow) against the
   public record. Director-orientation from the Director-branch store — must be
   re-derived, not assumed: finals on file are 2021 Barty d. Teichmann 6-3 6-1 ·
   2022 Garcia d. Kvitova 6-2 6-4 · 2023 Gauff d. Muchova 6-3 6-4 · 2024
   Sabalenka d. Pegula 6-3 7-5 · 2025 Swiatek d. Paolini 7-5 6-4.

## Reporting (per year, then consolidated)

- Per-year checkpoint → presented to the Director in this control loop:
  draw size confirmed + source · census table · gaps ledger (each entry:
  player / round transition / disposition RESOLVED-with-source or OPEN) ·
  newly discovered errors ledger (each with byte evidence or named source) ·
  accuracy spot-check results.
- **Final consolidated report 2021–2025:** one document covering all five
  years — file
  `data/tennis/phase1-audit/CINCINNATI_WTA_AUDIT_REPORT_2021-2025.md` in the
  `claude_1` workspace, committed there, plus presentation directly to the
  Director in this control loop. Every gap and error from the per-year passes
  must appear in the consolidated report with its final disposition.
- **Sign-off: Role + Branch ID** on every checkpoint and the final report.

## Constraints

- Audit = report. **No data edits** unless the Director orders them
  (standing order: nothing fixed in-flight). Report violations and gaps;
  do not silently repair anything.
- DATA-RULES Rule 3: nothing self-authored — every fact traces to a named,
  checkable source; if no source exists, the gap stays open and documented.
- Where DATA-RULES conflicts with this workorder, DATA-RULES wins and you flag
  the conflict. Any genuinely unclear instruction → one direct question to the
  Director before proceeding.

---

**Sign-off — Role: Director 1 · Branch ID: `arena/01a01588-the-creation-2`**
