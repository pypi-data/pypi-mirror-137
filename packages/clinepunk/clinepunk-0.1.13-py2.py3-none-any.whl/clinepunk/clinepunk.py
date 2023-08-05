import json
import logging
import pathlib
import random
import sys

import appdirs
import humanfriendly
import requests

from clinepunk import cache as cachemod
from clinepunk import words2

cache_path = pathlib.Path(appdirs.user_cache_dir(appname="clinepunk"))
url = "https://raw.githubusercontent.com/adambom/dictionary/master/dictionary.json"


def refresh_cache():
    r = requests.get(url)

    if r.status_code == 200:
        dct = r.json()
        js = json.dumps(dct, indent=2).encode("utf-8")
        return js
    return ""


def sample(count=2):
    return words2.get_words(count=2)


def get_words(count=2):
    js = cachemod.cache(cache_path, refresh_cache, "clinepunk.words")
    words = json.loads(js)
    words = words.keys()
    words = list(filter(lambda x: len(x) >= 3 and len(x) <= 7, words))

    size = humanfriendly.format_size(cache_path.stat().st_size, binary=True)
    logging.debug(f"cache path is {cache_path}")
    logging.debug(f"cache has {len(words):,d} words")
    logging.debug(f"cache has size {size}")

    remove = ["-", "sex", " "]
    sample = random.sample(words, count)
    for word in remove:
        if word in "".join(sample):
            sample = random.sample(words, count)

    logging.debug(f"sample words is {sample}")

    return [x.lower() for x in sample]


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="{%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(f"{pathlib.Path(__file__).stem}.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    # lst = get_words(count=2)
    lst = words2.get_words(count=2)
    out = "".join(lst)
    logging.debug(out)
    return out


if __name__ == "__main__":
    main()
