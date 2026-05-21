import re
from dataclasses import dataclass
from typing import Dict, Set, Optional, List

# --- Types (replacing TS interfaces) ---
@dataclass
class TranslationResult:
    original: str
    translation: str
    source: str  # 'dictionary', 'stemmed', 'mangled', 'compound', 'empty', 'ethnonym'
    explanation: str


# --- Bias sets ---
NORDALIAN_BIASES = {
    'dutch': {'bank', 'money', 'tax', 'contract', 'contracts', 'legal', 'bureaucracy',
              'finance', 'bill', 'invoice', 'deal', 'credit', 'loan', 'corrupt', 'bribe'},
    'norwegian': {'machine', 'machinery', 'broken', 'derail', 'bankrupt', 'bankruptcy',
                  'crash', 'accident', 'ruin', 'tracks', 'track', 'failure', 'rust', 'sink'},
    'spanish_mock': {'cheap', 'broken', 'shoddy', 'fraud', 'dodgy', 'barato', 'broke'},
    'welsh': {'slate', 'mining', 'quarry', 'valley', 'hill', 'mountain', 'bard', 'song',
              'stream', 'church', 'sheep', 'dragon', 'coal', 'iron', 'rain', 'green'}
}

# --- Ethnonym roots ---
ETHNONYM_ROOTS = {
    'polish': 'Poland', 'german': 'Vaterland', 'spanish': 'España', 'french': 'France',
    'norwegian': 'Fjelland', 'swedish': 'Skandiland', 'dutch': 'Vlakland', 'british': 'Angland',
    'american': 'Fleer', 'canadian': 'Mapleland', 'australian': 'Kangaroosandaal'
}

# --- Prefix map ---
PREFIX_MAP = {
    # Negation, Opposition
    "un": "nicht",
    "dis": "dis",
    "mis": "mis",
    "non": "niet",
    "anti": "anti",
    "counter": "tegen",
    "contra": "contra",
    "de": "de",
    "in": "on",
    "im": "on",
    "il": "on",
    "ir": "on",
    "ob": "tegen",
    "op": "tegen",
    "retro": "back",
    "mal": "slecht",
    "bene": "gut",
    "pseudo": "vals",

    # Direction, Location
    "sub": "sub",
    "super": "super",
    "inter": "inter",
    "intra": "binnen",
    "trans": "trans",
    "under": "unter",
    "over": "über",    # overridden by bias logic
    "out": "uit",
    "down": "ned",
    "up": "opp",
    "circum": "rond",
    "peri": "rond",
    "en": "in",
    "em": "in",
    "mid": "mid",
    "fore": "vor",
    "ante": "vor",
    "pre": "pre",
    "post": "post",
    "ex": "ex",
    "tele": "fern",
    "infra": "onder",
    "ultra": "uiter",
    "extra": "buiten",
    "intro": "inward",
    "ad": "zu",
    "ab": "af",
    "apo": "af",
    "epi": "op",
    "para": "bij",
    "endo": "endo",
    "exo": "buiten",
    "ecto": "buiten",
    "dia": "durch",
    "per": "durch",

    # Quantity, Size
    "mono": "een",
    "di": "twee",
    "bi": "twee",
    "tri": "drei",
    "quad": "vier",
    "penta": "vijf",
    "hexa": "zes",
    "poly": "veel",
    "multi": "veel",
    "semi": "half",
    "hemi": "half",
    "demi": "half",
    "omni": "al",
    "pan": "al",
    "macro": "groot",
    "micro": "klein",
    "mega": "groot",
    "giga": "reus",
    "hyper": "uber",
    "hypo": "onder",

    # Other high-frequency prefixes
    "co": "ko",
    "com": "mit",
    "con": "mit",
    "col": "mit",
    "cor": "mit",
    "syn": "zamen",
    "sym": "zamen",
    "auto": "zelf",
    "bio": "leb",
    "geo": "aard",
    "hydro": "vater",
    "pyro": "brand",
    "chrono": "zeit",
    "thermo": "warm",

    "re": "wieder",
}
PREFIXES_SORTED = sorted(PREFIX_MAP.keys(), key=len, reverse=True)

