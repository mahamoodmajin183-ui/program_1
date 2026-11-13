#!/usr/bin/env python3
"""Word-count REDUCER for Hadoop Streaming / the Unix pipe in Experiment 6.
Input must be sorted by word (that is what the shuffle/sort phase, or the `sort` command, provides)."""
import sys

current_word, current_count = None, 0
for line in sys.stdin:
    word, _, count = line.rstrip("\n").partition("\t")
    try:
        count = int(count)
    except ValueError:
        continue
    if word == current_word:
        current_count += count
    else:
        if current_word is not None:
            print(f"{current_word}\t{current_count}")
        current_word, current_count = word, count
if current_word is not None:
    print(f"{current_word}\t{current_count}")
