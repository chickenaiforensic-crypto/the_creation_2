import unittest

from sport_engine.rating.phase0 import (
    RatingError,
    normalize_set,
    points_for_games,
    rate_sets,
)


class TestPhase0WorkedExample(unittest.TestCase):
    """Director worked example: sets 6-2, 6-4 -> pA 20, pB 6 -> +14 / -14."""

    def test_totals_and_ratings(self):
        r = rate_sets([(6, 2), (6, 4)])
        self.assertEqual(r.total_a, 20)
        self.assertEqual(r.total_b, 6)
        self.assertEqual(r.delta_a, 14)
        self.assertEqual(r.delta_b, -14)

    def test_per_set_points(self):
        r = rate_sets([(6, 2), (6, 4)])
        self.assertEqual([(s.points_a, s.points_b) for s in r.sets], [(10, 2), (10, 4)])


class TestPointsTable(unittest.TestCase):
    def test_brackets(self):
        self.assertEqual(points_for_games(0), 2)
        self.assertEqual(points_for_games(1), 2)
        self.assertEqual(points_for_games(2), 2)
        self.assertEqual(points_for_games(3), 4)
        self.assertEqual(points_for_games(4), 4)
        self.assertEqual(points_for_games(5), 7)
        self.assertEqual(points_for_games(6), 10)

    def test_out_of_range(self):
        with self.assertRaises(RatingError):
            points_for_games(7)
        with self.assertRaises(RatingError):
            points_for_games(-1)


class TestNormalization(unittest.TestCase):
    def test_7_5_resolves_to_6_4(self):
        self.assertEqual(normalize_set(7, 5), (6, 4))

    def test_6_2_unchanged(self):
        self.assertEqual(normalize_set(6, 2), (6, 2))

    def test_8_6_steps_down_to_6_4(self):
        self.assertEqual(normalize_set(8, 6), (6, 4))

    def test_7_6_resolves_to_6_5(self):
        # Tiebreak set: -1 both sides. Pending Director confirmation (open question).
        self.assertEqual(normalize_set(7, 6), (6, 5))

    def test_reversed_input_keeps_orientation(self):
        self.assertEqual(normalize_set(2, 6), (2, 6))

    def test_b_won_set_assigns_points_to_b(self):
        r = rate_sets([(6, 3), (3, 6), (6, 4)])
        # set2 3-6: B has 6 games -> 10 pts, A has 3 -> 4 pts
        self.assertEqual([(s.points_a, s.points_b) for s in r.sets],
                         [(10, 4), (4, 10), (10, 4)])
        self.assertEqual((r.total_a, r.total_b), (24, 18))
        self.assertEqual((r.delta_a, r.delta_b), (6, -6))

    def test_tied_set_rejected(self):
        with self.assertRaises(RatingError):
            normalize_set(6, 6)

    def test_un_normalisable_rejected(self):
        with self.assertRaises(RatingError):
            normalize_set(7, 0)


class Test7_5Match(unittest.TestCase):
    def test_7_5_6_2(self):
        r = rate_sets([(7, 5), (6, 2)])
        self.assertEqual((r.total_a, r.total_b), (20, 6))
        self.assertEqual((r.delta_a, r.delta_b), (14, -14))


class TestTiebreakSetRating(unittest.TestCase):
    def test_7_6_tiebreak_gives_loser_5_games(self):
        # 7-6 -> 6-5 -> pB 7 pts. Marked against open question; asserts current impl.
        r = rate_sets([(6, 4), (7, 6)])
        self.assertEqual((r.total_a, r.total_b), (20, 11))
        self.assertEqual((r.delta_a, r.delta_b), (9, -9))


class TestNoSets(unittest.TestCase):
    def test_empty_rejected(self):
        with self.assertRaises(RatingError):
            rate_sets([])


if __name__ == "__main__":
    unittest.main()
