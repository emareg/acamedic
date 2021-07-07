from parsedic import read_hunspell, filter_allowed

import re
import sys

# check no unknown affixes, 
# check against hunspell implementation (binary + python)


PREFIXES = "AIUCEFK"
SUFFIXES = "SDGRTYPMBL"
UNITS="du"
CHEM="aphms"

AFFIXES=PREFIXES+SUFFIXES+UNITS+CHEM



def testAffixes(text):
    dicMatched = {}
    unknown = []

    for line in text.splitlines():
        word, _, affix = line.strip().partition('/')

        for a in affix:
            if a in dicMatched.keys():
                dicMatched[a] += 1
            elif a in AFFIXES:
                dicMatched[a] = 1
            else:
                unknown.append(line)

    unmatched = [a for a in AFFIXES if a not in dicMatched.keys()]

    if unmatched:
        print("ERR: {} unmatched affixes: {}".format(len(unmatched), unmatched) )
        sys.exit(-1)
    if unknown:
        print("ERR: {} unknown affix entries: {}".format(len(unknown), unknown))
        sys.exit(-2)
    else:
        print("PASS: {} known affixes found. All good.".format(len(dicMatched.keys())))


def testWords(text):
    unknown = {}
    dicAllowSyntax = {}
    read_hunspell(dicAllowSyntax, 'tests/lists/allowSyntax.dic')

    for line in text.splitlines():
        word, _, affix = line.strip().partition('/')
        # if not word.isalnum():
        if not re.match(r'[A-Za-z][a-z]*|[A-Z]+|[0-9µ]\w{0,2}|[α-ωΑ-ΩϑϕϜϝϱϵ]', word):
            unknown[word] = 0

    filter_allowed(unknown, dicAllowSyntax)
     
    if unknown.keys():
        print("ERR: {} unknown char in word: {}".format(len(unknown), unknown.keys()))
        sys.exit(-2)
    else:
        print("PASS: no unknown characters. All good.")




def testSyntax():


    with open('en-Academic.dic', 'r') as f:
        dict_txt = f.read()

    testAffixes(dict_txt)
    testWords(dict_txt)


testSyntax()
