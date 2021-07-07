from parsedic import read_hunspell, filter_allowed, compound
import re
import sys


COMMON_SUFFIXES=(
    'ry', 'ncy', 'acy', 'ion', 'ity', 'asm', 'ism', 'ment', 'ness', 'nce', 'ogy', 'phy', 'ique', 'graph', 'hood',
    'ium', 'uum', 'num',  #latin
    's', 'ed', 'ing', 'ize', 'ate', 'ify', 'ish', # verbs
    'al', 'ic', 'ive', 'ary', 'able', 'ible', 'less', 'est', 'ent', 'ful', 'lar', # adjectives
    'ant', 'er', 'tor', 'sor', 'ist', 'ian', # persons
    'ly', # adverbs
    'ase', # enzyms 
    're', 'ke', 'ge', 'ne', 'te', 'le', # too many words
    )

def findInconsistencies(dictionary):
    dicInconsistent = {}
    for word in dictionary.keys():
        if any(x.isdigit() for x in word[1:]):         # digit in word
            dicInconsistent[word] = dictionary[word]

        if word.endswith(('icly', 'yly', 'abley', 'lely')): # wrong adverb forms
            dicInconsistent[word] = dictionary[word]
        if re.match(r'.+(?:thes|xs|[^aeuo]ys)$', word):  # wrong plural forms
            dicInconsistent[word] = dictionary[word]
        if re.match(r'\w{3,10}(?:ed|able|less|ful|ify|ize|ly)\'s$', word): # wrong possessive forms
            dicInconsistent[word] = dictionary[word]

        if len(word) > 5 and re.match(r'[qwrtzpsdfghklxcvbnm]{3}(?<!sch|spr|str|sph|scr|spl|chr|chl|phr|thr)', word): # three consonants
            dicInconsistent[word] = dictionary[word]            

        if len(word) > 9 and not word[0].isupper():
            # if word.endswith('ing') and word[:-3]+'s' not in dictionary:   # -ing words have -s variant
            #     dicInconsistent[word] = dictionary[word]
            if word.endswith('iest') and word[:-2]+'r' not in dictionary:   # all -iest words have -ier
                dicInconsistent[word] = dictionary[word]

            # if word.endswith('able') and word[:-1]+'y' not in dictionary:   # all -able words have -ably
            #     dicInconsistent[word] = dictionary[word]

            # mainword = re.sub(r'\b(micro|milli|pico|kilo|mega|giga|mono|tera|octa|tetra|anti|auto|dis|fore|iso|mis|multi|pre|super|trans|over|under|un|hyper|hypo|hydro|sub|counter|ultra)', '', word)
            # if len(mainword) > 9 and not mainword.endswith(COMMON_SUFFIXES) and not compound(mainword, dictionary):
            #     dicInconsistent[word] = dictionary[word]
    return dicInconsistent


## Main Execution
## ===================================================

def testConsistency():
    dicAcamedic = {}
    dicInconsistent = {}
    dicAllowedInconsistent = {}

    read_hunspell(dicAcamedic, 'src/base/en_US_20.dic')
    read_hunspell(dicAcamedic, 'src/base/en_US_extra.dic') 
    read_hunspell(dicAcamedic, 'src/base/en_Latin.dic')
    read_hunspell(dicAcamedic, 'src/academic/en_US_biota.dic')
    read_hunspell(dicAcamedic, 'src/academic/en_US_tech.dic')
    read_hunspell(dicAcamedic, 'src/academic/en_US_computer.dic') 
    read_hunspell(dicAcamedic, 'src/academic/en_US_math.dic')
    read_hunspell(dicAcamedic, 'src/academic/en_US_physics.dic') 
    read_hunspell(dicAcamedic, 'src/academic/en_US_med.dic')


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
