#!/usr/bin/env python3

from pywrap import *

def write(path, string):
    f = open(path, "w", newline="")
    f.write(string)
    f.close()

def read(path):
    f = open(path, "r", newline="")
    string = f.read()
    f.close()
    return string

# Test 1
string = read("./tests/test_1.txt")
string = wrap_block(string)
write("./testout/test_1.txt", string)

# Test 2
string = read("./tests/test_2.txt")
newlines, blocks = create_blocks(string)
print(newlines, blocks)
string = "\n" * newlines
i = blocks[0][0]
for _, n, b in blocks:
    string += wrap_block(b, i, n)
write("./testout/test_2.txt", string)

# Test 3
string = read("./tests/test_3.txt")
newlines, blocks = create_blocks(string)
print(newlines, blocks)
string = "\n" * newlines
i = blocks[0][0]
for _, n, b in blocks:
    string += wrap_block(b, i, n)
write("./testout/test_3.txt", string)
