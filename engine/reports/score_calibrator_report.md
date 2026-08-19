# SCORE CALIBRATOR — Cincinnati Masters 2021–2025

Regional point-assignment layer: each year's raw Phase 0 ratings are analyzed from the top performer down to the last, density clusters are detected, and per-region supplemental points (isotonic/PAVA targets, min-adjustment threshold applied) are added so ratings reflect the leaderboard hierarchy. 2021 is the baseline; 2022–2025 follow.

| Year | Raw accuracy | Calibrated accuracy | Spearman raw | Spearman calibrated |
|---|---:|---:|---:|---:|
| 2021 | 94.89% | 94.98% | -0.8711 | -0.8715 |
| 2022 | 95.15% | 95.07% | -0.8763 | -0.8763 |
| 2023 | 95.03% | 95.22% | -0.8663 | -0.8677 |
| 2024 | 94.09% | 94.10% | -0.8476 | -0.8476 |
| 2025 | 91.82% | 91.85% | -0.8330 | -0.8330 |
| **Mean** | **94.20%** | **94.24%** | — | — |

Target accuracy: 90.00%. Method: regional_isotonic_pava. Accuracy = fraction of cross-region player pairs correctly ordered by rating; same-region and equal-rating pairs are not judged.

## 2021 — Cincinnati Masters

Matches: selected=55 rated=55 refused=0 players=56

### Distribution — regions (top performer down to last)

| Region (position) | Players | Mean raw rating | Min | Max | Std |
|---|---:|---:|---:|---:|---:|
| 1st | 1 | 62.00 | 62.0 | 62.0 | 0.00 |
| 2nd | 1 | 18.00 | 18.0 | 18.0 | 0.00 |
| 3rd | 2 | 31.00 | 22.0 | 40.0 | 9.00 |
| 5th | 4 | 12.50 | 6.0 | 20.0 | 5.17 |
| 9th | 8 | 8.75 | -6.0 | 20.0 | 7.41 |
| 17th | 16 | -1.25 | -8.0 | 8.0 | 5.09 |
| 33rd | 24 | -10.08 | -14.0 | -4.0 | 3.19 |

### Density clusters (rating gaps ≤ cluster_gap)

| Cluster | Players | Rating span | Members (first/last) |
|---|---:|---:|---|
| #1 | 37 | -14 .. 0 | Albert Ramos-Vinolas … Kevin Anderson (37 total) |
| #2 | 13 | 4 .. 14 | Benoit Paire … Marin Cilic (13 total) |
| #3 | 4 | 18 .. 22 | Stefanos Tsitsipas … Andrey Rublev (4 total) |

### Regional assignments (added points per region)

| Region | Mean raw | Target | Adjustment |
|---|---:|---:|---:|
| 1st | 62.00 | 62.00 | +0.00 |
| 2nd | 18.00 | 24.50 | +6.50 |
| 3rd | 31.00 | 24.50 | -6.50 |
| 5th | 12.50 | 12.50 | +0.00 |
| 9th | 8.75 | 8.75 | +0.00 |
| 17th | -1.25 | -1.25 | +0.00 |
| 33rd | -10.08 | -10.08 | +0.00 |

### Reflection accuracy

| Metric | Raw | Calibrated |
|---|---:|---:|
| Cross-region correctly-ordered pairs | 94.89% | 94.98% |
| Spearman (rating vs position) | -0.8711 | -0.8715 |

### Calibrated leaderboard (top 10 of 56) — rating = raw + region adjustment

| # | Player | Raw | Region adj | Calibrated | Position |
|---|---:|---:|---:|---:|---|
| 1 | Alexander Zverev | +62 | +0.00 | +62.00 | 1st |
| 2 | Daniil Medvedev | +40 | -6.50 | +33.50 | 3rd |
| 3 | Andrey Rublev | +18 | +6.50 | +24.50 | 2nd |
| 4 | Felix Auger-Aliassime | +20 | +0.00 | +20.00 | 5th |
| 5 | Lorenzo Sonego | +20 | +0.00 | +20.00 | 9th |
| 6 | Stefanos Tsitsipas | +22 | -6.50 | +15.50 | 3rd |
| 7 | Benoit Paire | +14 | +0.00 | +14.00 | 5th |
| 8 | Gael Monfils | +14 | +0.00 | +14.00 | 9th |
| 9 | Grigor Dimitrov | +12 | +0.00 | +12.00 | 9th |
| 10 | Guido Pella | +12 | +0.00 | +12.00 | 9th |

