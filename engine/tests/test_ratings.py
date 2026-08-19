import unittest

from sport_engine.compute.selection import Mutes, year_range
from sport_engine.config import load_config
from sport_engine.ratings.ratings import run_ratings
from sport_engine.ui.api import ratings_report

_DATA = load_config("test_data")
_R = _DATA["ratings"]


class TestYearRange(unittest.TestCase):
    """A single selected year must mean ONE year — not a range silently
    extended to the data's edge (the 'selected one year, saw all years' bug)."""

    def test_single_from_is_single_year(self):
        self.assertEqual(year_range("2024", None), ["2024"])

    def test_single_to_is_single_year(self):
        self.assertEqual(year_range(None, "2024"), ["2024"])

    def test_neither_is_all(self):
        self.assertEqual(year_range(None, None), [])

    def test_both_is_inclusive_range(self):
        self.assertEqual(year_range("2024", "2025"), ["2024", "2025"])

    def test_reversed_range_is_swapped(self):
        self.assertEqual(year_range("2025", "2024"), ["2024", "2025"])


class TestRunRatings(unittest.TestCase):
    """Ratings-only metric: a player's rating is the ACCUMULATION of their own
    Phase 0 points per match — no opponent subtraction."""

    def test_metric_definition(self):
        cfg = load_config("ratings")
        self.assertEqual(cfg["method"], "points_accumulation")
        self.assertFalse(cfg["subtract_opponent"])

    def test_sinner_cincinnati_total(self):
        r = run_ratings("Jannik Sinner", tournaments=["Cincinnati Masters"])
        exp = _R["sinner_cincinnati"]
        self.assertEqual(r["rating"], exp["rating"])
        self.assertEqual(r["matches_rated"], exp["matches_rated"])
        by_year = {x["year"]: x["points"] for x in r["per_year"]}
        self.assertEqual(by_year, exp["per_year"])

    def test_year_period(self):
        r = run_ratings(
            "Jannik Sinner", tournaments=["Cincinnati Masters"],
            years_from="2024", years_to="2024",
        )
        exp = _R["sinner_cincinnati_2024"]
        self.assertEqual(r["rating"], exp["rating"])
        self.assertEqual(r["matches_rated"], exp["matches_rated"])

    def test_single_year_from_only(self):
        # selecting only From=2024 must return 2024 ONLY (not 2024+2025)
        r = run_ratings(
            "Jannik Sinner", tournaments=["Cincinnati Masters"], years_from="2024",
        )
        exp = _R["sinner_cincinnati_2024"]
        self.assertEqual(r["rating"], exp["rating"])
        self.assertEqual([x["year"] for x in r["per_year"]], ["2024"])

    def test_no_opponent_subtraction(self):
        # the rating equals the sum of the player's own points across matches,
        # NOT the delta rating (which subtracts opponents' points)
        r = run_ratings("Jannik Sinner", tournaments=["Cincinnati Masters"])
        self.assertEqual(r["rating"], sum(m["points"] for m in r["matches"]))
        # Sinner's Phase 0 delta rating over the same scope is +106 (see
        # ratings_percentage tests) — far below the 274 accumulated points,
        # proving no subtraction is applied here.
        self.assertNotEqual(r["rating"], 106)

    def test_mute_years_excluded(self):
        full = run_ratings("Jannik Sinner", tournaments=["Cincinnati Masters"])
        muted = run_ratings(
            "Jannik Sinner", tournaments=["Cincinnati Masters"],
            mutes=Mutes(mute_years=["2024"]),
        )
        self.assertEqual(muted["rating"], full["rating"] - _R["sinner_cincinnati"]["per_year"]["2024"])

    def test_no_data_player(self):
        # Elsa Jacquemot (WTA) has no Cincinnati Masters matches
        r = run_ratings("Elsa Jacquemot", tournaments=["Cincinnati Masters"])
        self.assertEqual(r["rating"], 0)
        self.assertEqual(r["matches_rated"], 0)
        self.assertEqual(r["matches"], [])


class TestRatingsReport(unittest.TestCase):
    def test_ratings_report_endpoint(self):
        r = ratings_report("Carlos Alcaraz", tournaments=["Cincinnati Masters"])
        self.assertEqual(r["rating"], _R["alcaraz_cincinnati"]["rating"])
        self.assertEqual(r["matches_rated"], _R["alcaraz_cincinnati"]["matches_rated"])
        # UI labels attached for the frontend
        self.assertIn("ui", r)
        self.assertTrue(r["ui"]["total_label"])

    def test_ratings_ui_manifest_exposed(self):
        from sport_engine.ui.api import ui_manifest
        m = ui_manifest()
        self.assertIn("ratings", m["tabs"])
        self.assertIn("ratings", m)
        self.assertTrue(m["ratings"]["title"])


if __name__ == "__main__":
    unittest.main()
