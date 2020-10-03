#!/usr/bin/env python3
"""Main."""

import sys
from cpu import *
program_file_name = sys.argv[1]

cpu = CPU()

cpu.load(program_file_name)
cpu.run()
