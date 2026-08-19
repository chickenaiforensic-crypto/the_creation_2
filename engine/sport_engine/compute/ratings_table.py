"""Ratings table view — per-(year, tournament) Phase 0 ratings tables with the
actual-performance position column, for the UI's selectable year/tournament filters.

Zero-hardcoding: years, tournaments, players, round names, and position numbers all
come from the data and config — never from code. The caller selects the view with
Filters (year, tournament); the feed scope (config) still applies.
"""

from __future__ import annotations

from collections import defaultdict
from typing import List, Optional

from sport_engine.compute.compute import (
    REPO_ROOT,
    _aggregate,
    compute_ratings,
    field_names,
)
from sport_engine.compute.data_source import load_editions
from sport_engine.compute.selection import Filters, Mutes
from sport_engine.config import load_config


def _position_rules() -> dict:
    return load_config("position_rules")


def _ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def _derive_positions(editions: List[dict], mschema: dict, f: dict) -> dict:
    """(tournament, year, player) -> (position_ordinal, round_reached_label).

    Derived from each edition's result tree using the stored winner and round
    fields; round -> position mapping comes from config (position_rules.json).
    """
    rules = _position_rules()["rounds"]
    finish: dict = {}

    def loser(match: dict) -> str:
        return match[f["player_b"]] if match[f["winner"]] == "A" else match[f["player_a"]]

    for edition in editions:
        tournament = edition[mschema["edition_file_tournament"]]
        year = str(edition[mschema["edition_file_year"]])
        by_round: dict = defaultdict(list)
        for match in edition[mschema["edition_file_matches"]]:
            by_round[match[f["round"]]].append(match)

        finals = by_round.get("F", [])
        if finals:
            fm = finals[0]
            champion = fm[f["player_a"]] if fm[f["winner"]] == "A" else fm[f["player_b"]]
            runner = loser(fm)
            fr = rules["F"]
            finish[(tournament, year, champion)] = (_ordinal(fr["winner_position"]), fr["winner_label"])
            finish[(tournament, year, runner)] = (_ordinal(fr["loser_position"]), fr["loser_label"])

        for round_name, rule in rules.items():
            if round_name == "F":
                continue
            for match in by_round.get(round_name, []):
                finish[(tournament, year, loser(match))] = (
                    _ordinal(rule["loser_position"]),
                    rule["loser_label"],
                )
    return finish


def build_ratings_table(
    filters: Optional[Filters] = None,
    mutes: Optional[Mutes] = None,
) -> dict:
    """One ratings table per (year, tournament) in the selected set.

    Filters select the view (e.g. Filters(years=[...]), Filters(tournaments=[...]));
    the feed scope from config applies underneath. Each table lists every player
    individually, ranked by engine rating (Phase 0) top to bottom, with the actual
    performance position beside them.
    """
    report = compute_ratings(filters, mutes)
    cfg = load_config("compute")
    mschema = load_config("manifest_schema")
    f = field_names()

    editions = load_editions(
        REPO_ROOT / cfg["data_root_relative_to_repo"], cfg["manifest_file"], mschema
    )
    positions = _derive_positions(editions, mschema, f)

    groups: dict = defaultdict(list)
    for row in report["matches"]:
        groups[(row["tournament"], row["year"])].append(row)

    tables = []
    for (tournament, year) in sorted(groups, key=lambda k: (k[1], k[0])):
        group = groups[(tournament, year)]
        players = _aggregate(group)
        for p in players:
            pos, rnd = positions.get((tournament, year, p["player"]), ("—", "—"))
            p["position"] = pos
            p["round_reached"] = rnd
        for rank, p in enumerate(players, 1):
            p["rank"] = rank
        rated = sum(1 for r in group if r["rateable"])
        tables.append(
            {
                "tournament": tournament,
                "year": year,
                "summary": {
                    "matches_selected": len(group),
                    "matches_rated": rated,
                    "matches_refused": len(group) - rated,
                    "players": len(players),
                },
                "rows": players,
            }
        )

    return {
        "schema": "ratings_table.1.0",
        "scope": {
            "filters": report["scope"]["filters"],
            "mutes": report["scope"]["mutes"],
        },
        "tables": tables,
    }


def render_table_text(table: dict) -> str:
    """Render one ratings table as fixed-width tabulated text (for display/copy)."""
    rows = table["rows"]
    header = [
        ("POS", ">"),
        ("PLAYER", "<"),
        ("RATING", ">"),
        ("M", ">"),
        ("AVG", ">"),
        ("POSITION", ">"),
        ("ROUND REACHED", "<"),
    ]
    if not rows:
        return f"{table['tournament']} — {table['year']}: no matches selected"

    data = []
    for p in rows:
        avg = f"{p['average']:.1f}" if p["average"] is not None else "—"
        data.append(
            [
                str(p["rank"]),
                p["player"],
                f"{p['rating']:+d}",
                str(p["matches"]),
                avg,
                p["position"],
                p["round_reached"],
            ]
        )
    widths = [
        max([len(h)] + [len(r[ci]) for r in data]) for ci, (h, _) in enumerate(header)
    ]

    def fmt(ci: int, value: str) -> str:
        return value.ljust(widths[ci]) if header[ci][1] == "<" else value.rjust(widths[ci])

    lines = [f"{table['tournament']} — {table['year']}"]
    s = table["summary"]
    lines.append(
        f"matches: selected={s['matches_selected']} rated={s['matches_rated']} "
        f"refused={s['matches_refused']} players={s['players']}"
    )
    lines.append("  ".join(fmt(ci, h) for ci, (h, _) in enumerate(header)))
    lines.append("  ".join("-" * w for w in widths))
    for r in data:
        lines.append("  ".join(fmt(ci, r[ci]) for ci in range(len(header))))
    return "\n".join(lines)
