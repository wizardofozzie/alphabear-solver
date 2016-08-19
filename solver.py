#! python3

"""
    This script uses the hashmap (dict) generated in hashdict.py and uses it to
    find all valid matched of letters inputted to words.

"""
import hashdict
import itertools
import re
from collections import defaultdict
import copy

MINLEN = 5

def main():
    dmap = hashdict.read_json("map.json")
    global MINLEN
    MINLEN = int(input("Min word len"))
    minlen = MINLEN
    first_loop = True
    # Loops until user enters the character "0"
    while True:
        if first_loop:
            s = ""
            while s not in ("y", "Y", "n", "N"):
                s = input("Input turns? (y/n)")
                turns = s in ("y", "Y")
        
        letters = get_letters(minlen, turns)

        if "0" in letters:
            break
        else:

            # Print letters so user can check the inputs
            print("\nYour letters are")
            for L in letters:
                print(L, end=" ")
            print()

            if turns:
                parse_turns(letters, dmap)
            else:
                signatures = get_signatures(letters)
                matches = get_matches(dmap, signatures)
                print_matches(matches)


def get_letters(minlen=1, turns=False):
    """Returns a sanitised, sorted list of letters.

    :param turns: (bool) Whether the user should input them amount of turns.
    :return letters:
    """

    if turns:
        print("Syntax: [1];[2];[3];...[n] \n"
              "Where [1], [2] ... [n] are a list of letters (no spaces) with "
              "that amount of turns left.")
        arg = turns_popup()

        letterssorted = []
        if valid_syntax(arg):
            # Gets a list of letter groups
            lettergroups = arg.split(";")
            # Each letter group is sorted

            # Sort the groups
            for letters in lettergroups:
                letterssorted.append(sorted(letters))

            return letterssorted
        else:
            letterssorted.append("0")
            return letterssorted

    else:
        s = input("Input letters (no spaces): ")

        letters = []
        for letter in sorted(s):
            letters.append(letter)

        return letters


def get_matches(dmap, signatures):
    """
    """

    matches = []

    for signature in signatures:
        try:
            matches = matches + dmap[signature]
        except KeyError:
            pass

    return matches


def print_matches(matches):
    print("\nLength | Words\n-------|------")
    for match in matches:
        print("{0:6} | {1}".format(len(match), match))


def get_signatures(letters, minlen=1):
    """Generates all possible unique combination of the list of letters provided."""

    signatures = []
    minlen = len(letters) if minlen >= len(letters) else 1 if minlen < 1 else minlen
    for i in range(minlen, len(letters)):

        # Generates all sets k
        k = list(itertools.combinations(range(minlen-1, len(letters)), i))

        for kSet in k:
            signature = ""
            for pointer in kSet:
                signature = signature + letters[pointer]

            signature = "".join(sorted(signature))
            signatures.append(signature)

    # Finally check if raw letters are a valid signature
    signature = ""
    for letter in letters:  #
        signature += letter
    signature = "".join(sorted(signature))
    signatures.append(signature)

    return remove_dupes(signatures)


def remove_dupes(lst):
    """Returns all duplicates from a list (takes lst, returns unique_lst)"""

    output = []
    seen = set()
    for value in lst:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


def valid_syntax(arg):
    """Validates syntax used in parse_turns."""
    return bool(re.match(r"<(([a-z]+|\s?);)+[a-z]*>", "<{}>".format(arg)))


def parse_turns(lsletters, dmap):
    """Used when you want to use the 'turns' syntax. Prints the top 3 words to play, calculates using get_score."""
    letters = []
    turnmap = get_turn_map(lsletters)

    for ls in lsletters:
        for l in ls:
            letters.append(l)

    letters = sorted(letters)
    signatures = get_signatures(letters, MINLEN)

    matches = get_matches(dmap, signatures)
    print_matches(matches)

    scoredict = defaultdict(list)
    for match in matches:
        score = get_score(turnmap, match)

        scoredict[score].append(match)

    print("Top 3 words:")

    counter = 0
    for score in reversed(sorted(scoredict)):
        if counter == 3:
            break
        print("{0}. {1}".format(counter, scoredict[score]))
        counter += 1


def get_turn_map(lsletters):
    """Returns a map with the score as the key, and the words with that score as the corresponding values."""
    index = 1

    turnmap = defaultdict(list)
    for ls in lsletters:
        for letter in ls:
            if letter != " ":
                turnmap[index].append(letter)
        index += 1

    return turnmap


def get_score(turnmap, match):
    """Gets the score of each word. (NOT actual game score, just a number used to rank the words)"""
    score = 0
    tm = copy.deepcopy(turnmap)  # Create copy.

    for c in match:
        for k in tm:
            if c in tm[k]:
                # Removes first character
                match = match[1:]
                tm[k].remove(c)

                if k == 1:        score += 100
                elif k == 2:      score += 6
                elif k == 3:      score += 5
                else:             score += 1

    return score


def turns_popup():
    import collections, dialogs, ui
    def form_dialog_from_fields_dict(title, fields_dict, autotext=False, colors=True):
        ret = [{'title': k, 'type': v} for k, v in fields_dict.items()]
        if not autotext:
            for d in ret:
                d.update({
                    "autocorrection": False,
                    "autocapitalization": ui.AUTOCAPITALIZE_NONE,
                })
        if colors:
            for i, d in enumerate(ret, start=1):
                d.update({
                    "tint_color": "#{0}".format(
                        'ff0000' if i == 1 else
                        'ffae55' if i == 2 else
                        'f4ff00' if i == 3 else
                        '00ff16'
                        )
                })
        return dialogs.form_dialog(title, ret) 
    
    my_fields_dict1 = collections.OrderedDict((
    ('1',      'text'), ('2',     'text'), ('3',      'text'),
    ('4',      'text'), ('5',     'text'), ('6',      'text'),
    ('7',      'text'), ('8',     'text'), ('9',      'text'),
    ('10',     'text'),
    ))
    try:
        d = form_dialog_from_fields_dict("Enter letters (group by turns)", my_fields_dict1, False, True)
    except:
        return ";"*9

    argz = d['1'], d['2'], d['3'], d['4'], d['5'], d['6'], d['7'], d['8'], d['9'], d['10']

    return "{0};{1};{2};{3};{4};{5};{6};{7};{8};{9}".format(*argz)


if __name__ == '__main__':
    main()