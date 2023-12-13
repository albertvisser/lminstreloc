"""CLI starter voor samplelister commando
"""
import sys
import samplelister

out = open(sys.argv[2], 'w') if len(sys.argv) > 2 else sys.stdout
with out:
    for line in samplelister.list_samples(sys.argv[1]):
        print(line, file=out)
