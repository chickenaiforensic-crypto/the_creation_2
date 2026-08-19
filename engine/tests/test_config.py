import unittest

from sport_engine.config import load_config


class TestConfigLoads(unittest.TestCase):
    def test_rating_rules_spec_values(self):
        r = load_config("rating_rules")
        self.assertEqual(r["max_winner_games"], 6)
        self.assertEqual(r["points_by_games"]["0"], 2)
        self.assertEqual(r["points_by_games"]["3"], 4)
        self.assertEqual(r["points_by_games"]["5"], 7)
        self.assertEqual(r["points_by_games"]["6"], 10)
        self.assertEqual(r["tier_by_games"]["6"], "4x")

    def test_tennis_schema_fields(self):
        s = load_config("tennis_schema")
        self.assertEqual(s["sport"], "tennis")
        self.assertEqual(s["fields"]["status"], "status")
        self.assertEqual(s["fields"]["status_value_completed"], "completed")
        self.assertEqual(s["fields"]["void_flags"], ["retired", "walkover", "defaulted"])
        self.assertEqual(s["fields"]["sets_a"], "setsA")
        self.assertEqual(s["fields"]["sets_b"], "setsB")

    def test_sports_config_active_list(self):
        s = load_config("sports")
        self.assertEqual(s["active_adapters"], ["tennis", "football"])

    def test_missing_config_raises(self):
        with self.assertRaises(FileNotFoundError):
            load_config("does_not_exist")


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
            phase0.TIER_LABEL,
            {int(k): v for k, v in rules["tier_by_games"].items()},
        )


if __name__ == "__main__":
    unittest.main()
