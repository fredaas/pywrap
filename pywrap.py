#!/usr/bin/env python3

import sys
import re


#
# Wraps 'stream' at 'cutoff' (including)
#
def wrap_block(stream, indent=0, newlines=0, cutoff=80):
    stream = re.sub('\n', ' ', stream)

    if len(stream) + indent <= cutoff:
        return " " * indent + stream.rstrip() + "\n" + "\n" * newlines

    block = ""
    line = ""
    linelen = indent
    for word in stream.split():
        if linelen + len(word) > cutoff:
            block += " " * indent + line.rstrip() + "\n"
            line = ""
            linelen = indent
        line += word + " "
        linelen += len(word) + 1
    block += " " * indent + line.rstrip() + "\n"

    return block + "\n" * newlines


#
# Creates an array of text blocks from 'stream'
#
# Returns:
#
#     An array of tuples containing the block, the indentation level of the
#     block, and the number of newlines following the block. The tuple is of
#     the form:
#
#         (block_indent, block_newlines, block)
#
def create_blocks(stream):
    stream = [ x.rstrip() for x in stream.split("\n") ]

    numlines = len(stream)

    blocks = []
    blockline = ""
    block_indent = 0
    newlines = 0

    i = 0
    while i < numlines:
        line = stream[i]
        if line == "":
            block_newlines = 0
            while i < numlines and stream[i] == "":
                block_newlines += 1
                i += 1
            if blockline != "":
                blockline = re.sub('( )+', ' ', blockline.lstrip())
                blocks.append((block_indent, block_newlines, blockline))
                blockline = ""
            else:
                newlines = block_newlines
            if i == numlines:
                break
            line = stream[i]
        if blockline == "":
            block_indent = len(line) - len(line.lstrip())
        blockline += line
        i += 1

    if blockline != "":
        blocks.append((block_indent, 0, blockline))

    return newlines, blocks