## 2022 — Cincinnati Masters

Matches: selected=55 rated=54 refused=1 players=56

### Distribution — regions (top performer down to last)

| Region (position) | Players | Mean raw rating | Min | Max | Std |
|---|---:|---:|---:|---:|---:|
| 1st | 1 | 70.00 | 70.0 | 70.0 | 0.00 |
| 2nd | 1 | 22.00 | 22.0 | 22.0 | 0.00 |
| 3rd | 2 | 26.00 | 22.0 | 30.0 | 4.00 |
| 5th | 4 | 17.00 | 8.0 | 26.0 | 7.28 |
| 9th | 8 | 4.75 | 0.0 | 16.0 | 4.79 |
| 17th | 16 | 0.00 | -12.0 | 8.0 | 5.43 |
| 33rd | 24 | -10.42 | -16.0 | -4.0 | 3.70 |

### Density clusters (rating gaps ≤ cluster_gap)

| Cluster | Players | Rating span | Members (first/last) |
|---|---:|---:|---|
| #1 | 33 | -8 .. 8 | Emil Ruusuvuori … Maxime Cressy (33 total) |
| #2 | 15 | -16 .. -12 | Alejandro Davidovich Fokina … Sebastian Baez (15 total) |
| #3 | 3 | 22 .. 22 | Cameron Norrie … Stefanos Tsitsipas (3 total) |

### Regional assignments (added points per region)

| Region | Mean raw | Target | Adjustment |
|---|---:|---:|---:|
| 1st | 70.00 | 70.00 | +0.00 |
| 2nd | 22.00 | 24.00 | +2.00 |
| 3rd | 26.00 | 24.00 | -2.00 |
| 5th | 17.00 | 17.00 | +0.00 |
| 9th | 4.75 | 4.75 | +0.00 |
| 17th | 0.00 | 0.00 | +0.00 |
| 33rd | -10.42 | -10.42 | +0.00 |

### Reflection accuracy

| Metric | Raw | Calibrated |
|---|---:|---:|
| Cross-region correctly-ordered pairs | 95.15% | 95.07% |
| Spearman (rating vs position) | -0.8763 | -0.8763 |

### Calibrated leaderboard (top 10 of 56) — rating = raw + region adjustment

| # | Player | Raw | Region adj | Calibrated | Position |
|---|---:|---:|---:|---:|---|
| 1 | Borna Coric | +70 | +0.00 | +70.00 | 1st |
| 2 | Daniil Medvedev | +30 | -2.00 | +28.00 | 3rd |
| 3 | Taylor Fritz | +26 | +0.00 | +26.00 | 5th |
| 4 | Stefanos Tsitsipas | +22 | +2.00 | +24.00 | 2nd |
| 5 | Carlos Alcaraz | +22 | +0.00 | +22.00 | 5th |
| 6 | Cameron Norrie | +22 | -2.00 | +20.00 | 3rd |
| 7 | Sebastian Korda | +16 | +0.00 | +16.00 | 9th |
| 8 | John Isner | +12 | +0.00 | +12.00 | 5th |
| 9 | Emil Ruusuvuori | +8 | +0.00 | +8.00 | 17th |
| 10 | Felix Auger-Aliassime | +8 | +0.00 | +8.00 | 5th |

## 2023 — Cincinnati Masters

Matches: selected=55 rated=50 refused=5 players=56

### Distribution — regions (top performer down to last)

| Region (position) | Players | Mean raw rating | Min | Max | Std |
|---|---:|---:|---:|---:|---:|
| 1st | 1 | 46.00 | 46.0 | 46.0 | 0.00 |
| 2nd | 1 | 16.00 | 16.0 | 16.0 | 0.00 |
| 3rd | 2 | 35.00 | 34.0 | 36.0 | 1.00 |
| 5th | 4 | 11.50 | -2.0 | 26.0 | 9.94 |
| 9th | 8 | 11.00 | 0.0 | 24.0 | 7.87 |
| 17th | 16 | -1.62 | -12.0 | 12.0 | 6.09 |
| 33rd | 24 | -10.00 | -16.0 | -6.0 | 3.27 |

### Density clusters (rating gaps ≤ cluster_gap)

