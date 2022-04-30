import re
from spellchecker import SpellChecker

def reduce_lengthening(s):
    pattern = re.compile(r"(.)\1{2,}")
    return s.str.replace(pattern, r"\1\1")

def remove_extra_whitespace(s):
    # Remove from beginning and end of string
    s = s.str.strip()
    # Remove between words
    # NB. \s matches any whitespace (like a tab) and not just a space.
    pattern = re.compile(r"(\s){2,}")
    return s.str.replace(pattern, r"\1")

def drop_possessive_s(s):
    return s.str.replace("\'s", "")

def clean_responses(x):
    x = reduce_lengthening(x.str.lower())
    x = remove_extra_whitespace(x)
    x = drop_possessive_s(x)
    return x

def flag_misspelled(x):
    spell = SpellChecker()
    r = list(x)
    u = spell.unknown(r)
    z = [w in u for w in r]
    #s = [spell.correction(w) for w in u]
    return z

