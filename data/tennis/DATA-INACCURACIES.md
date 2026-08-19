# DATA INACCURACIES — all games with missing data (2021–2025 scope)

Single register of every match row in `data/tennis/editions/` that the engine cannot
rate, plus rows carrying an absent optional field.

**What this is NOT:** this register is **not** a list of data errors or gaps. The branch
is verified gapless — all 53 editions are `closed_verified_gapless`, `gap_count = 0`
(MANIFEST.json). Every row below is a present, recorded match.

**What this IS:**
- **Void matches** — retired / walkover / defaulted. Fully recorded results
  (date, round, players, winner all present) with no finished set score. The engine
  refuses to rate them by design — never guesses an unfinished score.
- **Completed matches with `duration_min` absent** — `duration_min` is an optional field;
  `DATA-RULES.md` and `build.py` do not require it.

- **Retired:** 99 rows
- **Walkover:** 22 rows
- **Defaulted:** 1 row
- **Completed, duration missing:** 227 rows
- **Total rows in register:** 349

## Retired matches (99 rows)

| Tournament | Year | Round | Player A | Player B | Score | Issue |
|---|---|---|---|---|---|---|
| Cincinnati | 2021 | R64 | Shelby Rogers | Danielle Collins | 6-4 2-1 | status=retired; retired; duration missing |
| Cincinnati | 2021 | R32 | Jelena Ostapenko | Jennifer Brady | 6-7(2) 5-4 | status=retired; retired; duration missing |
| Cincinnati | 2021 | R16 | Belinda Bencic | Karolina Muchova | 7-5 2-1 | status=retired; retired; duration missing |
| Cincinnati | 2021 | QF | Angelique Kerber | Petra Kvitova | 6-4 3-3 | status=retired; retired; tied set 3-3; duration missing |
| Cincinnati | 2021 | QF | Karolina Pliskova | Paula Badosa | 7-5 2-0 | status=retired; retired; duration missing |
| Cincinnati | 2022 | R64 | Marie Bouzkova | Coco Gauff | 7-5 1-0 | status=retired; retired; duration missing |
| Cincinnati | 2022 | R32 | Aryna Sabalenka | Anna Kalinskaya | 6-3 4-1 | status=retired; retired; duration missing |
| Cincinnati | 2023 | R16 | Ons Jabeur | Donna Vekic | 5-2 | status=retired; retired; duration missing |
| Cincinnati | 2023 | R16 | Jasmine Paolini | Elena Rybakina | 4-6 5-2 | status=retired; retired; duration missing |
| Cincinnati | 2023 | QF | Karolina Muchova | Marie Bouzkova | 3-0 | status=retired; retired; duration missing |
| Cincinnati Masters | 2022 | R32 | Jannik Sinner | Miomir Kecmanovic | 7-5 3-1 | status=retired; retired; duration missing |
| Cincinnati Masters | 2023 | R32 | Mackenzie McDonald | Holger Rune | 6-4 2-0 | status=retired; retired; duration missing |
| Cincinnati Masters | 2023 | R32 | Novak Djokovic | Alejandro Davidovich Fokina | 6-4 0-0 | status=retired; retired; tied set 0-0; duration missing |
| Cincinnati Masters | 2023 | R16 | Adrian Mannarino | Mackenzie McDonald | 6-4 3-0 | status=retired; retired; duration missing |
| Cincinnati Masters | 2023 | R16 | Taylor Fritz | Dusan Lajovic | 5-0 | status=retired; retired; duration missing |
| Cincinnati Masters | 2024 | R32 | Flavio Cobolli | Luciano Darderi | 7-6(4) 3-1 | status=retired; retired; duration missing |
| Cincinnati Masters | 2024 | QF | Frances Tiafoe | Hubert Hurkacz | 6-3 | status=retired; retired; duration missing |
| Cincinnati Masters | 2025 | R64 | Joao Fonseca | Alejandro Davidovich Fokina | 6-7(4) 5-4 | status=retired; retired; duration missing |
| Cincinnati Masters | 2025 | R64 | Francisco Comesana | Luciano Darderi | 6-4 3-1 | status=retired; retired; duration missing |
| Cincinnati Masters | 2025 | R64 | Ben Shelton | Camilo Ugo Carabelli | 6-3 3-1 | status=retired; retired; duration missing |
| Cincinnati Masters | 2025 | R32 | Felix Auger-Aliassime | Arthur Rinderknech | 7-6(4) 4-2 | status=retired; retired; duration missing |
| Cincinnati Masters | 2025 | R32 | Luca Nardi | Jakub Mensik | 6-2 2-1 | status=retired; retired; duration missing |
| Cincinnati Masters | 2025 | R16 | Holger Rune | Frances Tiafoe | 6-4 3-1 | status=retired; retired; duration missing |
| Cincinnati Masters | 2025 | R16 | Alexander Zverev | Karen Khachanov | 7-5 3-0 | status=retired; retired; duration missing |
| Cincinnati Masters | 2025 | F | Carlos Alcaraz | Jannik Sinner | 5-0 | status=retired; retired; duration missing |
| Cleveland | 2021 | R32 | Nagi Hanatani | Anna Blinkova | 1-0 | status=retired; retired; duration missing |
| Cleveland | 2023 | R32 | Peyton Stearns | Martina Trevisan | 6-1 4-5 | status=retired; retired; duration missing |
| Cleveland | 2023 | R32 | Sara Sorribes Tormo | Katerina Siniakova | 6-2 4-0 | status=retired; retired; duration missing |
| Cleveland | 2023 | R16 | Leylah Fernandez | Clara Tauson | 6-0 | status=retired; retired; duration missing |
| Dubai | 2021 | R64 | Malek Jaziri | Jo-Wilfried Tsonga | 3-3 | status=retired; retired; tied set 3-3; duration missing |
| Dubai | 2021 | R32 | Roberto Bautista Agut | Matthew Ebden | 4-1 | status=retired; retired; duration missing |
| Dubai | 2023 | R32 | Borna Coric | Daniel Evans | 2-2 | status=retired; retired; tied set 2-2; duration missing |
| Dubai | 2023 | R32 | Alexander Bublik | Alexandar Lazarov | 6-1 1-0 | status=retired; retired; duration missing |
| Dubai | 2024 | QF | Alexander Bublik | Jiri Lehecka | 6-4 4-1 | status=retired; retired; duration missing |
| Dubai | 2024 | QF | Andrey Rublev | Sebastian Korda | 6-4 4-3 | status=retired; retired; duration missing |
| Dubai | 2024 | R32 | Tallon Griekspoor | Abdullah Shelbayh | 7-5 2-0 | status=retired; retired; duration missing |
| Dubai | 2024 | R16 | Alejandro Davidovich Fokina | Jakub Mensik | 7-6(7) 1-0 | status=retired; retired; duration missing |
| Dubai | 2025 | R32 | Christopher O'Connell | Grigor Dimitrov | 6-0 | status=retired; retired; duration missing |
| Halle | 2021 | R32 | Corentin Moutet | David Goffin | 1-6 7-5 | status=retired; retired; duration missing |
| Halle | 2022 | R32 | Laslo Djere | Henri Squire | 4-3 | status=retired; retired; duration missing |
| Halle | 2022 | R32 | Roberto Bautista Agut | Marton Fucsovics | 6-2 3-0 | status=retired; retired; duration missing |
| Halle | 2023 | QF | Alexander Bublik | Jannik Sinner | 7-5 2-0 | status=retired; retired; duration missing |
| Halle | 2024 | R32 | Dominik Koepfer | Felix Auger-Aliassime | 6-4 4-3 | status=retired; retired; duration missing |
| Metz | 2022 | R32 | Nikoloz Basilashvili | Zizou Bergs | 4-6 1-2 | status=retired; retired; duration missing |
| Metz | 2022 | R16 | Holger Rune | Benjamin Bonzi | 6-4 4-1 | status=retired; retired; duration missing |
| Metz | 2022 | SF | Alexander Bublik | Stan Wawrinka | 2-1 | status=retired; retired; duration missing |
| Metz | 2023 | R16 | Luca Van Assche | Stan Wawrinka | 3-6 7-6(6) | status=retired; retired; duration missing |
| Metz | 2024 | R32 | Corentin Moutet | Sumit Nagal | 7-5 4-0 | status=retired; retired; duration missing |
| Metz | 2025 | R16 | Daniel Altmaier | Hugo Gaston | 4-6 6-0 0-0 | status=retired; retired; tied set 0-0; duration missing |
| Monastir | 2022 | R32 | Katerina Siniakova | Chloe Paquet | 6-4 4-0 | status=retired; retired; duration missing |
| Monastir | 2022 | R16 | Diane Parry | Lucrezia Stefanini | 6-3 1-0 | status=retired; retired; duration missing |
| Monastir | 2024 | SF | Sonay Kartal | Eva Lys | 5-1 | status=retired; retired; duration missing |
| Queen's Club | 2022 | R32 | Alexander Bublik | Lorenzo Musetti | 6-3 0-0 | status=retired; retired; tied set 0-0; duration missing |
| Queen's Club | 2024 | R32 | Rinky Hijikata | Frances Tiafoe | 7-5 4-6 1-0 | status=retired; retired; duration missing |
| Queen's Club | 2024 | R32 | Brandon Nakashima | Daniel Evans | 4-6 6-3 0-0 | status=retired; retired; tied set 0-0; duration missing |
| Queen's Club | 2024 | R16 | Jordan Thompson | Andy Murray | 4-1 | status=retired; retired; duration missing |
| Queen's Club | 2025 | R32 | Jaume Munar | Jordan Thompson | 7-5 0-0 | status=retired; retired; tied set 0-0; duration missing |
| Rotterdam | 2023 | R16 | Gijs Brouwer | Holger Rune | 6-4 4-0 | status=retired; retired; duration missing |
| Rotterdam | 2024 | QF | Jannik Sinner | Milos Raonic | 7-6 1-1 | status=retired; retired; tied set 1-1; duration missing |
| Rotterdam | 2025 | R32 | Andrea Vavassori | Felix Auger-Aliassime | 6-7(3) 6-4 0-0 | status=retired; retired; tied set 0-0; duration missing |
| Rotterdam | 2025 | R16 | Hubert Hurkacz | Jiri Lehecka | 7-5 2-0 | status=retired; retired; duration missing |
| US Open | 2021 | R128 | Nikoloz Basilashvili | Sebastian Korda | 6-2 2-1 | status=retired; retired; duration missing |
| US Open | 2021 | R128 | Philipp Kohlschreiber | Marin Cilic | 6-7(4) 6-7(3) 6-2 6-1 2-0 | status=retired; retired; duration missing |
| US Open | 2021 | R64 | Alexei Popyrin | Grigor Dimitrov | 7-6(4) 7-6(4) 4-0 | status=retired; retired; duration missing |
| US Open | 2021 | R32 | Alexander Zverev | Jack Sock | 3-6 6-2 6-3 2-1 | status=retired; retired; duration missing |
| US Open | 2021 | QF | Felix Auger-Aliassime | Carlos Alcaraz | 6-3 3-1 | status=retired; retired; duration missing |
| US Open | 2022 | R128 | Corentin Moutet | Stan Wawrinka | 6-4 7-6 | status=retired; retired; duration missing |
| US Open | 2022 | R128 | Carlos Alcaraz | Sebastian Baez | 7-5 7-5 2-0 | status=retired; retired; duration missing |
| US Open | 2022 | R128 | Diego Schwartzman | Jack Sock | 3-6 5-7 6-0 1-0 | status=retired; retired; duration missing |
| US Open | 2022 | R128 | Jenson Brooksby | Dusan Lajovic | 6-2 6-0 3-0 | status=retired; retired; duration missing |
| US Open | 2022 | R128 | Marton Fucsovics | Maxime Cressy | 6-7(4) 7-5 5-1 | status=retired; retired; duration missing |
| US Open | 2022 | R32 | Karen Khachanov | Jack Draper | 6-3 4-6 6-5 | status=retired; retired; duration missing |
| US Open | 2022 | R128 | Lauren Davis | Lucia Bronzetti | 4-6 7-6 5-4 | status=retired; retired; duration missing |
| US Open | 2023 | R128 | Botic van de Zandschulp | Jordan Thompson | 6-3 | status=retired; retired; duration missing |
| US Open | 2023 | R128 | Matteo Arnaldi | Jason Kubler | 6-3 1-0 | status=retired; retired; duration missing |
| US Open | 2023 | R128 | Carlos Alcaraz | Dominik Koepfer | 6-2 3-2 | status=retired; retired; duration missing |
| US Open | 2023 | R64 | Ben Shelton | Dominic Thiem | 7-6(1) 1-0 | status=retired; retired; duration missing |
| US Open | 2023 | R64 | Arthur Rinderknech | Matteo Berrettini | 6-4 5-3 | status=retired; retired; duration missing |
| US Open | 2023 | R64 | Sebastian Baez | Felipe Meligeni Alves | 6-7(7) 6-4 6-4 0-0 | status=retired; retired; tied set 0-0; duration missing |
| US Open | 2024 | R128 | Jiri Lehecka | Marton Fucsovics | 1-6 6-4 6-3 3-0 | status=retired; retired; duration missing |
| US Open | 2024 | R128 | Miomir Kecmanovic | Yoshihito Nishioka | 7-6(2) 2-6 5-7 7-5 1-0 | status=retired; retired; duration missing |
| US Open | 2024 | R128 | Jack Draper | Zhizhen Zhang | 6-3 6-0 4-0 | status=retired; retired; duration missing |
| US Open | 2024 | R64 | Novak Djokovic | Laslo Djere | 6-4 6-4 2-0 | status=retired; retired; duration missing |
| US Open | 2024 | R64 | Tallon Griekspoor | Sebastian Baez | 6-1 2-0 | status=retired; retired; duration missing |
| US Open | 2024 | R64 | Frances Tiafoe | Aleksandr Shevchenko | 6-4 6-1 1-0 | status=retired; retired; duration missing |
| US Open | 2024 | R64 | Tommy Paul | Max Purcell | 7-5 6-0 1-0 | status=retired; retired; duration missing |
| US Open | 2024 | QF | Frances Tiafoe | Grigor Dimitrov | 6-3 6-7 6-3 4-1 | status=retired; retired; duration missing |
| US Open | 2024 | R128 | Lucia Bronzetti | Lulu Sun | 6-3 | status=retired; retired; duration missing |
| US Open | 2024 | R128 | Varvara Lepchenko | Brenda Fruhvirtova | 2-1 | status=retired; retired; duration missing |
| US Open | 2024 | R128 | Yafan Wang | Maria Sakkari | 6-2 | status=retired; retired; duration missing |
| US Open | 2024 | R64 | Jasmine Paolini | Karolina Pliskova | 0-0 | status=retired; retired; tied set 0-0; duration missing |
| US Open | 2025 | R128 | Cameron Norrie | Sebastian Korda | 7-5 6-4 | status=retired; retired; duration missing |
| US Open | 2025 | R128 | Mattia Bellucci | Shang Juncheng | 7-6(0) 1-6 6-3 3-0 | status=retired; retired; duration missing |
| US Open | 2025 | R32 | Adrian Mannarino | Ben Shelton | 3-6 6-3 4-6 6-4 | status=retired; retired; duration missing |
| US Open | 2025 | R32 | Alex de Minaur | Daniel Altmaier | 6-7(7) 6-3 6-4 2-0 | status=retired; retired; duration missing |
| US Open | 2025 | R32 | Leandro Riedi | Kamil Majchrzak | 5-3 | status=retired; retired; duration missing |
| US Open | 2025 | R32 | Lorenzo Musetti | Flavio Cobolli | 6-3 6-2 2-0 | status=retired; retired; duration missing |
| US Open | 2025 | R128 | Polina Kudermetova | Nuria Parrizas Diaz | 2-2 | status=retired; retired; tied set 2-2; duration missing |
| US Open | 2025 | R64 | Linda Noskova | Eva Lys | 6-4 3-0 | status=retired; retired; duration missing |

