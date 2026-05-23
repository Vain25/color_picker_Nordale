import json
import os
from nordale import lexicon

# Load the dictionary once at startup
DICT_PATH = os.path.join(os.path.dirname(__file__), "dictionary.json")
with open(DICT_PATH, "r", encoding="utf-8") as f:
    dictionary = json.load(f)

def save_to_json(word, translation):
    """Save a single word to dictionary.json and update the running dictionary."""
    json_path = os.path.join(os.path.dirname(__file__), "dictionary.json")
    data = {}
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    
    data[word] = translation
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    dictionary[word] = translation   # keep in-memory dict up to date
    print(f"Successfully saved '{word}' → '{translation}' to dictionary.json!")

print("--- Nordalian Translator Initialized ---")
print(f"Loaded {len(dictionary)} entries from dictionary.json")

while True:
    user_input = input("\nEnter English word: ").strip()
    if user_input.lower() in ['exit', 'quit']:
        break
    if not user_input:
        continue

    # 1. Get the translation (result is an object, use attributes)
    result = lexicon.suggest_nordalian(user_input, dictionary, True)
    print(f"Translation: {result.translation} (Source: {result.source})")
    print(f"Explanation: {result.explanation}")

    # 2. If the word was not found in the dictionary, offer to save it
    if result.source != 'dictionary':
        save = input("This word was generated (not in dictionary). Save to dictionary.json? (y/n): ").lower().strip()
        if save == 'y':
            save_to_json(user_input, result.translation)