"""
This is ported from the original PHP version here:
https://gist.github.com/jbroadway/2836900
"""
import re

class Slimdown(object):
    def __init__(self):
        self.rules = [
            (r'\n([^\n]+)' ,  r'<p>\1</p>'),
            (r'````([^`]*)````' ,  r'<pre><code>\1</code></pre>'),
            (r'`([^`]*)`' ,  r'<code>\1</code>'),
            (r'\[([^\[]+)\]\(([^\)]+)\)' ,  r'<a href=\2>\1</a>'),
            (r'(#+)(.*)',  self.header),
            (r'(\*\*|__)(.*?)\1' ,  r'<strong>\2</strong>'),
            (r'(\*|_)(.*?)\1' ,  r'<em>\2</em>'),
            (r'\~\~(.*?)\~\~' ,  r'<del>\1</del>'),
            (r'\, \"(.*?)\"\, ' ,  r'<q>\1</q>'),
            (r'\n\*(.*)' ,  self.ul_list),
            (r'\n[0-9]+\.(.*)' ,  self.ol_list),
            (r'\n(&gt;|\>)(.*)' ,  self.blockquote),
            (r'\n-{5,}/' ,  r"\n<hr />"),
            (r'<\/ul>\s?<ul>' ,  ''),
            (r'<\/ol>\s?<ol>' ,  ''),
            (r'<\/blockquote><blockquote>' ,  r"\n")
        ]

    def para(self, match):
        line = match.group(0)
        stripped = line.strip()
        regex = re.compile(r'/^<\/?(ul|ol|li|h|p|bl)/')

        if regex.match(stripped):
            return stripped
        return "<p>{}</p>".format(stripped)

    def ul_list(self, match):
        item = match.group(0)
        return "\n<ul>\n\t<li>{}</li>\n</ul>".format(item.strip())

    def ol_list(self, match):
        item = match.group(0)
        return "\n<ol>\n\t<li>{}</li>\n</ol>".format(item.strip())

    def blockquote(self, match):
        item = match.group(0)
        return "\n<blockquote>{}</blockquote>".format(item.strip())

    def header(self, match):
        raise NotImplementedError()
        tmp, chars, header = match
        level = len(chars)
        return '<h{level}>{header}</h{level}>'.format(level=level, header=header.strip())

    def render(self, text):
        text = "\n{text}\n".format(text=text)
        import ipdb; ipdb.set_trace()
        for rule, output in self.rules:
            regex = re.compile(rule)
            text = regex.sub(output, text)

        return text.strip()
