#! /usr/bin/env python
"""starter program for lminstreloc: a tool to correct filenames for instruments in LMMS modules
"""
import sys
from rewrite_lmmsfile import copyfile

copyfile(sys.argv[1])
