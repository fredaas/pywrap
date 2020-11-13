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
string = read("./tests/test1.txt")
string = wrap_stream(string)
write("./testout/test1.txt", string)

# Test 2
string = read("./tests/test2.txt")
newlines, blocks = create_blocks(string)
string = "\n" * newlines
for block in blocks:
    string += wrap_stream(*block)
write("./testout/test2.txt", string)

# Test 3
string = read("./tests/test3.txt")
newlines, blocks = create_blocks(string)
string = "\n" * newlines
for block in blocks:
    string += wrap_stream(*block)
write("./testout/test3.txt", string)

# Test 4
string = read("./tests/test4.txt")
newlines, blocks = create_blocks(string)
string = "\n" * newlines
for block in blocks:
    string += wrap_stream(*block)
write("./testout/test4.txt", string)

# Test 5
string = read("./tests/test5.txt")
newlines, blocks = create_blocks(string)
string = "\n" * newlines
for block in blocks:
    string += wrap_stream(*block)
write("./testout/test5.txt", string)

# Test 6
string = read("./tests/test6.txt")
newlines, blocks = create_blocks(string)
string = "\n" * newlines
for block in blocks:
    string += wrap_stream(*block, cutoff=30)
write("./testout/test6.txt", string)
