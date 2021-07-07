# we do not want to mask mistakes by other correct words

from parsedic import read_hunspell, filter_allowed
import sys


def findTypoFriends(dictionary):
    """ finds all words that are only one edit apart from each other """
    dicTypoFriends = {}
    for word in dictionary.keys():
        if len(word) < 4: continue
        #if word[-1] in "sd": continue 
        if word[-3:] in ["ble", "bly"]: continue
        if word[0].isupper(): continue
        for edit in edits1(word):
            if edit in dictionary:
                if edit[-1] == "s" or edit == word: continue
                if word not in dicTypoFriends and edit not in dicTypoFriends:
                    dicTypoFriends[word] = edit
    return dicTypoFriends







def typo_letters(c):
    typos = {
        'q': 'wa',
        'w': 'aesv',
        'e': 'wsria',
        'r': 'fen',
        't': 'rfzd',
        'z': 'gasx',
        'u': 'zoya',
        'i': 'jyel',
        'o': 'lpu',
        'p': 'ob',  
        'a': 'qwszeu',
        's': 'weaxz',
        'd': 'efct',
        'f': 'rtdv',
        'g': 'yzck',
        'h': 'bn',
        'j': 'ik',
        'k': 'iojlgc',
        'l': 'ki',
        'y': 'sxgui',
        'x': 'syc',
        'c': 'xdvk',
        'v': 'cf',
        'b': 'hnp',
        'n': 'bhm',
        'm': 'n',
        '-': '',
        ' ': '',
    }
    if c not in typos.keys(): return "esianrtolcdugmphbyfvkwz"
    return typos[c.lower()]


def edits1(word):
    "All edits that are one edit away from `word`."
    letters = "esianrtolcdugmphbyfvkwz"
    splits = [(word[:i], word[i:]) for i in range(2, len(word)-1)]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in typo_letters(R[0])]
    inserts = [L + c + R for L, R in splits for c in letters]
    deletes = [L + R[1:] for L, R in splits if R]
    if len(word) <= 4:
        return list(set(transposes))
    elif len(word) <= 6:
        return list(set(transposes + replaces))
    elif len(word) == 7:
        return list(set(transposes + replaces + inserts))  
    elif 7 < len(word):
        return list(set(transposes + replaces + inserts + deletes))
    #return list(set(inserts + deletes))



## Main Execution
## ===================================================

def testSpecificity():
    dicAcamedic = {}

    read_hunspell(dicAcamedic, 'en-Academic.dic')

    dicTypoFriends = findTypoFriends(dicAcamedic)

    for word,edit in dicTypoFriends.items():
        print("Neighbors: {:20} : {:20}".format(word, edit))


testSpecificity()
