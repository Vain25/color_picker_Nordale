import os
import re

# ==============================================================================
# NORDALIAN DICTIONARY (For Local Fallback & AI Grounding)
# ==============================================================================
NORDALIAN_DICTIONARY = {
    # Core Server & Rail Terms
    "train": "tren",  
    "trains": "trens",            
    "locomotive": "loko",     
    "locomotives": "lokos",
    "loco": "loko",
    "locos": "lokos",
    "track": "via",     
    "tracks": "vias",
    "line": "line",      
    "lines": "lines",
    "curve": "curva",
    "bend": "curva",
    "straight": "recta",
    "crossover":"zigzag via",
    "crossovers":"zigzag vias",
    "siding":"loop fini",
    "accident": "unglück",
    "crash": "unglück",
    "blocked": "blockiert",
    "stuck": "blockiert",
    "late": "laat",
    "delayed": "laat",
    "schedule": "schema",
    "timetable": "schema",
    "go": "go",
    "light": "licht",
    "green":"go",
    "red":"stop",
    "danger": "achtung",   
    "warning":"achtung",
    "wagon": "wagon",
    "wagons": "wagons",
    "brake": "sakte",
    "brakes": "saktes",
    "couple":"hook",
    "coupling":"hooking",
    "couples":"hooks",
    "decouple":"unhook",
    "decoupling":"unhooking",
    "decouples":"unhooks",
    "uncouple":"unhook",
    "uncoupling":"unhooking",
    "uncouples":"unhooks",
    "switch": "wissel",
    "point": "wissel",
    "station": "bahnhof",        
    "stations": "bahnhofs",
    "terminus": "endbahnhof",
    "yard": "yard",  
    "yards": "yards",            
    "shunting": "shunting",        
    "company": "kompani",        
    "companies": "kompanis",
    "subsidiary": "sub-kompani",
    "subsidiaries": "sub-kompanis",
    "industry": "industri",
    "industries": "industris",
    "money": "geld",             
    "capital": "kapital",
    "owner": "eier",
    "owners": "eiers",
    "boss": "chef",
    "claim": "kleim",            
    "claims": "kleims",            
    "signal": "sein",            
    "signals": "seins",          
    "signalman": "seinman",      
    "signalbox": "seinbox",        
    "points": "wissels",          
    "bridge": "bru",             
    "bridges": "brus",           
    "tunnel": "tunnel",          
    "tunnels": "tunnels",        
    "coal": "oer",               
    "freight": "vracht",         
    "cargo": "vracht",           
    "passenger": "passagier",     
    "passengers": "passagiers",   
    "hello": "hallo",             
    "hey": "hej",                
    "goodbye": "tschüss",         
    "thank you": "dank je",
    "thanks": "dank je",
    "please": "alstublieft",
    "sorry": "sorry",
    "yeah": "ja",
    "nope": "nee",
    "maybe": "misschien",
    "okay": "oke",
    "sure": "zeker",
    "welcome": "welkom",
    "congrats":"bravo",
    "congratulations": "bravo",
    "diesel": "fuel",            
    "electric": "elektrik",      
    "steam": "steam",           
    "narrow gauge": "bach",
    "engine": "engine",             
    "clear" : "klar",              
    "clearance": "klarens",         
    "blok": "blok",
    "derail" : "debahn",            
    "derailed": "debahnt",          
    "weight": "gewicht",            
    "tonnage": "gewicht",          
    "slope": "smolfjell",
    "grade": "smolfjell",
    "incline": "smolfjell",
    "decline": "smolfjell fini",
    "iron": "fer",            
    "steel": "stahl",         
    "oil": "fuel",
    "gold":"geld",
    "stone":"stein",
    "smelly": "stinky",          
    "stink": "stinky",           
    "stinky": "stinky",          
    "smell": "stinky",           
    "stinks": "stinky",          
    "stank": "stinky",           
    "stunk": "stinky",          
    "man":"manfolk",
    "woman":"womanfolk",
    "person":"folk",
    "people":"folk",
    "human":"folk",
    "kid":"kleinfolk", 
    "child":"kleinfolk",
    "children":"kleinfolk",
    "evil":"nicht gut",
    "very": "zeer",
    "language": "taal",
    "languages": "taals",
    "talking": "taalen",
    "talk": "taal",
    "pidgin":"taal",
    "speak":"spreken",
    "speaking":"spreken",
    "poop": "schitt",
    "hurt": "owwie",
    "hurting": "owwie",
    "pain": "owwie",
    "paining": "owwie",
    "painful" : "owwie",
    "problem": "probleme",
    "problems": "problemes",
    "fix": "fixen",
    "fixing": "fixen",
    "fixed": "fixen",
    "break": "breaken",
    "end": "fini",
    "land": "grond",
    "ground": "grond",
    "earth": "grond",
    "mud": "modder",
    "rock": "stein",
    "water": "watter",
    "slip": "slide",
    "slide": "slide",
    
    # Nations & Cultures
    "america": "De Amerika",
    "european": "De European",
    "uk": "El Colonizador",
    "germany": "De Vaterland",
    "norway": "De Fjelland",
    "sweden": "De Skandiland",
    "finland": "De Snøland",
    "wales": "De Cymru",
    "netherlands": "De Vlakland",
    "nordal": "De Nordale",      
    "nordale": "De Nordale",
    "canada": "De Mapleland",
    "france": "La France",
    "spain": "La España",
    "spanish": "De Españarder",
    "germanic": "De Germanic",
    "german": "De Vaterlander",
    "british": "Britannian",
    "american": "De Fleer",      
    "americans": "De Fleers",    
    "germans": "De Vaterlands",   
    "norwegian": "De Fjellander",
    "norwegians": "De Fjellanders",
    "swedish": "De Skandander",
    "swedes": "De Skandanders",
    "finnish": "De Snølander",
    "finns": "De Snølanders",
    "welshmen": "De Cymrander",
    "welsh": "De Cymranders",
    "dutch": "De Vlaklander",
    "dutchmen": "De Vlaklanders",
    "nordalian": "De Nordaler",
    "nordalians": "De Nordalers",
    "canadian": "De Maplelander",
    "canadians": "De Maplelanders",
    "french": "Français",
    "frenchmen": "Françaises",
    "spainard": "De Españarder",
    "spainards": "De Españarders",
    "english": "De Anglander",
    "englishmen": "De Anglanders",
    "australia": "De Kangaroosandaalland",
    "australian": "De Kangaroosandaallander",
    "australians": "De Kangaroosandaallanders",
    "aussies": "De Kangaroosandaallanders",
    "basque": "De Basquander",
    "basques": "De Basquanders",
    "italian": "De Pastaland",
    "italians": "De Pastalanders",
    "xenophobic": "nicht nize",
    "xenophobia": "nicht nize",
    "racist": "nicht nize folk",
    "racism": "nicht nize",
    "act": "do",
    "action": "do",
    "illegal": "nicht nize",
    "crime": "nicht nize",

    # Roles & Professions
    "engineer": "ingeniér",
    "conductor": "konduktor",
    "manager": "manajer",
    "worker": "werker",
    "employee": "angestellter",
    "customer": "klient", 
    "client": "klient",  
    "partner": "partner",        
    "friend": "copine", 
    "friends": "copines",
    "friendship": "copinage",
    "laborer": "arbeiter",      
    "laborers": "arbeiters",     
    
    # Core Commodities & Mechanics
    "nickel": "Nickel",
    "lumber": "bois",            
    "timber": "bois",
    "wood": "bois",
    "imperial": "imperiale",
    "colonial": "coloniale",
    "railway": "bahn",
    "rail": "bahn",
    "port": "harbour",           
    "ship": "boot",
    "nazi": "Teufelsarbeiter",

    # Directional & Spatial
    "north": "nord",
    "south": "süd",
    "west": "west",
    "east": "ost",
    "northern": "nord",
    "southern": "süd",
    "western": "west",
    "eastern": "ost",
    "global": "global",
    "world": "welt",
    "universal": "universal",
    
    # Time & Weather Vibe
    "dawn": "aube",
    "morning": "matin",
    "day": "tag",
    "noon": "midi",           
    "afternoon": "après-midi",
    "evening": "soir",           
    "night": "nuit",
    "week": "woche",
    "time": "zeit",
    "hour": "heure",
    "good": "gut",
    "bad": "nicht gut",
    "happy": "gut",
    "sad": "nicht gut",
    "rain": "glaw",
    "sun": "sonne",
    "cloud": "wolke",
    "moon": "mond",
    
    # General Lexicon
    "slur": "nicht nize woord",  
    "slurs": "nicht nize woords",  
    "car": "brum",
    "cars": "brums",
    "truck": "brum brum",        
    "trucks": "brum brums",      
    "bus": "autobus",
    "buses": "autobuses",
    "word": "woord",
    "words": "woords",
    "nice": "nize",
    "beer": "bier",
    "beers": "biers",
    "drunk": "drunk",
    "drunkard": "alcoholiker",
    "drunkards": "alcoholikers",
    "alcohol": "alkohol",
    "alcoholic": "alcoholique",
    "coffee": "cafe",
    "shop": "winkel",
    "ready":"klar",
    
    # Politics & Systems
    "federal": "federal",        
    "federation": "federation",  
    "union": "unie",
    "republic": "republik",
    "federalism": "federalismus",
    "tarrif": "taxe",   
    "revolution": "revolu",
    "revolutions":"revolus",
    "uprising":"revolu",
    "uprisings":"revolus",
    "coup": "coup",
    "coups": "coups",
    "dictator": "dictator",  
    "dictators": "dictators",
    "democracy": "demokratie",
    "democratic": "demokratisch",
    "communism": "kommunismus",
    "communists": "kommunisten",
    "socialism": "socialismus",
    "socialists": "socialisten",
    "capitalism": "kapitalismus",
    "capitalists": "capitalisten",
    "anarchy": "anarchie",
    "anarchists": "anarchisten",
    "monarchy": "monarchie",
    "monarchs": "monarchen",
    "oligarchy": "oligarchie",
    "oligarchs": "oligarchen",
    "democrats": "demokraten",
    "treaty": "accord",
    "treaties": "accords",
    "agreement": "accord",
    "contract": "accord",
    "contracts": "accords",
    "conference": "konferenz",
    "border":"frontière",
    "frontier":"frontière",
    "war": "guerre",
    "law": "regel",
    "rule": "regel",
    "tax": "taxe",
    "taxes": "taxen",
    "many": "bouku",
    "a lot":"bouku",
    "some": "poko",
    "few": "poko",
    "why": "porkwa",
    "how":"komo",
    "because":"because",
    "nothing":"nada",
    "zero": "nada",
    "always": "siempre",
    "never": "jamays",    
    
    # Pronouns & Verbs
    "i": "me",                   
    "me": "me",
    "you": "yu",
    "your": "yu",
    "we": "vi",
    "they": "dey",
    "he": "he",
    "him":"he",
    "she": "she",
    "her": "she",
    "them": "dey",
    "is": "ist",                 
    "are": "ist",
    "am": "ist",
    "isn't": "ist nicht",
    "isnt": "ist nicht",
    "have": "hav",
    "hav": "hav",
    "want": "want",
    "need": "need",
    "join": "join",
    "buy": "bai",
    "purchase": "bai",
    "sell": "sel",
    "run": "run",
    "running": "running",
    "try": "try",
    "trying": "trying",
    "attempt": "try",
    "operate": "run",
    "make": "maken",
    "build": "bild",
    "work": "work",
    "pay": "pei",
    "earn": "ern",
    "deliver": "deliver",
    "ask": "ask",
    "slow": "sakte",             
    "stop": "stopp",             
    "drive": "rijden",           
    "look": "kyk",               
    "see": "kyk",                
    "watch": "kyk",              
    "wait": "wacht",             
    "listen": "luister",         
    "speak": "spreken",          
    "say": "zeg",                
    "call":"zeg",
    "saying": "zegging",
    "said": "gezegd",
    "think": "denken",            
    "know": "weten",             
    "understand": "begrijpen",    
    "learn": "leren",             
    "teach": "leren",             
    "help": "helpen",            
    "love": "amore",
    
    # Prepositions & Connectors
    "the": "de",
    "a": "un",                   
    "an": "un",
    "to": "pa",                   
    "for": "pa",
    "in": "in",
    "on": "on",
    "at": "at",
    "and": "and",
    "but": "but",
    "before": "before",
    "next": "next",
    "of": "of",
    "with": "vif",
    "from": "from",
    "this": "dis",
    "that": "dat",
    "not": "nicht",
    "do":"do",
    "don't": "do nicht",
    "dont": "do nicht",
    "no": "no",
    "yes": "ja",          
    "out": "uit",                
    "up": "opp",                 
    "down": "ned",               
    "through": "trw",                  
    "over": "over",              
    "under": "onder",            
    "between": "tussen",         
    "around": "rond",            
    "near": "nær",               
    "where": "waar",              
    "who": "wie",                
    "later": "later",              
    "now": "nu",                
    "hit": "klap",

    # Descriptive words
    "big": "big",
    "huge": "zeerbig",
    "giant": "zeerbig",
    "massive": "zeerbig",
    "large": "big",
    "little": "klein",
    "small": "klein",
    "tiny" : "zeerklein",
    "old": "old",
    "young": "jong",    
    "new": "neu",                
    "free": "frei",
    "all": "al",
    "more": "mor",
    "island": "ailand",          
    "city": "siti",
    "narrow": "bach",            
    "valley": "cwm",             
    "hill": "bryn",              
    "mountain": "fjell",         
    "snow": "snø",               
    "flat": "vlak",              
    "steep": "steil",             
    "long": "long",
    "short": "kort",
    "fast": "snel",
    "zigzag": "quiggle",
    "sharp": "sharp",
    "heavy": "gewicht",
}

