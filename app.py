import streamlit as st
import os
import re
from google import genai
from google.genai import types

# ==============================================================================
# NORDALIAN DICTIONARY (Comprehensive Core Specification)
# ==============================================================================
NORDALIAN_DICTIONARY = {
    # Core Server & Rail Terms
    "train": "tren", "trains": "trens", "locomotive": "loko", "locomotives": "lokos",
    "loco": "loko", "locos": "lokos", "track": "via", "tracks": "vias", "line": "line",
    "lines": "lines", "curve": "curva", "bend": "curva", "straight": "recta",
    "crossover": "zigzag via", "crossovers": "zigzag vias", "siding": "loop fini",
    "accident": "unglück", "crash": "unglück", "blocked": "blockiert", "stuck": "blockiert",
    "late": "laat", "delayed": "laat", "schedule": "schema", "timetable": "schema",
    "go": "go", "light": "licht", "green": "go", "red": "stop", "danger": "achtung", 
    "warning": "achtung", "wagon": "wagon", "wagons": "wagons", "brake": "sakte",
    "brakes": "saktes", "couple": "hook", "coupling": "hooking", "couples": "hooks",
    "decouple": "unhook", "decoupling": "unhooking", "decouples": "unhooks",
    "uncouple": "unhook", "uncoupling": "unhooking", "uncouples": "unhooks",
    "switch": "wissel", "point": "wissel", "station": "bahnhof", "stations": "bahnhofs",
    "terminus": "endbahnhof", "yard": "yard", "yards": "yards", "shunting": "shunting", 
    "company": "kompani", "companies": "kompanis", "subsidiary": "sub-kompani",
    "subsidiaries": "sub-kompanis", "industry": "industri", "industries": "industris",
    "money": "geld", "capital": "kapital", "owner": "eier", "owners": "eiers",
    "boss": "chef", "claim": "kleim", "claims": "kleims", "signal": "sein", 
    "signals": "seins", "signalman": "seinman", "signalbox": "seinbox",
    "points": "wissels", "bridge": "bru", "bridges": "brus", "tunnel": "tunnel", 
    "tunnels": "tunnels", "coal": "oer", "freight": "vracht", "cargo": "vracht", 
    "passenger": "passagier", "passengers": "passagiers", "hello": "hallo", 
    "hey": "hej", "goodbye": "tschüss", "thank you": "dank je", "thanks": "dank je",
    "please": "alstublieft", "sorry": "sorry", "yeah": "ja", "nope": "nee",
    "maybe": "misschien", "okay": "oke", "sure": "zeker", "welcome": "welkom",
    "congrats": "bravo", "congratulations": "bravo", "diesel": "fuel", 
    "electric": "elektrik", "steam": "steam", "narrow gauge": "bach",
    "engine": "engine", "clear": "klar", "clearance": "klarens", "blok": "blok",
    "derail": "debahn", "derailed": "debahnt", "weight": "gewicht", 
    "tonnage": "gewicht", "slope": "smolfjell", "grade": "smolfjell",
    "incline": "smolfjell", "decline": "smolfjell fini", "iron": "fer", 
    "steel": "stahl", "oil": "fuel", "gold": "geld", "stone": "stein",
    "smelly": "stinky", "stink": "stinky", "stinky": "stinky", "smell": "stinky", 
    "stinks": "stinky", "stank": "stinky", "stunk": "stinky", "man": "manfolk",
    "woman": "womanfolk", "person": "folk", "people": "folk", "human": "folk",
    "kid": "kleinfolk", "child": "kleinfolk", "children": "kleinfolk",
    "evil": "nicht gut", "very": "zeer", "language": "taal", "languages": "taals",
    "talking": "taalen", "talk": "taal", "pidgin": "taal", "speak": "spreken",
    "speaking": "spreken", "poop": "schitt", "hurt": "owwie", "hurting": "owwie",
    "pain": "owwie", "paining": "owwie", "painful": "owwie", "problem": "probleme",
    "problems": "problemes", "fix": "fixen", "fixing": "fixen", "fixed": "fixen",
    "break": "breaken", "end": "fini", "land": "grond", "ground": "grond",
    "earth": "grond", "mud": "modder", "rock": "stein", "water": "watter",
    "slip": "slide", "slide": "slide",
    
    # Nations & Cultures
    "america": "De Amerika", "european": "De European", "uk": "El Colonizador",
    "germany": "De Vaterland", "norway": "De Fjelland", "sweden": "De Skandiland",
    "finland": "De Snøland", "wales": "De Cymru", "netherlands": "De Vlakland",
    "nordal": "De Nordale", "nordale": "De Nordale", "canada": "De Mapleland",
    "france": "La France", "spain": "La España", "spanish": "De Españarder",
    "germanic": "De Germanic", "german": "De Vaterlander", "british": "Britannian",
    "american": "De Fleer", "americans": "De Fleers", "germans": "De Vaterlands", 
    "norwegian": "De Fjellander", "norwegians": "De Fjellanders",
    "swedish": "De Skandander", "swedes": "De Skandanders", "finnish": "De Snølander",
    "finns": "De Snølanders", "welshmen": "De Cymrander", "welsh": "De Cymranders",
    "dutch": "De Vlaklander", "dutchmen": "De Vlaklanders", "nordalian": "De Nordaler",
    "nordalians": "De Nordalers", "canadian": "De Maplelander", "canadians": "De Maplelanders",
    "french": "Français", "frenchmen": "Françaises", "spainard": "De Españarder",
    "spainards": "De Españarders", "english": "De Anglander", "englishmen": "De Anglanders",
    "australia": "De Kangaroosandaalland", "australian": "De Kangaroosandaallander",
    "australians": "De Kangaroosandaallanders", "aussies": "De Kangaroosandaallanders",
    "basque": "De Basquander", "basques": "De Basquanders", "italian": "De Pastaland",
    "italians": "De Pastalanders", "xenophobic": "nicht nize", "xenophobia": "nicht nize",
    "racist": "nicht nize folk", "racism": "nicht nize", "act": "do", "action": "do",
    "illegal": "nicht nize", "crime": "nicht nize",

    # Roles & Professions
    "engineer": "ingeniér", "conductor": "konduktor", "manager": "manajer",
    "worker": "werker", "employee": "angestellter", "customer": "klient", 
    "client": "klient", "partner": "partner", "friend": "copine", 
    "friends": "copines", "friendship": "copinage", "laborer": "arbeiter", 
    "laborers": "arbeiters", 
    
    # Core Commodities & Mechanics
    "nickel": "Nickel", "lumber": "bois", "timber": "bois", "wood": "bois",
    "imperial": "imperiale", "colonial": "coloniale", "railway": "bahn",
    "rail": "bahn", "port": "harbour", "ship": "boot", "nazi": "Teufelsarbeiter",

    # Directional & Spatial
    "north": "nord", "south": "süd", "west": "west", "east": "ost",
    "northern": "nord", "southern": "süd", "western": "west", "eastern": "ost",
    "global": "global", "world": "welt", "universal": "universal",
    
    # Time & Weather Vibe
    "dawn": "aube", "morning": "matin", "day": "tag", "noon": "midi", 
    "afternoon": "après-midi", "evening": "soir", "night": "nuit",
    "week": "woche", "time": "zeit", "hour": "heure", "good": "gut",
    "bad": "nicht gut", "happy": "gut", "sad": "nicht gut", "rain": "glaw",
    "sun": "sonne", "cloud": "wolke", "mond": "mond",
    
    # General Lexicon
    "slur": "nicht nize woord", "slurs": "nicht nize woords", "car": "brum",
    "cars": "brums", "truck": "brum brum", "trucks": "brum brums", "bus": "autobus",
    "buses": "autobuses", "word": "woord", "words": "woords", "nice": "nize",
    "beer": "bier", "beers": "biers", "drunk": "drunk", "drunkard": "alcoholiker",
    "drunkards": "alcoholikers", "alcohol": "alkohol", "alcoholic": "alcoholique",
    "coffee": "cafe", "shop": "winkel", "ready": "klar",
    
    # Politics & Systems
    "federal": "federal", "federation": "federation", "union": "unie",
    "republic": "republik", "federalismus": "federalismus", "tariff": "taxe", 
    "revolution": "revolu", "revolutions": "revolus", "uprising": "revolu",
    "uprisings": "revolus", "coup": "coup", "coups": "coups", "dictator": "dictator", 
    "dictators": "dictators", "democracy": "demokratie", "democratic": "demokratisch",
    "communism": "kommunismus", "communists": "kommunisten", "socialism": "socialismus",
    "socialists": "socialisten", "capitalism": "kapitalismus", "capitalists": "capitalisten",
    "anarchy": "anarchie", "anarchists": "anarchisten", "monarchy": "monarchie",
    "monarchen": "monarchen", "oligarchy": "oligarchie", "oligarchs": "oligarchen",
    "democrats": "demokraten", "treaty": "accord", "treaties": "accords",
    "agreement": "accord", "contract": "accord", "contracts": "accords",
    "conference": "konferenz", "border": "frontière", "frontier": "frontière",
    "war": "guerre", "law": "regel", "rule": "regel", "tax": "taxe",
    "taxes": "taxen", "many": "bouku", "a lot": "bouku", "some": "poko",
    "few": "poko", "why": "porkwa", "how": "komo", "because": "because",
    "nothing": "nada", "zero": "nada", "always": "siempre", "never": "jamays",    
    
    # Pronouns & Verbs
    "i": "me", "me": "me", "you": "yu", "your": "yu", "we": "vi", "they": "dey",
    "he": "he", "him": "he", "she": "she", "her": "she", "them": "dey",
    "is": "ist", "are": "ist", "am": "ist", "isn't": "ist nicht", "isnt": "ist nicht",
    "have": "hav", "hav": "hav", "want": "want", "need": "need", "join": "join",
    "buy": "bai", "purchase": "bai", "sell": "sel", "run": "run", "running": "running",
    "try": "try", "trying": "trying", "attempt": "try", "operate": "run",
    "make": "maken", "build": "bild", "work": "work", "pay": "pei", "earn": "ern",
    "deliver": "deliver", "ask": "ask", "slow": "sakte", "stop": "stopp", 
    "drive": "rijden", "look": "kyk", "see": "kyk", "watch": "kyk", "wait": "wacht", 
    "listen": "luister", "say": "zeg", "call": "zeg", "saying": "zegging",
    "said": "gezegd", "think": "denken", "know": "weten", "understand": "begrijpen", 
    "learn": "leren", "teach": "leren", "help": "helpen", "love": "amore",
    
    # Prepositions & Connectors
    "the": "de", "a": "un", "an": "un", "to": "pa", "for": "pa", "in": "in",
    "on": "on", "at": "at", "and": "and", "but": "but", "before": "before",
    "next": "next", "of": "of", "with": "vif", "from": "from", "this": "dis",
    "that": "dat", "not": "nicht", "do": "do", "don't": "do nicht", "dont": "do nicht",
    "out": "uit", "up": "opp", "down": "ned", "through": "trw", "over": "over", 
    "under": "onder", "between": "tussen", "around": "rond", "near": "nær", 
    "where": "waar", "who": "wie", "later": "later", "now": "nu", "hit": "klap",

    # Descriptive words
    "big": "big", "huge": "zeerbig", "giant": "zeerbig", "massive": "zeerbig",
    "large": "big", "little": "klein", "small": "klein", "tiny": "zeerklein",
    "old": "old", "young": "jong", "new": "neu", "free": "frei", "all": "al",
    "more": "mor", "island": "ailand", "city": "siti", "narrow": "bach",
    "valley": "cwm", "hill": "bryn", "mountain": "fjell", "snow": "snø",
    "flat": "vlak", "steep": "steil", "long": "long", "short": "kort",
    "fast": "snel", "zigzag": "quiggle", "sharp": "sharp", "heavy": "gewicht",
}

