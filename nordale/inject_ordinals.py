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

def get_english_ordinal_suffix(n):
    if 11 <= n % 100 <= 13:
        return "th"
    else:
        return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")

# Load existing dictionary file first so we protect all current data
if os.path.exists(dict_path):
    with open(dict_path, "r", encoding="utf-8") as f:
        existing_dict = json.load(f)
else:
    existing_dict = {}

ordinal_vocabulary = {}

# Generate Ordinals from 1st to 100th
for i in range(1, 101):
    nord_base = get_nordalian_zahlen_str(i)
    eng_suffix = get_english_ordinal_suffix(i)
    
    # Nordalian Ordinal Suffix Rules
    if i == 1:
        nord_ordinal = "un-st"
    elif i == 2:
        nord_ordinal = "zwei-nd"
    elif i == 3:
        nord_ordinal = "drei-rd"
    elif i == 100:
        nord_ordinal = "100-te"
    else:
        nord_ordinal = f"{nord_base}-te"
        
    # Map raw numeric forms: "1st", "2nd", "10th", "24th", "100th"
    ordinal_vocabulary[f"{i}{eng_suffix}"] = nord_ordinal

# Merge safely into the repository without removing previous keys
existing_dict.update(ordinal_vocabulary)

with open(dict_path, "w", encoding="utf-8") as f:
    json.dump(existing_dict, f, indent=4, ensure_ascii=False)

print(f"🚂 SUCCESS! Ordinal number formatting rules injected.")
print(f"Destination Asset: {dict_path}")
print(f"Sample Check: '1st' -> '{existing_dict['1st']}'")
print(f"Sample Check: '2nd' -> '{existing_dict['2nd']}'")
print(f"Sample Check: '9th' -> '{existing_dict['9th']}'")
print(f"Sample Check: '10th' -> '{existing_dict['10th']}'")
print(f"Sample Check: '24th' -> '{existing_dict['24th']}'")
print(f"Sample Check: '100th' -> '{existing_dict['100th']}'")