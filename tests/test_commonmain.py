# -*- coding: utf-8 -*-
import base64
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from commonmain import commonmain
from convert import convert2jch
from tests.fixtures import minimal_trf_four_players


class TestCommonMain(unittest.TestCase):
    def test_parse_known_args_returns_namespace(self):
        app = convert2jch()
        # force non-strict path via read_common_command_line
        import sys

        old = sys.argv
        try:
            sys.argv = ["convert", "-i", "-", "-f", "TRF"]
            params = app.read_common_command_line("test", False)
            self.assertIsInstance(params, dict)
            self.assertEqual(params["input_format"], "TRF")
        finally:
            sys.argv = old

    def test_open_failure_returns_without_crash(self):
        app = convert2jch()
        app.params = {
            "input_format": "TRF",
            "encoding": "latin1",
            "input_file": "Z:/no/such/file.trf",
            "output_file": "-",
            "verbose": 0,
        }
        app.read_input_file()
        self.assertEqual(app.chessfile.get_status(), 405)

    def test_data_payload_decodes(self):
        app = convert2jch()
        raw = minimal_trf_four_players().encode("latin1")
        app.params = {
            "input_format": "TRF",
            "encoding": "latin1",
            "input_file": "-",
            "output_file": "-",
            "verbose": 0,
            "data": base64.b64encode(raw).decode("ascii"),
        }
        app.read_input_file()
        self.assertEqual(app.chessfile.get_status(), 0)
        self.assertEqual(len(app.chessfile.chessjson["event"]["tournaments"][0]["competitors"]), 4)

    def test_score_override_applied(self):
        from decimal import Decimal
        from tests.fixtures import make_event_with_tournament

        app = convert2jch()
        cj = make_event_with_tournament()
        app.chessfile = cj
        app.params = {
            "tournament_number": "1",
            "game_score": {"W": Decimal("3.0"), "D": Decimal("1.0"), "L": Decimal("0.0")},
            "method": [""],
        }
        app.prepare_tournament()
        tm = cj.get_tournament(1)
        self.assertEqual(tm["scoreSystem"]["game"]["W"], Decimal("3.0"))


if __name__ == "__main__":
    unittest.main()
