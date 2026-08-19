import unittest

from sport_engine.rating.phase0 import (
    RatingError,
    normalize_set,
    rate_sets,
)


def load_test_data():
    from sport_engine.config import load_config

    return load_config("test_data")


_DATA = load_test_data()


class TestWorkedExample(unittest.TestCase):
    def test_director_worked_example(self):
        ex = _DATA["worked_example"]
        r = rate_sets(ex["sets"])
        self.assertEqual(r.total_a, ex["total_a"])
        self.assertEqual(r.total_b, ex["total_b"])
        self.assertEqual(r.delta_a, ex["delta_a"])
        self.assertEqual(r.delta_b, ex["delta_b"])

    def test_worked_example_per_set_points(self):
        ex = _DATA["worked_example"]
        r = rate_sets(ex["sets"])
        expected = [tuple(p) for p in ex["per_set_points"]]
        actual = [(s.points_a, s.points_b) for s in r.sets]
        self.assertEqual(actual, expected)


class TestNormalization(unittest.TestCase):
    def test_cases(self):
        for case in _DATA["normalization_cases"]:
            with self.subTest(case["label"]):
                a, b = case["input"]
                ea, eb = case["expected"]
                self.assertEqual(normalize_set(a, b), (ea, eb))


class TestRejectedSets(unittest.TestCase):
    def test_raises(self):
        for case in _DATA["rejected_sets"]:
            with self.subTest(case["label"]):
                with self.assertRaises(RatingError):
                    normalize_set(*case["input"])


class TestMatchExamples(unittest.TestCase):
    def test_examples(self):
        for ex in _DATA["match_examples"]:
            with self.subTest(ex["label"]):
                r = rate_sets(ex["sets"])
                self.assertEqual(r.total_a, ex["total_a"])
                self.assertEqual(r.total_b, ex["total_b"])
                self.assertEqual(r.delta_a, ex["delta_a"])
                self.assertEqual(r.delta_b, ex["delta_b"])

    def test_example_per_set_points(self):
        for ex in _DATA["match_examples"]:
            if "per_set_points" not in ex:
                continue
            with self.subTest(ex["label"]):
                r = rate_sets(ex["sets"])
                expected = [tuple(p) for p in ex["per_set_points"]]
                actual = [(s.points_a, s.points_b) for s in r.sets]
                self.assertEqual(actual, expected)


class TestEmptySets(unittest.TestCase):
    def test_empty_rejected(self):
        with self.assertRaises(RatingError):
            rate_sets([])


if __name__ == "__main__":
    unittest.main()
