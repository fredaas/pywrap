#!/usr/bin/env python3

import sys
import re


#
# Returns the number of leading spaces in 's'
#
def lspace(s):
    i = 0
    while i < len(s) and s[i] == " ":
        i += 1
    return i


#
# Wraps 'stream' at 'cutoff' (including)
#
def wrap_stream(stream, indent=None, newlines=0, cutoff=80):
    if not indent:
        indent = lspace(stream)

    stream = re.sub('(\n)+', ' ', stream)
    stream = re.sub('( )+', ' ', stream)
    stream = stream.strip()

    if len(stream) + indent <= cutoff:
        return " " * indent + stream + "\n" + "\n" * newlines

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
    block += " " * indent + line + "\n"

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
#         (block, block_indent, block_newlines)
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
                blocks.append((blockline, block_indent, block_newlines))
                blockline = ""
            else:
                newlines = block_newlines
            if i == numlines:
                break
            line = stream[i]
        if blockline == "":
            block_indent = lspace(line)
        blockline += line
        i += 1

    if blockline != "":
        blocks.append((blockline, block_indent, 0))

    return newlines, blocks
