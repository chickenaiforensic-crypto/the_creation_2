import unittest

from sport_engine.config import load_config


def load_test_data():
    return load_config("test_data")


_DATA = load_test_data()


class TestConfigStructure(unittest.TestCase):
    """Structural checks only — no spec-value literals (zero-hardcoding rule).
    Spec values are asserted end-to-end through the fixture-driven math tests."""

    def test_rating_rules_fully_cover_range(self):
        r = load_config("rating_rules")
        max_games = r["max_winner_games"]
        for games in range(max_games + 1):
            key = str(games)
            self.assertIn(key, r["points_by_games"])
            self.assertIn(key, r["section_by_games"])
            self.assertGreaterEqual(r["points_by_games"][key], 0)

    def test_tennis_schema_structure(self):
        s = load_config("tennis_schema")
        self.assertEqual(s["sport"], "tennis")
        self.assertIn("status", s["fields"])
        self.assertIn("status_value_completed", s["fields"])
        self.assertIn("void_flags", s["fields"])
        self.assertIn("score", s["fields"])
        self.assertIn("sets_a", s["fields"])
        self.assertIn("sets_b", s["fields"])

    def test_sports_config_non_empty(self):
        s = load_config("sports")
        self.assertTrue(s["active_adapters"])

    def test_football_schema_structure(self):
        f = load_config("football_schema")
        self.assertIn("sport", f)
        self.assertTrue(f["sport"])

    def test_missing_config_raises(self):
        with self.assertRaises(FileNotFoundError):
            load_config(_DATA["missing_config_name"])


class TestRulesCameFromConfig(unittest.TestCase):
    def test_phase0_uses_config_not_literals(self):
        import sport_engine.rating.phase0 as phase0

        rules = load_config("rating_rules")
        self.assertEqual(phase0.MAX_WINNER_GAMES, rules["max_winner_games"])
        self.assertEqual(
            phase0.GAMES_TO_POINTS,
            {int(k): int(v) for k, v in rules["points_by_games"].items()},
        )
        self.assertEqual(
            phase0.SECTION_LABEL,
            {int(k): v for k, v in rules["section_by_games"].items()},
        )

    def test_tennis_adapter_uses_config(self):
        from sport_engine.adapters.tennis import TennisAdapter

        schema = load_config("tennis_schema")
        self.assertEqual(TennisAdapter.sport, schema["sport"])

    def test_football_adapter_uses_config(self):
        from sport_engine.adapters.football import FootballAdapter

        schema = load_config("football_schema")
        self.assertEqual(FootballAdapter.sport, schema["sport"])


if __name__ == "__main__":
    unittest.main()
