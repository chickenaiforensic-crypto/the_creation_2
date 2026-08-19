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
from sport_engine.compute.selection import Filters, Mutes
from sport_engine.config import load_config
from sport_engine.h2h.h2h import h2h_percentage, run_h2h

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
        "h2h_ui": ui["h2h"],
        "mute_ui": ui["mute"],
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


def matchup_report(
    player_a: str,
    player_b: str,
    tournaments: Optional[List[str]] = None,
    years: Optional[List[str]] = None,
    tours: Optional[List[str]] = None,
    from_date: Optional[str] = None,
) -> dict:
    """H2H + rating + prediction-vector state for a player matchup.

    filters: tournaments/years/tours select the context; from_date bounds the
    H2H encounter history (date boundary). Prediction vector is zeroed until the
    predictive module is built (placeholder state per Director spec).
    """
    ui = load_config("ui")
    filters = Filters(
        players=[player_a, player_b],
        tournaments=tournaments or [],
        years=years or [],
        tours=tours or [],
    )
    mutes = Mutes()
    report = run_h2h(filters=filters, mutes=mutes)
    rating_report = compute_ratings(filters=filters, mutes=mutes)

    # H2H encounters within the date boundary, chronological
    encounters = [
        m
        for m in report["matches"]
        if m["rateable"] and (from_date is None or (m["date"] or "") >= from_date)
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

    # H2H percentage — isolated historical profile of the explicit pair:
    # only DIRECT pA-vs-pB encounters are aggregated (the standalone H2H module
    # sums each player's rating points across those matches, then converts the
    # absolute totals into a relative balance out of 100%, linear baseline).
    direct = [
        m
        for m in encounters
        if {m["player_a"], m["player_b"]} == {player_a, player_b}
    ]
    points_a = sum(m["h2h_a"] for m in direct if m["player_a"] == player_a)
    points_a += sum(m["h2h_b"] for m in direct if m["player_b"] == player_a)
    points_b = sum(m["h2h_b"] for m in direct if m["player_b"] == player_b)
    points_b += sum(m["h2h_a"] for m in direct if m["player_a"] == player_b)
    percentage = h2h_percentage(points_a, points_b)

    return {
        "matchup": {"player_a": player_a, "player_b": player_b},
        "scope": {
            "tournaments": list(filters.tournaments),
            "years": list(filters.years),
            "tours": list(filters.tours),
            "from_date": from_date,
        },
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
            "direct_encounter_count": len(direct),
            "encounters": encounters,
            "direct_encounters": direct,
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
