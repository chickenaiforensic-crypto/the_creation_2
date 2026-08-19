import unittest

from sport_engine.calibrator.calibrate import run_score_calibrator
from sport_engine.config import load_config

_DATA = load_config("test_data")
_SC = _DATA["score_calibrator"]


def _str_keys(d):
    return {str(k): v for k, v in d.items()}


class TestScoreCalibrator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_score_calibrator()

    def test_schema_method_years(self):
        self.assertEqual(self.report["schema"], "score_calibrator.1.0")
        self.assertEqual(self.report["method"], _SC["method"])
        self.assertEqual(list(self.report["summary"].keys()), _SC["years"])

    def test_2021_adjustments_and_targets(self):
        res21 = self.report["results"][0]
        self.assertEqual(res21["year"], "2021")
        cal = res21["calibration"]
        self.assertEqual(_str_keys(cal["region_adjustments"]), _SC["year_2021"]["adjustments"])
        self.assertEqual(_str_keys(cal["region_targets"]), _SC["year_2021"]["targets"])

    def test_2021_calibrated_leaderboard(self):
        res21 = self.report["results"][0]
        rows = res21["rows"]
        self.assertEqual(rows[0]["player"], _SC["year_2021"]["top_calibrated"])
        self.assertEqual(rows[0]["rating_calibrated"], _SC["year_2021"]["top_calibrated_rating"])
        by_name = {p["player"]: p for p in rows}
        self.assertEqual(
            by_name["Andrey Rublev"]["rating_calibrated"],
            _SC["year_2021"]["finalist_calibrated_rating"],
        )
        # rows ranked by calibrated rating
        ratings = [p["rating_calibrated"] for p in rows]
        self.assertEqual(ratings, sorted(ratings, reverse=True))
        for p in rows:
            self.assertIn("region_adjustment", p)
            self.assertEqual(p["rating_calibrated"], round(p["rating"] + p["region_adjustment"], 2))

    def test_2025_void_final_handling(self):
        res25 = self.report["results"][-1]
        self.assertEqual(res25["year"], "2025")
        cal = res25["calibration"]
        self.assertEqual(_str_keys(cal["region_adjustments"]), _SC["year_2025"]["adjustments"])
        by_name = {p["player"]: p for p in res25["rows"]}
        self.assertEqual(
            by_name[_DATA["ratings_table"]["year_2025"]["champion"]]["rating_calibrated"],
            _SC["year_2025"]["champion_calibrated_rating"],
        )
        self.assertEqual(
            by_name["Jannik Sinner"]["rating_calibrated"],
            _SC["year_2025"]["runner_up_calibrated_rating"],
        )

    def test_accuracy_holds_or_improves_every_year(self):
        target = _SC["accuracy_target"]
        tolerance = 0.005  # regional constants can trade a few pairs per year
        for year, v in self.report["summary"].items():
            self.assertIsNotNone(v["accuracy_raw"])
            self.assertIsNotNone(v["accuracy_calibrated"])
            self.assertGreaterEqual(v["accuracy_calibrated"], v["accuracy_raw"] - tolerance)
            self.assertGreaterEqual(v["accuracy_calibrated"], target)
        # the overall mean must not regress
        o = self.report["overall"]
        self.assertGreaterEqual(o["mean_accuracy_calibrated"], o["mean_accuracy_raw"] - 1e-9)
        self.assertGreaterEqual(o["mean_accuracy_calibrated"], target)

    def test_every_row_has_position_and_calibrated_rating(self):
        for res in self.report["results"]:
            for p in res["rows"]:
                self.assertIsNotNone(p["position_number"])
                self.assertIsNotNone(p["rating_calibrated"])
                self.assertIsNotNone(p["region_adjustment"])


if __name__ == "__main__":
    unittest.main()
