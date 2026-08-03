# -*- coding: utf-8 -*-
import unittest

from drawresult import drawresult


class TestDrawResult(unittest.TestCase):
    def test_seed_is_deterministic(self):
        a = drawresult(42)
        b = drawresult(42)
        results_a = [a.result(2000, 2000) for _ in range(20)]
        results_b = [b.result(2000, 2000) for _ in range(20)]
        self.assertEqual(results_a, results_b)

    def test_instances_do_not_share_rng(self):
        a = drawresult(1)
        b = drawresult(2)
        # Different seeds should generally diverge; force divergence via many draws
        seq_a = "".join(a.result(2000, 2000) for _ in range(50))
        seq_b = "".join(b.result(2000, 2000) for _ in range(50))
        self.assertNotEqual(seq_a, seq_b)

    def test_prob_sums_near_one(self):
        dr = drawresult(7)
        pw, pd, pb = dr.prob(2000, 2000)
        self.assertAlmostEqual(pw + pd + pb, 1.0, places=6)

    def test_has_bye_respects_rates(self):
        dr = drawresult(99)
        dr.set_params(zpb=1.0, hpb=0.0, forfeited=0.0)
        self.assertEqual(dr.has_bye(), "Z")


if __name__ == "__main__":
    unittest.main()
