# -*- coding: utf-8 -*-
import unittest

import berger


class TestBerger(unittest.TestCase):
    def test_even_players_round_count(self):
        table = berger.bergertables(6)
        self.assertEqual(table["players"], 6)
        self.assertEqual(len(table["pairing"]), 5)

    def test_odd_players_padded(self):
        table = berger.bergertables(5)
        self.assertEqual(table["players"], 6)

    def test_each_round_has_all_players_once(self):
        table = berger.bergertables(8)
        for rnd, boards in table["pairing"].items():
            players = []
            for board, pair in boards.items():
                players.extend([pair["white"], pair["black"]])
            self.assertEqual(sorted(players), list(range(1, 9)), "round %s" % rnd)

    def test_generic_matches_classic_for_small_n(self):
        for n in (4, 6, 8, 10):
            classic = berger.bergertables(n)
            generic = berger.bergertablesGeneric(n)
            self.assertEqual(classic["players"], generic["players"])
            for rnd in classic["pairing"]:
                for board in classic["pairing"][rnd]:
                    c = classic["pairing"][rnd][board]
                    g = generic["pairing"][rnd][board]
                    self.assertEqual(
                        {c["white"], c["black"]},
                        {g["white"], g["black"]},
                        "n=%s round=%s board=%s" % (n, rnd, board),
                    )


if __name__ == "__main__":
    unittest.main()
