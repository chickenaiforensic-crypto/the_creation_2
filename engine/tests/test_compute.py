import json
import shutil
import tempfile
import unittest
from pathlib import Path

from sport_engine.compute.compute import compute_ratings, REPO_ROOT
from sport_engine.compute.data_source import DataIntegrityError, load_editions
from sport_engine.compute.selection import Filters, Mutes
from sport_engine.config import load_config

_DATA = load_config("test_data")
_COMPUTE = _DATA["compute"]


def _expected(key):
    return _COMPUTE["expected"][key]


class TestComputeDefaults(unittest.TestCase):
    """Feed default: Cincinnati Masters only (Director: 'only feed cincinnati_masters')."""

    def test_default_feed_counts(self):
        report = compute_ratings()
        exp = _expected("default_feed")
        self.assertEqual(report["summary"]["matches_selected"], exp["matches_selected"])
        self.assertEqual(report["summary"]["matches_rated"], exp["matches_rated"])
        self.assertEqual(report["summary"]["matches_refused"], exp["matches_refused"])

    def test_default_feed_only_cincinnati_masters(self):
        report = compute_ratings()
        tournaments = {m["tournament"] for m in report["matches"]}
        self.assertEqual(tournaments, {_COMPUTE["feed_tournament"]})

    def test_scope_editions_are_manifest_verified(self):
        report = compute_ratings()
        editions = report["scope"]["editions"]
        cfg = load_config("compute")
        manifest = json.loads(
            (REPO_ROOT / cfg["data_root_relative_to_repo"] / cfg["manifest_file"]).read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(len(editions), manifest["total_editions"])
        cincy_years = sorted(
            e["year"] for e in editions if e["tournament"] == _COMPUTE["feed_tournament"]
        )
        self.assertEqual(cincy_years, ["2021", "2022", "2023", "2024", "2025"])


class TestFilters(unittest.TestCase):
    def test_year_filter(self):
        report = compute_ratings(filters=Filters(years=[_COMPUTE["year_2025"]]))
        exp = _expected("year_2025")
        self.assertEqual(report["summary"]["matches_selected"], exp["matches_selected"])
        self.assertEqual(report["summary"]["matches_rated"], exp["matches_rated"])
        self.assertEqual(report["summary"]["matches_refused"], exp["matches_refused"])
        years = {m["year"] for m in report["matches"]}
        self.assertEqual(years, {_COMPUTE["year_2025"]})

    def test_player_filter_single_match(self):
        report = compute_ratings(filters=Filters(players=[_COMPUTE["vukic"]]))
        exp = _expected("vukic_all")
        self.assertEqual(report["summary"]["matches_selected"], exp["matches_selected"])
        self.assertEqual(report["summary"]["matches_rated"], exp["matches_rated"])
        row = report["matches"][0]
        self.assertTrue(row["rateable"])
        self.assertEqual(row["rating_b"], exp["rating"])
        players = {p["player"]: p for p in report["players"]}
        self.assertEqual(players[_COMPUTE["vukic"]]["rating"], exp["rating"])
        self.assertEqual(players[_COMPUTE["vukic"]]["average"], exp["average"])

    def test_player_and_year_filter(self):
        report = compute_ratings(
            filters=Filters(players=[_COMPUTE["sinner"]], years=[_COMPUTE["year_2021"]])
        )
        exp = _expected("sinner_2021")
        self.assertEqual(report["summary"]["matches_selected"], exp["matches_selected"])
        self.assertEqual(report["summary"]["matches_rated"], exp["matches_rated"])
        self.assertEqual(report["summary"]["matches_refused"], exp["matches_refused"])
        players = {p["player"]: p for p in report["players"]}
        self.assertIn(_COMPUTE["sinner"], players)
        self.assertEqual(players[_COMPUTE["sinner"]]["rating"], exp["rating"])
        self.assertEqual(players[_COMPUTE["sinner"]]["matches"], exp["matches_rated"])
        self.assertEqual(players[_COMPUTE["sinner"]]["average"], exp["average"])

    def test_tier_filter(self):
        report = compute_ratings(filters=Filters(tiers=[_COMPUTE["tier_m1000"]]))
        exp = _expected("tier_all")
        self.assertEqual(report["summary"]["matches_selected"], exp["matches_selected"])
        self.assertEqual(report["summary"]["matches_rated"], exp["matches_rated"])

    def test_unknown_tournament_yields_nothing(self):
        report = compute_ratings(filters=Filters(tournaments=["Not A Tournament"]))
        self.assertEqual(report["summary"]["matches_selected"], 0)
        self.assertEqual(report["summary"]["matches_rated"], 0)


class TestMutes(unittest.TestCase):
    def test_mute_year(self):
        report = compute_ratings(mutes=Mutes(mute_years=[_COMPUTE["year_2025"]]))
        exp = _expected("mute_year_2025")
        self.assertEqual(report["summary"]["matches_selected"], exp["matches_selected"])
        self.assertEqual(report["summary"]["matches_rated"], exp["matches_rated"])
        self.assertEqual(report["summary"]["matches_refused"], exp["matches_refused"])
        years = {m["year"] for m in report["matches"]}
        self.assertNotIn(_COMPUTE["year_2025"], years)

    def test_mute_tournament(self):
        report = compute_ratings(
            mutes=Mutes(mute_tournaments=[_COMPUTE["feed_tournament"]])
        )
        exp = _expected("mute_tournament")
        self.assertEqual(report["summary"]["matches_selected"], exp["matches_selected"])

    def test_mute_composes_with_player_filter(self):
        report = compute_ratings(
            filters=Filters(players=[_COMPUTE["sinner"]]),
            mutes=Mutes(mute_years=[_COMPUTE["year_2025"]]),
        )
        exp = _expected("sinner_mute_2025")
        self.assertEqual(report["summary"]["matches_selected"], exp["matches_selected"])
        self.assertEqual(report["summary"]["matches_rated"], exp["matches_rated"])
        self.assertEqual(report["summary"]["matches_refused"], exp["matches_refused"])


class TestMatchLevel(unittest.TestCase):
    def setUp(self):
        self.report = compute_ratings()

    def _row(self, year, round_, player_a, player_b):
        for m in self.report["matches"]:
            if (
                m["year"] == year
                and m["round"] == round_
                and m["player_a"] == player_a
                and m["player_b"] == player_b
            ):
                return m
        self.fail(f"row not found: {year} {round_} {player_a} vs {player_b}")

    def test_rateable_row(self):
        c = _COMPUTE["match_checks"][0]
        row = self._row(c["year"], c["round"], c["player_a"], c["player_b"])
        self.assertTrue(row["rateable"])
        self.assertEqual(row["rating_a"], c["expected_rating_a"])
        self.assertEqual(row["rating_b"], c["expected_rating_b"])
        self.assertEqual(row["points_a"], c["expected_points_a"])
        self.assertEqual(row["points_b"], c["expected_points_b"])

    def test_refused_row_has_reason(self):
        c = _COMPUTE["match_checks"][1]
        row = self._row(c["year"], c["round"], c["player_a"], c["player_b"])
        self.assertFalse(row["rateable"])
        self.assertIn(c["expected_reason_contains"], row["reason"])

    def test_report_matches_balance(self):
        rated = sum(1 for m in self.report["matches"] if m["rateable"])
        refused = sum(1 for m in self.report["matches"] if not m["rateable"])
        self.assertEqual(rated, self.report["summary"]["matches_rated"])
        self.assertEqual(refused, self.report["summary"]["matches_refused"])
        self.assertEqual(
            self.report["summary"]["matches_selected"],
            self.report["summary"]["matches_rated"] + self.report["summary"]["matches_refused"],
        )


class TestDataIntegrity(unittest.TestCase):
    def test_tampered_edition_raises(self):
        cfg = load_config("compute")
        mschema = load_config("manifest_schema")
        src_root = REPO_ROOT / cfg["data_root_relative_to_repo"]
        manifest = json.loads((src_root / cfg["manifest_file"]).read_text(encoding="utf-8"))

        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            one = manifest[mschema["manifest_editions"]][0]
            edition_file = Path(one[mschema["edition_file_path"]])
            dest_edition = tmp_root / edition_file
            dest_edition.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src_root / edition_file, dest_edition)
            # tamper: append marker bytes -> checksum no longer matches manifest
            dest_edition.write_bytes(dest_edition.read_bytes() + _COMPUTE["tamper_marker"].encode())
            (tmp_root / cfg["manifest_file"]).write_text(
                json.dumps(
                    {
                        mschema["manifest_editions"]: [
                            {k: v for k, v in entry.items()}
                            for entry in manifest[mschema["manifest_editions"]][:1]
                        ]
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaises(DataIntegrityError):
                load_editions(tmp_root, cfg["manifest_file"], mschema)


if __name__ == "__main__":
    unittest.main()
