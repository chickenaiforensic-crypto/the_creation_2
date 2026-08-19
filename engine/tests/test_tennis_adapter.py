import unittest

from sport_engine.adapters.tennis import TennisAdapter

# Real row shapes from data/tennis/editions/ on arena/01a015bb-the-creation-2
DUBAI_BUBLIK = {
    "date": "2021-03-14", "tournament": "Dubai", "tier": "ATP500", "round": "R64",
    "tour": "ATP", "playerA": "Alexander Bublik", "playerB": "Yoshihito Nishioka",
    "setsA": 2, "setsB": 0, "gamesA": 13, "gamesB": 10, "score": "6-4 7-6(4)",
    "bestOf": 3, "retired": False, "walkover": False, "status": "completed",
    "defaulted": False, "winner": "A",
}
DUBAI_POPYRIN = {
    "date": "2021-03-14", "tournament": "Dubai", "tier": "ATP500", "round": "R64",
    "tour": "ATP", "playerA": "Alexei Popyrin", "playerB": "Dennis Novak",
    "setsA": 2, "setsB": 0, "gamesA": 14, "gamesB": 11, "score": "7-6(3) 7-5",
    "bestOf": 3, "retired": False, "walkover": False, "status": "completed",
    "defaulted": False, "winner": "A",
}


class TestTennisAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = TennisAdapter()

    def test_parses_tiebreak_score(self):
        sets = self.adapter.extract_sets(DUBAI_BUBLIK)
        self.assertEqual(sets, [(6, 4), (7, 6)])

    def test_parses_second_shape(self):
        sets = self.adapter.extract_sets(DUBAI_POPYRIN)
        self.assertEqual(sets, [(7, 6), (7, 5)])

    def test_three_set_with_dropped_set(self):
        row = dict(
            DUBAI_BUBLIK, score="6-3 3-6 6-4", setsA=2, setsB=1,
            gamesA=15, gamesB=13,
        )
        sets = self.adapter.extract_sets(row)
        self.assertEqual(sets, [(6, 3), (3, 6), (6, 4)])

    def test_three_set_rates(self):
        from sport_engine.rating.phase0 import rate_sets

        row = dict(DUBAI_BUBLIK, score="6-3 3-6 6-4", setsA=2, setsB=1, gamesA=15, gamesB=13)
        sets = self.adapter.extract_sets(row)
        r = rate_sets(sets)
        self.assertEqual((r.total_a, r.total_b), (24, 18))
        self.assertEqual((r.delta_a, r.delta_b), (6, -6))

    def test_retired_refused(self):
        row = dict(DUBAI_BUBLIK, retired=True, status="retired")
        self.assertIsNone(self.adapter.extract_sets(row))

    def test_walkover_refused(self):
        row = dict(DUBAI_BUBLIK, walkover=True)
        self.assertIsNone(self.adapter.extract_sets(row))

    def test_defaulted_refused(self):
        row = dict(DUBAI_BUBLIK, defaulted=True)
        self.assertIsNone(self.adapter.extract_sets(row))

    def test_non_completed_status_refused(self):
        row = dict(DUBAI_BUBLIK, status="interrupted")
        self.assertIsNone(self.adapter.extract_sets(row))

    def test_unfinished_set_refused(self):
        # Washington 2024 known-defect pattern: 7-6 6-6 -> 6-6 is not a final set
        row = dict(DUBAI_BUBLIK, score="7-6 6-6", setsA=1, setsB=0)
        self.assertIsNone(self.adapter.extract_sets(row))

    def test_missing_score_refused(self):
        row = dict(DUBAI_BUBLIK, score="")
        self.assertIsNone(self.adapter.extract_sets(row))

    def test_set_count_mismatch_refused(self):
        row = dict(DUBAI_BUBLIK, setsA=1, setsB=1)
        self.assertIsNone(self.adapter.extract_sets(row))

    def test_setsA_mismatch_refused(self):
        row = dict(DUBAI_BUBLIK, setsA=1, setsB=0)
        self.assertIsNone(self.adapter.extract_sets(row))

    def test_score_is_rateable_through_engine(self):
        from sport_engine.rating.phase0 import rate_sets

        sets = self.adapter.extract_sets(DUBAI_BUBLIK)
        r = rate_sets(sets)
        self.assertEqual((r.total_a, r.total_b), (20, 11))
        self.assertEqual((r.delta_a, r.delta_b), (9, -9))


class TestRegistry(unittest.TestCase):
    def test_sports_registered(self):
        from sport_engine.registry import get_sport, sports

        self.assertIn("tennis", sports())
        self.assertIn("football", sports())
        self.assertEqual(get_sport("tennis").sport, "tennis")

    def test_unknown_sport_raises(self):
        from sport_engine.registry import get_sport

        with self.assertRaises(KeyError):
            get_sport("cricket")

    def test_football_stub_not_implemented(self):
        from sport_engine.registry import get_sport

        with self.assertRaises(NotImplementedError):
            get_sport("football")().extract_sets({})


if __name__ == "__main__":
    unittest.main()
