import unittest

from sport_engine.config import load_config
from sport_engine.rating.phase0 import rate_sets


def load_test_data():
    from sport_engine.config import load_config

    return load_config("test_data")


_DATA = load_test_data()


class TestTennisAdapter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from sport_engine.adapters.tennis import TennisAdapter

        cls.adapter = TennisAdapter()

    def test_extraction_cases(self):
        for row in _DATA["tennis_rows"]:
            with self.subTest(row["label"]):
                sets = self.adapter.extract_sets(row["match"])
                expected = row["expected_sets"]
                if expected is None:
                    self.assertIsNone(sets)
                else:
                    self.assertEqual(sets, [tuple(s) for s in expected])
                    if "expected_totals" in row:
                        r = rate_sets(sets)
                        self.assertEqual(r.total_a, row["expected_totals"]["total_a"])
                        self.assertEqual(r.total_b, row["expected_totals"]["total_b"])


class TestRegistry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from sport_engine.config import load_config

        cls.sports_config = load_config("sports")

    def test_active_adapters_registered(self):
        from sport_engine.registry import sports

        for name in self.sports_config["active_adapters"]:
            with self.subTest(name):
                self.assertIn(name, sports())

    def test_unknown_sport_raises(self):
        from sport_engine.registry import get_sport

        with self.assertRaises(KeyError):
            get_sport(_DATA["unknown_sport_name"])

    def test_football_stub_not_implemented(self):
        from sport_engine.registry import get_sport

        football_name = load_config("football_schema")["sport"]
        self.assertIn(football_name, self.sports_config["active_adapters"])
        with self.assertRaises(NotImplementedError):
            get_sport(football_name)().extract_sets({})


if __name__ == "__main__":
    unittest.main()
