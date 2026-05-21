import json
import os
import re

# -----------------------------------------------
# 1. Paths – both input and output will be in the same folder as this script
# -----------------------------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
dict_path = os.path.join(script_dir, "dictionary.json")
output_path = os.path.join(script_dir, "dictionary_cleaned.json")

# Load the dictionary
with open(dict_path, "r", encoding="utf-8") as f:
    full_dict = json.load(f)


# -----------------------------------------------
# 2. Helpers
# -----------------------------------------------
def is_number_entry(english_word: str) -> bool:
    """Return True if the word is a number (digit or spelled) or number‑like."""
    if english_word.isdigit():
        return True

    num_words = {
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
        "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
        "seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty", "fifty",
        "sixty", "seventy", "eighty", "ninety", "hundred", "thousand", "million",
        "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth",
        "ninth", "tenth", "eleventh", "twelfth", "thirteenth", "fourteenth",
        "fifteenth", "sixteenth", "seventeenth", "eighteenth", "nineteenth",
        "twentieth", "thirtieth", "fortieth", "fiftieth", "sixtieth", "seventieth",
        "eightieth", "ninetieth", "hundredth", "thousandth", "millionth",
    }
    lower = english_word.lower()

    if lower in num_words:
        return True

    # Hyphenated numbers like "twenty-one"
    if re.fullmatch(r"[a-z]+-[a-z]+", lower):
        parts = lower.split("-")
        if all(part in num_words for part in parts):
            return True

    # Ordinals: 1st, 2nd, 3rd, 4th, 21st, etc.
    if re.fullmatch(r"\d+(st|nd|rd|th)", lower):
        return True

    # Number‑point combos: "1-point", "2-points", "one-point", etc.
    if "-point" in lower or lower.endswith("-point"):
        return True

    return False


def looks_like_mangling(eng: str, trans: str) -> bool:
    """
    Return True if the translation appears to be a simple mangling
    (truncation) of the English word.
    """
    if not trans or not eng:
        return False

    # Translation must be a prefix of the English word (otherwise it's probably a real word)
    if not eng.lower().startswith(trans.lower()):
        return False

    # Suspicious if English is long (>6) and translation is very short (≤6)
    if len(eng) > 6 and len(trans) <= 6:
        return True

    # If both are short, it's probably fine (abbreviation, etc.)
    return False


# -----------------------------------------------
# 3. Filter
# -----------------------------------------------
cleaned = {}
removed = 0

for eng, trans in full_dict.items():
    if is_number_entry(eng):
        cleaned[eng] = trans
    elif looks_like_mangling(eng, trans):
        removed += 1
        # Uncomment to see what’s being removed:
        # print(f"Removing: {eng} → {trans}")
    else:
        cleaned[eng] = trans

# -----------------------------------------------
# 4. Save cleaned dictionary
# -----------------------------------------------
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=4)

print(f"Original entries: {len(full_dict)}")
print(f"Cleaned entries : {len(cleaned)}")
print(f"Removed (mangled) : {removed}")
print(f"Cleaned file saved to: {output_path}")