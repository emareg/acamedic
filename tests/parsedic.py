import re


def plural(string):
    """ returns the plural of a word """
    splural = ""
    if string[-1] in "sxz" or (string[-1] == "h" and string[-2] in "sc"):
        splural = string + "es"
    elif string[-1] == "y" and string[-2] not in "aeiou":
        splural = string[:-1] + "ies"
    else:
        splural = string + "s"
    return splural


def adverb(word):
    if word[-2:] == "ic":
        return word + "ally"
    elif len(word) > 5 and word[-3:] == "ble":
        return word[:-2] + "ly"
    elif word[-1] == "y":
        return word[:-1] + "ily"
    else:
        return word + "ly"


def parse_affix(word, affix, affextra=True):
    addwords = []
    pfxwords = [word]
    prefixes = [c for c in affix if c in "AIUCEFK"]
    suffixes = [c for c in affix if c not in "AIUCEFK"]

    for char in prefixes:
        # prefixes
        if char == 'A': pfxwords.append('re'+word) 
        elif char == 'I': pfxwords.append('in'+word)
        elif char == 'U': pfxwords.append('un'+word)
        elif char == 'C': pfxwords.append('de'+word)
        elif char == 'E': pfxwords.append('dis'+word)
        elif char == 'F': pfxwords.append('con'+word)
        elif char == 'K': pfxwords.append('pro'+word)

    for pfxword in pfxwords:
        for char in suffixes:
            if char == 'V': addwords.append(re.sub('e$|$', 'ive', pfxword))
            elif char == 'N': addwords.append(re.sub(r'(?<!ion)$', 'en', re.sub('y$', 'ication', re.sub('e$', 'ion', pfxword))))
            elif char == 'X': addwords.append(re.sub(r'(?<!ions)$', 'ens', re.sub('y$', 'ications', re.sub('e$', 'ions', pfxword))))
            elif char == 'H': addwords.append(re.sub(r'y$', 'ie', pfxword)+'th')  # 
            elif char == 'Y': addwords.append(adverb(pfxword))
            elif char == 'G': addwords.append(re.sub(r'(?<=[^eyo])e$', '', pfxword)+'ing')  # gerund
            elif char == 'J': addwords.append(re.sub(r'e$', '', pfxword)+'ings')  # gerund
            elif char == 'D': addwords.append(re.sub(r'e$', '', re.sub(r'(?<=[^aeiou])y$', 'i', pfxword))+'ed') # past
            elif char == 'T': addwords.append(re.sub(r'e$', '', re.sub(r'(?<=[^aeiou])y$', 'i', pfxword))+'est') # superlative CHECK?
            elif char == 'R': addwords.append(re.sub(r'e$', '', re.sub(r'(?<=[^aeiou])y$', 'i', pfxword))+'er')
            elif char == 'Z': addwords.append(re.sub(r'e$', '', re.sub(r'(?<=[^aeiou])y$', 'i', pfxword))+'ers')
            elif char == 'S': 
                if affextra:
                    addwords.append(plural(pfxword))
                else:
                    addwords.append(re.sub(r'(?<=[sxzh])$', 'e', re.sub(r'(?<=[^aeiou])y$', 'ie', pfxword))+'s')  # plural
            elif char == 'P': addwords.append(re.sub(r'(?<=[^aeiou])y$', 'i', pfxword)+'ness')  # 
            elif char == 'M': addwords.append(pfxword+'\'s') # noun
            elif char == 'B': addwords.append(re.sub(r'(?<=[^e])e$', '', pfxword)+'able') # adjective
            elif char == 'L': addwords.append(pfxword+'ment') # noun

    addwords += pfxwords
    return addwords 



def read_hunspell(dictionary, dictfile, affextra=True):
    lines = ""
    try:
        fh = open(dictfile, "r", encoding="utf8")
        lines = fh.read()
        fh.close()
    except FileNotFoundError:
        print("ERROR: Dictionary File '{}' not found. Install hunspell.".format(dictfile))

    lines = re.sub(r"#.*?(?:\n|$)", "\n", lines).strip()  # remove comments
    lines = re.sub(r"\n\s*\n", "\n", lines)  # empty lines

    for line in lines.splitlines():
        word, _, affix = line.strip().partition('/')
        if affix in ['m', 'h', 'c', 'i', 's', 'p']: continue
        for additional in parse_affix(word, affix, affextra):
            if additional in dictionary.keys(): 
                dictionary[additional] += 1
                if len(affix) > 0 and affix in "aphms": continue
            else:
                dictionary[additional] = 0
    print("Loaded {}: {} words".format(dictfile, len(dictionary.keys())))
    return dictionary


def filter_allowed(dic_own, dic_allow):
    dicFilt = {}
    for key in dic_allow.keys():
        if key in dic_own.keys():
            dicFilt[key] = dicFilt[key] + 1 if key in dicFilt else 0
            del dic_own[key]
    return dicFilt

