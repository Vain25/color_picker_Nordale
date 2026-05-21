import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
dict_path = os.path.join(script_dir, "dictionary.json")
new_path = os.path.join(script_dir, "new_words.json")

with open(dict_path, 'r', encoding='utf-8') as f:
    master = json.load(f)

with open(new_path, 'r', encoding='utf-8') as f:
    additions = json.load(f)

# Add new words (existing keys are NOT overwritten – your originals stay safe)
for key, value in additions.items():
    if key not in master:
        master[key] = value

with open(dict_path, 'w', encoding='utf-8') as f:
    json.dump(master, f, ensure_ascii=False, indent=4)

print(f"Merged {len(additions)} new words. Dictionary now has {len(master)} entries.")