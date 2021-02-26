from parsedic import read_hunspell, filter_allowed
import sys

def findDplicates(dictionary):
    dicDuplicates = {}
    for word in dictionary.keys():
        if dictionary[word] > 0: 
            dicDuplicates[word] = dictionary[word]
    return dicDuplicates


## Main Execution
## ===================================================

def testDuplicates():
    dicAcamedic = {}
    dicDuplicates = {}
    dicAllowedDuplicates = {}

    read_hunspell(dicAcamedic, 'en-Academic.dic')
    read_hunspell(dicAllowedDuplicates, 'tests/lists/allowDuplicates.dic')


    dicDuplicates = findDplicates(dicAcamedic)

    dicFilt = filter_allowed(dicDuplicates, dicAllowedDuplicates)
    unmatched = [k for k in dicAllowedDuplicates.keys() if k not in dicFilt]
    unknown = [k for k in dicDuplicates.keys()]

    if unmatched:
        print("ERR: {} unmatched known duplicates: {}".format(len(unmatched), unmatched) )
        sys.exit(-1)
    elif unknown:
        print("ERR: {} unknown new duplicates: {}".format(len(unknown), unknown))
        sys.exit(-2)
    else:
        print("PASS: {} known duplicates found and ignored. All good.".format(len(dicAllowedDuplicates.keys())))



testDuplicates()





