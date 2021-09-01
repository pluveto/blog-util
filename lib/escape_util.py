
import os
import sys
import re

def _escape_multiline(m):
    original = m.group(1)
    s = re.sub(r'(\r\n.?)+', r'\r\n', original)
    s = '\n'.join([line.strip() for line in s.splitlines()])
    return "\n<div>\n$$\n%s\n$$\n</div>\n" % (s.strip('\n'))


def _escape_singleline(m):
    return "$%s$" % _escape(m)


def _escape(m):
    return re.sub(r"([<>*_()\[\]#\\])", r"\\\1", m.group(1))


def escape_math(s0):
    # s0 = open(path, 'r', encoding='utf-8').read()
    s1 = re.sub(r'\$\$\n*((.|\n)*?)\n*\$\$', _escape_multiline, s0)
    # print(s1)
    s2 = re.sub(r'\$(.*?)\$', _escape_singleline, s1)
    return s2


