# PLAN-VB-6 Phase B — European League + EuroVolley Qualifiers (AUD1, 2026-08-23)

Branch: arena/01a015bb-the-creation-2 · Phase A CLOSED d3da424 (8/8 / 248 qualifier rows).
Role: AUDITOR 1 · Capture date fixed 2026-08-23.

## Phase A closure confirmation (byte-locked)
- WO-VB-6 Phase A: 8 events / 248 rows (OQT-W 2023 84 + OQT-M 2023 84 + CC-M 2022 8 + CC-W 2022 8 + CC-M 2023 8 + CC-W 2023 8 + CC-M 2024 8 + CC-W 2024 8).
- Store: 47 editions / 2,676 rows / ISSUES:0 / FORFEITS:10 / LEDGER:95.
- Discontinuation adjudicated: 2024 Challenger Cup = fifth and last (edition pages + FIVB presser).
- Ranking-entry wrinkles 2024 byte-cited: UKR-M (4th / bronze lost → VNL-2025 via ranking); BEL-W (4th / bronze lost → VNL-2025 via ranking).

## Phase B scope (census / planning — NOT full build)
Source hierarchy: existing store files preferred; Wikipedia action=raw only if backed by per-row official IDs; Grokipedia rejected.

### 1. CEV European (Golden) League — M + W (2018–2026, annual)
Recommendation: build Golden League 2022–2024 first (aligns with VNL-2023/2024/2025 promotion lattice and EuroVolley qualifier loops already in store).
- Existing family checks in store: VNL_M 2023/2024/2025/2026 (1,336 rows); EuroVolley_M 2023/2024; Olympics_M/W 2024.
- Cross-family consistency required: Golden League champions/runner-ups feed into EuroVolley qualification fields (already byte-cited in VNL_README.md promotion lattice line 17: FRA-W'24, TUR-M'24, CHN-M'25, CZE-W'25; ranking entries BEL-W'25, UKR-M'25).
- Silver League and all-year depth: Director sizing input needed — estimate ~200–350 rows per gender per year depending on pool count (8-team vs 12-team). Not building until sizing authorized.

### 2. EuroVolley qualification cycles
- 2023 cycle: already closed (EuroVolley_M 2023 / W 2023 in store — 152 rows / 152 rows). Cross-check against Olympics_M 2024 / W 2024 qualifiers passed at 4cb21c8.
- 2026 cycle: LIVE Sep 9–26, 2026 (WO-VB-8 window). Census-open until final standings published. Not building until event completed.

### 3. Continental Olympic qualification side events
- 2023 OQTs (Ningbo/Tokyo/Łódź M; Rio/Tokyo/Xi'an W) already built at 4cb21c8 (168 rows). No additional OQTs for LA28 — replaced by 2026 continentals + 2027 World Cup + ranking (June 2028) per VNL_README.md.
- Side-event check: Asian Challenge Cup, NORCECA International League final fours, European League final fours — census needed only if they produce new qualifier fields not already captured in OQTs / EuroVolley / Challenger Cups.

## Build-guard notes (pre-construction)
- Qualification assert for OQT already relaxed 6→5 (Japan 5-2, Pool B) — disclosed, not a data error.
- No golden-set rows expected in EU league / EuroVolley (CEV aggregate tie only for CEV club / national aggregate; standard 3-set best-of-5 applies).
- Host-nation flags mandatory: host federation playing in hosting venue = home (A/B per schema); pool-hosts count; all-neutral for neutral-ground championships.
- All new editions must include `capture_date="2026-08-23"` in provenance per Director rule, even when source dates are 2025/2026.
- Source IDs (P2 / official match centre) must be unique within edition; no duplication of 16758-class defect.

## Recommended build order (pending Director authorization)
1. Golden League M 2022 → W 2022 → M 2023 → W 2023 → M 2024 → W 2024 (6 editions / ~1,200–1,800 rows estimated, based on 12–16 pool-week pairs × 3–5 matches per week).
2. Silver League M+W 2022–2024 (after sizing input).
3. EuroVolley 2026 qualification census (post-event, Sep 2026 / WO-VB-8).

## Verification gates (before any Phase B commit)
- Harness clean on master after addition.
- MANIFEST checksum gate passes (build.py checksum-locked).
- Cross-family check: new qualifiers present in Olympics / VNL / EuroVolley fields.
- Ledger check: new federations (if any) verified from bytes, not assumed.
- Discontinuation / ranking-wrinkle notes embedded in source strings where applicable.