# ==============================================================================
# SYSTEM PROMPT CONFIGURATION
# ==============================================================================
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

RULES OF ENGAGEMENT (WITH INTER-FACTION FRICTION):

1. DICTIONARY PRIORITY: If an English word appears as an exact key in NORDALIAN_DICTIONARY, use it. Never override explicit dictionary mappings.

2. THE DUTCH-SPANISH GRUDGE (MERCANTILE BIAS): If an unmapped English word relates to bureaucracy, finance, legal contracts, or bad deals, the Dutch influence dominates. Because they hate the Spanish, the AI must actively avoid Spanish roots for negative mercantile concepts, instead using corrupted Dutch/Low German roots to describe corruption, dynamic failures, or legal trickery, while weaponizing harsh, mocking Spanish derivatives specifically to describe things that are broken, cheap, or untrustworthy.

3. THE NORWEGIAN CORPORATE OVERTAKE (RAIL DOMINANCE): If an unmapped word relates to broken machinery, financial ruin, bankruptcy, or systemic failure on the tracks, the Norwegian substrate dominates. It must express this using aggressive, prideful Norwegian-derived terms that subtly mock or reference the "bankrupt Swedish legacy" (e.g., dynamically inventing terms that imply structural weakness or financial incompetence when referencing old lines).

