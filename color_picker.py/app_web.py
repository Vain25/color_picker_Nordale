import streamlit as st
import csv
import math
import os
import io
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates
from streamlit_paste_button import paste_image_button

# File Path Configuration
# Updated line 11
CSV_FILE = os.path.join("color_picker.py", "modded_blocks_with_names.csv")

# --- Helper Functions ---
def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    # Ensures we don't crash on invalid hex codes
    if len(hex_str) != 6:
        return (0, 0, 0)
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb[:3])

@st.cache_data
def load_block_colors(csv_path):
    if not os.path.exists(csv_path): return None
    blocks = []
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            next(reader) # Skip header
        except StopIteration:
            return None
        
        for row in reader:
            if len(row) >= 3:
                hex_val = row[2].strip()
                # Validate hex format before adding
                if hex_val.startswith('#') and len(hex_val) == 7:
                    try:
                        blocks.append({
                            "mod": row[0], 
                            "texture": row[1].replace(".png", ""), 
                            "rgb": hex_to_rgb(hex_val), 
                            "hex": hex_val
                        })
                    except ValueError:
                        continue # Skip rows that have invalid hex characters
    return blocks

def find_closest_block(picked_rgb, block_list):
    closest_block, min_distance = None, float('inf')
    pr, pg, pb = picked_rgb
    for block in block_list:
        br, bg, bb = block["rgb"]
        dist = math.sqrt((pr - br)**2 + (pg - bg)**2 + (pb - bb)**2)
        if dist < min_distance:
            min_distance, closest_block = dist, block
    return closest_block, min_distance

# --- Main App ---
st.set_page_config(page_title="Nordale Color Matcher", page_icon="🎨")
st.title("🎨 Nordale Block Color Matcher")
blocks = load_block_colors(CSV_FILE)

if not blocks:
    st.error(f"Could not find or load valid data from `{CSV_FILE}`.")
    st.stop()

# Option 1: Paste
st.subheader("📋 Option 1: Paste an Image")
paste_result = paste_image_button(label="📋 Paste Image", background_color="#f0f8ff")
if paste_result.image_data is not None:
    img = Image.open(io.BytesIO(paste_result.image_data)) if isinstance(paste_result.image_data, bytes) else paste_result.image_data
    st.image(img, use_container_width=True)
    coords = streamlit_image_coordinates(img, key="paste_c")
    if coords:
        rgb = img.convert("RGB").getpixel((coords["x"], coords["y"]))
        st.session_state["p_res"] = find_closest_block(rgb, blocks)
        st.session_state["p_col"] = rgb_to_hex(rgb)

if "p_res" in st.session_state:
    c, s = st.session_state["p_res"]
    st.info(f"Match: {c['texture']} ({c['mod']}) | Precision: {s:.2f}")

# Option 2: Manual
st.subheader("🎨 Option 2: Manual Color Picker")
manual_hex = st.color_picker("Pick a color", "#007bff")
c, s = find_closest_block(hex_to_rgb(manual_hex), blocks)
st.write(f"Match: **{c['texture']}** | Mod: {c['mod']}")

# Option 3: Upload
st.subheader("📁 Option 3: Upload Image")
up_file = st.file_uploader("Upload", type=["png", "jpg"])
if up_file:
    img = Image.open(up_file)
    coords = streamlit_image_coordinates(img, key="up_c")
    if coords:
        rgb = img.convert("RGB").getpixel((coords["x"], coords["y"]))
        c, s = find_closest_block(rgb, blocks)
        st.write(f"Match: **{c['texture']}** | Mod: {c['mod']}")