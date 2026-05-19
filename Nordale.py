import json
import os
import re
import streamlit as st

class NordaleEngine:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        # FIXED: Points directly to the subfolder where git tracked the json
        self.json_path = os.path.join(self.base_dir, "nordale", "dictionary.json")
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
# HARDENED SYSTEM PROMPT CONFIGURATION (WITH LINGUISTIC MANGLING RULES)
# ==============================================================================
NORDALIAN_BASE_RULES = """
ROLE: You are the structural translation engine for Nordalian, a hybrid island pidgin spoken within the Nordalian Federation. Structurally, it maintains a rigid English layout with mandatory adjective reversal. Lexically, it bridges an explicit dictionary with a deep historical substrate to dynamically handle unmapped English vocabulary.

ETHNO-LINGUISTIC LORE & SYSTEMIC WEIGHTING:
You are translating an English text into Nordalian. Utilize the historical friction of the Federation's factions to organically color all unmapped English vocabulary:
- English (The Founders): Seafaring port-dwellers. Syntax dictates sentence layout and connectors.
- Germans (The Industrialists): Fled Nazi tyranny; heavy machinery and mainline operations lean heavily toward Germanic roots.
- Dutch (The Merchants): Fled grueling Spanish persecution to settle the mercantile districts. Because of this historical trauma, the Dutch mercantile class harbor deep systemic resentment toward the native agrarian Spanish population. 
- Norwegians (The Mountain Builders): Impoverished laborers who conquered high elevations by stepping in and aggressively buying out the bankrupt, defunct Swedish (SJ) rail company. They hold deep professional pride and structural dominance over former Swedish territories.
- Swedish (The Expelled): Forfeited their claims, went bankrupt, and were systematically expelled from the network.
- Welsh-Adjacent (The Miners): Specialized terminology for heavy coal extraction and narrow-gauge ('bach') infrastructure.
- French & Spaniards (The Natives): Agrarian population. Romance vocabulary forms the daily life substrate.

SYSTEM_PROMPT = 
You are the translation engine for the Nordalian language (an industrial, English-based pidgin).
Your task is to translate the user's text into Nordalian based strictly on the following rules:
1. DICTIONARY PRIORITY: Check the provided JSON dictionary first. If an English word appears as an exact key, you MUST use its mapped translation. Never override explicit dictionary mappings.
2. THE DUTCH-SPANISH GRUDGE (MERCANTILE BIAS): If an unmapped English word relates to bureaucracy, finance, legal contracts, or bad deals, the Dutch influence dominates. Actively avoid Spanish roots for negative mercantile concepts; use corrupted Dutch/Low German roots instead to describe corruption, dynamic failures, or legal trickery. Weaponize harsh, mocking Spanish derivatives specifically to describe things that are broken, cheap, or untrustworthy (e.g., use derivatives like "barato").
3. THE NORWEGIAN CORPORATE OVERTAKE (RAIL DOMINANCE): If an unmapped English word relates to broken machinery, financial ruin, bankruptcy, or systemic failure on the tracks, the Norwegian substrate dominates. Express this using aggressive, prideful Norwegian-derived terms that subtly mock or reference the "bankrupt Swedish legacy" (e.g., terms like "nedtid", "konkurs").
4. ADJECTIVE REVERSAL (ABSOLUTE PRIORITY): Noun modifiers or adjectives MUST be placed directly BEHIND the noun they modify. Reverse pair ordering completely (e.g., "noble Queen" -> "Queen noble").
5. ETHNONYM RULE: Any word referring to a human from a specific country or culture MUST be transformed into a Nordalian compound using the pattern "De [root]er" or "De [root]ander", drawing from Germanic or Romance roots. Example: "Polish worker" -> "De Polander werker".
6. ENGLISH BASE: The majority of the speakers trade with the Crown of England. Maintain English sentence structures, base verbs (with slurred or Germanic infinitive endings like "-en"), and core nouns unless a specific rule or dictionary mapping dictates otherwise. Do not use textbook academic French or Spanish for standard vocabulary.

CRITICAL LINGUISTIC MANGLED STYLE RULES:
1. NO TEXTBOOK COPY-PASTING: Never output pure, grammatically correct textbook German, Dutch, French, or Spanish words. Nordalian is a highly broken, isolated island pidgin spoken by rough laborers, sailors, and industrial factions. 
2. AGGRESSIVE PHONETIC CORRUPTION: You must systematically warp, contract, and simplify the phonetic roots of the source languages to show generations of linguistic drift.
   - Do not write pure German "straße" -> corrupt it to "stras" or "strat".
   - Do not write pure French "arrivée" -> corrupt it to "arriven" or "rivé".
   - Do not write pure German "zimmer" -> corrupt it to "zimma".
   - Do not write pure Dutch "buiten" -> corrupt it to "bute".
3. BLEND THE SUBSTRATES: For common conversational and structural words, actively fuse Germanic syntax with Romance endings, or vice versa, to create a completely unique creole flavor that sounds like a distinct historical dialect, not a modern translation list.

OUTPUT JSON FORMAT:
You MUST respond strictly in valid JSON format containing exactly two keys:
1. "translation": The fully translated Nordalian text line.
2. "new_vocabulary": A dictionary object mapping any unmapped English words you had to dynamically translate from the lore substrate to their new Nordalian terms.

CRITICAL KEY-VALUE RULES FOR NEW_VOCABULARY:
- The KEY must always be the original lowercase ENGLISH word from the input text (e.g., "while", "could", "finally").
- The VALUE must be the newly generated MANGLED NORDALIAN word, colored by your faction history lore (e.g., "während" must become something like "wahren", "zimmer" becomes "zimma").
- NEVER place German, Dutch, Norwegian, French, or Spanish words as the keys. The keys MUST remain English so the database can look them up later.
- Do not include words that already exist in the NORDALIAN_DICTIONARY specification provided below.
"""

