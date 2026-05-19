import json
import os

# 1. Paste the brand new words from the AI inside this dictionary block
NEW_AI_WORDS = {
    "limestone": "kalkstein",
    "quicklime": "kalk snel",
    "lime kiln": "kalkofen",
    "horse-drawn": "chevalgezogen",
    "goods yard": "yard marchandises"
}

def merge_to_library():
    json_path = os.path.join("nordale", "dictionary.json")
    
    # Check if the dictionary file exists yet
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            try:
                current_dictionary = json.load(f)
            except json.JSONDecodeError:
                print("Error: dictionary.json is corrupted or empty. Starting fresh.")
                current_dictionary = {}
    else:
        current_dictionary = {}

    # 2. Merge the new words into the main library
    added_count = 0
    updated_count = 0
    
    for key, value in NEW_AI_WORDS.items():
        # Lowercase the key to keep matching consistent
        clean_key = key.lower().strip()
        
        if clean_key in current_dictionary:
            if current_dictionary[clean_key] != value:
                current_dictionary[clean_key] = value
                updated_count += 1
        else:
            current_dictionary[clean_key] = value
            added_count += 1

    # 3. Ensure the directory exists and write back the unified JSON data
    os.makedirs("nordale", exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(current_dictionary, f, indent=4, ensure_ascii=False)

    print(f"--- Feedback Loop Complete ---")
    print(f"Added {added_count} brand new terms.")
    print(f"Updated {updated_count} existing definitions.")
    print(f"Total words in your library now: {len(current_dictionary)}")

if __name__ == "__main__":
    merge_to_library()
    
    