# ==============================================================================
# LORE AND RULE-BASED TRANSLATION SYSTEM CONFIGURATION
# ==============================================================================
NORDALIAN_BASE_RULES = """
ROLE: You are the structural translation engine for Nordalian, a hybrid island pidgin spoken within the Nordalian Federation. Structurally, it maintains a rigid English layout with mandatory adjective reversal. Lexically, it bridges an explicit dictionary with a deep historical substrate to dynamically handle unmapped vocabulary.

ETHNO-LINGUISTIC LORE & SYSTEMIC WEIGHTING:
Utilize the historical background of the Federation's factions to organically color all unmapped vocabulary:
- English (The Founders): Seafaring port-dwellers who settled the capital and shipping hubs. Their syntax dictates the underlying sentence layout and basic connectors.
- Germans (The Industrialists): Fled Nazi tyranny but retained imperial heritage. They built the heavy manufacturing hubs; technical machinery, steelworks, and mainline operations lean heavily toward Germanic roots.
- Dutch (The Merchants): Fled Spanish persecution to settle shopping districts near the ports. Masters of canals, land reclamation, and complex hydraulic switch-systems.
- Norwegians (The Mountain Builders): Migrated from an impoverished Norway to build lines through grueling high elevations after taking over the railway from the broke, defunct Swedish (SJ) system owners.
- Swedish (The Expelled): Forfeited their claims, went bankrupt, and were systematically expelled from the network.
- Welsh-Adjacent (The Miners): Brought specialized terminology for heavy coal extraction and narrow-gauge ('bach') valley infrastructure.
- French & Spaniards (The Natives): The original agrarian population of the island. Their romance vocabulary forms the deep, living substrate for daily life, the land, weather, time, and agrarian pursuits.

RULES OF ENGAGEMENT:
1. DICTIONARY PRIORITY: If an English word appears as an exact key in the NORDALIAN_DICTIONARY, you MUST use the provided translation value. Never override explicit dictionary mappings.
2. SUBSTRATE FALLBACK (THE LORE RULE): If an English word is NOT in the provided dictionary, do NOT leave it in English. Instead, adapt it dynamically into a pidginized variant drawing from the historical factions—heavily favoring a French or Spanish Romance substrate for general/agrarian terms, Germanic for heavy industrial terms, or Dutch for mercantile/waterway terms.
3. ADJECTIVE REVERSAL (ABSOLUTE PRIORITY): Regardless of word origin (explicit dictionary or dynamic substrate fallback), every single noun modifier or adjective MUST be placed directly BEHIND the noun it modifies. Reverse the pair ordering completely.
   - "old locomotive" -> "loko old"
   - "heavy steel wagon" -> "wagon stahl gewicht"
   - "narrow valley" -> "cwm bach"
   - "main line" -> "line main"
4. PRONOUNS & VERBAL GROUNDING: Always follow the literal dictionary entries for structural pieces. Ensure that verbs like "am", "are", and "is" consistently resolve to "ist" to keep the pidgin structurally unified (e.g., "I am driving" -> "me ist driving").

OUTPUT FORMAT: Return only the final Nordalian text line. No introductions, explanations, or commentary.
"""

