import json
import os
from nordale import lexicon
from nordale.lexicon import get_bias

def run_pipeline(input_path: str, staging_path: str, nord_dict: dict, enable_hyphen_fix: bool):
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        return

    print("Loading English word list...")
    if input_path.endswith('.json'):
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            words = list(data.keys()) if isinstance(data, dict) else data
    else:
        with open(input_path, 'r', encoding='utf-8') as f:
            words = [line.strip() for line in f if line.strip()]

    staging_data = {
        "auto_approved": {},
        "review_queue": {
            "dutch_lore": {},
            "norwegian_lore": {},
            "spanish_mock": {},
            "blends": {}
        }
    }

    total_words = len(words)
    print(f"Loaded {total_words:,} words. Starting processing with Sanity Filter...")

    for i, word in enumerate(words, 1):
        clean = word.lower().strip()
        if not clean:
            continue

        res = lexicon.suggest_nordalian(clean, nord_dict, enable_hyphen_fix)
        trans = res.translation
        source = res.source

        if not trans:
            continue

        # Sanity filter
        if trans.startswith("De ") and clean not in lexicon.ETHNONYM_ROOTS:
            trans = trans[3:].strip()
            if not trans.lower().endswith(('er', 'or', 'ist', 'ian', 'e')):
                trans += "er"

        if len(trans) < 4 and len(clean) > 4:
            trans = clean[:6]

        if source in ('dictionary', 'stemmed', 'ethnonym', 'compound'):
            staging_data["auto_approved"][clean] = trans
        elif source == 'mangled':
            bias = get_bias(clean)
            if bias == 'dutch':
                staging_data["review_queue"]["dutch_lore"][clean] = trans
            elif bias == 'norwegian':
                staging_data["review_queue"]["norwegian_lore"][clean] = trans
            elif bias == 'spanish_mock':
                staging_data["review_queue"]["spanish_mock"][clean] = trans
            else:
                staging_data["review_queue"]["blends"][clean] = trans

        if i % 50000 == 0 or i == total_words:
            print(f"Progress: {i:,} / {total_words:,} words processed...")

    print(f"Saving structured staging file to {staging_path}...")
    with open(staging_path, 'w', encoding='utf-8') as f:
        json.dump(staging_data, f, ensure_ascii=False, indent=4)

    print("Pipeline complete! Your staging JSON is clean and sorted. 🚀")


if __name__ == "__main__":
    INPUT = "C:/Users/Ali/Documents/Github Work/giantwordlist.txt"
    STAGING_FILE = "C:/Users/Ali/Documents/Github Work/nordalian_staging.json"

    # Load dictionary once
    DICT_PATH = os.path.join(os.path.dirname(__file__), 'dictionary.json')
    with open(DICT_PATH, 'r', encoding='utf-8') as f:
        NORD_DICT = json.load(f)

    ENABLE_HYPHEN_FIX = True
    run_pipeline(INPUT, STAGING_FILE, NORD_DICT, ENABLE_HYPHEN_FIX)