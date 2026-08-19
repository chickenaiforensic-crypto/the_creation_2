# HANDOFF-07 — Auditor 1 — Fix all Cincinnati WTA 1000 issues and gaps (2021–2025) thoroughly, and report

| Field | Value |
|---|---|
| **Handoff No** | **07** (absolute order) |
| **Task ID** | `T-007` |
| **From** | Director 1 (relaying ADMIN) |
| **To** | Auditor 1 |
| **Issuer sign-off** | **Role: Director 1 · Branch ID: `arena/01a01588-the-creation-2`** |
| **Date** | 2026-08-19 |
| **Priority** | **HIGH — Admin-ordered.** |

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

> ask auditor_1 to fix all present issues and gaps thoroughly and report

## Context — your Checkpoint 1 is Director-verified

Every headline claim reproduced byte-exact from `claude_1`'s pinned store
(`a280b2fb…`): **15 missing rows** (2021:4 · 2022:5 · 2023:2 · 2024:0 ·
2025:4), 2024 complete at 55/55, 11 Phase-1B entries, slice name-scan 0 flags,
rank fields 0/300. Two record corrections for you:

1. **HANDOFF-06 EXISTS** — `hand_offs/director/HANDOFF-06-2026-08-19-AUD1-CINCINNATI-WTA-AUDIT.md`
   on the Director branch `arena/01a01588-the-creation-2` @ commit `7839841`.
   Your "absent from all branches" was stale refs. Pull it and reconcile your
   Step-0 reconstruction against it.
2. Your branch's force-reset event (chain of custody, `b403312…`) is noted on
   the Board. The Director branch is intact.

## Fix order (T-007) — exactly this

**Target:** the 15 missing Cincinnati WTA rows, 2021–2025, one year at a time
in your checkpoint sequence (2021 already evidenced → 2022 → 2023 → 2025 →
2024 certification in the close-out).

**Per missing row — the only acceptable dispositions:**
- **FIXED** — row built with: full player names (Rule 1) · verified opponent +
  score + round + date from a **named, checkable source** recorded in that
  row's per-row `provenance` (Rule 3) · schema fields only (Rule 4 — no rank
  fields) · score digits exactly as the source gives them.
- **OPEN** — source cannot supply a required fact (e.g. Pegula–Halep: no
  completed-set digits anywhere). The row stays absent, the gap stays
  documented with the best evidence you have. **Never invent a digit.**
  Rule 3 wins over completeness.

**Known starting points (from your verified report):**
- 2021: Ostapenko d. Brady 6-7(2) 5-4 ret. · Bencic d. Muchova 7-5 2-1 ret. ·
  Pegula d. Halep (digits hunt; else OPEN) · Rogers' R64 (opponent + score).
- 2022: 4×R32 (Riske-Amritraj, Sabalenka, Rogers, V. Kudermetova) + 1×R64
  (N2 — identify the invisible winner from the source; no name asserted without it).
- 2023: 2×R16 (Paolini, Jabeur opponents).
- 2025: 2×R64 + 2×R32 (Gauff, Swiatek) — confirm the 96-draw per Rule 2 from an
  edition-specific source as part of the fix record.

**After each year's fixes (DATA-RULES Rules 2/5/6 — your branch's editions
workspace):** round-transition gap check green before `closed_verified_gapless`;
manifest `match_count` + `checksum_sha256` updated in the same change; `build.py`
green; summaries regenerated via `generate_summaries.py` — both in order, same change.

## Location of fixes

Your branch `arena/01a015bb-the-creation-2` (the only branch you can push).
Build the fixed Cincinnati editions in your `data/tennis/editions/` workspace
per DATA-RULES. Migration into `claude_1` is Director/Admin side — flag it in
your delivery; do not block on it.

## Out of scope (queued, not forgotten)

- ~~`J.J. Wolf` Rule-1 flag (AO 2024 row — outside the WTA Cincinnati slice):
  queued for a separate Admin ruling.~~ **AMENDED — see Amendment 1: name fixes
  are IN scope per Admin.**
- Anything outside Cincinnati WTA 1000, 2021–2025 (except as Amendment 1 specifies).

## Deliverable

- Consolidated fix report `CINCINNATI_WTA_FIX_REPORT_2021-2025.md` on your
  branch + presentation to the Director in this control loop.
- Per-gap final disposition table: FIXED (row + source cited) / OPEN (reason +
  evidence) — all 15 must end with a disposition.
- Build/manifest/summaries verification output in the report.
- **Sign-off: Role + Branch ID.**

Director will independently re-verify every added row from bytes plus at
least one external re-check per year (Rule 7).

---

**Sign-off — Role: Director 1 · Branch ID: `arena/01a01588-the-creation-2`**

---

## AMENDMENT 1 (2026-08-19, Admin clarification)

**Admin:** "this is the auditors branch [arena/01a015bb-the-creation-2] and
that's where pull files from Claude_1 will be fixed. J.J is not out of scope
as there's a doc requiring proper name fixes."

**A1.1 — Fix location confirmed.** The fix workspace IS your branch
`arena/01a015bb-the-creation-2`. Flow: **pull the source files from `claude_1`
→ fix them in your `data/tennis/editions/` workspace** per DATA-RULES. The
HANDOFF-07 "Location of fixes" section stands as written; this amendment makes
the pull-from-claude_1 flow explicit.

**A1.2 — Name fixes are IN scope (Rule 1).** The `J.J. Wolf` initials violate
DATA-RULES Rule 1. Execute:

1. **Adjudicate the canonical table entry first** — `player_canonical_names.json`
   on your branch (and in the claude_1 pull) currently holds
   `canonical_full_name: "J.J. Wolf"` (`differs: true` vs store's "J J Wolf").
   The table's canonical field itself violates Rule 1 and must be corrected as
   part of this work. Resolve the full name from an official/checkable source
   (ATP player bio, Wikipedia, or ITF profile — Rule 1's allowed references;
   the full legal name is expected to be "Jeffrey John Wolf" — **do not write
   it unsourced**). Record the source in the table entry's evidence fields and
   update `canonical_full_name` + `store_v3_spelling`-reconciliation consistently.
2. **Apply to the pulled Cincinnati files** — the name appears in 2 rows of the
   Cincinnati pulls: `Cincinnati Masters` 2022 R64 (Ruusuvuori v Wolf) and
   2023 R64 (de Minaur v Wolf), both ATP-side. Fix the player name in those
   rows, same adjudicated spelling, same source cited in per-row provenance.
3. **Scan every pulled file for further Rule-1 violations** (initial-pattern
   scan). Legitimate particles are NOT violations and must not be "fixed" —
   e.g. `Christopher O'Connell` is a false positive of naive initial-scans
   (Rule 1 explicitly protects particles; "O'" is one).
4. **Census (Director byte-verified, claude_1 store):** `J.J. Wolf` appears in
   ~58 further rows store-wide (33 tournament-editions) beyond the 2 Cincinnati
   rows; the canonical table entry affects all of them. Those rows are
   **queued, not forgotten**: fix them in this task only if they fall inside
   files you pull; otherwise list them in your report's queued section for a
   follow-up sweep (the Director will order it if Admin wants the full-store
   sweep now).

**A1.3 — Disposition rule unchanged.** FIXED = sourced full name written;
OPEN = source not found, gap documented. Never write an unsourced name.