# Suffix map
SUFFIX_MAP = {
    "s": "s",
    "es": "es",
    "ed": "t",
    "ing": "en",
    "ly": "li",
    "ily": "ili",
    "less": "los",
    "ful": "vol",
    "ous": "eus",
    "al": "al",
    "ial": "ial",
    "ical": "isch",
    "ic": "ik",
    "y": "ig",
    "ish": "isch",
    "like": "lijk",
    "proof": "fest",
    "old": "alt",
    "est": "st",
    "iest": "st",
    "ward": "wärts",
    "wise": "weise",
    "fold": "fach",
    "ness": "het",
    "ity": "ität",
    "ility": "ilität",
    "ability": "abilität",
    "ship": "schaft",
    "hood": "heid",
    "dom": "tum",
    "ism": "ismus",
    "tion": "sjon",
    "sion": "sjon",
    "ation": "asjon",
    "ition": "isjon",
    "ization": "isierung",
    "ment": "ment",
    "ance": "anz",
    "ence": "enz",
    "acy": "atie",
    "ure": "uur",
    "age": "age",
    "ery": "erei",
    "ary": "ar",
    "ory": "orium",
    "ize": "isieren",
    "ify": "ifizieren",
    "ate": "ieren",
    "en": "en",
    "ist": "ist",
    "er": "er",
    "or": "or",
    "ar": "ar",
    "ian": "ianer",
    "ive": "iv",
    "ent": "ent",
    "ant": "ant",
    "able": "abel",
    "ible": "ibel",
    "ology": "ologie",
    "logist": "loge",
    "logy": "logie",
    "phobia": "fobie",
    "cide": "zid",
    "graphy": "grafie",
    "graph": "graf",
    "gram": "gramm",
    "scope": "skop",
    "ectomy": "ektomie",
    "itis": "itis",
    "cracy": "kratie",
    "crat": "krat",
    "archy": "archie",
    "arch": "arch",
    "craft": "kraft",
    "mentally": "mentli",
    "sphere": "sfere"
}
SUFFIXES_SORTED = sorted(SUFFIX_MAP.keys(), key=len, reverse=True)


# --- Helper functions ---
def normalize_word(word: str) -> str:
    return re.sub(r"[^a-zA-Z'\-]", "", word).strip().lower()


def get_bias(word: str) -> str:
    clean = word.lower()
    if clean in NORDALIAN_BIASES['dutch']:
        return 'dutch'
    if clean in NORDALIAN_BIASES['norwegian']:
        return 'norwegian'
    if clean in NORDALIAN_BIASES['spanish_mock']:
        return 'spanish_mock'
    if clean in NORDALIAN_BIASES['welsh']:
        return 'welsh'
    return 'blend'


def ethnonym_translation(word: str) -> Optional[TranslationResult]:
    clean = word.lower()

    # Only handle direct ethnonym matches (e.g., 'norwegian' → 'De Fjellander')
    if clean in ETHNONYM_ROOTS:
        root = ETHNONYM_ROOTS[clean]
        suffix = 'ander' if root.endswith('land') else 'er'
        return TranslationResult(
            original=word,
            translation=f"De {root}{suffix}",
            source='ethnonym',
            explanation=f"Mapped direct ethnic nationality root '{root}' with suffix '{suffix}' plus aristocratic 'De' prefix."
        )

    # All other words go to the suffix engine
    return None


