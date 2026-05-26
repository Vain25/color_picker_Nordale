import os
import zipfile
import csv
import re
import io
from PIL import Image

# ===== CONFIGURATION =====
MODS_DIR = r"C:\Users\Ali\AppData\Roaming\ATLauncher\instances\Nordalium\mods"   # change if needed
OUTPUT_CSV = "modded_blocks_with_names.csv"
# =========================

def get_average_hex(image_bytes):
    """Calculates the average hex color of a PNG image, ignoring transparent pixels."""
    try:
        with Image.open(io.BytesIO(image_bytes)) as img:
            img = img.convert("RGBA")
            pixels = list(img.getdata())
            visible = [p for p in pixels if p[3] > 0]
            if not visible:
                return None
            r = sum(p[0] for p in visible) // len(visible)
            g = sum(p[1] for p in visible) // len(visible)
            b = sum(p[2] for p in visible) // len(visible)
            return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return None

def load_lang(jar, modid):
    """Return a dict {key: value} from en_us.lang inside the jar, or {} if not found."""
    try:
        path = f"assets/{modid}/lang/en_us.lang"
        data = jar.read(path).decode("utf-8")
        mapping = {}
        for line in data.splitlines():
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                mapping[k] = v.strip()
        return mapping
    except (KeyError, UnicodeDecodeError):
        return {}

def texture_to_candidate_registry_name(filename):
    """
    Convert a texture filename like 'andesite_ballast1.png' or 'bamboo_block_top.png'
    into a candidate block registry name without suffixes.
    """
    name = os.path.splitext(filename)[0]   # remove .png
    # Remove known directional / variant suffixes
    suffixes = [
        "_side", "_top", "_bottom", "_front", "_back", "_left", "_right",
        "_upper", "_lower", "_end", "_wall", "_edge", "_inside", "_outside",
        "_overlay", "_snowed", "_path", "_off", "_on", "_lit", "_active",
        "_honey", "_normal", "_smooth", "_planks", "_log", "_wood", "_stem",
        "_block", "_bricks", "_tiles", "_small", "_medium", "_large",
        "_fancy", "_simple", "_carved", "_chiseled", "_polished", "_cracked",
        "_mossy", "_weathered", "_exposed", "_oxidised", "_cut", "_grate",
        "_pane", "_rod", "_pole", "_support", "_fence", "_gate", "_door",
        "_trapdoor", "_button", "_pressure_plate", "_sign"
    ]
    # Remove suffixes one by one (longest first to avoid partial matches)
    for suf in sorted(suffixes, key=len, reverse=True):
        if name.endswith(suf):
            name = name[:-len(suf)]
            break
    # Remove trailing digits (e.g., _1, _2, _3)
    name = re.sub(r'_\d+$', '', name)
    # Remove trailing underscores
    name = name.rstrip('_')
    # If nothing left, use original
    if not name:
        name = os.path.splitext(filename)[0]
    return name

def get_display_name(texture_filename, modid, lang_dict):
    """Return the best display name using lang file + fallback."""
    candidate = texture_to_candidate_registry_name(texture_filename)
    # Try common language keys
    for key_format in ["tile.{}.{}.name", "block.{}.{}.name"]:
        key = key_format.format(modid, candidate)
        if key in lang_dict:
            return lang_dict[key]
    # Fallback: human-readable from candidate
    return candidate.replace("_", " ").title()

# ===== Main process =====
if not os.path.exists(MODS_DIR):
    print(f"ERROR: Mods directory not found: {MODS_DIR}")
    exit(1)

with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Mod Name", "Texture File Name", "Average Hex Code", "Block Display Name"])

    print("Scanning mods for block textures...")
    for mod_filename in os.listdir(MODS_DIR):
        if not mod_filename.endswith(".jar"):
            continue

        jar_path = os.path.join(MODS_DIR, mod_filename)
        try:
            with zipfile.ZipFile(jar_path, 'r') as jar:
                # Cache language dict per mod (lazy load)
                lang_cache = {}

                for file_info in jar.infolist():
                    # Must match assets/<modid>/textures/blocks/*.png
                    if not (file_info.filename.startswith("assets/") and
                            "/textures/blocks/" in file_info.filename and
                            file_info.filename.endswith(".png")):
                        continue

                    parts = file_info.filename.split("/")
                    if len(parts) < 4:
                        continue
                    modid = parts[1]   # assets / <modid> / textures / blocks / ...

                    # Load lang once per mod
                    if modid not in lang_cache:
                        lang_cache[modid] = load_lang(jar, modid)

                    img_data = jar.read(file_info.filename)
                    hex_code = get_average_hex(img_data)
                    if not hex_code:
                        continue

                    texture_name = os.path.basename(file_info.filename)
                    display_name = get_display_name(texture_name, modid, lang_cache[modid])

                    writer.writerow([mod_filename, texture_name, hex_code, display_name])

        except (zipfile.BadZipFile, OSError) as e:
            print(f"Skipping {mod_filename}: {e}")

print(f"\nDone! Output saved to {os.path.abspath(OUTPUT_CSV)}")