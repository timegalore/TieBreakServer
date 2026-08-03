# -*- coding: utf-8 -*-
# noqa
"""
Copyright 2024, Otto Milvang
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Created on Mon Aug  7 16:48:53 2023
@author: Otto Milvang, sjakk@milvang.no
"""
import sys

from convert import convert2jch
from pairingchecker import pairingchecker
from tiebreakchecker import tiebreakchecker

# ==============================


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    program = "help"
    if argv and not argv[0].startswith("-"):
        program = argv.pop(0)
        sys.argv = [sys.argv[0]] + argv

    if program in ("help", "-h", "--help"):
        print("xxxmain <program> [options]")
        print("  programs: convert | tiebreak | pairing | help")
        return 0
    if program == "tiebreak":
        return tiebreakchecker().common_main()
    if program == "convert":
        return convert2jch().common_main()
    if program == "pairing":
        return pairingchecker().common_main()
    print("Unknown program:", program, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
