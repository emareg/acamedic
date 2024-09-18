from parsedic import read_hunspell, filter_allowed


# get entries that are in the small dictionary but not in the large
def compare_dicts(dic_small, dic_large):
    matches = {} 
    for key in dic_small.keys():
        if key[0].isupper(): continue
        if any(char in key for char in [" ", ".", "-"]): continue
        if len(key) == 1: continue
        if key not in dic_large.keys():
            matches[key] = 0
    return matches





def filter_clear_cases(dic_err, dic_full):
    toRemoveKeys = []
    for key in dic_err.keys():
        if len(key) < 4: continue
        if "'" in key: toRemoveKeys.append(key)
        if key[-4:] == "ally":   # adverb form of ic/ical
            if key[:-4] in dic_full or key[:-2] in dic_full:
                toRemoveKeys.append(key)
        if key[-4:] == "ably":   # adverb form of able
            if key[:-1]+"e" in dic_full:
                toRemoveKeys.append(key)                
    for key in toRemoveKeys:
        del dic_err[key]
    # print("Removed {} obvious test entries.".format(len(toRemoveKeys)))
    return len(toRemoveKeys)

# main

def testCorrectness():
    dicAcamedic = {}
    dicScowlFull = {}
    dicAllowedMisses = {}
    dicDisallowed = {}

    # Read own dictionary
    #read_hunspell(dicAcamedic, 'en-Academic.dic')
    read_hunspell(dicAcamedic, 'src/base/en_US_20.dic')
    read_hunspell(dicAcamedic, 'src/base/en_US_extra.dic') 
    read_hunspell(dicAcamedic, 'src/base/en_US_abbr.dic') 
    read_hunspell(dicAcamedic, 'src/base/en_Latin.dic')
    read_hunspell(dicAcamedic, 'src/academic/en_US_tech.dic')
    read_hunspell(dicAcamedic, 'src/academic/en_US_computer.dic') 
    read_hunspell(dicAcamedic, 'src/academic/en_US_math.dic')
    read_hunspell(dicAcamedic, 'src/academic/en_US_physics.dic') 
    read_hunspell(dicAcamedic, 'src/academic/en_US_med.dic')

    # Read reference dictionary
    read_hunspell(dicScowlFull, 'tests/refdics/en_US-95.dic', False)
    read_hunspell(dicScowlFull, 'tests/refdics/en_US.dic', False)

    # read double checked exceptions
    read_hunspell(dicAllowedMisses, 'tests/lists/allowNonScowl.dic')
    read_hunspell(dicAllowedMisses, 'tests/lists/allowCompounds.dic')
    read_hunspell(dicAllowedMisses, 'tests/lists/allowExtraAdverbs.dic')
    read_hunspell(dicAllowedMisses, 'tests/lists/unclear_spelling.dic')

    # disallowed words
    read_hunspell(dicDisallowed, 'tests/lists/disallowWords.dic')

    dicMissing = compare_dicts(dicAcamedic, dicScowlFull)

    filter_clear_cases(dicMissing, dicAcamedic)
    nRemoved = filter_clear_cases(dicAllowedMisses, dicAcamedic)
    dicFilt = filter_allowed(dicMissing, dicAllowedMisses)



    unmatched = [k for k in dicAllowedMisses.keys() if k not in dicFilt]
    unknown = [k for k in dicMissing.keys()]
    disallowed = list(set(dicAcamedic).intersection(set(dicDisallowed.keys())))

    if unmatched:
        print("ERR: {} exceptions already in larger dictionary: {}".format(len(unmatched), unmatched) )
    if unknown:
        print("ERR: {} words not in larger dictionary: {}".format(len(unknown), unknown))
    if disallowed:
        print("ERR: {} words that are not allowed in dictionary: {}".format(len(disallowed), disallowed))
    else:
        print("PASS: {} known exceptions found and ignored. All good.".format(len(dicAllowedMisses.keys())+nRemoved))




testCorrectness()





