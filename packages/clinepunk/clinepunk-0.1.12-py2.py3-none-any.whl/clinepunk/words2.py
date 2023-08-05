import logging
import pathlib
import random
import sys
import typing

import pkg_resources

__WORD_LIST__: typing.List[str] = []


def parse_flist(path):
    package = __name__.split(".")[0]
    TEMPLATES_PATH = pathlib.Path(
        pkg_resources.resource_filename(package, "wordlists/")
    )
    path = TEMPLATES_PATH / "words3.txt"
    words = []
    for line in path.read_text().splitlines():
        if line.startswith("#"):
            continue
        clean = line.strip()
        words.append(clean)
    return words


def _generate_word_list():
    logging.debug("_generate_word_list")
    words = parse_flist("clinepunk/wordlists/words.txt")
    return list(filter(lambda x: len(x) >= 2, words))


def get_words(count=2):
    global __WORD_LIST__
    if not __WORD_LIST__:
        __WORD_LIST__ = _generate_word_list()

    sample = random.sample(__WORD_LIST__, count)

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

    lst = get_words(count=2)
    out = "".join(lst)
    logging.debug(out)

    lst = get_words(count=2)
    out = "".join(lst)
    logging.debug(out)
    return out


if __name__ == "__main__":
    main()
