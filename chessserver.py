#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 08:16:13 2024
@author: Otto Milvang, sjakk@milvang.no
"""
import json
import json
import sys
from convert import convert2jch
import helpers
from pairingchecker import pairingchecker
from tiebreakchecker import tiebreakchecker
import version
from commonmain import commonmain
from tiebreak import tiebreak
from pairing import pairing


"""
==============================
Request:
{
    "filetype": "convert request" | "tiebreak request" ,
    "version": "1.0",
    "origin": "<Free text>",
    "published": "<date on format 2018-08-14 05:07:44>",
    "options": {
        "service" : "convert" | tiebreak,
        "input_filename" : "<original file name>",
        "input_filetype": "TRF" | "TS" | < other known format >,
        "data": ["<lines with base 64 encoded file>"],
        "tournament_number": <0 or tournamentno to convert>,
        "current_round": <int>,
        "number_of_rounds": <int>,
        // parameters for tiebreaks
            "tiebreak" : [string list],
            "pre-determined" : true | false,
            "swiss" : true | false, 
            "unrated" : <rating for unrated players>,
        // parameters for pairing   
            "pairing" : true | false,
            "method" : "dutch",
            "top_color" : "white" | "black",
            "maxmeets" : <int>,
            "unpaired" : [<cid>, …],
            "analysis" : true | false,  }

    }
}

Response:
{
    "filetype": "convert response" | "tiebreak response",
    "version": "1.0",
    "origin": "chessserver ver. 1.04",
    "published": "2024-10-01 14:32:16",
    "status": {
        "code": 0,
        "error": []
    },
    "convertResult": {
        <Json chess file>
    }
    "tiebreakResult": {
        "check": false,
        "tiebreaks": [ … ],
        "competitors": [ {
            "cid": <cid>,
            "rank": <rank>,
            "tiebreakScore": [ … ],
            "boardPoints": { … },
            "tiebreakDetails": [{ … }, … ]
    }
}


"""


class chessserver(commonmain):

    methods = {
         "convert":  convert2jch,  
         "tiebreak": tiebreakchecker, 
         "pairing":  pairingchecker 
         }


    def __init__(self):
        super().__init__()
        self.origin = "chessserver ver. " + version.version()["version"]
        self.tournamentno = 0

    # Client-supplied path fields are ignored in server mode to prevent
    # arbitrary host file read/write. Only in-memory payloads are accepted.
    SERVER_ALLOWED_KEYS = {
        "service",
        "input_format",
        "input_filetype",
        "input_filename",
        "encoding",
        "tournament_number",
        "current_round",
        "number_of_rounds",
        "delimiter",
        "decimal_point",
        "check",
        "experimental",
        "verbose",
        "tiebreak",
        "pre-determined",
        "swiss",
        "unrated",
        "pairing",
        "method",
        "top_color",
        "maxmeets",
        "unpaired",
        "analysis",
        "rank",
        "game_score",
        "match_score",
        "base64",
        "jch",
        "data",
    }
    MAX_REQUEST_BYTES = 10 * 1024 * 1024
    MAX_PAYLOAD_BYTES = 10 * 1024 * 1024

    def read_command_line(self):
        # form = cgi.FieldStorage()
        # helpers.json_output('c:\\temp\\t.txt', form)
        charset = "utf-8"
        raw = sys.stdin.buffer.read(self.MAX_REQUEST_BYTES + 1)
        if len(raw) > self.MAX_REQUEST_BYTES:
            raise ValueError("Request exceeds maximum size of %d bytes" % self.MAX_REQUEST_BYTES)
        data = raw.decode(charset)
        jsondata = json.loads(data)
        command = jsondata["command"]
        # helpers.json_output('c:\\temp\\t2.txt', command)
        self.params = {
            "service": "",
            "input_file": "-",
            "output_file": "-",
            "output_format": "JSON",
            "encoding": "ascii",
            "tournament_number": 1,
            "current_round": -1,
            "delimiter": None,
            "check": False,
            "experimental": [],
            "verbose": 0,
        }

        for key, value in command.items():
            if key in self.SERVER_ALLOWED_KEYS:
                self.params[key] = value
        # Never honor client path fields; always write JSON to stdout.
        self.params["input_file"] = "-"
        self.params["output_file"] = "-"
        if "input_format" not in self.params:
            filetype = command.get("input_filetype") or command.get("input_format")
            if filetype:
                self.params["input_format"] = filetype
            elif "input_filename" in command:
                self.params["input_format"] = helpers.getFileFormat(command["input_filename"])
            else:
                self.params["input_format"] = "TRF"
        if "base64" not in self.params and "jch" not in self.params and "data" not in self.params:
            raise ValueError("Server requests require an in-memory payload (base64, jch, or data)")
        for key in ("base64", "jch", "data"):
            if key in self.params:
                payload = self.params[key]
                if isinstance(payload, list):
                    payload = "".join(payload)
                if isinstance(payload, str) and len(payload.encode("utf-8")) > self.MAX_PAYLOAD_BYTES:
                    raise ValueError("Payload exceeds maximum size of %d bytes" % self.MAX_PAYLOAD_BYTES)
        self.baseclass = self.methods.get(self.params["service"], convert2jch)()
        self.baseclass.params = self.params
        self.baseclass.resultjson["options"] = self.params
        return self.params

    def read_input_file(self):
        self.baseclass.read_input_file()
        
    def prepare_tournament(self):
        self.baseclass.prepare_tournament()

    def write_text_file(self, f, result, delimiter):
        pass

    def do_checker(self):
        self.baseclass.do_checker()
        return

    def apply_result(self):
         self.baseclass.apply_result()
         self.chessfile = self.baseclass.chessfile
         self.resultjson = self.baseclass.resultjson
         pass

    def write_output_file(self):
        self.baseclass.write_output_file()


# run program
if __name__ == "__main__":
    jch = chessserver()
    code = jch.common_main()
    sys.exit(code)