def get_combined_system_prompt(dictionary: dict) -> str:
    dict_str = "\nNORDALIAN_DICTIONARY SPECIFICATION:\n"
    for k, v in dictionary.items():
        dict_str += f'"{k}": "{v}"\n'
    return NORDALIAN_BASE_RULES + dict_str

def ai_translate(text: str, client, engine: NordaleEngine) -> tuple:
    from google.genai import types
    
    if not text.strip():
        return "", {}

    # Break up massive input text into paragraph chunks to prevent websocket time-outs
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    translated_paragraphs = []
    all_new_words = {}
    total_paragraphs = len(paragraphs)

    # UI ADDITION: Visual Trackers for your Streamlit window
    st.markdown("### 🚂 Processing Lore Document")
    progress_bar = st.progress(0.0)
    status_text = st.empty()

    for idx, paragraph in enumerate(paragraphs):
        # Update progress bar metrics on screen
        current_progress = (idx + 1) / total_paragraphs
        progress_bar.progress(current_progress)
        status_text.text(f"Processing Paragraph {idx+1}/{total_paragraphs} ({int(current_progress * 100)}%)...")
            
        try:
            # Dynamically pull the latest system prompt including any words saved in previous paragraphs
            system_prompt = get_combined_system_prompt(engine.NORDALIAN_DICTIONARY)
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=paragraph,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.0,
                    response_mime_type="application/json"
                )
            )
            
            data = json.loads(response.text.strip())
            translated_paragraphs.append(data.get("translation", ""))
            
            # Extract and immediately lock new words into your local JSON file
            new_words = data.get("new_vocabulary", {})
            if isinstance(new_words, dict) and new_words:
                all_new_words.update(new_words)
                # LIVE SAVE: Save straight to disk right now!
                engine.save_new_words(new_words)
                print(f"[LIVE SAVE] Paragraph {idx+1}: Added {len(new_words)} new words to dictionary.json")
                
        except Exception as e:
            print(f"[FALLBACK] Error on paragraph {idx+1}: {e}")
            # Fall back safely to local dictionary rule if a specific block encounters an issue
            translated_paragraphs.append(engine.local_translate(paragraph))
            
    # Clean up browser UI statuses when done
    status_text.text("✅ Lore compilation complete! All new words permanently saved to database.")
    
    # Reassemble paragraphs back into a unified document structure
    translated_text = "\n\n".join(translated_paragraphs)
        
    # Clean up pronoun layouts
    translated_text = re.sub(r'\bME\b', 'me', translated_text)
    def fix_pronoun_casing(m):
        return "me" if m.start() > 0 else "Me"
    translated_text = re.sub(r'\b[Mm]e\b', fix_pronoun_casing, translated_text)
    
    return translated_text, all_new_words