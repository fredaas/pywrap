#!/usr/bin/env python3

import sys
import re


#
# Returns the valid prefix of 's'
#
def match_token(s):
    s = s.lstrip()
    l = len(s)
    for i in range(l):
        # Only check the first two characters
        if i >= 2:
            break
        c = s[i]
        if c == "-":
            return "-"
        if c == "#":
            return "#"
        if c == "/":
            if i + 1 < l and c == s[i + 1]:
                return "//"
        if c == "~":
            return "~"
    return ""


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

    prefix = match_token(stream)
    prefix_indent = indent

    stream = re.sub('(\n)+', ' ', stream)
    stream = re.sub('( )+', ' ', stream)
    stream = re.sub('({})'.format(prefix), '', stream, 1)
    stream = stream.strip()

    if (len(prefix) > 0):
        prefix_indent += len(prefix) + 1
        prefix += " "

    if len(stream) + indent <= cutoff:
        return " " * indent + prefix + stream + "\n" + "\n" * newlines

    leader = 1
    block = ""
    line = ""
    linelen = indent
    for word in stream.split():
        if linelen + len(word) > cutoff:
            if not leader:
                block += " " * prefix_indent + line.rstrip() + "\n"
            else:
                leader = 0
                block += " " * indent + prefix + line.rstrip() + "\n"
            line = ""
            linelen = indent
        line += word + " "
        linelen += len(word) + 1
    block += " " * prefix_indent + line.rstrip() + "\n"

    return block + "\n" * newlines


#
# Creates an array of text blocks from 'stream'
#
# Returns:
#
#     An array of tuples containing the block, the indentation level of the
#     block, and the number of newlines following the block:
#
#         (block, block_indent, block_newlines)
#
def create_blocks(stream, tokens=[]):
    stream = [ x.rstrip() for x in stream.split("\n") ]

    numlines = len(stream)

    blocks = []
    blockline = ""
    block_indent = 0
    newlines = 0

    i = 0
    while i < numlines:
        line = stream[i]

        # If the current line is empty
        if line == "":
            # Consume and count newlines
            block_newlines = 0
            while i < numlines and stream[i] == "":
                block_newlines += 1
                i += 1

            # Remove redundant newline from last block
            if (block_newlines >= 1 and i == numlines):
                block_newlines -= 1

            # Add newlines to block and append to list
            if blockline != "":
                blockline = re.sub('( )+', ' ', blockline.lstrip())
                blocks.append((blockline, block_indent, block_newlines))
                blockline = ""
            # These are leading newlines
            else:
                newlines = block_newlines

            # End of stream
            if i == numlines:
                break

            line = stream[i]

        # Encountered new block, store indentation
        if blockline == "":
            block_indent = lspace(line)

        blockline += line
        i += 1

    # Corner case where there is no empty newline at end of stream
    if blockline != "":
        blockline = re.sub('( )+', ' ', blockline.lstrip())
        blocks.append((blockline, block_indent, 0))

    return newlines, blocks
