# -*- coding: utf-8 -*-
import base64
import io
import json
import sys
import unittest
from unittest import mock

from chessserver import chessserver
from tests.fixtures import minimal_trf_four_players


class TestChessServer(unittest.TestCase):
    def _request(self, command):
        return json.dumps({"command": command})

    def test_rejects_missing_payload(self):
        srv = chessserver()
        payload = self._request({"service": "convert", "input_format": "TRF"})
        with mock.patch.object(sys, "stdin", mock.Mock(buffer=io.BytesIO(payload.encode("utf-8")))):
            with self.assertRaises(ValueError):
                srv.read_command_line()

    def test_ignores_client_paths(self):
        raw = minimal_trf_four_players().encode("latin1")
        b64 = base64.b64encode(raw).decode("ascii")
        srv = chessserver()
        payload = self._request(
            {
                "service": "convert",
                "input_format": "TRF",
                "base64": b64,
                "input_file": "C:/Windows/System32/config/SAM",
                "output_file": "C:/temp/pwned.json",
            }
        )
        with mock.patch.object(sys, "stdin", mock.Mock(buffer=io.BytesIO(payload.encode("utf-8")))):
            params = srv.read_command_line()
        self.assertEqual(params["input_file"], "-")
        self.assertEqual(params["output_file"], "-")
        self.assertIn("base64", params)

    def test_accepts_data_list_payload(self):
        raw = minimal_trf_four_players().encode("latin1")
        b64 = base64.b64encode(raw).decode("ascii")
        srv = chessserver()
        payload = self._request(
            {
                "service": "convert",
                "input_format": "TRF",
                "data": [b64],
            }
        )
        with mock.patch.object(sys, "stdin", mock.Mock(buffer=io.BytesIO(payload.encode("utf-8")))):
            params = srv.read_command_line()
        self.assertEqual(params["data"], [b64])

    def test_rejects_oversized_request(self):
        srv = chessserver()
        huge = b"x" * (chessserver.MAX_REQUEST_BYTES + 10)
        with mock.patch.object(sys, "stdin", mock.Mock(buffer=io.BytesIO(huge))):
            with self.assertRaises(ValueError):
                srv.read_command_line()


if __name__ == "__main__":
    unittest.main()
