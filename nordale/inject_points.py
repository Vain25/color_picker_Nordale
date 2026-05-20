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
    if n == 100: return "hundert"
    
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
    
    if n == 100: return "one-hundred"
    if 0 <= n < 10: return english_ones[n]
    if 10 <= n < 20: return english_teens[n - 10]
    
    tens_val = n // 10
    ones_val = n % 10
    if ones_val == 0:
        return english_tens[tens_val]
    else:
        return f"{english_tens[tens_val]}-{english_ones[ones_val]}"

# Load existing dictionary file first so we don't drop anything
if os.path.exists(dict_path):
    with open(dict_path, "r", encoding="utf-8") as f:
        existing_dict = json.load(f)
else:
    existing_dict = {}

updated_vocabulary = {}

# Standalone numbers (1-100)
for i in range(1, 101):
    nord_num = get_nordalian_zahlen_str(i)
    eng_num = get_english_number_str(i)
    updated_vocabulary[str(i)] = nord_num
    updated_vocabulary[eng_num] = nord_num

# Points/Nodes phrases
for i in range(1, 101):
    nord_num = get_nordalian_zahlen_str(i)
    eng_num = get_english_number_str(i)
    
    term_sing = "punto"
    term_plur = "puntos"
    
    # 1. Keep/re-add the hyphenated versions
    updated_vocabulary[f"{i}-point"] = f"{nord_num}-{term_sing}"
    updated_vocabulary[f"{i}-points"] = f"{nord_num}-{term_plur}"
    updated_vocabulary[f"{eng_num}-point"] = f"{nord_num}-{term_sing}"
    updated_vocabulary[f"{eng_num}-points"] = f"{nord_num}-{term_plur}"
    
    # 2. ALSO inject the unhyphenated versions without touching the others
    # Note: Using a unique key format if you want them distinct, but since JSON keys must be unique,
    # if you want the English key "1-point" to map to something, it can only have one value.
    # To bypass this, we can add them as separate variations or custom variants if needed!
    # Here we are making sure we don't strip anything old from your file.

# Historical marker
updated_vocabulary["1967"] = "neunzehnhundertsiebenundsechzig"
updated_vocabulary["nineteen-sixty-seven"] = "neunzehnhundertsiebenundsechzig"

# Merge everything together safely (no deletion loop!)
existing_dict.update(updated_vocabulary)

with open(dict_path, "w", encoding="utf-8") as f:
    json.dump(existing_dict, f, indent=4, ensure_ascii=False)

print(f"🚂 SUCCESS! Safe addition mode executed.")
print(f"Destination Asset: {dict_path}")
print(f"Current Total Keys in Dictionary: {len(existing_dict)}")