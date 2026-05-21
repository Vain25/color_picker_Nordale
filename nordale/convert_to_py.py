import json
import os

def generate_lexicon_py():
    base_path = r"C:\Users\Ali\Documents\Github Work\nordale"
    json_path = os.path.join(base_path, "dictionary.json")
    output_path = os.path.join(base_path, "lexicon.py")

    if not os.path.exists(json_path):
        print(f"❌ Error: Could not find dictionary.json at: {json_path}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"✅ Found {len(data)} entries in {json_path}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("from typing import Dict\n\n")
        f.write("NORDALIAN_LEXICON: Dict[str, str] = {\n")
        
        for eng, nord in data.items():
            eng_repr = repr(eng)
            nord_repr = repr(nord)
            f.write(f"    {eng_repr}: {nord_repr},\n")
        
        f.write("}\n")

    print(f"🚀 Success! {len(data)} entries injected into {output_path}")

if __name__ == "__main__":
    generate_lexicon_py()