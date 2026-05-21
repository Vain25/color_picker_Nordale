import json
import os

def commit_translations(staging_path: str, master_dict_path: str):
    if not os.path.exists(staging_path):
        print(f"Error: Staging file not found at {staging_path}")
        return
        
    with open(staging_path, 'r', encoding='utf-8') as f:
        stage = json.load(f)
        
    # Read existing master dictionary, or start empty if missing
    master = {}
    if os.path.exists(master_dict_path):
        with open(master_dict_path, 'r', encoding='utf-8') as f:
            master = json.load(f)

    # Merge everything you looked over
    master.update(stage["auto_approved"])
    master.update(stage["review_queue"]["dutch_lore"])
    master.update(stage["review_queue"]["norwegian_lore"])
    master.update(stage["review_queue"]["spanish_mock"])
    master.update(stage["review_queue"]["blends"])

    # Write the results straight back into your real dictionary.json
    with open(master_dict_path, 'w', encoding='utf-8') as f:
        json.dump(master, f, ensure_ascii=False, indent=4)
        
    print(f"All decisions successfully committed to master dictionary at: {master_dict_path}!")

if __name__ == "__main__":
    # Define your actual file paths here
    STAGING = "C:/Users/Ali/Documents/Github Work/nordalian_staging.json"
    MASTER_DICT = "C:/Users/Ali/Documents/Github Work/nordale/dictionary.json"
    
    commit_translations(STAGING, MASTER_DICT)
    
    