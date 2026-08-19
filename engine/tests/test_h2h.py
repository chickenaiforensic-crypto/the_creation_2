import unittest

from sport_engine.compute.selection import Filters
from sport_engine.config import load_config
from sport_engine.h2h.h2h import match_game_difference, run_h2h

_DATA = load_config("test_data")
_H2H = _DATA["h2h"]


class TestMatchGameDifference(unittest.TestCase):
    def test_examples(self):
        for ex in _H2H["match_examples"]:
            with self.subTest(ex["label"]):
                r = match_game_difference(ex["sets"])
                self.assertEqual(r["games_a"], ex["games_a"])
                self.assertEqual(r["games_b"], ex["games_b"])
                self.assertEqual(r["game_difference"], ex["game_difference"])
                self.assertEqual(r["h2h_a"], ex["h2h_a"])
                self.assertEqual(r["h2h_b"], ex["h2h_b"])

    def test_invariant_per_set(self):
        # per-set difference sums to the match difference; games sum too
        for ex in _H2H["match_examples"]:
            r = match_game_difference(ex["sets"])
            self.assertEqual(sum(s["difference"] for s in r["sets"]), r["game_difference"])
            self.assertEqual(sum(s["games_a"] for s in r["sets"]), r["games_a"])
            self.assertEqual(sum(s["games_b"] for s in r["sets"]), r["games_b"])
            self.assertEqual(r["h2h_a"], -r["h2h_b"])


class TestH2HReport(unittest.TestCase):
    def test_feed_counts(self):
        r = run_h2h()
        exp = _H2H["feed"]
        self.assertEqual(r["schema"], "h2h.1.0")
        self.assertEqual(r["summary"]["matches_selected"], exp["matches_selected"])
        self.assertEqual(r["summary"]["matches_rated"], exp["matches_rated"])
        self.assertEqual(r["summary"]["matches_refused"], exp["matches_refused"])

    def test_2021_players_hand_computed(self):
        r = run_h2h(filters=Filters(years=["2021"]))
        by = {p["player"]: p for p in r["players"]}
        self.assertEqual(by["Alexander Zverev"]["game_difference"], _H2H["year_2021"]["zverev"])
        self.assertEqual(by["Jannik Sinner"]["game_difference"], _H2H["year_2021"]["sinner"])

    def test_refused_same_policy_as_primary(self):
        # the adapter refuses the same rows -> same per-year refused counts
        for y, refused in (("2021", 0), ("2022", 1), ("2023", 5), ("2024", 3), ("2025", 8)):
            r = run_h2h(filters=Filters(years=[y]))
            self.assertEqual(r["summary"]["matches_refused"], refused, f"{y}")

    def test_aggregate_invariants(self):
        r = run_h2h()
        # sum of players' game differences is 0 (every match +d cancels -d)
        self.assertEqual(sum(p["game_difference"] for p in r["players"]), 0)
        # players ranked by difference desc
        diffs = [p["game_difference"] for p in r["players"]]
        self.assertEqual(diffs, sorted(diffs, reverse=True))
        # average == difference / matches where matches > 0
        for p in r["players"]:
            if p["matches"] > 0:
                self.assertAlmostEqual(p["average"], p["game_difference"] / p["matches"])


