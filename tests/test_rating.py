# -*- coding: utf-8 -*-
import unittest
from decimal import Decimal

import rating


class TestRating(unittest.TestCase):
    def test_expected_score_equal_ratings(self):
        pd = rating.ComputeExpectedScore(2000, 2000)
        self.assertEqual(pd, Decimal("0.50"))

    def test_expected_score_favorite(self):
        pd = rating.ComputeExpectedScore(2200, 2000)
        self.assertGreater(pd, Decimal("0.50"))

    def test_average_opponents(self):
        self.assertEqual(rating.ComputeAverageRatingOpponents([2000, 2100, 1900]), 2000)

    def test_average_empty(self):
        self.assertIsNone(rating.ComputeAverageRatingOpponents([]))

    def test_tpr_norm_uses_upper_key(self):
        # Should not KeyError on lowercase "gm"
        tpr = rating.ComputeTournamentPerformanceRating(
            Decimal("5.0"), [2400, 2350, 2300, 2250, 2200, 2150, 2100, 2050, 2000], "gm"
        )
        self.assertIsInstance(tpr, int)

    def test_ptp_zero_score(self):
        ptp = rating.ComputePerfectTournamentPerformance(Decimal("0.0"), [2000, 2100])
        self.assertEqual(ptp, 2000 - 800)


if __name__ == "__main__":
    unittest.main()
