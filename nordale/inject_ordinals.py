import json
import os

# Get the directory where THIS script is running so we find the right dictionary.json
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
dict_path = os.path.join(SCRIPT_DIR, "dictionary.json")

def get_nordalian_zahlen_str(n):
    if n == 1: return "un"
    if n == 11: return "onze"
    if n == 12: return "zwölf"
    if n == 15: return "fünfzehn"
    if n == 100: return "100"  # Raw pass-through rule
    
    germanic_ones = ["", "un", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun"]
    germanic_teens = ["zehn", "onze", "zwölf", "dreizehn", "vierzehn", "fünfzehn", "sechzehn", "siebzehn", "achtzehn", "neunzehn"]
    germanic_tens = ["", "zehn", "zwanzig", "dreißig", "vierzig", "fünfzig", "sechzig", "siebzig", "achtzig", "neunzig"]
    
    if 0 <= n < 10: 
        return germanic_ones[n]
    if 10 <= n < 20: 
        return germanic_teens[n - 10]
    
    tens_val = n // 10
    ones_val = n % 10
    if ones_val == 0:
        return germanic_tens[tens_val]
    else:
        return f"{germanic_ones[ones_val]}und{germanic_tens[tens_val]}"

def get_english_number_str(n):
    english_ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    english_teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    english_tens = ["", "ten", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    if n == 100: return "hundred"
    if 0 <= n < 10: return english_ones[n]
    if 10 <= n < 20: return english_teens[n - 10]
    
    tens_val = n // 10
    ones_val = n % 10
    if ones_val == 0:
        return english_tens[tens_val]
    else:
        return f"{english_tens[tens_val]}-{english_ones[ones_val]}"

def get_english_ordinal_suffix(n):
    if 11 <= n % 100 <= 13:
        return "th"
    else:
        return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")

def get_english_written_ordinal(n):
    # Base dictionaries for conversion logic
    ones_ord = ["", "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth"]
    teens_ord = ["tenth", "eleven-th", "twelf-th", "thirteen-th", "fourteen-th", "fifteen-th", "sixteen-th", "seventeen-th", "eighteen-th", "nineteen-th"]
    tens_ord = ["", "tenth", "twentieth", "thirtieth", "fortieth", "fiftieth", "sixtieth", "seventieth", "eightieth", "ninetieth"]
    english_tens = ["", "ten", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

    if n == 100: return "hundredth"
    if 0 <= n < 10: return ones_ord[n]
    if 10 <= n < 20: return teens_ord[n - 10]
    
    tens_val = n // 10
    ones_val = n % 10
    if ones_val == 0:
        return tens_ord[tens_val]
    else:
        return f"{english_tens[tens_val]}-{ones_ord[ones_val]}"

# Load existing dictionary file first so we protect all current data
if os.path.exists(dict_path):
    with open(dict_path, "r", encoding="utf-8") as f:
        existing_dict = json.load(f)
else:
    existing_dict = {}

ordinal_vocabulary = {}

# Generate Ordinals from 1 to 100
for i in range(1, 101):
    nord_base = get_nordalian_zahlen_str(i)
    eng_dig_suffix = get_english_ordinal_suffix(i)
    eng_word_ord = get_english_written_ordinal(i)
    
    # Nordalian Abbreviated Ordinal Logic (e.g., "un-st", "100-te")
    if i == 1:
        nord_dig_ordinal = "un-st"
    elif i == 2:
        nord_dig_ordinal = "zwei-nd"
    elif i == 3:
        nord_dig_ordinal = "drei-rd"
    elif i == 100:
        nord_dig_ordinal = "100-te"
    else:
        nord_dig_ordinal = f"{nord_base}-te"
        
    # Nordalian Written Word Ordinal Logic (Flat, unhyphenated style)
    if i == 1:
        nord_word_ordinal = "unste"
    elif i == 2:
        nord_word_ordinal = "zweite"
    elif i == 3:
        nord_word_ordinal = "dreite"
    elif i == 100:
        nord_word_ordinal = "100-te"  # Clamped to your flat pass-through number rule
    else:
        nord_word_ordinal = f"{nord_base}ste"

    # Map digital variations: "9th", "100th"
    ordinal_vocabulary[f"{i}{eng_dig_suffix}"] = nord_dig_ordinal
    
    # Map written word variations: "ninth", "hundredth", "twenty-fourth"
    ordinal_vocabulary[eng_word_ord] = nord_word_ordinal
    
    # Extra safety: Also map variations prefixed with "one-" if applicable
    if i == 100:
        ordinal_vocabulary["one-hundredth"] = "100-te"

# Merge safely into the repository without removing previous keys
existing_dict.update(ordinal_vocabulary)

with open(dict_path, "w", encoding="utf-8") as f:
    json.dump(existing_dict, f, indent=4, ensure_ascii=False)

print(f"🚂 SUCCESS! Both digital and written word ordinals fully injected.")
print(f"Destination Asset: {dict_path}")
print(f"Sample Check: '9th' -> '{existing_dict['9th']}'")
print(f"Sample Check: 'ninth' -> '{existing_dict['ninth']}'")
print(f"Sample Check: '24th' -> '{existing_dict['24th']}'")
print(f"Sample Check: 'twenty-fourth' -> '{existing_dict['twenty-fourth']}'")
print(f"Sample Check: '100th' -> '{existing_dict['100th']}'")
print(f"Sample Check: 'hundredth' -> '{existing_dict['hundredth']}'")

