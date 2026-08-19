import json
from collections import defaultdict

d = json.load(open('data/tennis/master_store_tennis_SSoT.json'))
matches = d['matches']

# Filter to M1000, 2021-2025 (workorder scope)
m1000 = [m for m in matches if m['tier'] == 'M1000' and m['edition_year'] in ('2021','2022','2023','2024','2025')]

# Group by (tour, tournament, edition_year) = "edition"
editions = defaultdict(list)
for m in m1000:
    key = (m['tour'], m['tournament'], m['edition_year'])
    editions[key].append(m)

print("Total M1000 2021-2025 editions found (by tour/tournament/year triple):", len(editions))

round_order = ['R128', 'R64', 'R32', 'R16', 'QF', 'SF', 'F']
# Transitions to check, per stated method: R32->R16->QF->SF->F (R64->R32 excluded)
transitions = [('R32','R16'), ('R16','QF'), ('QF','SF'), ('SF','F')]

gaps = []
for (tour, tournament, year), edm in editions.items():
    by_round = defaultdict(list)
    for m in edm:
        by_round[m['round']].append(m)

    for prior_r, next_r in transitions:
        if next_r not in by_round:
            continue  # round doesn't exist in this edition at all (e.g. edition never reached that round - not a gap)
        # participants in next round
        next_participants = set()
        for m in by_round[next_r]:
            next_participants.add(m['playerA'])
            next_participants.add(m['playerB'])
        # winners of prior round
        prior_winners = set()
        for m in by_round.get(prior_r, []):
            if m['winner'] == 'A':
                prior_winners.add(m['playerA'])
            elif m['winner'] == 'B':
                prior_winners.add(m['playerB'])
        missing = next_participants - prior_winners
        for player in missing:
            gaps.append({
                "tour": tour,
                "tournament": tournament,
                "edition_year": year,
                "missing_round": prior_r,
                "missing_opponent_in_round": next_r,
                "player_with_no_traceable_win": player
            })

print("Total gap instances found by my script:", len(gaps))
affected_editions = set((g['tour'], g['tournament'], g['edition_year']) for g in gaps)
print("Editions affected:", len(affected_editions))
print("Total editions checked:", len(editions))

json.dump({'total_gap_instances': len(gaps), 'editions_affected': len(affected_editions), 'total_editions_checked': len(editions), 'gaps': gaps}, open('data/tennis/phase1-audit/m1000_r32_onward_gaps_REPRODUCED.json','w'), indent=2)
