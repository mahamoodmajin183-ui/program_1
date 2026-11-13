#!/usr/bin/env python3
"""Word-count MAPPER for Hadoop Streaming / the Unix pipe in Experiment 6.
(The manual refers to mapper.py but does not print it - this is the standard version.)
Reads text from stdin, writes "word<TAB>1" for every word."""
import re
import sys

for line in sys.stdin:
    for word in re.findall(r"[a-z0-9']+", line.lower()):
        print(f"{word}\t1")
