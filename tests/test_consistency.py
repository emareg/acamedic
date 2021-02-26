from parsedic import read_hunspell, filter_allowed
import re
import sys


COMMON_SUFFIXES=(
    'ry', 'ncy', 'acy', 'ion', 'ity', 'ism', 'ment', 'ness', 'nce', 'ogy', 'phy', 
    'ium', 'uum', 'num',  #latin
    's', 'ed', 'ing', 'ize', 'ate', 'ify', # verbs
    'al', 'ic', 'ive', 'ary', 'able', 'ible', 'less', 'est', 'ent', 'ful', # adjectives
    'ant', 'er', 'tor', 'sor', 'ist', 'ian', # persons
    'ly', # adverbs
    'ase', # enzyms 
    're', 'ke', 'ge', 'ne', 'te', 'le', # too many words
    )

def findInconsistencies(dictionary):
    dicInconsistent = {}
    for word in dictionary.keys():
        if word.endswith(('icly', 'yly', 'abley', 'lely')): # wrong adverb forms
            dicInconsistent[word] = dictionary[word]
        if re.match(r'.+(?:thes|xs|[^aeuo]ys)$', word):  # wrong plural forms
            dicInconsistent[word] = dictionary[word]
        if re.match(r'\w{3,10}(?:ed|able|less|ful|ify|ize|ly)\'s$', word): # wrong possessive forms
            dicInconsistent[word] = dictionary[word]

        # todo: check that -ing forms have -s  AND that -est (T) forms have (R)

        # if len(word) > 8 and not word[0].isupper():
        #     mainword = re.sub(r'^(micro|milli|pico|kilo|mega|giga|tera|anti|mis|super|over|under|hyper|sub|counter)(.+)$', r'\2', word)
        #     if len(mainword) > 8 and not mainword.endswith(COMMON_SUFFIXES):
        #         dicInconsistent[word] = dictionary[word]
    return dicInconsistent


## Main Execution
## ===================================================

def testConsistency():
    dicAcamedic = {}
    dicInconsistent = {}
    dicAllowedInconsistent = {}

    read_hunspell(dicAcamedic, 'en-Academic.dic')
    read_hunspell(dicAllowedInconsistent, 'tests/lists/allowInconsistencies.dic')


    dicInconsistent = findInconsistencies(dicAcamedic)

    dicFilt = filter_allowed(dicInconsistent, dicAllowedInconsistent)
    unmatched = [k for k in dicAllowedInconsistent.keys() if k not in dicFilt]
    unknown = [k for k in dicInconsistent.keys()]

    if unmatched:
        print("ERR: {} unmatched known inconsistencies: {}".format(len(unmatched), unmatched) )
        sys.exit(-1)
    elif unknown:
        print("ERR: {} unknown new inconsistencies: {}".format(len(unknown), unknown))
        sys.exit(-2)
    else:
        print("PASS: {} known inconsistencies found and ignored. All good.".format(len(dicAllowedInconsistent.keys())))



testConsistency()