# ==============================================================================
# ENGINE CORE PIPELINES
# ==============================================================================
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

    return word_pattern.sub(replace_word, text)

def ai_translate(text: str, client) -> str:
    dict_str = "\nNORDALIAN_DICTIONARY SPECIFICATION:\n" + "\n".join([f'"{k}": "{v}"' for k, v in NORDALIAN_DICTIONARY.items()])
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=text,
        config=types.GenerateContentConfig(
            system_instruction=NORDALIAN_BASE_RULES + dict_str,
            temperature=0.0
        )
    )
    translated_text = response.text.strip()
    
    # Handle explicit post-processing pronoun adjustments safely
    translated_text = re.sub(r'\bME\b', 'me', translated_text)
    translated_text = re.sub(r'\b[Mm]e\b', lambda m: "me" if m.start() > 0 else "Me", translated_text)
    return translated_text

# ==============================================================================
# STREAMLIT FRONTEND WEB UI
# ==============================================================================
st.set_page_config(page_title="Nordalian Translator", page_icon="🚂", layout="centered")

# Visual Headers
st.title("🚂 Nordalian Language Translator")
st.write("Convert standard English into Nordalian rail pidgin seamlessly.")

# --- API KEY MANAGEMENT SIDEBAR ---
st.sidebar.header("🔑 Engine Settings")

