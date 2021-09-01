import re
import sys

def slugify(words):
    # https://gist.github.com/hagemann/382adfc57adbd5af078dc93feef01fe1
    a = 'àáâäæãåāăąçćčđďèéêëēėęěğǵḧîïíīįìłḿñńǹňôöòóœøōõőṕŕřßśšşșťțûüùúūǘůűųẃẍÿýžźż·/_,:;'
    b = 'aaaaaaaaaacccddeeeeeeeegghiiiiiilmnnnnoooooooooprrsssssttuuuuuuuuuwxyyzzz------'
    p = "|".join(list(a))

    # regex = re.compile(p)
    slugified_words = words.lower()

    maps = [
        (r'\s+', '-'),
        (r'{}'.format(p), lambda c: b[a.find(c.group(0))]),
        (r'&', '-and-'),
        (r'[^\w\-]+', ''),
        (r'\-\-+', '-'),
        (r'^-+', ''),
        (r'-+$/', '')
    ]

    for old, new in maps:
        slugified_words = re.sub(old, new, slugified_words)
    return slugified_words