def mangle_word(word: str, bias: str) -> dict:
    raw = word.lower()
    steps = []

    if 'th' in raw:
        raw = re.sub(r'th', 't', raw, flags=re.I)
        steps.append("'th' -> 't'")
    if 'ph' in raw:
        raw = re.sub(r'ph', 'f', raw, flags=re.I)
        steps.append("'ph' -> 'f'")
    if 'qu' in raw:
        raw = re.sub(r'qu', 'kw', raw, flags=re.I)
        steps.append("'qu' -> 'kw'")
    if 'ck' in raw:
        raw = re.sub(r'ck', 'k', raw, flags=re.I)
        steps.append("'ck' -> 'k'")
    if raw.endswith('tion'):
        raw = re.sub(r'tion$', 'en', raw)
        steps.append("'tion' suffix -> 'en'")
    if raw.endswith('ity'):
        raw = re.sub(r'ity$', 'it', raw)
        steps.append("'ity' suffix -> 'it'")
    if raw.endswith('ing'):
        raw = re.sub(r'ing$', 'en', raw)
        steps.append("'ing' suffix -> 'en'")

    original_vowels = raw
    raw = re.sub(r'[aeioua]{2,}', lambda m: m.group(0)[0], raw, flags=re.I)
    if raw != original_vowels:
        steps.append(f"collapsed vowels '{original_vowels}' -> '{raw}'")

    truncated = raw[:6]
    if len(original_vowels) > 6:
        steps.append(f"truncated to 6 characters: '{truncated}'")

    if bias == 'dutch':
        warped = truncated.replace('c', 'k').replace('s', 'z').replace('v', 'f')
        final_trans = f"{warped}en"
        bias_explanation = (
            f"Dutch mercantile bias: applied harsh consonant shifting (c->k, s->z, v->f) "
            f"and appended '+en' suffix -> '{final_trans}'"
        )
    elif bias == 'norwegian':
        nor_trunc = truncated[:4]
        final_trans = f"ned{nor_trunc}en"
        bias_explanation = (
            f"Norwegian industrial rail bias: added Norwegian failing prefix 'ned-' "
            f"and appended '+en' suffix -> '{final_trans}'"
        )
    elif bias == 'spanish_mock':
        sub = truncated[:-1] + 'u' if truncated.endswith('a') else truncated
        final_trans = f"{sub}ato"
        bias_explanation = (
            f"Spanish broken/bargain mock bias: replaced trailing vowelic sounds with unified 'u' "
            f"and appended cheap suffix '+ato' -> '{final_trans}'"
        )
    elif bias == 'welsh':
        welsh_trunc = truncated[:5]
        welsh_trunc = welsh_trunc.replace('c','g').replace('p','b').replace('t','d')
        final_trans = f"{welsh_trunc}og"
        bias_explanation = (
            f"Welsh bardic/landscape bias: softened consonants, truncated to 5 chars, "
            f"appended Welsh suffix '‑og' → '{final_trans}'"
        )
    else:  # blend
        final_trans = truncated
        bias_explanation = f"Standard phonetic blend: preserved mangled core truncated form -> '{final_trans}'"

    return {
        'translation': final_trans,
        'explanation': (
            f"Phonetic mangling pipeline: [{'; '.join(steps)}]. "
            f"{bias_explanation}"
        )
    }


