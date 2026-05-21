import json
import os
import re
import time
import random
import streamlit as st
from google.genai import types

class NordaleEngine:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.json_path = os.path.join(self.base_dir, "nordale", "dictionary.json")
        self.load_dictionary()

    def load_dictionary(self):
        with open(self.json_path, "r", encoding="utf-8") as f:
            self.dictionary = json.load(f)
        self.NORDALIAN_DICTIONARY = self.dictionary
        self.sorted_keywords = sorted(self.dictionary.keys(), key=len, reverse=True)

    def save_new_words(self, new_words: dict):
        updated = False
        for eng_word, nord_word in new_words.items():
            clean_eng = eng_word.lower().strip()
            clean_nord = nord_word.lower().strip()
            if not clean_eng or not clean_nord or clean_eng in self.dictionary:
                continue
            self.dictionary[clean_eng] = clean_nord
            updated = True
        if updated:
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(self.dictionary, f, indent=4, ensure_ascii=False)
            self.sorted_keywords = sorted(self.dictionary.keys(), key=len, reverse=True)

    def local_translate(self, text: str) -> str:
        if not text: return ""
        # Match words including optional hyphens to keep compound items together
        word_pattern = re.compile(r'\b[a-zA-Z]+(?:-[a-zA-Z]+)*\b')
        
        def replace_word(match):
            word = match.group(0)
            lower_word = word.lower()
            
            # Use lexicon helper if importing lexicon, or check local dictionary
            if lower_word in self.dictionary:
                translated = self.dictionary[lower_word]
            elif '-' in lower_word:
                # Fallback splitting inside the engine itself
                parts = lower_word.split('-')
                translated_parts = []
                for p in parts:
                    translated_parts.append(self.dictionary.get(p, p)) # Use dict translation if exists
                translated = '-'.join(translated_parts)
            else:
                return word
                
            if lower_word == "i": return "Me" if match.start() == 0 else "me"
            if word.isupper(): return translated.upper() if len(translated) <= 3 else translated.capitalize()
            elif word[0].isupper(): return translated.capitalize()
            return translated
            
        return word_pattern.sub(replace_word, text)
    
    def enforce_morphology(self, word: str, translation: str) -> str:
        """
        Final check: Strips illegal 'De-' prefixes and forces 
        proper Germanic/Romance suffixes for agent/professional nouns.
        """
        # 1. Strip 'De-' unless it's a high-status title (Add your specific titles here)
        high_status = ["governor", "king", "queen", "lord", "lady", "emperor"]
        
        if translation.lower().startswith("de ") and word.lower() not in high_status:
            # Remove 'De'
            translation = translation[3:].strip()
            
            # 2. If it's an agent/professional noun and lacks a suffix, force one
            # Professional/Agent words often end in 'or', 'er', 'ist', 'ian'
            valid_suffixes = ('er', 'or', 'ist', 'ian', 'e', 'ling')
            if not translation.lower().endswith(valid_suffixes):
                # Pick a suffix that fits the "pidgin" feel
                translation = translation + "er"
                
        return translation.capitalize() if translation[0].isupper() else translation


# CONSOLIDATED RULES
NORDALIAN_BASE_RULES = """
ROLE: You are the structural translation engine for Nordalian, a hybrid island pidgin. 
Structure: Rigid English layout with mandatory adjective reversal.

ETHNO-LINGUISTIC LORE & SYSTEMIC WEIGHTING:
- Germans (Industrialists): Heavy machinery lean towards Germanic roots.
- Dutch (Merchants): Mercantile districts; resentment towards native Spanish.
- Norwegians (Mountain Builders): Rail dominance, aggressive pride, mocking of Swedish bankruptcy.
- Natives (French/Spaniards): Agrarian substrate.

RULES:
1. DICTIONARY PRIORITY: Use mapped JSON definitions first.
2. MERCANTILE BIAS: Negative mercantile terms use Dutch/Low German roots; use harsh Spanish (e.g., 'barato') for broken/cheap items.
3. RAIL DOMINANCE: Failure/machinery terms use aggressive Norwegian (e.g., 'nedtid', 'konkurs').
4. ADJECTIVE REVERSAL: Adjectives MUST follow the noun they modify.
5. ETHNONYM & AGENT RULE: DO NOT repeat 'De-' prefix. Use diverse markers: Germanic suffixes ('-er', '-ling', '-ist') or Romance markers ('-or', '-ian', '-e'). Only use 'De' sparingly for high-status titles.
6. ENGLISH BASE: Maintain English sentence structure and base verbs.

CRITICAL STYLE:
- AGGRESSIVE PHONETIC CORRUPTION: Simplify roots (e.g., 'zimmer' -> 'zimma').
- NO TEXTBOOK COPY-PASTING: Nordalian is a broken pidgin, not a standard language.

6. STRICT ETHNONYM & AGENT RULE:
   - 'De-' prefix is EXCLUSIVELY for:
     a) High-status government/aristocratic titles (e.g., 'De Governor').
     b) Ethnicities and Nationalities (e.g., 'De Pro-serbian').
   - ALL OTHER agent/professional nouns (e.g., 'prosecutor', 'proselytizer', 'proser') MUST use suffixes ONLY (e.g., '-er', '-ist', '-or').
   - NEVER use 'De-' for these professional roles. If you use 'De-' for a non-aristocratic or non-ethnic word, you have failed the task.
"""

def get_combined_system_prompt(dictionary: dict) -> str:
    dict_str = "\nNORDALIAN_DICTIONARY SPECIFICATION:\n"
    for k, v in dictionary.items():
        dict_str += f'"{k}": "{v}"\n'
    return NORDALIAN_BASE_RULES + dict_str

def ai_translate(text: str, client, engine: NordaleEngine) -> tuple:
    if not text.strip(): return "", {}
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    translated_paragraphs, all_new_words = [], {}
    total_paragraphs = len(paragraphs)

    st.markdown("### 🚂 Processing Lore Document")
    progress_bar = st.progress(0.0)
    status_text = st.empty()

    for idx, paragraph in enumerate(paragraphs):
        current_progress = (idx + 1) / total_paragraphs
        progress_bar.progress(current_progress)
        status_text.text(f"Processing Paragraph {idx+1}/{total_paragraphs}...")
        
        try:
            mood = random.choice(["Industrial-Heavy", "Merchant-Dialect", "Seafarer-Slang", "Mountain-Builder-Speak"])
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"MOOD: {mood}\n\nTEXT: {paragraph}",
                config=types.GenerateContentConfig(
                    system_instruction=get_combined_system_prompt(engine.NORDALIAN_DICTIONARY),
                    temperature=0.1, 
                    response_mime_type="application/json"
                )
            )
            data = json.loads(response.text.strip())
            raw_translation = data.get("translation", "")
            
            # --- GUARDRAIL INTEGRATION ---
            # Now enforcing morphology on every successful AI translation
            clean_translation = engine.enforce_morphology(paragraph, raw_translation)
            translated_paragraphs.append(clean_translation)
            # -----------------------------
            
            new_words = data.get("new_vocabulary", {})
            if isinstance(new_words, dict) and new_words:
                all_new_words.update(new_words)
                engine.save_new_words(new_words)
            
            time.sleep(4.0)
        except Exception as e:
            # Fallback remains pure local translation if AI fails
            print(f"Error on paragraph {idx+1}: {e}")
            translated_paragraphs.append(engine.local_translate(paragraph))
            
    status_text.text("✅ Lore compilation complete!")
    return "\n\n".join(translated_paragraphs), all_new_words