4. ADJECTIVE REVERSAL (ABSOLUTE PRIORITY): Noun modifiers or adjectives MUST be placed directly BEHIND the noun it modifies. Reverse pair ordering completely.

5. ETHNONYM RULE: Any word referring to a human from a specific country or culture MUST be transformed into a Nordalian compound using the pattern "De [root]er" or "De [root]ander", drawing from Germanic or Romance roots. Never leave an ethnonym in English. Examples:
- "Polish worker" -> "De Polander werker"
- "Greek captain" -> "De Greker kapitän"
- "Japanese engineer" -> "De Nipponer ingeniér"
- "Russian merchant" -> "De Russlander koopman"

OUTPUT FORMAT: Return only the final Nordalian text line. No introductions, explanations, or commentary.
"""

# ==============================================================================
# ENGINES & PIPELINES
# ==============================================================================

# Helper to combine instructions with the live dictionary state
def get_combined_system_prompt() -> str:
    dict_str = "\nNORDALIAN_DICTIONARY SPECIFICATION:\n"
    for k, v in NORDALIAN_DICTIONARY.items():
        dict_str += f'"{k}": "{v}"\n'
    return NORDALIAN_BASE_RULES + dict_str

def local_translate(text: str) -> str:
    word_pattern = re.compile(r'\b[a-zA-Z]+\b')
    
    def replace_word(match):
        word = match.group(0)
        lower_word = word.lower()
        if lower_word in NORDALIAN_DICTIONARY:
            translated = NORDALIAN_DICTIONARY[lower_word]
            if lower_word == "i":
                return "Me" if match.start() == 0 else "me"
            if word.isupper():
                return translated.upper() if len(translated) <= 3 else translated.capitalize()
            elif word[0].isupper():
                return translated.capitalize()
            return translated
        return word

    translated_text = word_pattern.sub(replace_word, text)
    return translated_text

def ai_translate(text: str, client) -> str:
    from google.genai import types
    
    # Inject rules + the explicit map directly into the content generation sequence
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=text,
        config=types.GenerateContentConfig(
            system_instruction=get_combined_system_prompt(),
            temperature=0.1, # Complete deterministic execution to stomp out variation
        )
    )
    translated_text = response.text.strip()
    
    # Eradicate edge-case casing errors
    translated_text = re.sub(r'\bME\b', 'me', translated_text)
    def fix_pronoun_casing(m):
        return "me" if m.start() > 0 else "Me"
    translated_text = re.sub(r'\b[Mm]e\b', fix_pronoun_casing, translated_text)
    
    return translated_text

# ==============================================================================
# MAIN RUNTIME APPLICATION
# ==============================================================================
if __name__ == "__main__":
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if api_key:
        try:
            from google import genai
            client = genai.Client()
            print("Nordalian System: Connected to Gemini AI Translation Engine.")
            translate_func = lambda text: ai_translate(text, client)
        except Exception as e:
            print(f"Failed to boot AI Engine ({e}). Shifting to Local Fallback.")
            translate_func = local_translate
    else:
        print("Nordalian System: No API Key detected. Running on Local Dictionary Fallback.")
        translate_func = local_translate

    print("Type 'exit' to shut down.\n")
    while True:
        user_input = input("English > ")
        if user_input.lower() == 'exit': 
            print("Tschüss!")
            break
        if not user_input.strip():
            continue
        print(f"Pidgin  > {translate_func(user_input)}\n")