import unittest

from sport_engine import __version__
from sport_engine.ui.api import ui_manifest


class TestUIManifest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = ui_manifest()

    def test_version_exposed(self):
        # the app version is a single source of truth in sport_engine/__init__,
        # exposed via the manifest, bumped every update (v1.1, v1.2, ...)
        self.assertEqual(self.m["app"]["version"], __version__)
        self.assertRegex(__version__, r"^v\d+\.\d+$")

    def test_tabs_present(self):
        self.assertIn("dashboard", self.m["tabs"])
        self.assertIn("configurations", self.m["tabs"])
        self.assertTrue(self.m["tabs"]["dashboard"])
        self.assertTrue(self.m["tabs"]["configurations"])

    def test_matchup_selector_swap(self):
        self.assertIn("matchup_selector", self.m)
        self.assertTrue(self.m["matchup_selector"]["swap_label"])
        self.assertTrue(self.m["matchup_selector"]["select_prefix"])

    def test_configurations_engine_parameters(self):
        cfg = self.m["configurations"]
        self.assertTrue(cfg["engine_parameters_label"])
        params = cfg["engine_parameters"]
        self.assertIn("points_per_game_difference", params)
        self.assertIn("feed_tournaments", params)
        self.assertIn("development_lock_rule", params)
        self.assertIn("sports_exposed", params)

    def test_placeholders(self):
        for key in ("select_sport", "select_players_rating", "select_players_h2h"):
            self.assertIn(key, self.m["placeholders"])
            self.assertTrue(self.m["placeholders"][key])

    def test_h2h_drilldown_columns(self):
        cols = self.m["h2h_ui"]["columns"]
        for key in ("date", "player_a", "player_b", "score", "h2h_a", "h2h_b", "winner"):
            self.assertIn(key, cols)
            self.assertTrue(cols[key])


if __name__ == "__main__":
    unittest.main()
