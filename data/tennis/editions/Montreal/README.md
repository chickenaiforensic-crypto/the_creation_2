# Montreal (WTA 1000, hard, Canada) — 2021, 2023, 2025

WTA half of the Canadian Open in its Montreal years. **City alternation: the WTA plays Montreal in odd years (2021/2023/2025) and Toronto in even years (2022/2024) — the reverse of the ATP.** Store tournament names are kept per-edition as stored (`Montreal` / `Toronto`); the Toronto years live in `editions/Toronto/`.

Three editions pulled from the claude_1 pinned store (md5 `a280b2fb56e64f64724473e767d90485`) and gap-fixed under T-034b (2026-08-19, Auditor 1, pre-audit → work → post-audit cycle). Canada WTA gaps CA001–CA016 span both folders: 16 total = 12 retirements + 4 walkovers (this folder: 8).

## Draw-size adjudication — 2021
The n=50 pull (R64:21, 11 entries-at-R32) raised a COVID-special suspicion pre-audit. **TE bracket bytes prove a standard 56-draw with exactly 8 seed byes** (Sabalenka, Andreescu, Svitolina, Pliskova, Muguruza, Halep, Kvitova, Azarenka). All 3 missing R64s were retirements won by exactly the 3 non-bye ghost entrants (Sakkari, Anisimova, Konta) — true deficit 5, no special template needed (contrast: Toronto ATP 2021 was a genuine 64/16-bye COVID draw).

## Era mix (byte-asserted)
- 2021, 2023: 56-draw / 8 byes (55 matches, template 24/16/8/4/2/1)
- 2025: 96-draw / 32 byes (95 matches, template 32/32/16/8/4/2/1)

## Fixes in this folder
| Gap | Year | Round | Result |
|-----|------|-------|--------|
| CA001 | 2021 | R64 | Sakkari d. Bouzkova 6-4 3-1 ret |
| CA002 | 2021 | R64 | Anisimova d. Martincova 6-1 4-3 ret |
| CA003 | 2021 | R64 | Konta d. Shuai Zhang 4-6 5-2 ret (Zhang won set 1 — truthful 1-1) |
| CA004 | 2021 | R32 | Gauff d. Potapova 5-0 ret |
| CA005 | 2021 | R16 | Gauff d. Konta W/O (left knee — Reuters/Sky/WTA Insider) |
| CA009 | 2023 | R32 | Stephens d. Azarenka W/O (warm-up re-injury, own statement; body part unspecified) |
| CA010 | 2023 | R32 | Paolini d. Keys W/O (hip per Keys' own post; WTA.com said glute — both kept) |
| CA016 | 2025 | R64 | Mirra Andreeva d. Andreescu W/O (left-ankle ligament tear on match point of her R128 win, own presser) |

## Highlights
- **Gauff double-chain 2021**: two consecutive rungs of one run (R32 ret + R16 W/O) were both missing and are restored.
- **CA003 verbatim wire lock**: Reuters 2021-08-13 — "Konta advanced from the opening round when China's Zhang Shuai retired with a leg injury."
- Pre-existing ret/wo rows in pulled slices (untouched, fidelity-preserved): 2021 R64 Ferro d. Tomljanovic 2-6 6-2 (tennisabstract path); 2025 QF Rybakina d. Kostyuk 6-1 2-1 (CSV path).

Status per edition: `closed_verified_gapless`.
