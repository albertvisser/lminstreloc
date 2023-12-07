#! /usr/bin/env python
"""starter program for lminstreloc: a tool to correct filenames for instruments in LMMS modules
"""
import os.path
import subprocess
from rewrite_lmmsfile import copyfile
start_here = os.path.expanduser('~/lmms/projects/*.mmpz')

while True:
    result = subprocess.run(['zenity', '--file-selection', f'--filename={start_here}'],
                            capture_output=True)
    selected = result.stdout.decode().strip()
    if not selected:
        break
    message = copyfile(selected)
    result = subprocess.run(['zenity', '--question', f'--text={message}\n\nContinue?'])
    if result.returncode:
        break
