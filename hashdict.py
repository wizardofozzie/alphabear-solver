#! python3

"""
    This script reads from a file (dictionary.txt), generates a hashmap (dict)
    and dumps it to a json file. Only needs to be run once, unless the
    dictionary changes.

    It's quite slow, but once completed lookup of valid matches is blazing
    fast.
"""

import __future__
from os import path
import os
from collections import defaultdict
import json

try:
    import requests
except:
    try: import urllib
    except: import urllib.request


dictFileName = path.join(path.split(__file__)[0], "dictionary.txt") # /var/mobile/Containers/Shared/AppGroup/AA78F2EC-3EE8-40F4-A318-8A9AB1BCB5FF/Pythonista3/Documents/alphabear-solver/dictionary.txt
mapFileName =  path.join(path.split(__file__)[0], "map.json")       # /var/mobile/Containers/Shared/AppGroup/AA78F2EC-3EE8-40F4-A318-8A9AB1BCB5FF/Pythonista3/Documents/alphabear-solver/map.json


dicttxt = "https://raw.github.com/jmlewis/valett/master/scrabble/sowpods.txt"


def dl_dict():
    if not os.path.exists(dictFileName):
        r = requests.get(dicttxt)
        assert r.ok
        with open("dictionary.txt", "w") as fo:
            fo.write(r.text.splitlines)

def main():
    dictmap = create_dict(dictFileName)
    store_json(dictmap)
    print("JSON file generated from " + dictFileName)
    #d = read_json(mapFileName)
    #print(d)


def create_dict(filename):
    """
        Reads a txt file of words, one word per line, and stores that in a map
        (dict).

        Keys are unique signatures of one or more words - an ordered list of
        letters that can make up each word in the dictionary. The values are
        the words the signature can make.

    :return dmap:
    :param filename: A text file, one word per line
    """
    # the "signature" of a word is the ordered list of its letters

    # open the wordlist
    dictfile = open(filename)
    # associate to each signature the words that have that signature
    dmap = defaultdict(list)

    for word in dictfile.readlines():
        word = word.lower()
        signature = "".join(sorted(word.strip()))  # get the word signature
        dmap[signature].append(word.strip())

    dictfile.close()

    return dmap


def store_json(dmap):
    """Stores the map as a json txt file. """

    jsoncontent = json.dumps(dmap)

    with open(mapFileName, "w") as f:
        f.write(jsoncontent)


def read_json(filename):
    """
        Reads a json file and returns it as a dict (map)
    :param filename:
    :return json dict:
    """

    with open(filename) as f:

        data = json.loads(f.read())

    return data


if __name__ == '__main__':
    main()