class TestTournamentContext(unittest.TestCase):
    """Tournament-aware tracking: H2H traces the specific tournament context for
    each individual player."""

    @classmethod
    def setUpClass(cls):
        cls.feed = run_h2h()  # multi-tournament feed (all Cincinnati Masters years)

    def test_every_player_has_tournament_context(self):
        for p in self.feed["players"]:
            self.assertIn("tournaments", p)
            self.assertIsInstance(p["tournaments"], list)
            # per-tournament totals reconcile with all-tournament totals
            tot_m = sum(t["matches"] for t in p["tournaments"])
            tot_f = sum(t["games_for"] for t in p["tournaments"])
            tot_a = sum(t["games_against"] for t in p["tournaments"])
            self.assertEqual(tot_m, p["matches"])
            self.assertEqual(tot_f, p["games_for"])
            self.assertEqual(tot_a, p["games_against"])
            self.assertEqual(sum(t["game_difference"] for t in p["tournaments"]),
                             p["game_difference"])
            # each per-tournament context has its own average
            for t in p["tournaments"]:
                if t["matches"] > 0:
                    self.assertAlmostEqual(t["average"],
                                           t["game_difference"] / t["matches"])

    def test_player_tournament_context_breakdown(self):
        z = next(p for p in self.feed["players"] if p["player"] == "Alexander Zverev")
        self.assertEqual(len(z["tournaments"]), 1)  # feed = Cincinnati Masters only
        ctx = z["tournaments"][0]
        self.assertEqual(ctx["tournament"], "Cincinnati Masters")
        self.assertEqual(ctx["matches"], z["matches"])
        self.assertEqual(ctx["game_difference"], z["game_difference"])

    def test_multi_tournament_ingestion_via_filter(self):
        # select an additional tournament (Dubai) alongside the feed default
        from sport_engine.compute.selection import Filters

        r = run_h2h(filters=Filters(tournaments=["Cincinnati Masters", "Dubai"]))
        self.assertEqual(r["summary"]["matches_selected"], 315 + 168)
        tournaments = {t["tournament"] for m in r["matches"] for t in [m]}
        self.assertEqual(tournaments, {"Cincinnati Masters", "Dubai"})
        # a player who appears in both tournaments carries both contexts
        # (e.g. Jannik Sinner played Cincinnati Masters AND Dubai)
        by = {p["player"]: p for p in r["players"]}
        self.assertIn("Jannik Sinner", by)
        ctx_names = {t["tournament"] for t in by["Jannik Sinner"]["tournaments"]}
        self.assertEqual(ctx_names, {"Cincinnati Masters", "Dubai"})


class TestConversionHook(unittest.TestCase):
    """Future per-tournament calibration hook — abstraction present, not active."""

    def test_hook_reported_not_available(self):
        r = run_h2h()
        self.assertIn("conversion_hook", r)
        self.assertFalse(r["conversion_hook"]["available"])
        self.assertEqual(r["conversion_hook"]["configured_method"], "not_specified")

    def test_hook_convert_raises_not_implemented(self):
        from sport_engine.h2h import conversion_hook

        self.assertFalse(conversion_hook.available())
        with self.assertRaises(NotImplementedError):
            conversion_hook.convert({})


class TestH2HDecoupled(unittest.TestCase):
    def test_rows_have_no_absolute_rating_fields(self):
        r = run_h2h()
        for m in r["matches"]:
            self.assertNotIn("rating_a", m)
            self.assertNotIn("rating_b", m)
            self.assertNotIn("points_a", m)
            self.assertNotIn("rating_calibrated", m)
            if m["rateable"]:
                self.assertIn("h2h_a", m)
                self.assertIn("h2h_b", m)
                self.assertIn("game_difference", m)

    def test_module_does_not_import_absolute_point_routines(self):
        import sport_engine.h2h.h2h as h2h_module

        # inspect only the actual import statements (docstring text is not code)
        with open(h2h_module.__file__) as fh:
            imports = [
                line.strip()
                for line in fh.read().splitlines()
                if line.strip().startswith(("import ", "from "))
            ]
        joined = "\n".join(imports)
        for forbidden in ("rate_sets", "GAMES_TO_POINTS", "compute_ratings", "rating.phase0 import rate"):
            self.assertNotIn(forbidden, joined)
        self.assertIn("normalize_set", joined)  # the pre-built difference engine hook
        # and the module namespace must not expose the absolute-point functions
        self.assertNotIn("rate_sets", h2h_module.__dict__)
        self.assertNotIn("compute_ratings", h2h_module.__dict__)

    def test_stand_alone_execution(self):
        # runs without any interaction with the absolute-point pipeline
        r = run_h2h()
        self.assertGreater(r["summary"]["matches_rated"], 0)
        self.assertEqual(r["summary"]["matches_rated"] + r["summary"]["matches_refused"],
                         r["summary"]["matches_selected"])


if __name__ == "__main__":
    unittest.main()
