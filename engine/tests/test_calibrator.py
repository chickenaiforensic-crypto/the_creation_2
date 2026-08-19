import unittest

from sport_engine.calibrator.calibrate import run_score_calibrator
from sport_engine.config import load_config

_DATA = load_config("test_data")
_SC = _DATA["score_calibrator"]


class TestScoreCalibratorCentral(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_score_calibrator()

    def test_schema_scope_method(self):
        self.assertEqual(self.report["schema"], "score_calibrator.1.0")
        self.assertEqual(self.report["scope"], "central")
        self.assertEqual(self.report["method"], _SC["method"])
        self.assertEqual(self.report["years"], _SC["years"])

    def test_not_applied(self):
        # Director decision: calibration dropped, raw points used
        self.assertFalse(self.report["applied"])

    def test_pooled_players(self):
        self.assertEqual(self.report["pooled_players"], _SC["pooled_players"])

    def test_all_regions_1st_to_last(self):
        # every leaderboard region present: 1,2,3,5,9,17,33,(65)
        expected = set(_SC["regions"])
        self.assertEqual(set(self.report["regions"].keys()), expected)
        # region counts match expectations
        for pos, n in _SC["region_counts"]:
            self.assertEqual(self.report["regions"][pos]["count"], n, f"region {pos}")

    def test_central_adjustments_all_zero(self):
        for pos, adj in self.report["adjustments"].items():
            self.assertEqual(adj, 0.0, f"region {pos} adjustment should be 0.0")

    def test_raw_equals_calibrated_accuracy(self):
        self.assertTrue(self.report["accuracy"]["equal"])
        self.assertGreaterEqual(self.report["accuracy"]["raw"], _SC["accuracy_target"])

    def test_per_year_scope_present(self):
        py = self.report["per_year_adjustments"]
        self.assertEqual(set(py.keys()), set(_SC["years"]))
        all_regions = set(_SC["regions"])
        for year, adj in py.items():
            self.assertTrue(set(adj.keys()) <= all_regions, f"{year} has unknown region")
        # 56-draw years (2021-2024) have no 65th region; 2025 (96-draw) has all 8
        for year in ("2021", "2022", "2023", "2024"):
            self.assertNotIn(65, py[year], f"{year} should not have a 65th region")
        self.assertEqual(set(py["2025"].keys()), all_regions)

    def test_targets_ordered(self):
        targets = self.report["targets"]
        positions = sorted(targets)
        for a, b in zip(positions, positions[1:]):
            self.assertGreaterEqual(targets[a], targets[b] - 1e-9)


if __name__ == "__main__":
    unittest.main()
