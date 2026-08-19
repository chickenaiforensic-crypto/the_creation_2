import unittest

from sport_engine.config import load_config
from sport_engine.convert.ratio import ratio_lock, region_points, region_points_for_set

_DATA = load_config("test_data")
_PCT = _DATA["h2h"]["percentage"]


class TestRatioLock(unittest.TestCase):
    """Standalone conversion layer — every section plugs in; sectional answers
    are independent (no shared state between calls)."""

    def test_theory_table(self):
        # Director theory table (§3.6): raw region point totals -> %
        for case in _PCT["cases"]:
            with self.subTest(case["label"]):
                r = ratio_lock(case["points_a"], case["points_b"])
                self.assertAlmostEqual(r["pA_pct"], case["pA_pct"], places=2)
                self.assertAlmostEqual(r["pB_pct"], case["pB_pct"], places=2)

    def test_differential_rejected(self):
        with self.assertRaises(ValueError):
            ratio_lock(12, -12)  # +12/-12 is the rating, not raw points

    def test_zero_total(self):
        r = ratio_lock(0, 0)
        self.assertIsNone(r["pA_pct"])
        self.assertIsNone(r["pB_pct"])

    def test_scaling_from_config(self):
        r = ratio_lock(20, 8)
        self.assertEqual(r["scaling"], "linear")
        self.assertFalse(r["exponential_enabled"])

    def test_independent_sectional_answers(self):
        # two sections calling the layer get their own answer, no cross-talk
        a = ratio_lock(20, 8)   # 71.43/28.57
        b = ratio_lock(20, 14)  # 58.82/41.18
        self.assertAlmostEqual(a["pA_pct"], 71.43, places=2)
        self.assertAlmostEqual(b["pA_pct"], 58.82, places=2)


class TestRegionPoints(unittest.TestCase):
    def test_theory_table_matches(self):
        cases = [
            ([(6, 0), (6, 0)], 20, 4),
            ([(6, 4), (6, 4)], 20, 8),
            ([(6, 2), (6, 3)], 20, 6),
            ([(7, 6), (7, 6)], 20, 14),  # 7-6 -> 6-5 -> 10/7 per set
        ]
        for sets, ea, eb in cases:
            with self.subTest(sets):
                r = region_points(sets)
                self.assertEqual(r["region_points_a"], ea)
                self.assertEqual(r["region_points_b"], eb)

    def test_region_points_for_set(self):
        self.assertEqual(region_points_for_set(6, 4), (10, 4))
        self.assertEqual(region_points_for_set(7, 6), (10, 7))  # 7-6 -> 6-5
        self.assertEqual(region_points_for_set(7, 5), (10, 4))  # 7-5 -> 6-4
        self.assertEqual(region_points_for_set(8, 6), (10, 4))  # 8-6 -> 7-5 -> 6-4
        self.assertEqual(region_points_for_set(6, 2), (10, 2))

    def test_tied_set_rejected(self):
        with self.assertRaises(ValueError):
            region_points_for_set(6, 6)


if __name__ == "__main__":
    unittest.main()
