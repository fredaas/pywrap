#!/usr/bin/env python3

from pywrap import *

# Test 1
text = open("./tests/test_1.txt", "r").read()
out = wrap_block(text)
fout = open("./testout/test_1.out", "w")
fout.write(out)
fout.close()

# Test 2
text = open("./tests/test_2.txt", "r").read()
blocks = create_blocks(text)
a, b = blocks[0]
indent = blocks[1][1]
out = "\n" * a
for block, local_indent, trail in blocks[1:]:
    out += wrap_block(block, indent, trail, 60)
out += "\n" * b
fout = open("./testout/test_2.out", "w")
fout.write(out)
fout.close()

# Test 3
text = open("./tests/test_3.txt", "r").read()
blocks = create_blocks(text)
a, b = blocks[0]
indent = blocks[1][1]
out = "\n" * a
for block, local_indent, trail in blocks[1:]:
    out += wrap_block(block, indent, trail, 60)
out += "\n" * b
fout = open("./testout/test_3.out", "w")
fout.write(out)
fout.close()
