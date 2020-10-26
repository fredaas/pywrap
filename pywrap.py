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
def wrap_stream(stream, indent=None, newlines=0, prefix="", cutoff=80):
    if not indent:
        indent = lspace(stream)

    prefix_indent = indent
    prefix_length = len(prefix)

    if prefix_length != 0:
        prefix += " "
        prefix_indent += prefix_length + 1

    stream = re.sub('(\n)+', ' ', stream)
    stream = re.sub('( )+', ' ', stream)
    stream = stream.strip()

    if len(stream) + indent <= cutoff:
        return " " * indent + prefix + stream + "\n" + "\n" * newlines

    block = ""
    line = ""
    linelen = indent

    leader = 1
    for word in stream.split():
        if linelen + len(word) > cutoff:
            if not leader:
                block += " " * prefix_indent + line.rstrip() + "\n"
            else:
                block += " " * indent + prefix + line.rstrip() + "\n"
                leader = 0
            line = ""
            linelen = indent
        line += word + " "
        linelen += len(word) + 1
    block += " " * prefix_indent + line + "\n"

    return block + "\n" * newlines


#
# Returns the valid prefix of 's', if any
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
# Creates an array of text blocks from 'stream'
#
# Returns:
#
#     An array of tuples containing the block, the indentation level of the
#     block, and the number of newlines following the block. The tuple is of
#     the form:
#
#         (block, block_indent, block_newlines, prefix)
#
def create_blocks(stream, tokens=[]):
    stream = [ x.rstrip() for x in stream.split("\n") ]

    numlines = len(stream)

    blocks = []
    blockline = ""
    block_indent = 0
    newlines = 0
    prefix = ""

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
                blocks.append((blockline, block_indent, block_newlines, prefix))
                blockline = ""
                prefix = ""
            else:
                newlines = block_newlines
            if i == numlines:
                break
            line = stream[i]
        if blockline == "":
            block_indent = lspace(line)

        if blockline == "":
            prefix = match_token(line)
            if len(prefix) > 0:
                line = line.lstrip()[len(prefix):]

        blockline += line
        i += 1

    if blockline != "":
        blockline = re.sub('( )+', ' ', blockline.lstrip())
        blocks.append((blockline, block_indent, 0, prefix))

    return newlines, blocks
