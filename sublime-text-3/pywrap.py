import sublime
import sublime_plugin
from Default.paragraph import expand_to_paragraph
import re

# TODO: Import pywrap methods.

class PywrapBlockCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            region = expand_to_paragraph(self.view, region.begin())
            _, blocks = create_blocks(self.view.substr(region))
            string = wrap_block(blocks[0][2], blocks[0][0])
            self.view.replace(edit, sublime.Region(region.begin(), region.end()), string)

class PywrapSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                newlines, blocks = create_blocks(self.view.substr(region))
                i = blocks[0][0]
                string = "\n" * newlines
                for _, n, b in blocks:
                    string += wrap_block(b, i, n)
                self.view.replace(edit, region, string)
