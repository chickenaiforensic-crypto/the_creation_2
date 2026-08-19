import unittest
from collections import Counter

from sport_engine.compute.ratings_table import build_ratings_table, render_table_text
from sport_engine.compute.selection import Filters
from sport_engine.config import load_config

_DATA = load_config("test_data")
_RT = _DATA["ratings_table"]


class TestRatingsTableView(unittest.TestCase):
    def test_one_table_per_selected_year(self):
        res = build_ratings_table()
        self.assertEqual(res["schema"], "ratings_table.1.0")
        self.assertEqual([t["year"] for t in res["tables"]], _RT["years"])

    def test_year_filter_selects_single_table(self):
        res = build_ratings_table(filters=Filters(years=[_RT["years"][0]]))
        self.assertEqual(len(res["tables"]), 1)
        self.assertEqual(res["tables"][0]["year"], _RT["years"][0])

    def test_year_2021_table(self):
        exp = _RT["year_2021"]
        res = build_ratings_table(filters=Filters(years=["2021"]))
        t = res["tables"][0]
        self.assertEqual(t["year"], "2021")
        self.assertEqual(len(t["rows"]), exp["rows"])
        self.assertEqual(t["summary"]["matches_selected"], exp["selected"])
        self.assertEqual(t["summary"]["matches_rated"], exp["rated"])
        self.assertEqual(t["summary"]["matches_refused"], exp["refused"])
        top = t["rows"][0]
        self.assertEqual(top["player"], exp["top_player"])
        self.assertEqual(top["rating"], exp["top_rating"])
        self.assertEqual(top["position"], exp["top_position"])
        # every player individually listed with a position, ranked 1..N
        self.assertEqual([p["rank"] for p in t["rows"]], list(range(1, exp["rows"] + 1)))
        counts = Counter(p["position"] for p in t["rows"])
        self.assertEqual(dict(counts), exp["position_counts"])
        by_name = {p["player"]: p for p in t["rows"]}
        self.assertEqual(
            by_name[exp["top_player"]]["round_reached"], "Champion"
        )
        # Rublev = finalist -> 2nd
        rublev = next(p for p in t["rows"] if p["player"] == "Andrey Rublev")
        self.assertEqual(rublev["position"], exp["finalist_position"])

    def test_year_2025_table(self):
        exp = _RT["year_2025"]
        res = build_ratings_table(filters=Filters(years=["2025"]))
        t = res["tables"][0]
        self.assertEqual(len(t["rows"]), exp["rows"])
        self.assertEqual(t["summary"]["matches_rated"], exp["rated"])
        self.assertEqual(t["summary"]["matches_refused"], exp["refused"])
        by_name = {p["player"]: p for p in t["rows"]}
        self.assertEqual(by_name[exp["champion"]]["position"], exp["champion_position"])
        self.assertEqual(by_name["Jannik Sinner"]["position"], exp["runner_up_position"])
        self.assertIn(exp["r128_loser_position"], {p["position"] for p in t["rows"]})
        # rating sort: Sinner (72) ahead of Alcaraz (50) — rating vs position diverge
        self.assertEqual(t["rows"][0]["player"], exp["top_rating_player"])

    def test_tournament_filter(self):
        from sport_engine.compute.selection import Mutes

        cfg = load_config("compute")
        feed = cfg["feed"]["tournaments"]
        self.assertTrue(feed)
        res = build_ratings_table(filters=Filters(tournaments=feed))
        self.assertEqual(len(res["tables"]), len(_RT["years"]))
        # unknown tournament -> no tables
        res2 = build_ratings_table(filters=Filters(tournaments=["Not A Tournament"]))
        self.assertEqual(res2["tables"], [])

    def test_mute_year_removes_table(self):
        from sport_engine.compute.selection import Mutes

        res = build_ratings_table(mutes=Mutes(mute_years=["2025"]))
        years = [t["year"] for t in res["tables"]]
        self.assertNotIn("2025", years)
        self.assertEqual(len(years), 4)

    def test_render_table_text_tabulated(self):
        res = build_ratings_table(filters=Filters(years=["2021"]))
        text = render_table_text(res["tables"][0])
        self.assertIn("POS", text)
        self.assertIn("Alexander Zverev", text)
        self.assertIn("1st", text)
        lines = text.splitlines()
        # title + summary + header + separator + 56 rows
        self.assertEqual(len(lines), 4 + 56)
        # all rows aligned: same column count
        body = [ln for ln in lines[4:] if ln.strip()]
        self.assertEqual(len(body), 56)


if __name__ == "__main__":
    unittest.main()
