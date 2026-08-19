"""Phase 1 — Tournament Performance Metric Subsystem (3rd UI layer).

Core computational hub for per-player tournament performance:
- 5-match sliding window per player (config performance.json window_size).
- INTRAMURAL constraint: the window is computed only from the player's matches
  within the identical tournament — cross-tournament matching data is strictly
  barred until cross-tournament normalization weightings are verified.
- Rolling queue: matches are ingested chronologically; when the queue exceeds
  the window, the LOWEST historical player rating drops out of the evaluation
  set.
- Absolute rating basis: the baseline point compilation uses the player's
  Phase 0 rating points per match (their points minus the opponent's points) —
  no raw game-score subtraction.
- Asymmetric performance calibration (high-disparity upsets, e.g. an absolute
  system-rated 73 pt player defeated by an absolute system-rated -8 pt player):
    Step 1: total net score = sum of the player's ratings across the 5 targeted
            matches (each match already deducts that opponent's score points).
    Step 2: baseline reference average = (player's absolute system rating +
            mean of the 5 opponents' absolute system ratings) / 2.
    Step 3: Tournament Performance index = net score / baseline.

Decoupled subsystem (own pipeline, own state) — reuses the pre-built rating
engine (rate_sets), the manifest-verified loader, and the TennisAdapter.
Zero-hardcoding: window size, methods, field names all from config.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import List, Optional

from sport_engine.adapters.tennis import TennisAdapter
from sport_engine.compute.compute import compute_ratings
from sport_engine.compute.data_source import load_editions
from sport_engine.compute.selection import Filters, Mutes
from sport_engine.config import load_config
from sport_engine.rating.phase0 import rate_sets

REPO_ROOT = Path(__file__).resolve().parents[3]


def _fields() -> dict:
    t = load_config("tennis_schema")["fields"]
    return {
        "date": t["date"],
        "tournament": t["tournament"],
        "tour": t["tour"],
        "round": t["round"],
        "edition_year": t["edition_year"],
        "player_a": t["player_a"],
        "player_b": t["player_b"],
        "score": t["score"],
        "status": t["status"],
        "status_completed": t["status_value_completed"],
        "void_flags": tuple(t["void_flags"]),
    }


def _match_player_rating(match: dict, player: str, adapter: TennisAdapter, f: dict) -> Optional[dict]:
    """The player's Phase 0 rating for this match (their points − opponent's
    points). None when the match is not rateable (refused, never guessed)."""
    sets = adapter.extract_sets(match)
    if sets is None:
        return None
    r = rate_sets(sets)
    if match.get(f["player_a"]) == player:
        return {
            "rating": r.delta_a,
            "points": r.total_a,
            "opponent_points": r.total_b,
            "opponent": match.get(f["player_b"]),
        }
    return {
        "rating": r.delta_b,
        "points": r.total_b,
        "opponent_points": r.total_a,
        "opponent": match.get(f["player_a"]),
    }


def calibrate(net: float, player_rating: float, opponent_ratings: List[float]) -> dict:
    """Asymmetric performance calibration (Steps 2-3).

    Step 2: baseline reference average = (player's absolute system rating +
            mean of the opponents' absolute system ratings) / 2.
    Step 3: Tournament Performance index = net score / baseline.
    """
    opp_avg = sum(opponent_ratings) / len(opponent_ratings) if opponent_ratings else 0.0
    baseline = (player_rating + opp_avg) / 2
    index = None
    if baseline != 0:
        index = round(net / baseline, 4)
    return {
        "opponents_avg_rating": round(opp_avg, 2) if opponent_ratings else None,
        "baseline": round(baseline, 2),
        "index": index,
    }


def rolling_window(entries: List[dict], window: int) -> List[dict]:
    """Ingest chronologically; keep at most `window` entries, dropping the
    LOWEST historical player rating on overflow (rolling queue)."""
    queue: List[dict] = []
    for e in entries:
        queue.append(e)
        if len(queue) > window:
            queue.remove(min(queue, key=lambda x: x["rating"]))
    return queue


def tournament_performance(
    player: str,
    tournaments: List[str],
    years: List[str],
    tours: List[str],
    window: int,
    system_ratings: dict,
    mutes: Optional[Mutes] = None,
) -> dict:
    """Per-tournament performance for one player (intramural windows only)."""
    cfg = load_config("compute")
    mschema = load_config("manifest_schema")
    f = _fields()
    adapter = TennisAdapter()
    editions = load_editions(
        REPO_ROOT / cfg["data_root_relative_to_repo"], cfg["manifest_file"], mschema
    )

    per_tournament: dict = defaultdict(list)
    for edition in editions:
        tournament = edition[mschema["edition_file_tournament"]]
        if tournaments and tournament not in tournaments:
            continue
        if years and str(edition[mschema["edition_file_year"]]) not in years:
            continue
        for match in edition[mschema["edition_file_matches"]]:
            if tours and match.get(f["tour"]) not in tours:
                continue
            if mutes is not None and mutes.applies(match, f):
                continue
            if match.get(f["player_a"]) == player or match.get(f["player_b"]) == player:
                per_tournament[tournament].append(match)

    results = []
    for tournament, matches in per_tournament.items():
        matches.sort(key=lambda m: m.get(f["date"]) or "")
        entries = []
        for m in matches:
            r = _match_player_rating(m, player, adapter, f)
            if r is None:
                continue
            entries.append(
                {
                    "date": m.get(f["date"]),
                    "round": m.get(f["round"]),
                    "score": m.get(f["score"]),
                    **r,
                }
            )
        window_entries = rolling_window(entries, window)
        net = sum(e["rating"] for e in window_entries)
        opp_ratings = [system_ratings.get(e["opponent"], 0.0) for e in window_entries]
        cal = calibrate(net, system_ratings.get(player, 0.0), opp_ratings)
        results.append(
            {
                "tournament": tournament,
                "matches_in_tournament": len(entries),
                "window": window_entries,
                "window_size": len(window_entries),
                "net": net,
                **cal,
            }
        )
    results.sort(key=lambda r: r["tournament"])
    return results


def run_performance(
    player: str,
    tournaments: Optional[List[str]] = None,
    years: Optional[List[str]] = None,
    tours: Optional[List[str]] = None,
    mutes: Optional[Mutes] = None,
) -> dict:
    """Tournament Performance for one player over the selected context.

    System ratings are the absolute Phase 0 ratings computed over the same
    selected context (filters), so the baseline uses the system's own absolute
    ratings (e.g. a 73 pt player vs a -8 pt player). mutes exclude designated
    years/tournaments from both the baseline ratings and the window matches.
    """
    pcfg = load_config("performance")
    window = int(pcfg["window_size"])
    filters = Filters(tournaments=tournaments or [], years=years or [], tours=tours or [])
    mutes = mutes or Mutes()
    rating_report = compute_ratings(filters=filters, mutes=mutes)
    system_ratings = {p["player"]: float(p["rating"]) for p in rating_report["players"]}

    results = tournament_performance(
        player, tournaments or [], years or [], tours or [], window, system_ratings, mutes
    )

    return {
        "schema": "performance.1.0",
        "player": player,
        "system_rating": system_ratings.get(player, 0.0),
        "window_size": window,
        "cross_tournament_barred": bool(pcfg["cross_tournament_barred"]),
        "index_method": pcfg["index_method"],
        "results": results,
    }
