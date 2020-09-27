#!/usr/bin/env python3

import sys
import re


# Wraps 'stream' at 'cutoff' (including)
def wrap_block(stream, indent=0, trail=0, cutoff=80):
    stream = re.sub('\n', ' ', stream)

    if len(stream) + indent <= cutoff:
        return " " * indent + stream + "\n" + "\n" * trail

    block = ""
    line = ""
    linelen = indent
    for word in stream.split():
        if linelen + len(word) > cutoff:
            block += " " * indent + line + "\n"
            line = ""
            linelen = indent
        line += word + " "
        linelen += len(word) + 1
    block += " " * indent + line + "\n"

    return block + "\n" * trail


# Creates single-line text blocks from 'stream'
#
# Returns:
#
#     An array of tuples of the form (block, indent, trail)
def create_blocks(stream):
    stream = stream.split("\n")

    numlines = len(stream)
    p = 0
    q = numlines
    while len(stream[p].rstrip()) == 0:
        p += 1
    while len(stream[q - 1].rstrip()) == 0:
        q -= 1

    blocks = [(p, numlines - q)]
    stream = stream[p:q]
    numlines = q - p

    # Create blocks
    i = 0
    blockline = ""
    indent = 0
    trail = 0
    while i < numlines:
        line = stream[i]
        linelen = len(line.rstrip())
        if linelen == 0:
            while linelen == 0:
                i += 1
                trail += 1
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
