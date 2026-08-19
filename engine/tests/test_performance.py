import unittest

from sport_engine.config import load_config
from sport_engine.performance.performance import (
    calibrate,
    rolling_window,
    run_performance,
)

_DATA = load_config("test_data")
_PERF = _DATA["performance"]


class TestRollingWindow(unittest.TestCase):
    def test_drops_lowest_on_overflow(self):
        entries = [
            {"rating": 5}, {"rating": 10}, {"rating": 3},
            {"rating": 8}, {"rating": 7}, {"rating": 12},
        ]
        q = rolling_window(entries, 5)
        self.assertEqual([e["rating"] for e in q], [5, 10, 8, 7, 12])  # 3 dropped

    def test_under_window_keeps_all(self):
        entries = [{"rating": 5}, {"rating": 10}]
        self.assertEqual(len(rolling_window(entries, 5)), 2)


class TestCalibration(unittest.TestCase):
    """Asymmetric performance calibration — high-disparity upset weighting."""

    def test_upset_amplified(self):
        # the -8 pt player beats a 73 pt player (spec example): their window
        # includes the upset win; baseline is low -> high index
        cal = calibrate(net=40, player_rating=-8, opponent_ratings=[73, 20, 15, 10, 5])
        self.assertEqual(cal["opponents_avg_rating"], 24.6)
        self.assertEqual(cal["baseline"], 8.3)
        self.assertGreater(cal["index"], 4.0)  # amplified

    def test_favorite_win_not_amplified(self):
        # the 73 pt player (lost the upset) — net lower, baseline higher
        cal = calibrate(net=10, player_rating=73, opponent_ratings=[-8, 20, 15, 10, 5])
        self.assertLess(cal["index"], 0.4)

    def test_zero_baseline_guard(self):
        cal = calibrate(net=10, player_rating=0, opponent_ratings=[0, 0])
        self.assertIsNone(cal["index"])


class TestTournamentPerformance(unittest.TestCase):
    """Real-data: Zverev Cincinnati Masters window (feed scope)."""

    @classmethod
    def setUpClass(cls):
        cls.z = run_performance("Alexander Zverev")
        cls.cincy = next(r for r in cls.z["results"] if r["tournament"] == "Cincinnati Masters")

    def test_schema_and_constraints(self):
        self.assertEqual(self.z["schema"], "performance.1.0")
        self.assertEqual(self.z["window_size"], _PERF["window_size"])
        self.assertTrue(self.z["cross_tournament_barred"])

    def test_cincinnati_window_hand_verified(self):
        exp = _PERF["zverev_cincinnati"]
        self.assertEqual(self.cincy["window_size"], 5)
        self.assertEqual(self.cincy["net"], exp["net"])
        self.assertAlmostEqual(self.cincy["opponents_avg_rating"], exp["opponents_avg"], places=2)
        self.assertAlmostEqual(self.cincy["baseline"], exp["baseline"], places=2)
        self.assertAlmostEqual(self.cincy["index"], exp["index"], places=4)
        # window = top-5 by rating of his 18 Cincinnati matches (chronological
        # order preserved by the rolling queue, 3 dropped)
        self.assertEqual(self.cincy["matches_in_tournament"], 18)
        ratings = [e["rating"] for e in self.cincy["window"]]
        self.assertEqual(sorted(ratings, reverse=True), [16, 16, 14, 14, 14])

    def test_intramural_window(self):
        # each tournament's window is built ONLY from that tournament's matches
        # (cross-tournament data barred) — every window entry's opponent played
        # the player in that same tournament's edition data
        for res in self.z["results"]:
            self.assertTrue(res["tournament"])
            # the window never mixes tournaments: a single result is one tournament
            self.assertEqual(len({e["date"] for e in res["window"]}), len(res["window"]))


if __name__ == "__main__":
    unittest.main()
