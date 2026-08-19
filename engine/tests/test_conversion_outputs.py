import unittest

from sport_engine.config import load_config
from sport_engine.ui.api import matchup_report, performance_report

_DATA = load_config("test_data")
_RP = _DATA["ratings_percentage"]
_PP = _DATA["performance_percentage"]


class TestRatingsPercentage(unittest.TestCase):
    """Ratings layer feeds the standalone conversion layer — independent
    sectional output over a selectable year range (default 2021-2025)."""

    def test_feed_default_range(self):
        r = matchup_report("Jannik Sinner", "Carlos Alcaraz")
        exp = _RP["sinner_alcaraz_feed"]
        p = r["ratings_percentage"]
        self.assertAlmostEqual(p["points_a"], exp["points_a"], places=2)
        self.assertAlmostEqual(p["points_b"], exp["points_b"], places=2)
        self.assertAlmostEqual(p["pA_pct"], exp["pA_pct"], places=2)
        self.assertAlmostEqual(p["pB_pct"], exp["pB_pct"], places=2)

    def test_selectable_range_2024(self):
        r = matchup_report("Jannik Sinner", "Carlos Alcaraz",
                           years_from="2024", years_to="2024")
        exp = _RP["sinner_alcaraz_2024"]
        p = r["ratings_percentage"]
        self.assertAlmostEqual(p["pA_pct"], exp["pA_pct"], places=2)
        self.assertAlmostEqual(p["pB_pct"], exp["pB_pct"], places=2)
        self.assertEqual(r["scope"]["ratings_range"], {"from": "2024", "to": "2024"})

    def test_ratings_displayed_alongside(self):
        r = matchup_report("Jannik Sinner", "Carlos Alcaraz")
        self.assertEqual(r["players"]["player_a"]["system_rating"]["rating"], 106)
        self.assertEqual(r["players"]["player_b"]["system_rating"]["rating"], 70)


class TestPerformancePercentage(unittest.TestCase):
    """Tournament Performance layer also computes a 100% output between the two
    players (per tournament, via the standalone conversion layer)."""

    def test_per_tournament_percentages(self):
        p = performance_report("Jannik Sinner", "Alexander Zverev")
        by = {x["tournament"]: x for x in p["percentages"]}
        for tournament, exp in _PP["sinner_zverev"].items():
            self.assertIn(tournament, by, tournament)
            self.assertAlmostEqual(by[tournament]["points_a"], exp["points_a"], places=2)
            self.assertAlmostEqual(by[tournament]["points_b"], exp["points_b"], places=2)
            self.assertAlmostEqual(by[tournament]["pA_pct"], exp["pA_pct"], places=2)
            self.assertAlmostEqual(by[tournament]["pB_pct"], exp["pB_pct"], places=2)

    def test_performance_has_both_players_and_labels(self):
        p = performance_report("Jannik Sinner", "Alexander Zverev")
        self.assertIn("player_a", p)
        self.assertIn("player_b", p)
        self.assertTrue(p["percentage_label"])
        self.assertTrue(p["performance_label"])


if __name__ == "__main__":
    unittest.main()
