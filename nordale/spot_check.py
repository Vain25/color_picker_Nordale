import random
import json
from nordale import lexicon

def perform_spot_check(input_path: str, sample_size: int = 1000):
    # 1. Load the list
    with open(input_path, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]

    # 2. Get random sample
    sample = random.sample(words, sample_size)
    
    print(f"--- Spot checking {sample_size} random words ---")
    
    results = []
    for word in sample:
        clean = word.lower().strip()
        res = lexicon.suggest_nordalian(clean)
        trans = res['translation']
        
        # Apply the exact same logic we used in your pipeline
        if trans.startswith("De ") and clean not in lexicon.ETHNONYM_ROOTS:
            trans = trans.replace("De ", "").strip()
            if not trans.endswith(('er', 'or', 'ist', 'ian', 'e')):
                trans += "er"
        
        results.append((clean, trans))

    # 3. Print a few to the console for quick visual verification
    for clean, trans in results[:20]:
        print(f"{clean:<20} -> {trans}")
        
    # 4. Save the full 1k sample to a file for deeper inspection
    with open("spot_check_results.json", 'w', encoding='utf-8') as f:
        json.dump(dict(results), f, indent=4)
        
    print(f"\nFull 1,000 word sample saved to 'spot_check_results.json'.")

if __name__ == "__main__":
    INPUT = "C:/Users/Ali/Documents/Github Work/giantwordlist.txt"
    perform_spot_check(INPUT)