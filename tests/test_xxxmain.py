# -*- coding: utf-8 -*-
import unittest

import xxxmain


class TestXxxMain(unittest.TestCase):
    def test_help_returns_zero(self):
        self.assertEqual(xxxmain.main(["help"]), 0)

    def test_unknown_program(self):
        self.assertEqual(xxxmain.main(["nope"]), 2)


if __name__ == "__main__":
    unittest.main()
