import json
import os
from nordale import lexicon

def save_to_json(word, translation):
    json_path = "nordale/dictionary.json"
    data = {}
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    
    data[word] = translation
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Successfully saved '{word}' to dictionary.json!")

print("--- Nordalian Translator Initialized ---")

while True:
    user_input = input("\nEnter English word: ").strip()
    if user_input.lower() in ['exit', 'quit']: 
        break
    if not user_input:
        continue
    
    # 1. Get the translation (result is created here)
    result = lexicon.suggest_nordalian(user_input)
    print(f"Translation: {result['translation']} (Source: {result['source']})")
    
    # 2. Check source ONLY if result exists
    if result['source'] != 'dictionary':
        save = input("This is a new word. Save to dictionary.json? (y/n): ")
        if save.lower() == 'y':
            save_to_json(user_input, result['translation'])
            # Reload the lexicon so it's recognized immediately next time
            lexicon.NORDALIAN_LEXICON = lexicon.load_lexicon()