"""SaaS UI presentation-layer API — engine side.

Every value the UI renders comes from config (ui.json, sports.json, compute.json,
tennis_schema.json) and live engine results — never from code (zero-hardcoding).

Endpoints (dicts returned by functions here; the server layer maps them to HTTP):
- ui_manifest(): everything the UI needs to render (app name, sports, labels,
  defaults, development lock status, options, prediction vector state)
- player_options(): selectable players from the feed data
- matchup_report(): H2H + rating + prediction-vector state for a player matchup
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from sport_engine.compute.compute import compute_ratings
from sport_engine.compute.data_source import load_editions
from sport_engine.compute.selection import Filters, Mutes, year_range
from sport_engine.config import load_config
from sport_engine.convert.ratio import ratio_lock
from sport_engine.h2h.h2h import run_h2h
from sport_engine.performance.performance import run_performance
from sport_engine.ratings.ratings import run_ratings

REPO_ROOT = Path(__file__).resolve().parents[3]


def _field_names() -> dict:
    t = load_config("tennis_schema")["fields"]
    return {
        "tournament": t["tournament"],
        "tour": t["tour"],
        "tier": t["tier"],
        "edition_year": t["edition_year"],
        "player_a": t["player_a"],
        "player_b": t["player_b"],
    }


def _available_options() -> dict:
    """Distinct selectable option lists from the FULL dataset (tournament, tour,
    tier, year, player) — independent of the feed scope, so the UI can constrain
    or broaden the processed dataset. All names come from the data."""
    cfg = load_config("compute")
    mschema = load_config("manifest_schema")
    f = _field_names()
    editions = load_editions(REPO_ROOT / cfg["data_root_relative_to_repo"],
                             cfg["manifest_file"], mschema)
    tournaments = set()
    tours = set()
    tiers = set()
    years = set()
    players = set()
    for edition in editions:
        for match in edition[mschema["edition_file_matches"]]:
            tournaments.add(match.get(f["tournament"]))
            tours.add(match.get(f["tour"]))
            tiers.add(match.get(f["tier"]))
            years.add(str(match.get(f["edition_year"])))
            players.add(match.get(f["player_a"]))
            players.add(match.get(f["player_b"]))
    return {
        "tournaments": sorted(x for x in tournaments if x),
        "tours": sorted(x for x in tours if x),
        "tiers": sorted(x for x in tiers if x),
        "years": sorted(x for x in years if x),
        "players": sorted(x for x in players if x),
    }


def ui_manifest() -> dict:
    ui = load_config("ui")
    sports_cfg = load_config("sports")
    compute_cfg = load_config("compute")

    feed_filters = Filters.from_config(compute_cfg["feed"])
    options = _available_options()  # full-dataset option lists
    # the tournament filter control offers ALL tournaments in the data so the
    # user can constrain OR broaden the processed dataset beyond the feed scope

    return {
        "app": ui["app"],
        "sports": ui["sports"],
        "tabs": ui["tabs"],
        "entity_labels": ui["entity_labels"],
        "matchup_selector": ui["matchup_selector"],
        "tournament_filter": ui["tournament_filter"],
        "all_tournaments": options["tournaments"],
        "development_lock": sports_cfg["development_lock"],
        "prediction_vector": {
            "placeholder_label": ui["prediction_vector"]["placeholder_label"],
            "zeroed_state_text": ui["prediction_vector"]["zeroed_state_text"],
            "vs_label": ui["prediction_vector"]["vs_label"],
            "state": "zeroed",
            "pA": None,
            "pB": None,
        },
        "system_rating_label": ui["system_rating_label"],
        "ratings_percentage": ui["ratings_percentage"],
        "ratings": ui["ratings"],
        "h2h_ui": ui["h2h"],
        "performance": ui["performance"],
        "mute_ui": ui["mute"],
        "parameters_labels": ui["parameters_labels"],
        "placeholders": ui["placeholders"],
        "options": options,
        "feed": {"tournaments": list(feed_filters.tournaments)},
        "configurations": {
            "system_configurations_label": ui["tabs"]["system_configurations_label"],
            "engine_parameters_label": ui["tabs"]["engine_parameters_label"],
            "engine_parameters": {
                "points_per_game_difference": load_config("h2h")["points_per_game_difference"],
                "feed_tournaments": list(feed_filters.tournaments),
                "development_lock_rule": sports_cfg["development_lock"]["rule"],
                "sports_exposed": sports_cfg["development_lock"]["exposed_sports"],
            },
        },
    }


def player_options() -> dict:
    ui = load_config("ui")
    options = _available_options()
    return {
        "players": options["players"],
        "tournaments": options["tournaments"],
        "years": options["years"],
        "entity_labels": ui["entity_labels"],
    }


def performance_report(
    player_a: str,
    player_b: str,
    tournaments: Optional[List[str]] = None,
    years: Optional[List[str]] = None,
    tours: Optional[List[str]] = None,
    years_from: Optional[str] = None,
    years_to: Optional[str] = None,
    mute_years: Optional[List[str]] = None,
    mute_tournaments: Optional[List[str]] = None,
) -> dict:
    """Tournament Performance (3rd UI layer) for both players over the selected
    context — per-tournament 5-match windows, intramural, absolute rating basis,
    asymmetric calibration index. The performance layer ALSO feeds the standalone
    conversion layer: for every tournament where both players have a window, the
    players' total window points become a 100% split (independent sectional
    output)."""
    ui = load_config("ui")
    range_years = year_range(
        years_from, years_to,
        ui["ratings_percentage"]["default_from_year"], ui["ratings_percentage"]["default_to_year"],
    )
    mutes = Mutes(mute_years=mute_years or [], mute_tournaments=mute_tournaments or [])
    eff_years = range_years or (list(years) if years else [])
    pa = run_performance(player_a, tournaments, eff_years, tours, mutes)
    pb = run_performance(player_b, tournaments, eff_years, tours, mutes)

    def window_points(perf) -> dict:
        out = {}
        for res in perf["results"]:
            out[res["tournament"]] = sum(e.get("points", 0.0) for e in res["window"])
        return out

    pa_pts = window_points(pa)
    pb_pts = window_points(pb)
    percentages = []
    for tournament in sorted(set(pa_pts) & set(pb_pts)):
        a, b = pa_pts[tournament], pb_pts[tournament]
        if a + b == 0:
            continue
        lock = ratio_lock(a, b)
        percentages.append(
            {
                "tournament": tournament,
                "points_a": lock["points_a"],
                "points_b": lock["points_b"],
                "pA_pct": lock["pA_pct"],
                "pB_pct": lock["pB_pct"],
            }
        )
    return {
        "performance_label": ui["performance"]["title"],
        "window_label": ui["performance"]["window_label"],
        "percentage_label": ui["performance"]["percentage_label"],
        "player_a": pa,
        "player_b": pb,
        "percentages": percentages,
    }


def ratings_report(
    player: str,
    tournaments: Optional[List[str]] = None,
    years: Optional[List[str]] = None,
    tours: Optional[List[str]] = None,
    years_from: Optional[str] = None,
    years_to: Optional[str] = None,
    mute_years: Optional[List[str]] = None,
    mute_tournaments: Optional[List[str]] = None,
) -> dict:
    """Ratings-only view (accumulated Phase 0 points, no opponent subtraction)
    for one player over a selected tournament scope + year (or year period).

    filters: tournaments/years/tours + years_from/years_to (year period) select
    the scope; mute_years/mute_tournaments EXCLUDE designated years/tournaments
    (engine Mutes)."""
    ui = load_config("ui")
    mutes = Mutes(mute_years=mute_years or [], mute_tournaments=mute_tournaments or [])
    result = run_ratings(
        player,
        tournaments=tournaments,
        years=years,
        tours=tours,
        years_from=years_from,
        years_to=years_to,
        mutes=mutes,
    )
    result["ui"] = ui["ratings"]
    return result


def matchup_report(
    player_a: str,
    player_b: str,
    tournaments: Optional[List[str]] = None,
    years: Optional[List[str]] = None,
    tours: Optional[List[str]] = None,
    from_date: Optional[str] = None,
    years_from: Optional[str] = None,
    years_to: Optional[str] = None,
    mute_years: Optional[List[str]] = None,
    mute_tournaments: Optional[List[str]] = None,
) -> dict:
    """H2H + ratings + prediction-vector state for a player matchup.

    filters: tournaments/years/tours select the context; from_date bounds the
    H2H encounter history (date boundary); years_from/years_to select the
    RATINGS range (default: the full dataset, 2021-2025); mute_years /
    mute_tournaments EXCLUDE designated years/tournaments from computation
    (engine Mutes). Prediction vector is zeroed until the predictive module is
    built (placeholder state per spec).
    """
    ui = load_config("ui")
    range_years = year_range(
        years_from, years_to,
        ui["ratings_percentage"]["default_from_year"], ui["ratings_percentage"]["default_to_year"],
    )
    # An explicit `years` list (caller) wins over the ratings range; otherwise
    # the ratings range selects the year scope (default: full dataset).
    effective_years = list(years) if years else range_years
    filters = Filters(
        players=[player_a, player_b],
        tournaments=tournaments or [],
        years=effective_years,
        tours=tours or [],
    )
    mutes = Mutes(mute_years=mute_years or [], mute_tournaments=mute_tournaments or [])
    report = run_h2h(filters=filters, mutes=mutes)
    rating_report = compute_ratings(filters=filters, mutes=mutes)

    # H2H encounters = DIRECT pA-vs-pB meetings only, within the date boundary,
    # chronological. A player's own non-head-to-head matches are their context
    # (rating panel), not encounters — two players who never met must output
    # "no encounter".
    encounters = [
        m
        for m in report["matches"]
        if m["rateable"]
        and (from_date is None or (m["date"] or "") >= from_date)
        and {m["player_a"], m["player_b"]} == {player_a, player_b}
    ]
    encounters.sort(key=lambda m: m["date"] or "")

    by_player = {p["player"]: p for p in report["players"]}
    ratings = {p["player"]: p for p in rating_report["players"]}

    def player_payload(name: str) -> dict:
        h = by_player.get(name)
        r = ratings.get(name)
        return {
            "player": name,
            "h2h": {
                "matches": h["matches"] if h else 0,
                "game_difference": h["game_difference"] if h else 0,
                "average": h["average"] if h else None,
                "refused": h["refused"] if h else 0,
                "tournaments": h["tournaments"] if h else [],
            },
            "system_rating": {
                "rating": r["rating"] if r else 0,
                "matches": r["matches"] if r else 0,
                "average": r["average"] if r else None,
            },
        }

    net = 0
    for m in encounters:
        if m["player_a"] == player_a:
            net += m["h2h_a"]
        else:
            net += m["h2h_b"]

    # H2H percentage — isolated historical profile of the explicit pair from
    # their DIRECT encounters. The lock uses each player's RAW REGION POINT
    # TOTALS across those matches (non-negative), NOT the differential rating:
    # %A = pointsA / (pointsA + pointsB).
    points_a = 0.0
    points_b = 0.0
    for m in encounters:
        if m["player_a"] == player_a:
            points_a += m["region_points_a"]
            points_b += m["region_points_b"]
        else:  # the requested player is on side B
            points_b += m["region_points_a"]
            points_a += m["region_points_b"]
    percentage = ratio_lock(points_a, points_b)

    # RATINGS percentage — the ratings layer also feeds the standalone
    # conversion layer: each player's total Phase 0 points gathered over the
    # selected range (years_from/years_to, default 2021-2025) become the
    # non-negative raw totals for the ratio lock. Ratings themselves (deltas)
    # are exposed alongside for display.
    def player_points(name: str) -> float:
        total = 0.0
        for m in rating_report["matches"]:
            if not m["rateable"]:
                continue
            if m["player_a"] == name:
                total += m["points_a"]
            elif m["player_b"] == name:
                total += m["points_b"]
        return total

    ratings_pa = player_points(player_a)
    ratings_pb = player_points(player_b)
    # no-data guard: if either player has ZERO rated matches in the selected
    # scope, the percentage is a no-data state (null), not 0%/100% — that would
    # misrepresent "no matches in scope" as "scored zero".
    def rated_matches(name: str) -> int:
        return sum(
            1
            for m in rating_report["matches"]
            if m["rateable"] and (m["player_a"] == name or m["player_b"] == name)
        )

    if rated_matches(player_a) == 0 or rated_matches(player_b) == 0:
        ratings_percentage = {
            "points_a": None,
            "points_b": None,
            "pA_pct": None,
            "pB_pct": None,
            "scaling": "linear",
            "exponential_enabled": False,
            "no_data": True,
        }
    else:
        ratings_percentage = ratio_lock(ratings_pa, ratings_pb)

    return {
        "matchup": {"player_a": player_a, "player_b": player_b},
        "scope": {
            "tournaments": list(filters.tournaments),
            "years": list(filters.years),
            "tours": list(filters.tours),
            "from_date": from_date,
            "ratings_range": {"from": years_from, "to": years_to},
            "mutes": mutes.as_dict(),
        },
        "ratings_percentage": ratings_percentage,
        "prediction_vector": {
            "placeholder_label": ui["prediction_vector"]["placeholder_label"],
            "zeroed_state_text": ui["prediction_vector"]["zeroed_state_text"],
            "state": "zeroed",
            "pA": None,
            "pB": None,
        },
        "h2h": {
            "net_h2h_balance": net,
            "encounter_count": len(encounters),
            "direct_encounter_count": len(encounters),
            "encounters": encounters,
            "direct_encounters": encounters,
            "percentage": percentage,
            "percentage_label": ui["h2h"]["percentage_label"],
            "drilldown_title": ui["h2h"]["score_sheet_title"],
            "no_data_text": ui["h2h"]["no_data_text"],
        },
        "players": {
            "player_a": player_payload(player_a),
            "player_b": player_payload(player_b),
        },
    }