| Cluster | Players | Rating span | Members (first/last) |
|---|---:|---:|---|
| #1 | 38 | -16 .. 0 | Holger Rune … Grigor Dimitrov (38 total) |
| #2 | 12 | 4 .. 16 | Carlos Alcaraz … Stan Wawrinka (12 total) |
| #3 | 2 | 34 .. 36 | Alexander Zverev … Hubert Hurkacz (2 total) |
| #4 | 2 | 24 .. 26 | Max Purcell … Dusan Lajovic (2 total) |

### Regional assignments (added points per region)

| Region | Mean raw | Target | Adjustment |
|---|---:|---:|---:|
| 1st | 46.00 | 46.00 | +0.00 |
| 2nd | 16.00 | 25.50 | +9.50 |
| 3rd | 35.00 | 25.50 | -9.50 |
| 5th | 11.50 | 11.50 | +0.00 |
| 9th | 11.00 | 11.00 | +0.00 |
| 17th | -1.62 | -1.62 | +0.00 |
| 33rd | -10.00 | -10.00 | +0.00 |

### Reflection accuracy

| Metric | Raw | Calibrated |
|---|---:|---:|
| Cross-region correctly-ordered pairs | 95.03% | 95.22% |
| Spearman (rating vs position) | -0.8663 | -0.8677 |

### Calibrated leaderboard (top 10 of 56) — rating = raw + region adjustment

| # | Player | Raw | Region adj | Calibrated | Position |
|---|---:|---:|---:|---:|---|
| 1 | Novak Djokovic | +46 | +0.00 | +46.00 | 1st |
| 2 | Alexander Zverev | +36 | -9.50 | +26.50 | 3rd |
| 3 | Max Purcell | +26 | +0.00 | +26.00 | 5th |
| 4 | Carlos Alcaraz | +16 | +9.50 | +25.50 | 2nd |
| 5 | Hubert Hurkacz | +34 | -9.50 | +24.50 | 3rd |
| 6 | Dusan Lajovic | +24 | +0.00 | +24.00 | 9th |
| 7 | Tommy Paul | +20 | +0.00 | +20.00 | 9th |
| 8 | Emil Ruusuvuori | +14 | +0.00 | +14.00 | 9th |
| 9 | Mackenzie McDonald | +14 | +0.00 | +14.00 | 9th |
| 10 | Alejandro Davidovich Fokina | +12 | +0.00 | +12.00 | 17th |

## 2024 — Cincinnati Masters

Matches: selected=55 rated=52 refused=3 players=56

### Distribution — regions (top performer down to last)

| Region (position) | Players | Mean raw rating | Min | Max | Std |
|---|---:|---:|---:|---:|---:|
| 1st | 1 | 38.00 | 38.0 | 38.0 | 0.00 |
| 2nd | 1 | 26.00 | 26.0 | 26.0 | 0.00 |
| 3rd | 2 | 28.00 | 26.0 | 30.0 | 2.00 |
| 5th | 4 | 16.00 | 4.0 | 24.0 | 7.48 |
| 9th | 8 | 12.00 | 0.0 | 22.0 | 7.48 |
| 17th | 16 | -2.50 | -14.0 | 12.0 | 6.26 |
| 33rd | 24 | -10.00 | -14.0 | -6.0 | 3.06 |

### Density clusters (rating gaps ≤ cluster_gap)

| Cluster | Players | Rating span | Members (first/last) |
|---|---:|---:|---|
| #1 | 43 | -14 .. 6 | Fabian Marozsan … Sebastian Korda (43 total) |
| #2 | 11 | 12 .. 26 | Alexander Zverev … Luciano Darderi (11 total) |

### Regional assignments (added points per region)

| Region | Mean raw | Target | Adjustment |
|---|---:|---:|---:|
| 1st | 38.00 | 38.00 | +0.00 |
| 2nd | 26.00 | 27.00 | +1.00 |
| 3rd | 28.00 | 27.00 | -1.00 |
| 5th | 16.00 | 16.00 | +0.00 |
| 9th | 12.00 | 12.00 | +0.00 |
| 17th | -2.50 | -2.50 | +0.00 |
| 33rd | -10.00 | -10.00 | +0.00 |

### Reflection accuracy

| Metric | Raw | Calibrated |
|---|---:|---:|
| Cross-region correctly-ordered pairs | 94.09% | 94.10% |
| Spearman (rating vs position) | -0.8476 | -0.8476 |

### Calibrated leaderboard (top 10 of 56) — rating = raw + region adjustment

