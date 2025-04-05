#! /usr/bin/env python
"""starter program for lminstreloc: a tool to correct filenames for instruments in LMMS modules
"""
import os.path
import subprocess
from app import rewrite_lmmsfile
start_here = os.path.expanduser('~/lmms/projects')
rewrite_lmmsfile.Rewriter(start_here)
