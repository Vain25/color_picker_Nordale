import json
import os
import re

class NordaleEngine:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.json_path = os.path.join(self.base_dir, "dictionary.json")
        self.load_dictionary()

    def load_dictionary(self):
        with open(self.json_path, "r", encoding="utf-8") as f:
            self.dictionary = json.load(f)
        self.NORDALIAN_DICTIONARY = self.dictionary
        self.sorted_keywords = sorted(self.dictionary.keys(), key=len, reverse=True)

    def save_new_words(self, new_words: dict):
        """Silently merges all new words straight into dictionary.json"""
        updated = False
        for eng_word, nord_word in new_words.items():
            clean_eng = eng_word.lower().strip()
            clean_nord = nord_word.lower().strip()
            
            # Skip only if empty or if it's already an existing definition
            if not clean_eng or not clean_nord or clean_eng in self.dictionary:
                continue
                
            self.dictionary[clean_eng] = clean_nord
            updated = True
            
        if updated:
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(self.dictionary, f, indent=4, ensure_ascii=False)
            self.sorted_keywords = sorted(self.dictionary.keys(), key=len, reverse=True)

    def local_translate(self, text: str) -> str:
        if not text:
            return ""
        word_pattern = re.compile(r'\b[a-zA-Z]+\b')
        
        def replace_word(match):
            word = match.group(0)
            lower_word = word.lower()
            if lower_word in self.dictionary:
                translated = self.dictionary[lower_word]
                if lower_word == "i":
                    return "Me" if match.start() == 0 else "me"
                if word.isupper():
                    return translated.upper() if len(translated) <= 3 else translated.capitalize()
                elif word[0].isupper():
                    return translated.capitalize()
                return translated
            return word

        return word_pattern.sub(replace_word, text)

# ==============================================================================
# SYSTEM PROMPT CONFIGURATION
# ==============================================================================
NORDALIAN_BASE_RULES = """
ROLE: You are the structural translation engine for Nordalian, a hybrid island pidgin spoken within the Nordalian Federation. Structurally, it maintains a rigid English layout with mandatory adjective reversal. Lexically, it bridges an explicit dictionary with a deep historical substrate to dynamically handle unmapped vocabulary.

ETHNO-LINGUISTIC LORE & SYSTEMIC WEIGHTING:
Utilize the historical friction of the Federation's factions to organically color all unmapped vocabulary:
- English (The Founders): Seafaring port-dwellers. Syntax dictates sentence layout and connectors.
- Germans (The Industrialists): Fled Nazi tyranny; heavy machinery and mainline operations lean heavily toward Germanic roots.
- Dutch (The Merchants): Fled grueling Spanish persecution to settle the mercantile districts. Because of this historical trauma, the Dutch mercantile class harbor deep systemic resentment toward the native agrarian Spanish population. 
- Norwegians (The Mountain Builders): Impoverished laborers who conquered high elevations by stepping in and aggressively buying out the bankrupt, defunct Swedish (SJ) rail company. They hold deep professional pride and structural dominance over former Swedish territories.
- Swedish (The Expelled): Forfeited their claims, went bankrupt, and were systematically expelled from the network.
- Welsh-Adjacent (The Miners): Specialized terminology for heavy coal extraction and narrow-gauge ('bach') infrastructure.
- French & Spaniards (The Natives): Agrarian population. Romance vocabulary forms the daily life substrate.

RULES of ENGAGEMENT (WITH INTER-FACTION FRICTION):
1. DICTIONARY PRIORITY: If an English word appears as an exact key in NORDALIAN_DICTIONARY, use it. Never override explicit dictionary mappings.
2. THE DUTCH-SPANISH GRUDGE (MERCANTILE BIAS): If an unmapped English word relates to bureaucracy, finance, legal contracts, or bad deals, the Dutch influence dominates. Because they hate the Spanish, the AI must actively avoid Spanish roots for negative mercantile concepts, instead using corrupted Dutch/Low German roots to describe corruption, dynamic failures, or legal trickery, while weaponizing harsh, mocking Spanish derivatives specifically to describe things that are broken, cheap, or untrustworthy.
3. THE NORWEGIAN CORPORATE OVERTAKE (RAIL DOMINANCE): If an unmapped word relates to broken machinery, financial ruin, bankruptcy, or systemic failure on the tracks, the Norwegian substrate dominates. It must express this using aggressive, prideful Norwegian-derived terms that subtly mock or reference the "bankrupt Swedish legacy".
4. ADJECTIVE REVERSAL (ABSOLUTE PRIORITY): Noun modifiers or adjectives MUST be placed directly BEHIND the noun it modifies. Reverse pair ordering completely.
5. ETHNONYM RULE: Any word referring to a human from a specific country or culture MUST be transformed into a Nordalian compound using the pattern "De [root]er" or "De [root]ander", drawing from Germanic or Romance roots. Examples: "Polish worker" -> "De Polander werker".

OUTPUT JSON FORMAT:
You MUST respond strictly in valid JSON format containing exactly two keys:
1. "translation": The fully translated Nordalian text line.
2. "new_vocabulary": A dictionary object mapping any unmapped English words you had to dynamically translate from the lore substrate to their new Nordalian terms. Only include brand new base words you created, omitting common punctuation and structural parts.
"""

def get_combined_system_prompt(dictionary: dict) -> str:
    dict_str = "\nNORDALIAN_DICTIONARY SPECIFICATION:\n"
    for k, v in dictionary.items():
        dict_str += f'"{k}": "{v}"\n'
    return NORDALIAN_BASE_RULES + dict_str

def ai_translate(text: str, client, engine: NordaleEngine) -> tuple:
    from google.genai import types
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=text,
        config=types.GenerateContentConfig(
            system_instruction=get_combined_system_prompt(engine.NORDALIAN_DICTIONARY),
            temperature=0.0,
            response_mime_type="application/json"
        )
    )
    
    try:
        data = json.loads(response.text.strip())
        translated_text = data.get("translation", "")
        new_words = data.get("new_vocabulary", {})
    except Exception:
        return engine.local_translate(text), {}
        
    translated_text = re.sub(r'\bME\b', 'me', translated_text)
    def fix_pronoun_casing(m):
        return "me" if m.start() > 0 else "Me"
    translated_text = re.sub(r'\b[Mm]e\b', fix_pronoun_casing, translated_text)
    
    return translated_text, new_words

