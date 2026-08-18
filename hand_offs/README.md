# Hand-offs — README

**All hand-offs are shared in the repository under `hand_offs/` — every
role, including the director's folder (`hand_offs/director/`).**
Outside `hand_offs/`, the branch receives code work only, and only when
the Director asks.

## Hand-off numbering — ABSOLUTE ORDER

Every hand-off carries a global sequence number: **01, 02, 03, …** —
issued by the Director, never reused, never renumbered. The running
registry is `hand_offs/director/BOARD.md`.

| Rule | Detail |
|---|---|
| Number | Global and absolute: `HANDOFF-01-…`, `HANDOFF-02-…`, … |
| Replies | Same absolute sequence: `REPLY-01-…`, `REPLY-02-…`, … |
| Registry | `hand_offs/director/BOARD.md` tracks who, when, status |
| Embed | Every hand-off contains the fixed relay message, verbatim |
| Sign-off | **Every relay, summary, and hand-off — including onscreen relay messages — carries Role + Branch ID** of the issuer |
| Location | Hand-offs **issued by the Director** live in `hand_offs/director/` (with the board). Each team member's own replies and outputs live in **their role folder** (e.g. `hand_offs/auditor/REPLY-01-…`). All of it is committed to the repo |

## Fixed relay message

Every hand-off must contain the following block verbatim (canonical copy:
`hand_offs/PROTOCOL.md`):

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

## Layout

```text
hand_offs/
├── README.md               this file — rules every agent must follow
├── PROTOCOL.md             canonical fixed relay message
├── director/
│   ├── BOARD.md            absolute-order registry + task status
│   └── HANDOFF-01-…        hand-offs issued BY the Director
├── auditor/                Auditor's own replies and outputs (REPLY-01-…)
├── engineer/               Engineer's own replies and outputs
└── others/                 Others' own replies and outputs
```

All of the above is committed to the repo, including `hand_offs/director/`.
A hand-off goes in the folder of the person who **wrote** it: the
Director's hand-offs sit in `hand_offs/director/`, team members' replies
sit in their own role folder.
