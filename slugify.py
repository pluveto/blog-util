import sys

from lib import slug_util
from lib import translate_util

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("error: missing arg")
        exit(1)
    word = " ".join(sys.argv[1:])
    word = translate_util.ch_to_en(word)
    print(slug_util.slugify(word))
