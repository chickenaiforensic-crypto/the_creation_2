# HANDOFF-08 — Auditor 1 — Cincinnati Masters (ATP, M1000): close all gaps and fix all issues, present in the approved uniform way

| Field | Value |
|---|---|
| **Handoff No** | **08** (absolute order) |
| **Task ID** | `T-008` |
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

> so for this **Cincinnati Masters (ATP, M1000)** they should close all gaps
> known and issues and present it in the newly approved way

> Uniformity is approved - next audit - both known gaps and a verification of
> system accuracy and share report of the current issues

## Context — your REPLY-12 is Director-verified where claimed

- 25 editions / 948 rows, zero drift, zero defects — accepted.
- The 11 claude_1 ATP Cincinnati gap instances **reproduce byte-exact**
  (2022×1 Sinner · 2023×4 Popyrin, Djokovic, Mannarino, Fritz · 2024×2
  Cobolli, Sinner · 2025×4 Auger-Aliassime, Nardi, Zverev, Rune).
- Census-derived Director expectation (verify from bytes, do not assume):
  56-draw 2021–2024 → 55 matches each; 96-draw 2025 → 95. claude_1 holds
  55/54/50/53/88 → short by **0/1/5/2/7 = 15 total**, i.e. **4 gaps beyond
  the known 11** (expected at the R64/R128 layer: 2023 +1, 2025 +3 — the
  layer Phase-1B excludes). The full-census extension that found N1/N2 in
  the WTA pass is how you find them.

## Task (T-008)

**1. Pull the 5 ATP editions** from `claude_1` (pinned store `a280b2fb…`) into
your workspace as `editions/Cincinnati_Masters/{2021..2025}.json` +
`summaries/` + `README.md` (folder name `Cincinnati_Masters` — the WTA folder
`editions/Cincinnati/` is taken). On import apply, per DATA-RULES:
- Rule 4: drop `rankA`/`rankB` if present.
- Marker policy (T-003 D3): score strings carry no `RET`/`Def.`/`DEF` tokens —
  strip with set digits byte-preserved (the claude_1 Cincy 2025 final row
  carries `5-0 RET`).
- Row schema exactly as the existing edition files.

**2. Draw sizes, edition-specifically confirmed** (Rule 2): expected 56/56/56/56/96
per Phase-1A — confirm each year for the **ATP** edition from an edition-specific
source (Wikipedia edition page / ATP draws archive), recorded in the manifest
`source` field.

**3. Close ALL gaps** — the known 11 plus every census-derived gap the
full-draw check reveals (target: 55/55/55/55/95 matches per year). Per gap,
the only dispositions:
- **FIXED** — row added with named checkable source, per-row `provenance`,
  real score digits, correct round/date.
- **OPEN** — source cannot supply a required fact; row stays absent,
  documented. **Rule 3 wins over completeness. Never invent.**
- Retirement/walkover pattern expected (WTA pass found 8 ret + 7 WO) — confirm
  each against its own source, don't pattern-match as evidence.

**4. Fix all issues in the pulled slice:**
- **Rule 1:** `J.J. Wolf` appears in Cincinnati Masters 2022 R64
  (Ruusuvuori v Wolf) and 2023 R64 (de Minaur v Wolf). Fix to **Jeffrey Wolf**
  per the branch's own precedent (`ddb6019`, ATP Tour + Wikipedia), source
  recorded in per-row provenance. Scan the full pull for any other Rule-1
  flags (particles protected).
- Score arithmetic vs `setsA/setsB/gamesA/gamesB`; status↔flag coherence;
  duplicates/self-play; date windows; winner=="A". Handle the tied-unfinished
  retirement-set parser artifact per your REPLY-12 ruling (correct data, not
  defects — disclose each).

**5. Governance outputs, same change as the data (Rule 5/6 + T-005 precedent):**
- `MANIFEST.json`: +5 entries — tournament `"Cincinnati Masters"`, tour `"ATP"`,
  tier `"M1000"`, per-year `draw_size`, `source`, `match_count`,
  `checksum_sha256`, `file_path`, `gap_count: 0`, `status:
  closed_verified_gapless` **only after** the R32→F gap check passes (Rule 2).
- `gap_report.json`: every closed gap gets `status: closed` + `resolution`
  naming the source and what was found (T-005 format).
- `build.py` green; `generate_summaries.py` green (run both, in order); zero
  manifest↔file drift.

**6. Present in the newly approved uniform way:**
- `editions/Cincinnati_Masters/README.md` = the approved 3-part format
  (title line · one-line tour/tier/editions · manifest pointer only — no
  tables, no narrative), identical in structure to the other five folders.
- Consolidated report `hand_offs/auditor/REPLY-13-2026-08-19-AUD1.md` on your
  branch + control-loop presentation: clean blocks, per-gap disposition table,
  verification output, Rule-1 ledger, open items. **Sign-off: Role + Branch ID.**

## Explicitly NOT in this task

- **Cincinnati ATP 2026** — live event (13–23 Aug), absent from all branches.
  Do NOT pull it. Queued: after 23 Aug, pull with in-progress status only.
- Cincinnati WTA 2026 (same live-event rule — stays STOPPED per your register).
- The Wolf sweep across claude_1's remaining ~58 rows (outside this pull) —
  queued; note the count in your report.
- Migration of your branch's editions into `claude_1` — Director/Admin side.

## Acceptance

Every claim in REPLY-13 must survive: build.py clean · manifest checksums
reproduce from bytes · 0 ghosts on all 5 ATP editions · Rule-1 scan clean on
the pull · every added row's source independently re-openable. Director will
re-verify from bytes plus at least one external re-check per year (Rule 7).

---

**Sign-off — Role: Director 1 · Branch ID: `arena/01a01588-the-creation-2`**