def stem_word(word: str, dictionary: Dict[str, str]) -> dict:
    nord_prefix = ""
    current = word
    word_bias = get_bias(word)

    # 1. Strip known prefix
    for eng_pref in PREFIXES_SORTED:
        if current.startswith(eng_pref) and len(current) > len(eng_pref) + 2:
            if eng_pref == "over":
                if word_bias == 'dutch':
                    nord_prefix = "over"
                elif word_bias == 'norwegian':
                    nord_prefix = "over"
                elif word_bias == 'spanish_mock':
                    nord_prefix = "sobre"
                elif word_bias == 'welsh':
                    nord_prefix = "dros"
                else:
                    nord_prefix = "sur"
            else:
                nord_prefix = PREFIX_MAP[eng_pref]
            current = current[len(eng_pref):]
            break

    # 2. Exact dictionary match after prefix removal
    if current in dictionary:
        core = dictionary[current]
        return {
            'translation': f"{nord_prefix}{core}",
            'source': 'dictionary',
            'explanation': f"Identified prefix '{nord_prefix}-'. Core '{current}' found in dictionary as '{core}'."
        }

    # 3. Multi‑suffix decomposition
    original_current = current
    suffixes_found = []          # English suffixes removed (in order of removal)
    nord_suffixes = []           # corresponding Nordalian suffixes

    while True:
        matched = False
        for suffix in SUFFIXES_SORTED:
            if current.endswith(suffix) and len(current) > len(suffix) + 1:
                root_candidate = current[:-len(suffix)]
                nord_suffix = SUFFIX_MAP.get(suffix, suffix)
                suffixes_found.append(suffix)
                nord_suffixes.append(nord_suffix)
                current = root_candidate
                matched = True
                break
        if not matched:
            break
        # If the remaining stem is in the dictionary, stop stripping further
        if current in dictionary:
            break

    if suffixes_found:
        # At this point `current` is the final root (possibly in dictionary, or not)
        root = current
        if root in dictionary:
            core = dictionary[root]
        else:
            bias = get_bias(root)
            core = mangle_word(root, bias)['translation']

        # Build the translation: prefix + core + reversed list of Nordalian suffixes
        # (because we stripped from the end, we must reattach in the reverse order)
        translation = nord_prefix + core + ''.join(reversed(nord_suffixes))

        explanation = (
            f"Multi‑suffix stripped: {', '.join(reversed(suffixes_found))} → "
            f"{', '.join(reversed(nord_suffixes))}. Root '{root}' "
            f"{'found in dictionary' if root in dictionary else 'mangled'} to '{core}'."
        )
        return {
            'translation': translation,
            'source': 'stemmed',
            'explanation': explanation
        }

    # 4. Fallback to mangling the whole word (no suffix stripped)
    bias = get_bias(original_current)
    mangled = mangle_word(original_current, bias)
    return {
        'translation': f"{nord_prefix}{mangled['translation']}",
        'source': 'mangled',
        'explanation': (
            f"No dictionary root found. Applied phonetic mangling with {bias.upper()} rules. "
            f"{mangled['explanation']}"
        )
    }


def suggest_nordalian(word: str, dictionary: Dict[str, str], enable_hyphen_fix: bool) -> TranslationResult:
    clean = normalize_word(word)
    if not clean:
        return TranslationResult(original=word, translation='', source='empty',
                                 explanation='Word is empty or contained invalid characters.')

    # 1. Exact dictionary match
    if clean in dictionary:
        return TranslationResult(
            original=word,
            translation=dictionary[clean],
            source='dictionary',
            explanation=f"Exact dictionary mapping matched: '{clean}' translates directly to '{dictionary[clean]}'."
        )

    # 2. Ethnonyms/Nationalities rules (only direct ethnonym matches)
    eth_res = ethnonym_translation(clean)
    if eth_res:
        return eth_res

    # 3. Hyphenated compound words
    if enable_hyphen_fix and '-' in clean:
        parts = clean.split('-')
        sub_results = [suggest_nordalian(part, dictionary, enable_hyphen_fix) for part in parts]
        joined_translation = '-'.join(r.translation for r in sub_results)
        joined_exps = ', '.join(
            f'Part {i+1} ("{parts[i]}") -> "{r.translation}" [{r.source}]'
            for i, r in enumerate(sub_results)
        )
        return TranslationResult(
            original=word,
            translation=joined_translation,
            source='compound',
            explanation=(
                f"COMPOUND RULE IN EFFECT: Split word by hyphen into [{', '.join(parts)}]. "
                f"Translated each sub-part independently: {{{joined_exps}}}. Joined: '{joined_translation}'."
            )
        )

    # 4. Default stemming/mangling
    stemmed = stem_word(clean, dictionary)
    return TranslationResult(
        original=word,
        translation=stemmed['translation'],
        source=stemmed['source'],
        explanation=stemmed['explanation']
    )


def translate_sentence_or_paragraph(text: str, dictionary: Dict[str, str], enable_hyphen_fix: bool) -> str:
    if not text:
        return ""

    word_pattern = re.compile(r"\b[a-zA-Z'\-]+\b")

    def replace_word(match):
        word = match.group(0)
        res = suggest_nordalian(word, dictionary, enable_hyphen_fix)
        translated = res.translation
        if not translated:
            return word

        if word == word.upper():
            if len(translated) <= 3:
                return translated.upper()
            return translated[0].upper() + translated[1:].lower()
        elif word[0].isupper():
            return translated[0].upper() + translated[1:]
        else:
            return translated

    return word_pattern.sub(replace_word, text)