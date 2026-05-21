import json
import os
from nordale import lexicon

def batch_translate_list(input_words_path: str, output_json_path: str):
    # Load words
    if input_words_path.endswith('.json'):
        with open(input_words_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            english_words = list(data.keys()) if isinstance(data, dict) else data
    else:
        with open(input_words_path, 'r', encoding='utf-8') as f:
            english_words = [line.strip() for line in f if line.strip()]

    total_words = len(english_words)
    bulk_results = {}
    stats = {"dictionary": 0, "stemmed": 0, "mangled": 0, "compound": 0, "empty": 0, "ethnonym": 0}

    def is_protected(word):
        high_status = {"governor", "king", "queen", "lord", "lady", "emperor", "president"}
        return word in lexicon.ETHNONYM_ROOTS or word in high_status

    for i, word in enumerate(english_words, 1):
        clean_word = word.lower().strip()
        res = lexicon.suggest_nordalian(clean_word)
        trans = res.translation        # ✅ attribute
        source = res.source

        # Sanity filter
        if trans.startswith("De ") and not is_protected(clean_word):
            trans = trans[3:].strip()
            if not trans.lower().endswith(('er', 'or', 'ist', 'ian', 'e')):
                trans += "er"

        if trans:
            bulk_results[clean_word] = trans
            if source in stats:
                stats[source] += 1

        if i % 50000 == 0 or i == total_words:
            print(f"Progress: {i:,} / {total_words:,} words processed...")

    print("\nProcessing complete.")
    print("Stats:")
    for key, count in stats.items():
        print(f"  {key}: {count}")
    print(f"\nTotal translated: {len(bulk_results)} / {total_words}")

    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(bulk_results, f, ensure_ascii=False, indent=4)
    print(f"Output saved to {output_json_path}")

if __name__ == "__main__":
    INPUT_FILE = "C:/Users/Ali/Documents/Github Work/your_giant_word_list.txt"
    OUTPUT_FILE = "C:/Users/Ali/Documents/Github Work/nordalian_compiled_lexicon.json"
    batch_translate_list(INPUT_FILE, OUTPUT_FILE)