## Walkover matches (22 rows)

| Tournament | Year | Round | Player A | Player B | Score | Issue |
|---|---|---|---|---|---|---|
| Cincinnati | 2021 | R32 | Jessica Pegula | Simona Halep | W/O | status=walkover; walkover; duration missing |
| Cincinnati | 2022 | R32 | Shelby Rogers | Amanda Anisimova | W/O | status=walkover; walkover; duration missing |
| Cincinnati | 2022 | R32 | Alison Riske-Amritraj | Marie Bouzkova | W/O | status=walkover; walkover; duration missing |
| Cincinnati | 2022 | R32 | Veronika Kudermetova | Simona Halep | W/O | status=walkover; walkover; duration missing |
| Cincinnati | 2025 | R64 | Amanda Anisimova | Leolia Jeanjean | W/O | status=walkover; walkover; duration missing |
| Cincinnati | 2025 | R64 | Jelena Ostapenko | Camila Osorio | W/O | status=walkover; walkover; duration missing |
| Cincinnati | 2025 | R32 | Iga Swiatek | Marta Kostyuk | W/O | status=walkover; walkover; duration missing |
| Cincinnati | 2025 | R32 | Coco Gauff | Dayana Yastremska | W/O | status=walkover; walkover; duration missing |
| Cincinnati Masters | 2023 | R32 | Alexei Popyrin | Nicolas Jarry | W/O | status=walkover; walkover; duration missing |
| Cincinnati Masters | 2024 | R16 | Jannik Sinner | Jordan Thompson | W/O | status=walkover; walkover; duration missing |
| Cleveland | 2021 | R16 | Sara Sorribes Tormo | Vera Zvonareva | W/O | status=walkover; walkover; duration missing |
| Cleveland | 2022 | R16 | Shuai Zhang | Martina Trevisan | W/O | status=walkover; walkover; duration missing |
| Cleveland | 2023 | R16 | Tatjana Maria | Anhelina Kalinina | W/O | status=walkover; walkover; duration missing |
| Cleveland | 2025 | QF | Anastasia Zakharova | Eva Lys | W/O | status=walkover; walkover; duration missing |
| Metz | 2024 | QF | Corentin Moutet | Andrey Rublev | W/O | status=walkover; walkover; duration missing |
| US Open | 2021 | R64 | Naomi Osaka | Olga Danilovic | W/O | status=walkover; walkover; duration missing |
| US Open | 2022 | R64 | Holger Rune | John Isner | W/O | status=walkover; walkover; duration missing |
| US Open | 2022 | R64 | Petra Kvitova | Anhelina Kalinina | W/O | status=walkover; walkover; duration missing |
| US Open | 2023 | R64 | Elena Rybakina | Ajla Tomljanovic | W/O | status=walkover; walkover; duration missing |
| US Open | 2024 | R64 | Jessika Ponchet | Elena Rybakina | W/O | status=walkover; walkover; duration missing |
| US Open | 2025 | R64 | Zizou Bergs | Jack Draper | W/O | status=walkover; walkover; duration missing |
| US Open | 2025 | QF | Aryna Sabalenka | Marketa Vondrousova | W/O | status=walkover; walkover; duration missing |

