"""CLI starter voor samplelister commando
"""
import sys
import samplelister

with open(sys.argv[2], 'w') as f:
    for line in samplelister.list_files(sys.argv[1]):
        print(line, file=f)
