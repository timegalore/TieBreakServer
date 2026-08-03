# -*- coding: utf-8 -*-
import unittest
from decimal import Decimal

from scoresystem import scoresystem


class TestScoreSystem(unittest.TestCase):
    def setUp(self):
        self.ss = scoresystem()
        self.ss.score["game"] = self.ss.fill_default_scoresystem("game")
        self.ss.score["match"] = self.ss.fill_default_scoresystem("match")

    def test_default_game_win(self):
        self.assertEqual(self.ss.score["game"]["W"], Decimal("1.0"))

    def test_default_match_win(self):
        self.assertEqual(self.ss.score["match"]["W"], Decimal("2.0"))

    def test_get_result_prefers_loss_over_zero(self):
        tournament = {
            "scoresystem": {
                "game": {
                    "W": Decimal("1.0"),
                    "D": Decimal("0.5"),
                    "L": Decimal("0.0"),
                    "Z": Decimal("0.0"),
                }
            }
        }
        self.assertEqual(self.ss.get_result(tournament, "game", Decimal("0.0")), "L")
        self.assertEqual(self.ss.get_result(tournament, "game", Decimal("1.0")), "W")
        self.assertEqual(self.ss.get_result(tournament, "game", Decimal("0.5")), "D")

    def test_solve_scoresystem_p_resets_accumulator(self):
        # Two equations that only fit W=1, D=0.5, L=0 with U=D
        equations = [
            {"sum": Decimal("1.5"), "W": 1, "D": 1, "L": 0, "P": 0, "U": 0, "Z": 0, "A": 0},
            {"sum": Decimal("0.5"), "W": 0, "D": 1, "L": 0, "P": 0, "U": 0, "Z": 0, "A": 0},
        ]
        ret = self.ss.solve_scoresystem_p(equations, ["W"])
        self.assertIsNotNone(ret)
        self.assertEqual(ret["W"], Decimal("1.0"))
        self.assertEqual(ret["D"], Decimal("0.5"))


if __name__ == "__main__":
    unittest.main()
