#!/usr/bin/env python3

from pywrap import *

# Test 1
text = open("./tests/test_1.txt", "r").read()
wrap_block(text)
print()

# Test 2
text = open("./tests/test_2.txt", "r").read()
blocks = create_blocks(text)
indent = blocks[0][1]
for block, _, trail in blocks:
    wrap_block(block, indent, trail, 50)
