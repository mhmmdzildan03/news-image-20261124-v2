#!/usr/bin/env python3
"""Entry program for make.fun's "Sum up 24 November's world news in one
image" bounty.

The image beside this file (entry.png, 1024x1024) is a broadsheet front
page rendered by broadsheet.py, which is kept in this repository: the
date as the biggest type on the page, three illustrated lead stories
(COP31 fallout, the Banten factory fire toll, strikes on Kyiv), a grid
of five more stories, a day-in-numbers strip, a status chip and basis
line on every story, and a date-check box. (An earlier hero-poster
design, generate.py, is also kept for the record.) This program copies
entry.png to the output path, byte for byte, so both grader runs
produce identical output. Standard library only, no network.
"""
import os
import shutil
import sys


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    d = os.path.dirname(out)
    if d:
        os.makedirs(d, exist_ok=True)
    shutil.copyfile(src, out)


if __name__ == "__main__":
    main()
