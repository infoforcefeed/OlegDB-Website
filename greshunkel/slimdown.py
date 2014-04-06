"""
This is ported from the original PHP version here:
https://gist.github.com/jbroadway/2836900
"""
import re

class Slimdown(object):
    def __init__(self):
        self.rules = {
            r'(#+)(.*)': self.header,
            r'\[([^\[]+)\]\(([^\)]+)\)' : r'<a href=\2>\1</a>',
            r'(\*\*|__)(.*?)\1' : r'<strong>\2</strong>',
            r'(\*|_)(.*?)\1' : r'<em>\2</em>',
            r'\~\~(.*?)\~\~' : r'<del>\1</del>',
            r'\:\"(.*?)\"\:' : r'<q>\1</q>',
            r'`(.*?)`' : r'<code>\1</code>',
            r'\n\*(.*)' : self.ul_list,
            r'\n[0-9]+\.(.*)' : self.ol_list,
            r'\n(&gt;|\>)(.*)' : self.blockquote,
            r'\n-{5,}/' : r"\n<hr />",
            r'\n([^\n]+)' : self.para,
            r'<\/ul>\s?<ul>' : '',
            r'<\/ol>\s?<ol>' : '',
            r'<\/blockquote><blockquote>' : r"\n"
        }

    def para(self, match):
        line = match.group(0)
        stripped = line.strip()
        regex = re.compile(r'/^<\/?(ul|ol|li|h|p|bl)/')

        if regex.match(stripped):
            return "\n{line}\n".format(line=line)
        return "\n<p>{}</p>\n".format(stripped)

    def ul_list(self, regs):
        item = regs[1]
        return "\n<ul>\n\t<li>{}</li>\n</ul>".format(item.strip())

    def ol_list(self, regs):
        item = regs[1]
        return "\n<ol>\n\t<li>{}</li>\n</ol>".format(item.strip())

    def blockquote(self, regs):
        item = regs[1]
        return "\n<blockquote>{}</blockquote>".format(item.strip())

    def header(self, regs):
        tmp, chars, header = regs
        level = len(chars)
        return '<h{level}>{header}</h{level}>'.format(level=level, header=header.strip())

    def render(self, text):
        text = "\n{text}\n".format(text=text)
        for rule, output in self.rules.iteritems():
            regex = re.compile(rule)
            text = regex.sub(output, text)

        return text.strip()
