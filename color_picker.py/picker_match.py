import csv
import math
from tkinter import colorchooser, messagebox
import os

CSV_FILE = "modded_blocks_hex.csv"

def hex_to_rgb(hex_str):
    """Converts #ffffff format string to (r, g, b) tuple."""
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def load_block_colors(csv_path):
    """Loads block data from the CSV file into memory."""
    blocks = []
    if not os.path.exists(csv_path):
        messagebox.showerror("Error", f"Could not find {csv_path}. Please run your extractor first!")
        return None
        
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for row in reader:
            if len(row) >= 3:
                mod_name, texture_name, hex_code = row[0], row[1], row[2]
                blocks.append({
                    "mod": mod_name,
                    "texture": texture_name,
                    "rgb": hex_to_rgb(hex_code),
                    "hex": hex_code
                })
    return blocks

def find_closest_block(picked_rgb, block_list):
    """Calculates Euclidean distance in 3D RGB space to find the closest match."""
    closest_block = None
    min_distance = float('inf')
    
    pr, pg, pb = picked_rgb
    
    for block in block_list:
        br, bg, bb = block["rgb"]
        # Standard 3D distance formula: sqrt((r1-r2)^2 + (g1-g2)^2 + (b1-b2)^2)
        distance = math.sqrt((pr - br)**2 + (pg - bg)**2 + (pb - bb)**2)
        
        if distance < min_distance:
            min_distance = distance
            closest_block = block
            
    return closest_block, min_distance

def main():
    blocks = load_block_colors(CSV_FILE)
    if not blocks:
        return

    print("Opening color picker... Select a color to find its matching Minecraft block.")
    # Open the native OS color picker dialog
    color_code = colorchooser.askcolor(title="Choose a Color")
    
    # color_code returns ((R, G, B), "#hex") or (None, None) if cancelled
    if color_code[0]:
        picked_rgb = [int(x) for x in color_code[0]]
        picked_hex = color_code[1]
        
        closest, match_score = find_closest_block(picked_rgb, blocks)
        
        print("\n=== MATCH FOUND ===")
        print(f"Picked Color: {picked_hex}")
        print(f"Closest Block: {closest['texture'].replace('.png', '')}")
        print(f"From Mod Jar: {closest['mod']}")
        print(f"Block Avg Hex: {closest['hex']}")
        print(f"Color Distance: {match_score:.2f} (Lower means closer match)")

if __name__ == "__main__":
    main()
