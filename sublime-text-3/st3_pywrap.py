import sublime
import sublime_plugin
from Default.paragraph import expand_to_paragraph
import re

# TODO: Import pywrap methods.

class PywrapBlock(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            region = expand_to_paragraph(self.view, region.begin())
            blocks = create_blocks(self.view.substr(region))
            indent = blocks[1][1]
            out = ""
            for block, local_indent, trail in blocks[1:]:
                out += wrap_block(block, indent, trail, 80)
            self.view.replace(edit, sublime.Region(region.begin(), region.end()), out)

class PywrapSelection(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                blocks = create_blocks(self.view.substr(region))
                newlines, _ = blocks[0]
                indent = blocks[1][1]
                out = "\n" * newlines
                for block, local_indent, trail in blocks[1:]:
                    out += wrap_block(block, indent, trail, 80)
                self.view.replace(edit, region, out)
