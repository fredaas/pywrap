#!/usr/bin/env python3

import sys
import re


# Wraps 'stream' at 'cutoff' (including)
def wrap_block(stream, indent=0, trail=0, cutoff=80):
    stream = re.sub('\n', ' ', stream)
    if len(stream) + indent <= cutoff:
        print(" " * indent + stream.rstrip())
    else:
        line = ""
        linelen = indent
        for word in stream.split():
            if linelen + len(word) > cutoff:
                print(" " * indent + line.rstrip())
                line = ""
                linelen = indent
            line += word + " "
            linelen += len(word) + 1
    if trail > 0:
        print("\n" * (trail - 1))


# Creates single-line text blocks from 'stream'
#
# Returns:
#
#     An array of tuples of the form (block, indent, trail)
def create_blocks(stream):
    # Removes leading and trail empty lines
    stream = stream.rstrip().split("\n")
    i = 0
    while len(stream[i].rstrip()) == 0:
        i += 1
    stream = stream[i:]

    numlines = len(stream)

    # Create blocks. Strip whitespace.
    i = 0
    blocks = []
    blockline = ""
    indent = 0
    trail = 0
    while i < numlines:
        line = stream[i]
        linelen = len(line.rstrip())
        if linelen == 0:
            while linelen == 0:
                trail += 1
                i += 1
                line = stream[i]
                linelen = len(line.rstrip())
            blockline = re.sub('( )+', ' ', blockline)
            blocks.append((blockline.strip(), indent, trail))
            blockline = ""
            trail = 0
        if blockline == "":
            indent = len(line) - len(line.lstrip())
        blockline += line + " "
        i += 1
    blockline = re.sub('( )+', ' ', blockline)
    blocks.append((blockline.strip(), indent, trail))

    return blocks