| # | Player | Raw | Region adj | Calibrated | Position |
|---|---:|---:|---:|---:|---|
| 1 | Jannik Sinner | +38 | +0.00 | +38.00 | 1st |
| 2 | Holger Rune | +30 | -1.00 | +29.00 | 3rd |
| 3 | Frances Tiafoe | +26 | +1.00 | +27.00 | 2nd |
| 4 | Alexander Zverev | +26 | -1.00 | +25.00 | 3rd |
| 5 | Ben Shelton | +24 | +0.00 | +24.00 | 5th |
| 6 | Felix Auger-Aliassime | +22 | +0.00 | +22.00 | 9th |
| 7 | Andrey Rublev | +20 | +0.00 | +20.00 | 5th |
| 8 | Jordan Thompson | +20 | +0.00 | +20.00 | 9th |
| 9 | Jiri Lehecka | +18 | +0.00 | +18.00 | 9th |
| 10 | Hubert Hurkacz | +16 | +0.00 | +16.00 | 5th |

## 2025 — Cincinnati Masters

Matches: selected=95 rated=87 refused=8 players=96

### Distribution — regions (top performer down to last)

| Region (position) | Players | Mean raw rating | Min | Max | Std |
|---|---:|---:|---:|---:|---:|
| 1st | 1 | 50.00 | 50.0 | 50.0 | 0.00 |
| 2nd | 1 | 72.00 | 72.0 | 72.0 | 0.00 |
| 3rd | 2 | 34.00 | 28.0 | 40.0 | 6.00 |
| 5th | 4 | 13.50 | 8.0 | 26.0 | 7.26 |
| 9th | 8 | 13.75 | 4.0 | 24.0 | 8.51 |
| 17th | 16 | 6.12 | -6.0 | 20.0 | 8.17 |
| 33rd | 32 | -3.31 | -14.0 | 12.0 | 6.24 |
| 65th | 32 | -10.81 | -16.0 | -4.0 | 3.12 |

### Density clusters (rating gaps ≤ cluster_gap)

| Cluster | Players | Rating span | Members (first/last) |
|---|---:|---:|---|
| #1 | 58 | -8 .. 14 | Hamad Medjedovic … Yunchaokete Bu (58 total) |
| #2 | 27 | -16 .. -12 | Alejandro Tabilo … Yoshihito Nishioka (27 total) |
| #3 | 8 | 18 .. 28 | Alexander Zverev … Taylor Fritz (8 total) |

### Regional assignments (added points per region)

| Region | Mean raw | Target | Adjustment |
|---|---:|---:|---:|
| 1st | 50.00 | 61.00 | +11.00 |
| 2nd | 72.00 | 61.00 | -11.00 |
| 3rd | 34.00 | 34.00 | +0.00 |
| 5th | 13.50 | 13.62 | +0.00 |
| 9th | 13.75 | 13.62 | +0.00 |
| 17th | 6.12 | 6.12 | +0.00 |
| 33rd | -3.31 | -3.31 | +0.00 |
| 65th | -10.81 | -10.81 | +0.00 |

### Reflection accuracy

| Metric | Raw | Calibrated |
|---|---:|---:|
| Cross-region correctly-ordered pairs | 91.82% | 91.85% |
| Spearman (rating vs position) | -0.8330 | -0.8330 |

### Calibrated leaderboard (top 10 of 96) — rating = raw + region adjustment

| # | Player | Raw | Region adj | Calibrated | Position |
|---|---:|---:|---:|---:|---|
| 1 | Carlos Alcaraz | +50 | +11.00 | +61.00 | 1st |
| 2 | Jannik Sinner | +72 | -11.00 | +61.00 | 2nd |
| 3 | Terence Atmane | +40 | +0.00 | +40.00 | 3rd |
| 4 | Alexander Zverev | +28 | +0.00 | +28.00 | 3rd |
| 5 | Andrey Rublev | +26 | +0.00 | +26.00 | 5th |
| 6 | Frances Tiafoe | +24 | +0.00 | +24.00 | 9th |
| 7 | Karen Khachanov | +24 | +0.00 | +24.00 | 9th |
| 8 | Adrian Mannarino | +22 | +0.00 | +22.00 | 9th |
| 9 | Arthur Rinderknech | +20 | +0.00 | +20.00 | 17th |
| 10 | Reilly Opelka | +18 | +0.00 | +18.00 | 17th |

