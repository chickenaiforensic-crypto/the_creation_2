# Director's Board — the_creation_2

**Committed to the repo under `hand_offs/director/`** (Handoff Isolation
Rule — the director's folder is included). Registry of hand-offs in
absolute order. Protocol: `hand_offs/PROTOCOL.md` · Rules:
`hand_offs/README.md`.

## Absolute order registry

| No | Task | To | Date | Status | Hand-off / Reply |
|---|---|---|---|---|---|
| 01 | T-001 · Data category index (tennis tournaments, football competitions) | Auditor 1 | 2026-08-18 | ✅ **Completed & Director-verified** — REPLY-01 @ `ecf6c6a`; digests + row/tier counts reproduced from bytes. ⚠️ **Monitor-flagged (verified):** REPLY-01 headers "34 ATP / 30 WTA" were wrong (bytes: 33 ATP even pre-sweep; post-T-003 33/31, ATP rows 9,420) — doc fix assigned via HANDOFF-04 | `hand_offs/director/HANDOFF-01-2026-08-18-AUD1-DATA-INDEX.md` → `hand_offs/auditor/REPLY-01-2026-08-18-AUD1.md` |
| 02 | T-002 · Tennis accuracy audit — one tournament type at a time; US Open year-by-year; auditing plan first | Auditor 1 | 2026-08-18 | ✅ **COMPLETED & Director-verified — T-002 CLOSED.** 305 editions / 17,285 rows across all 5 types; zero arithmetic defects; zero verified result discrepancies; pinned §3/§4/§6 reproduced byte-exact; new classes M-1 (0 WO non-GS), M-2 (205 spine absent), F-1 Adelaide merge, F-2 Dubai 2026 title, F-3, F-4 (48 season-start rows), O-1/O-2/O-3/O-5/D-NEW-1; 2 errata accepted; LE def resolved. Sweep recommendations queued (PA-04) awaiting Director's one-sweep order | `hand_offs/director/HANDOFF-02-2026-08-18-AUD1-TENNIS-AUDIT.md` → replies 02–08 |
| 03 | T-003 · Tennis remediation sweep — fix the audited errors on the repo (Director's one-sweep order, tennis part) | **ENGINEER 5** → executed by AUDITOR 1 (acting engineer) | 2026-08-18 | ✅ **COMPLETED & Director-verified** (+ independent monitor corroboration: zero falsehoods in execution). Store `ad0b261d…` → **`fa273ca4…` (17,286 rows)**; D1–D5 verified from bytes; integrated onto Director branch. Monitor also flagged 5 doc-level items — **all 5 verified and closed**: Director branch fixed directly (relay "LOCALLY" struck ×5 copies, KNOWN-GAPS §3 T-003 note, §9 recomputed 45/82 + 208, auditor README complete); auditor-branch items (REPLY-01 headers, REPLY-02 C3, their README) → HANDOFF-04 | `hand_offs/director/HANDOFF-03-2026-08-18-TENNIS-REMEDIATION.md` → `hand_offs/engineer/REPLY-03-2026-08-18.md` |
| 04 | T-004 · Doc errata on the Auditor's branch (REPLY-01 headers 33/31 + 9,420, REPLY-02 C3 wording, auditor README) | Auditor 1 | 2026-08-18 | 📨 Relayed | `hand_offs/director/HANDOFF-04-2026-08-18-AUD1-DOC-ERRATA.md` → `hand_offs/auditor/REPLY-04-…` |

**Next hand-off number: 05.** Never reused, never renumbered.

## Director actions log

| Date | Action | Commit |
|---|---|---|
| 2026-08-18 | **Old-team identity scrub** across tennis data (Director order): table `fetched_by`×190/`verified_by`×17/`repaired_by`×1 neutralized; store `capture_agent`×134 neutralized; AIRP-AUD3/AIRP-ENG3/AUD3/ENG3 citations and Engineer/Auditor-3 attributions removed (facts, dates, branch IDs, program names preserved). **Store digest changed `9b271a35…` → `ad0b261d…`**; table digest re-pinned; MANIFEST/PIN/KNOWN-GAPS/GS134 card all re-pinned and verified consistent | `9799e97` |
| 2026-08-18 | **Consolidated all-known-gaps document created** (tennis pinned §1–§8 + new D-NEW-1/O-1/O-2 + T-001 flag + football F-1–F-4; Director-verified from bytes). **Held LOCAL per Director order — NOT committed** (`hand_offs/director/ALL-KNOWN-GAPS-AUDITOR-2026-08-18-LOCAL.md`, untracked) | — |
| 2026-08-18 | **Independent monitor report received; every claim Director-verified from bytes; all 5 doc-level flags closed.** Director-branch fixes: relay sign-off "…HANDOFFS LOCALLY." → "…HANDOFFS." in all 5 copies (the word contradicted the repo-sharing rule; v2 correction completed); KNOWN-GAPS §3 T-003 status-mix note (28/0/4); §9 spine recomputed post-sweep (500s 45/82, 54 absent; total 208 = 103+54+51); auditor README lists all handoffs. Auditor-branch items routed as HANDOFF-04 | (this commit) |

## Standing orders (from Director)

1. Every hand-off contains the fixed relay message verbatim and a global sequence number.
2. All hand-offs are committed to the repo under `hand_offs/` (Handoff Isolation Rule — the director's folder is included).
3. **Hand-offs issued by the Director live in `hand_offs/director/`. Team members' replies and outputs live in their own role folder.**
4. Outside `hand_offs/`, the branch receives code work only, and only on the Director's order.
5. Every relay message, summary, and hand-off carries Role + Branch ID — onscreen relays included.
6. **Data freeze until verified:** no data information is used to update the system or documentation until the accuracy audits verify it. After verification, the Director orders one sweep: update system, documentation, and all other fixes. Audit findings are recorded, never fixed in-flight.

## Queued — post-audit sweep (no handoff number until the Director orders it)

| ID | Item | Source | Status |
|---|---|---|---|
| PA-01 | Update system + documentation with verified data; fix everything else found by the audits | Director 2026-08-18 | ⏸ Parked until audits verify accuracy |
| PA-02 | Correct stale tennis figures in `data/README.md` (17,151/`06ceabb6…` → current) | T-001 flag (Auditor 1, Director-confirmed) | ⏸ Parked — untouched until post-audit sweep |
| PA-03 | KNOWN-GAPS §6 wording review: `13-12(2)` at Wimbledon 2021 is format-consistent (12-12 final-set TB era 2019–2021); data needs no change, register wording does | O-flag from Auditor 1 (GS close-out), Director-confirmed | ⏸ Parked — untouched until post-audit sweep |
| PA-04 | Tennis sweep (post-T-002, Auditor's recommendations, not executed): document M-1/M-2 in KNOWN-GAPS · split Adelaide 2023 edition · non-GS walkover policy · §6 wording + 9 AO §4 rows review · marker conventions (O-1/D-NEW-1/F-3) · refresh `data/README.md` tennis figures | T-002 close-out (Auditor 1), Director-verified | ⏸ Parked — awaiting Director's one-sweep order |
