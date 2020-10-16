import re
import sublime
import sublime_plugin

from Default.paragraph import expand_to_paragraph


def lspace(s):
    i = 0
    while i < len(s) and s[i] == " ":
        i += 1
    return i


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
    block += " " * indent + line.rstrip() + "\n"

    return block + "\n" * newlines


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
        blockline += line + " "
        i += 1

    if blockline != "":
        blocks.append((blockline, block_indent, 0))

    return newlines, blocks


def get_wrap_width(view):
    wrap_width = view.settings().get("wrap_width")
    if not wrap_width or wrap_width < 10:
        return 80
    return wrap_width


class WrapBlock(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        wrap_width = get_wrap_width(view)
        region = view.sel()[0]
        region = expand_to_paragraph(view, region.begin())
        string = wrap_stream(view.substr(region), cutoff=wrap_width)
        view.replace(edit, sublime.Region(region.begin(), region.end()), string)


class WrapSelection(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        wrap_width = get_wrap_width(view)
        region = view.sel()[0]
        if not region.empty():
            newlines, blocks = create_blocks(self.view.substr(region))
            string = "\n" * newlines
            for block in blocks:
                string += wrap_stream(*block, cutoff=wrap_width)
            self.view.replace(edit, region, string)