## Defaulted matches (1 rows)

| Tournament | Year | Round | Player A | Player B | Score | Issue |
|---|---|---|---|---|---|---|
| Dubai | 2024 | SF | Alexander Bublik | Andrey Rublev | 6-7(4) 7-6(5) 6-5 | status=defaulted; defaulted; duration missing |

## Completed matches with missing duration (227 rows)

| Tournament | Year | Round | Player A | Player B | Score | Issue |
|---|---|---|---|---|---|---|
| Cincinnati | 2021 | QF | Ashleigh Barty | Barbora Krejcikova | 6-2 6-4 | duration missing |
| Cincinnati | 2021 | QF | Jil Teichmann | Belinda Bencic | 6-3 6-2 | duration missing |
| Cincinnati | 2022 | QF | Aryna Sabalenka | Shuai Zhang | 6-4 7-6 | duration missing |
| Cincinnati | 2022 | QF | Madison Keys | Elena Rybakina | 6-2 6-4 | duration missing |
| Cincinnati | 2022 | QF | Petra Kvitova | Ajla Tomljanovic | 6-2 6-3 | duration missing |
| Cincinnati | 2022 | QF | Caroline Garcia | Jessica Pegula | 6-1 7-5 | duration missing |
| Cincinnati | 2023 | QF | Coco Gauff | Jasmine Paolini | 6-3 6-2 | duration missing |
| Cincinnati | 2023 | QF | Iga Swiatek | Marketa Vondrousova | 7-6 6-1 | duration missing |
| Cincinnati | 2023 | QF | Aryna Sabalenka | Ons Jabeur | 7-5 6-3 | duration missing |
| Cincinnati | 2024 | QF | Aryna Sabalenka | Liudmila Samsonova | 6-3 6-2 | duration missing |
| Cincinnati | 2024 | QF | Iga Swiatek | Mirra Andreeva | 4-6 6-3 7-5 | duration missing |
| Cincinnati | 2024 | QF | Jessica Pegula | Leylah Fernandez | 7-5 6-7 7-6 | duration missing |
| Cincinnati | 2024 | QF | Paula Badosa | Anastasia Pavlyuchenkova | 6-3 6-2 | duration missing |
| Cincinnati | 2025 | QF | Elena Rybakina | Aryna Sabalenka | 6-1 6-4 | duration missing |
| Cincinnati | 2025 | QF | Iga Swiatek | Anna Kalinskaya | 6-3 6-4 | duration missing |
| Cincinnati | 2025 | QF | Veronika Kudermetova | Varvara Gracheva | 6-1 6-2 | duration missing |
| Cincinnati | 2025 | QF | Jasmine Paolini | Coco Gauff | 2-6 6-4 6-3 | duration missing |
| Cincinnati Masters | 2021 | R64 | Benoit Paire | Miomir Kecmanovic | 5-7 6-3 6-2 | duration missing |
| Cincinnati Masters | 2021 | R64 | Guido Pella | David Goffin | 6-3 6-3 | duration missing |
| Cincinnati Masters | 2021 | QF | Andrey Rublev | Benoit Paire | 6-2 3-6 6-3 | duration missing |
| Cincinnati Masters | 2021 | QF | Daniil Medvedev | Pablo Carreno Busta | 6-1 6-1 | duration missing |
| Cincinnati Masters | 2021 | QF | Alexander Zverev | Casper Ruud | 6-1 6-3 | duration missing |
| Cincinnati Masters | 2021 | QF | Stefanos Tsitsipas | Felix Auger-Aliassime | 6-2 5-7 6-1 | duration missing |
| Cincinnati Masters | 2022 | QF | Daniil Medvedev | Taylor Fritz | 7-6 6-3 | duration missing |
| Cincinnati Masters | 2022 | QF | Stefanos Tsitsipas | John Isner | 7-6 5-7 6-3 | duration missing |
| Cincinnati Masters | 2022 | QF | Borna Coric | Felix Auger-Aliassime | 6-4 6-4 | duration missing |
| Cincinnati Masters | 2022 | QF | Cameron Norrie | Carlos Alcaraz | 7-6 6-7 6-4 | duration missing |
| Cincinnati Masters | 2023 | QF | Carlos Alcaraz | Max Purcell | 4-6 6-3 6-4 | duration missing |
| Cincinnati Masters | 2023 | QF | Hubert Hurkacz | Alexei Popyrin | 6-1 7-6 | duration missing |
| Cincinnati Masters | 2023 | QF | Alexander Zverev | Adrian Mannarino | 6-2 6-3 | duration missing |
| Cincinnati Masters | 2023 | QF | Novak Djokovic | Taylor Fritz | 6-0 6-4 | duration missing |
| Cincinnati Masters | 2024 | QF | Alexander Zverev | Ben Shelton | 3-6 7-6 7-5 | duration missing |
| Cincinnati Masters | 2024 | QF | Jannik Sinner | Andrey Rublev | 4-6 7-5 6-4 | duration missing |
| Cincinnati Masters | 2024 | QF | Holger Rune | Jack Draper | 6-4 6-2 | duration missing |
| Cincinnati Masters | 2025 | QF | Jannik Sinner | Felix Auger-Aliassime | 6-0 6-2 | duration missing |
| Cincinnati Masters | 2025 | QF | Carlos Alcaraz | Andrey Rublev | 6-3 4-6 7-5 | duration missing |
| Cincinnati Masters | 2025 | QF | Terence Atmane | Holger Rune | 6-2 6-3 | duration missing |
| Cincinnati Masters | 2025 | QF | Alexander Zverev | Ben Shelton | 6-2 6-2 | duration missing |
| Cleveland | 2021 | QF | Anett Kontaveit | Katerina Siniakova | 6-3 5-7 6-2 | duration missing |
| Cleveland | 2021 | QF | Irina-Camelia Begu | Aliaksandra Sasnovich | 6-2 6-4 | duration missing |
| Cleveland | 2021 | QF | Magda Linette | Daria Kasatkina | 6-1 6-2 | duration missing |
| Cleveland | 2021 | QF | Sara Sorribes Tormo | Shuai Zhang | 6-3 6-1 | duration missing |
| Cleveland | 2022 | QF | Aliaksandra Sasnovich | Madison Brengle | 6-4 6-1 | duration missing |
| Cleveland | 2022 | QF | Alizé Cornet | Shuai Zhang | 6-4 6-2 | duration missing |
| Cleveland | 2022 | QF | Bernarda Pera | Sofia Kenin | 6-2 5-7 6-3 | duration missing |
| Cleveland | 2022 | QF | Liudmila Samsonova | Magda Linette | 6-4 6-3 | duration missing |
| Cleveland | 2023 | QF | Ekaterina Alexandrova | Xinyu Wang | 5-7 6-0 7-5 | duration missing |
| Cleveland | 2023 | QF | Lin Zhu | Caroline Garcia | 6-4 6-1 | duration missing |
| Cleveland | 2023 | QF | Tatjana Maria | Leylah Fernandez | 6-3 6-2 | duration missing |
| Cleveland | 2023 | QF | Sara Sorribes Tormo | Sloane Stephens | 6-1 6-3 | duration missing |
| Cleveland | 2024 | QF | Anastasia Potapova | Ana Bogdan | 6-2 6-1 | duration missing |
| Cleveland | 2024 | QF | Beatriz Haddad Maia | Clara Burel | 6-2 6-2 | duration missing |
| Cleveland | 2024 | QF | Katerina Siniakova | Peyton Stearns | 1-6 6-3 6-4 | duration missing |
| Cleveland | 2024 | QF | McCartney Kessler | Arantxa Rus | 6-4 6-2 | duration missing |
| Cleveland | 2025 | QF | Ann Li | Elsa Jacquemot | 6-1 5-7 6-1 | duration missing |
| Cleveland | 2025 | QF | Sorana Cirstea | Liudmila Samsonova | 6-4 6-1 | duration missing |
| Cleveland | 2025 | QF | Xinyu Wang | Viktorija Golubic | 4-6 6-4 6-4 | duration missing |
| Dubai | 2021 | QF | Andrey Rublev | Marton Fucsovics | 7-5 6-2 | duration missing |
| Dubai | 2021 | QF | Aslan Karatsev | Jannik Sinner | 6-7 6-3 6-2 | duration missing |
| Dubai | 2021 | QF | Denis Shapovalov | Jeremy Chardy | 7-5 6-4 | duration missing |
| Dubai | 2021 | QF | Lloyd Harris | Kei Nishikori | 6-1 3-6 6-3 | duration missing |
| Dubai | 2022 | QF | Andrey Rublev | Mackenzie McDonald | 2-6 6-3 6-1 | duration missing |
| Dubai | 2022 | QF | Denis Shapovalov | Ricardas Berankis | 7-6 6-3 | duration missing |
| Dubai | 2022 | QF | Hubert Hurkacz | Jannik Sinner | 6-3 6-3 | duration missing |
| Dubai | 2022 | QF | Jiri Vesely | Novak Djokovic | 6-4 7-6 | duration missing |
| Dubai | 2023 | QF | Alexander Zverev | Lorenzo Sonego | 7-5 6-4 | duration missing |
| Dubai | 2023 | QF | Andrey Rublev | Botic van de Zandschulp | 6-3 7-6 | duration missing |
| Dubai | 2023 | QF | Daniil Medvedev | Borna Coric | 6-3 6-2 | duration missing |
| Dubai | 2023 | QF | Novak Djokovic | Hubert Hurkacz | 6-3 7-5 | duration missing |
| Dubai | 2024 | QF | Daniil Medvedev | Alejandro Davidovich Fokina | 6-2 6-3 | duration missing |
| Dubai | 2024 | QF | Ugo Humbert | Hubert Hurkacz | 3-6 7-6 6-3 | duration missing |
| Dubai | 2025 | QF | Felix Auger-Aliassime | Marin Cilic | 6-4 3-6 6-2 | duration missing |
| Dubai | 2025 | QF | Quentin Halys | Luca Nardi | 2-6 6-3 7-6 | duration missing |
| Dubai | 2025 | QF | Stefanos Tsitsipas | Matteo Berrettini | 7-6 1-6 6-4 | duration missing |
| Dubai | 2025 | QF | Tallon Griekspoor | Daniil Medvedev | 2-6 7-6 7-5 | duration missing |
| Halle | 2021 | QF | Andrey Rublev | Philipp Kohlschreiber | 7-6 6-2 | duration missing |
| Halle | 2021 | QF | Felix Auger-Aliassime | Marcos Giron | 6-3 6-2 | duration missing |
| Halle | 2021 | QF | Nikoloz Basilashvili | Lloyd Harris | 6-4 7-6 | duration missing |
| Halle | 2021 | QF | Ugo Humbert | Sebastian Korda | 6-2 6-7 6-4 | duration missing |
| Halle | 2022 | QF | Daniil Medvedev | Roberto Bautista Agut | 6-2 6-4 | duration missing |
| Halle | 2022 | QF | Hubert Hurkacz | Felix Auger-Aliassime | 7-6 7-6 | duration missing |
| Halle | 2022 | QF | Nick Kyrgios | Pablo Carreno Busta | 6-4 6-2 | duration missing |
| Halle | 2022 | QF | Oscar Otte | Karen Khachanov | 4-6 7-6 6-4 | duration missing |
| Halle | 2023 | QF | Alexander Zverev | Nicolas Jarry | 7-5 6-3 | duration missing |
| Halle | 2023 | QF | Andrey Rublev | Tallon Griekspoor | 3-6 6-3 6-4 | duration missing |
| Halle | 2023 | QF | Roberto Bautista Agut | Daniil Medvedev | 7-5 7-6 | duration missing |
| Halle | 2024 | QF | Alexander Zverev | Arthur Fils | 6-7 6-3 6-4 | duration missing |
| Halle | 2024 | QF | Hubert Hurkacz | Marcos Giron | 7-6 6-4 | duration missing |
| Halle | 2024 | QF | Jannik Sinner | Jan-Lennard Struff | 6-2 6-7 7-6 | duration missing |
| Halle | 2024 | QF | Zhizhen Zhang | Christopher Eubanks | 6-4 4-6 7-5 | duration missing |
| Halle | 2025 | QF | Alexander Bublik | Tomas Machac | 7-6 6-3 | duration missing |
| Halle | 2025 | QF | Alexander Zverev | Flavio Cobolli | 6-4 7-6 | duration missing |
| Halle | 2025 | QF | Daniil Medvedev | Alex Michelsen | 6-4 6-3 | duration missing |
| Halle | 2025 | QF | Karen Khachanov | Tomas Martin Etcheverry | 6-3 6-2 | duration missing |
| Metz | 2021 | QF | Gael Monfils | Nikoloz Basilashvili | 6-3 6-3 | duration missing |
| Metz | 2021 | QF | Hubert Hurkacz | Andy Murray | 7-6 6-3 | duration missing |
| Metz | 2021 | QF | Pablo Carreno Busta | Holger Rune | 6-4 3-6 6-4 | duration missing |
| Metz | 2021 | QF | Peter Gojowczyk | Marcos Giron | 3-6 6-1 6-3 | duration missing |
| Metz | 2022 | QF | Alexander Bublik | Holger Rune | 6-3 5-7 6-4 | duration missing |
| Metz | 2022 | QF | Hubert Hurkacz | Arthur Rinderknech | 6-3 6-2 | duration missing |
| Metz | 2022 | QF | Lorenzo Sonego | Sebastian Korda | 6-4 6-4 | duration missing |
| Metz | 2022 | QF | Stan Wawrinka | Mikael Ymer | 6-4 4-6 7-6 | duration missing |
| Metz | 2023 | QF | Aleksandr Shevchenko | Karen Khachanov | 6-4 6-4 | duration missing |
| Metz | 2023 | QF | Fabio Fognini | Lorenzo Sonego | 6-1 6-2 | duration missing |
| Metz | 2023 | QF | Pierre-Hugues Herbert | Luca Van Assche | 4-6 6-3 7-5 | duration missing |
| Metz | 2023 | QF | Ugo Humbert | Harold Mayot | 6-3 7-5 | duration missing |
| Metz | 2024 | QF | Alex Michelsen | Yunchaokete Bu | 6-7 6-2 6-4 | duration missing |
| Metz | 2024 | QF | Benjamin Bonzi | Quentin Halys | 6-3 7-6 | duration missing |
| Metz | 2024 | QF | Cameron Norrie | Zizou Bergs | 6-3 6-7 6-1 | duration missing |
| Metz | 2025 | QF | Cameron Norrie | Kyrian Jacquet | 4-6 7-6 6-4 | duration missing |
| Metz | 2025 | QF | Learner Tien | Matteo Berrettini | 5-7 6-2 6-3 | duration missing |
| Metz | 2025 | QF | Lorenzo Sonego | Daniel Altmaier | 6-4 7-6 | duration missing |
| Metz | 2025 | QF | Vitaliy Sachko | Clement Tabur | 6-4 3-6 6-4 | duration missing |
| Monastir | 2022 | QF | Alizé Cornet | Tamara Zidansek | 7-5 7-6 | duration missing |
| Monastir | 2022 | QF | Claire Liu | Ons Jabeur | 6-3 4-6 6-4 | duration missing |
| Monastir | 2022 | QF | Elise Mertens | Moyuka Uchijima | 6-0 3-6 6-4 | duration missing |
| Monastir | 2022 | QF | Veronika Kudermetova | Diane Parry | 6-4 6-1 | duration missing |
| Monastir | 2023 | QF | Clara Burel | Lucrezia Stefanini | 6-3 6-1 | duration missing |
| Monastir | 2023 | QF | Elise Mertens | Mai Hontama | 6-3 6-2 | duration missing |
| Monastir | 2023 | QF | Jasmine Paolini | Lucia Bronzetti | 7-5 7-6 | duration missing |
| Monastir | 2023 | QF | Lesia Tsurenko | Nuria Parrizas Diaz | 6-3 6-2 | duration missing |
| Monastir | 2024 | R32 | Clara Burel | Marina Bassols Ribera | 6-2 6-2 | duration missing |
| Monastir | 2024 | R32 | Diane Parry | Chiraz Bechri | 6-3 6-0 | duration missing |
| Monastir | 2024 | R32 | Eva Lys | Lesia Tsurenko | 6-3 7-5 | duration missing |
| Monastir | 2024 | R32 | Mai Hontama | Priska Madelyn Nugroho | 6-2 6-1 | duration missing |
| Monastir | 2024 | R32 | Sara Sorribes Tormo | Anna Blinkova | 6-4 6-4 | duration missing |
| Monastir | 2024 | R32 | Yuriko Lily Miyazaki | Alycia Parks | 6-3 5-7 6-3 | duration missing |
| Monastir | 2024 | R32 | Ann Li | Kristina Mladenovic | 6-2 6-1 | duration missing |
| Monastir | 2024 | R32 | Antonia Ruzic | Nadia Podoroska | 1-6 6-2 6-4 | duration missing |
| Monastir | 2024 | R32 | Elise Mertens | Anastasia Zakharova | 6-2 6-0 | duration missing |
| Monastir | 2024 | R32 | Greet Minnen | Aliona Falei | 6-0 3-6 6-2 | duration missing |
| Monastir | 2024 | R32 | Jana Fett | Mayar Sherif | 1-6 6-3 6-4 | duration missing |
| Monastir | 2024 | R32 | Lucia Bronzetti | Dalma Galfi | 6-2 6-1 | duration missing |
| Monastir | 2024 | R32 | Rebecca Sramkova | Elsa Jacquemot | 2-6 7-5 6-3 | duration missing |
| Monastir | 2024 | R32 | Sonay Kartal | Jaqueline Cristian | 4-6 6-3 7-5 | duration missing |
| Monastir | 2024 | R32 | Yuliia Starodubtseva | Suzan Lamens | 6-2 3-6 6-4 | duration missing |
| Monastir | 2024 | R32 | Zeynep Sonmez | Rebeka Masarova | 4-6 7-6(4) 6-3 | duration missing |
| Monastir | 2024 | R16 | Rebecca Sramkova | Clara Burel | 7-6(4) 7-5 | duration missing |
| Monastir | 2024 | R16 | Sara Sorribes Tormo | Jana Fett | 5-7 6-3 6-4 | duration missing |
| Monastir | 2024 | R16 | Sonay Kartal | Mai Hontama | 6-2 6-2 | duration missing |
| Monastir | 2024 | R16 | Yuliia Starodubtseva | Diane Parry | 6-4 6-4 | duration missing |
| Monastir | 2024 | R16 | Antonia Ruzic | Yuriko Lily Miyazaki | 6-3 6-1 | duration missing |
| Monastir | 2024 | R16 | Eva Lys | Elise Mertens | 1-6 6-2 7-6(4) | duration missing |
| Monastir | 2024 | R16 | Lucia Bronzetti | Ann Li | 6-4 7-6(3) | duration missing |
| Monastir | 2024 | R16 | Zeynep Sonmez | Greet Minnen | 6-4 1-6 6-3 | duration missing |
| Monastir | 2024 | QF | Eva Lys | Zeynep Sonmez | 7-5 6-3 | duration missing |
| Monastir | 2024 | QF | Lucia Bronzetti | Antonia Ruzic | 6-2 6-1 | duration missing |
| Monastir | 2024 | QF | Rebecca Sramkova | Sara Sorribes Tormo | 1-6 7-6 7-5 | duration missing |
| Monastir | 2024 | QF | Sonay Kartal | Yuliia Starodubtseva | 7-6 6-2 | duration missing |
| Monastir | 2024 | SF | Rebecca Sramkova | Lucia Bronzetti | 6-3 6-4 | duration missing |
| Monastir | 2024 | F | Sonay Kartal | Rebecca Sramkova | 6-3 7-5 | duration missing |
| Queen's Club | 2021 | QF | Alex de Minaur | Marin Cilic | 3-6 6-3 6-4 | duration missing |
| Queen's Club | 2021 | QF | Cameron Norrie | Jack Draper | 6-3 6-3 | duration missing |
| Queen's Club | 2021 | QF | Matteo Berrettini | Daniel Evans | 7-6 6-3 | duration missing |
| Queen's Club | 2021 | QF | Denis Shapovalov | Frances Tiafoe | 6-3 6-4 | duration missing |
| Queen's Club | 2022 | QF | Botic van de Zandschulp | Alejandro Davidovich Fokina | 6-2 6-4 | duration missing |
| Queen's Club | 2022 | QF | Filip Krajinovic | Ryan Peniston | 4-6 6-3 6-3 | duration missing |
| Queen's Club | 2022 | QF | Marin Cilic | Emil Ruusuvuori | 7-6 6-4 | duration missing |
| Queen's Club | 2022 | QF | Matteo Berrettini | Tommy Paul | 6-4 6-2 | duration missing |
| Queen's Club | 2023 | QF | Alex de Minaur | Adrian Mannarino | 6-4 4-6 6-4 | duration missing |
| Queen's Club | 2023 | QF | Carlos Alcaraz | Grigor Dimitrov | 6-4 6-4 | duration missing |
| Queen's Club | 2023 | QF | Holger Rune | Lorenzo Musetti | 6-4 7-5 | duration missing |
| Queen's Club | 2023 | QF | Sebastian Korda | Cameron Norrie | 6-4 7-6 | duration missing |
| Queen's Club | 2024 | QF | Jordan Thompson | Taylor Fritz | 6-4 6-3 | duration missing |
| Queen's Club | 2024 | QF | Lorenzo Musetti | Billy Harris | 6-3 7-5 | duration missing |
| Queen's Club | 2024 | QF | Sebastian Korda | Rinky Hijikata | 6-7 6-3 6-4 | duration missing |
| Queen's Club | 2024 | QF | Tommy Paul | Jack Draper | 6-3 5-7 6-4 | duration missing |
| Queen's Club | 2025 | QF | Carlos Alcaraz | Arthur Rinderknech | 7-5 6-4 | duration missing |
| Queen's Club | 2025 | QF | Jack Draper | Brandon Nakashima | 6-4 5-7 6-4 | duration missing |
| Queen's Club | 2025 | QF | Jiri Lehecka | Jacob Fearnley | 7-5 6-2 | duration missing |
| Queen's Club | 2025 | QF | Roberto Bautista Agut | Holger Rune | 7-6 6-7 6-2 | duration missing |
| Rotterdam | 2021 | QF | Andrey Rublev | Jeremy Chardy | 7-6 6-7 6-4 | duration missing |
| Rotterdam | 2021 | QF | Borna Coric | Kei Nishikori | 7-6 7-6 | duration missing |
| Rotterdam | 2021 | QF | Marton Fucsovics | Tommy Paul | 6-4 6-3 | duration missing |
| Rotterdam | 2021 | QF | Stefanos Tsitsipas | Karen Khachanov | 4-6 6-3 7-5 | duration missing |
| Rotterdam | 2022 | QF | Andrey Rublev | Marton Fucsovics | 6-4 6-3 | duration missing |
| Rotterdam | 2022 | QF | Felix Auger-Aliassime | Cameron Norrie | 7-5 7-6 | duration missing |
| Rotterdam | 2022 | QF | Jiri Lehecka | Lorenzo Musetti | 6-3 1-6 7-5 | duration missing |
| Rotterdam | 2022 | QF | Stefanos Tsitsipas | Alex de Minaur | 6-4 6-4 | duration missing |
| Rotterdam | 2023 | QF | Daniil Medvedev | Felix Auger-Aliassime | 6-2 6-4 | duration missing |
| Rotterdam | 2023 | QF | Grigor Dimitrov | Alex de Minaur | 6-3 3-6 7-6 | duration missing |
| Rotterdam | 2023 | QF | Jannik Sinner | Stan Wawrinka | 6-1 6-3 | duration missing |
| Rotterdam | 2023 | QF | Tallon Griekspoor | Gijs Brouwer | 6-4 6-4 | duration missing |
| Rotterdam | 2024 | QF | Alex de Minaur | Andrey Rublev | 7-6 4-6 6-3 | duration missing |
| Rotterdam | 2024 | QF | Grigor Dimitrov | Aleksandr Shevchenko | 7-6 3-6 6-4 | duration missing |
| Rotterdam | 2024 | QF | Tallon Griekspoor | Emil Ruusuvuori | 7-5 7-6 | duration missing |
| Rotterdam | 2025 | QF | Alex de Minaur | Daniel Altmaier | 6-1 6-4 | duration missing |
| Rotterdam | 2025 | QF | Carlos Alcaraz | Pedro Martinez | 6-2 6-1 | duration missing |
| Rotterdam | 2025 | QF | Hubert Hurkacz | Andrey Rublev | 6-7 6-3 6-4 | duration missing |
| Rotterdam | 2025 | QF | Mattia Bellucci | Stefanos Tsitsipas | 6-4 6-2 | duration missing |
| US Open | 2021 | QF | Daniil Medvedev | Botic van de Zandschulp | 6-3 6-0 4-6 7-5 | duration missing |
| US Open | 2021 | QF | Alexander Zverev | Lloyd Harris | 7-6 6-3 6-4 | duration missing |
| US Open | 2021 | QF | Novak Djokovic | Matteo Berrettini | 5-7 6-2 6-2 6-3 | duration missing |
| US Open | 2021 | QF | Leylah Fernandez | Elina Svitolina | 6-3 3-6 7-6 | duration missing |
| US Open | 2021 | QF | Aryna Sabalenka | Barbora Krejcikova | 6-1 6-4 | duration missing |
| US Open | 2021 | QF | Emma Raducanu | Belinda Bencic | 6-3 6-4 | duration missing |
| US Open | 2021 | QF | Maria Sakkari | Karolina Pliskova | 6-4 6-4 | duration missing |
| US Open | 2022 | QF | Casper Ruud | Matteo Berrettini | 6-1 6-4 7-6 | duration missing |
| US Open | 2022 | QF | Frances Tiafoe | Andrey Rublev | 7-6 7-6 6-4 | duration missing |
| US Open | 2022 | QF | Karen Khachanov | Nick Kyrgios | 7-5 4-6 7-5 6-7 6-4 | duration missing |
| US Open | 2022 | QF | Carlos Alcaraz | Jannik Sinner | 6-3 6-7 6-7 7-5 6-3 | duration missing |
| US Open | 2022 | QF | Ons Jabeur | Ajla Tomljanovic | 6-4 7-6 | duration missing |
| US Open | 2022 | QF | Aryna Sabalenka | Karolina Pliskova | 6-1 7-6 | duration missing |
| US Open | 2022 | QF | Caroline Garcia | Coco Gauff | 6-3 6-4 | duration missing |
| US Open | 2022 | QF | Iga Swiatek | Jessica Pegula | 6-3 7-6 | duration missing |
| US Open | 2023 | QF | Novak Djokovic | Taylor Fritz | 6-1 6-4 6-4 | duration missing |
| US Open | 2023 | QF | Ben Shelton | Frances Tiafoe | 6-2 3-6 7-6 6-2 | duration missing |
| US Open | 2023 | QF | Daniil Medvedev | Andrey Rublev | 6-4 6-3 6-4 | duration missing |
| US Open | 2023 | QF | Carlos Alcaraz | Alexander Zverev | 6-3 6-2 6-4 | duration missing |
| US Open | 2023 | QF | Coco Gauff | Jelena Ostapenko | 6-0 6-2 | duration missing |
| US Open | 2023 | QF | Aryna Sabalenka | Qinwen Zheng | 6-1 6-4 | duration missing |
| US Open | 2023 | QF | Karolina Muchova | Sorana Cirstea | 6-0 6-3 | duration missing |
| US Open | 2023 | QF | Madison Keys | Marketa Vondrousova | 6-1 6-4 | duration missing |
| US Open | 2024 | QF | Taylor Fritz | Alexander Zverev | 7-6 3-6 6-4 7-6 | duration missing |
| US Open | 2024 | QF | Jack Draper | Alex de Minaur | 6-3 7-5 6-2 | duration missing |
| US Open | 2024 | QF | Jannik Sinner | Daniil Medvedev | 6-2 1-6 6-1 6-4 | duration missing |
| US Open | 2024 | QF | Emma Navarro | Paula Badosa | 6-2 7-5 | duration missing |
| US Open | 2024 | QF | Aryna Sabalenka | Qinwen Zheng | 6-1 6-2 | duration missing |
| US Open | 2024 | QF | Karolina Muchova | Beatriz Haddad Maia | 6-1 6-4 | duration missing |
| US Open | 2024 | QF | Jessica Pegula | Iga Swiatek | 6-2 6-4 | duration missing |
| US Open | 2025 | QF | Carlos Alcaraz | Jiri Lehecka | 6-4 6-2 6-4 | duration missing |
| US Open | 2025 | QF | Felix Auger-Aliassime | Alex de Minaur | 4-6 7-6 7-5 7-6 | duration missing |
| US Open | 2025 | QF | Novak Djokovic | Taylor Fritz | 6-3 7-5 3-6 6-4 | duration missing |
| US Open | 2025 | QF | Jannik Sinner | Lorenzo Musetti | 6-1 6-4 6-2 | duration missing |
| US Open | 2025 | QF | Jessica Pegula | Barbora Krejcikova | 6-3 6-3 | duration missing |
| US Open | 2025 | QF | Amanda Anisimova | Iga Swiatek | 6-4 6-3 | duration missing |
| US Open | 2025 | QF | Naomi Osaka | Karolina Muchova | 6-4 7-6 | duration missing |

## Scope note

- Data scope is 2021–2025 only. No 2026 or unplayed events are listed (not data inaccuracies).
- Generated from the edition files' own bytes on 2026-08-19 (53 editions, 2,917 matches).
