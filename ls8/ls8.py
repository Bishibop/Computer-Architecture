#!/usr/bin/env python3
"""Main."""

import sys
from cpu import *
try:
    program_file_name = sys.argv[1]
except IndexError as e:
    print("Missing program file name")
    sys.exit(1)

cpu = CPU()

cpu.load(program_file_name)
cpu.run()
