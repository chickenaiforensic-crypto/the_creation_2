# Director's Board — the_creation_2

**Committed to the repo under `hand_offs/director/`** (Handoff Isolation
Rule — the director's folder is included). Registry of hand-offs in
absolute order. Protocol: `hand_offs/PROTOCOL.md` · Rules:
`hand_offs/README.md`.

## Absolute order registry

| No | Task | To | Date | Status | Hand-off / Reply |
|---|---|---|---|---|---|
| 01 | T-001 · Data category index (tennis tournaments, football competitions) | Auditor 1 | 2026-08-18 | ✅ **Completed & Director-verified** — REPLY-01 @ `ecf6c6a` (branch `arena/01a015bb-the-creation-2`); digests + all headline counts reproduced from bytes | `hand_offs/director/HANDOFF-01-2026-08-18-AUD1-DATA-INDEX.md` → `hand_offs/auditor/REPLY-01-2026-08-18-AUD1.md` |
| 02 | T-002 · Tennis accuracy audit — one tournament type at a time; US Open year-by-year; auditing plan first | Auditor 1 | 2026-08-18 | 🔄 **In progress** — **GS CLOSED** (46/46 verified). **M1000 verified** (`50365bf`; LE def resolved: 161 exact). **500s delivered** (`bbf5eaf`): rows/editions/status byte-exact; F-1 Adelaide merge, F-2 Dubai 2026 title walkover (externally confirmed), F-3 §6-exact, F-4 Brisbane Dec dates; C15 exact. **One direct question out: counting rules for 44/81+51 absent, Adelaide "17", Brisbane "32"** (Director recomputes differ). Next after clarification: 250s → T-002 close-out ledger | `hand_offs/director/HANDOFF-02-2026-08-18-AUD1-TENNIS-AUDIT.md` → replies 02–07 |

**Next hand-off number: 03.** Never reused, never renumbered.

## Director actions log

| Date | Action | Commit |
|---|---|---|
| 2026-08-18 | **Old-team identity scrub** across tennis data (Director order): table `fetched_by`×190/`verified_by`×17/`repaired_by`×1 neutralized; store `capture_agent`×134 neutralized; AIRP-AUD3/AIRP-ENG3/AUD3/ENG3 citations and Engineer/Auditor-3 attributions removed (facts, dates, branch IDs, program names preserved). **Store digest changed `9b271a35…` → `ad0b261d…`**; table digest re-pinned; MANIFEST/PIN/KNOWN-GAPS/GS134 card all re-pinned and verified consistent | `9799e97` |
| 2026-08-18 | **Consolidated all-known-gaps document created** (tennis pinned §1–§8 + new D-NEW-1/O-1/O-2 + T-001 flag + football F-1–F-4; Director-verified from bytes). **Held LOCAL per Director order — NOT committed** (`hand_offs/director/ALL-KNOWN-GAPS-AUDITOR-2026-08-18-LOCAL.md`, untracked) | — |

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