system_key = os.environ.get("GEMINI_API_KEY")
user_key = None
active_key = None
client = None

if system_key:
    st.sidebar.success("🟢 Using Developer System Key")
    active_key = system_key
else:
    st.sidebar.write("To use advanced AI grammar features, provide a Gemini API Key. Otherwise, the app uses the local dictionary fallback.")
    user_key = st.sidebar.text_input("Enter Gemini API Key:", type="password", help="Grab a free key from Google AI Studio")
    
    if user_key:
        st.sidebar.success("🟢 Custom User Key Active")
        active_key = user_key
    else:
        st.sidebar.warning("🟡 Local Dictionary Fallback Active")
        active_key = None

# Boot standard client context if matching keys are located
if active_key:
    try:
        from google import genai
        client = genai.Client(api_key=active_key)
        st.sidebar.info("AI Engine ready to process structures.")
    except Exception as e:
        st.sidebar.error(f"SDK Initialization Error: {e}")
        client = None

# Sidebar Demographics Overview Info Container
st.sidebar.divider()
st.sidebar.header("🗺️ Federation Demographics")
st.sidebar.markdown("""
**🔧 Faction Sectors:**
* **English:** Capitals & Ports Layout Framework
* **Germans:** Mainline Heavy Steel & Machining
* **Dutch:** Canal Switch & Hydrological Networks
* **Norwegians:** Mountain Pass Infrastructure
* **Welsh-Adjacent:** Narrow-Gauge Valley Coal Mining
* **Romance Native:** Agrarian Valleys, Weather, & Time
""")

st.divider()

# Create User Input UI interface elements
user_input = st.text_area("Enter English Text:", placeholder="Type your sentence here... (e.g., The green train did not stop at the big station.)")

# Execution trigger
if st.button("Translate to Nordalian", type="primary"):
    if user_input.strip():
        with st.spinner("Processing language structures..."):
            if client:
                try:
                    result = ai_translate(user_input, client)
                    engine_status = "Gemini AI Engine (Substrate Dynamic Integration)"
                except Exception as api_err:
                    result = local_translate(user_input)
                    engine_status = f"Local Fallback Loop (AI Error: {api_err})"
            else:
                result = local_translate(user_input)
                engine_status = "Local Dictionary Structural Fallback Engine"
                
            # Display outputs in clean programmatic blocks
            st.subheader("Nordalian Output:")
            st.info(result)
            st.caption(f"Processed via: {engine_status}")
    else:
        st.error("Please enter some text first!")