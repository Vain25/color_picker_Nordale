import csv
import math
import os
import pyautogui
from pynput import mouse

CSV_FILE = "modded_blocks_hex.csv"

def hex_to_rgb(hex_str):
    return tuple(int(hex_str.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

def load_block_colors(csv_path):
    blocks = []
    if not os.path.exists(csv_path):
        print(f"Error: Could not find {csv_path}. Please run your extractor first!")
        return None
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) >= 3:
                blocks.append({
                    "mod": row[0],
                    "texture": row[1],
                    "rgb": hex_to_rgb(row[2]),
                    "hex": row[2]
                })
    return blocks

def find_closest_block(picked_rgb, block_list):
    closest_block = None
    min_distance = float('inf')
    pr, pg, pb = picked_rgb
    for block in block_list:
        br, bg, bb = block["rgb"]
        distance = math.sqrt((pr - br)**2 + (pg - bg)**2 + (pb - bb)**2)
        if distance < min_distance:
            min_distance = distance
            closest_block = block
    return closest_block, min_distance

# Load the CSV data once at startup
blocks = load_block_colors(CSV_FILE)

def on_click(x, y, button, pressed):
    """Triggers every time a mouse button is pressed anywhere on screen."""
    # Only trigger when the left mouse button is pressed down
    if pressed and button == mouse.Button.left:
        try:
            # Sample the exact pixel color beneath the cursor coordinates
            picked_rgb = pyautogui.pixel(int(x), int(y))
            picked_hex = f"#{picked_rgb[0]:02x}{picked_rgb[1]:02x}{picked_rgb[2]:02x}"
            
            closest, match_score = find_closest_block(picked_rgb, blocks)
            
            print("\n=== LIVE EYE-DROPPER MATCH ===")
            print(f"Captured Hex: {picked_hex}")
            print(f"Closest Block: {closest['texture'].replace('.png', '')}")
            print(f"From Mod:      {closest['mod']}")
            print(f"Match Score:   {match_score:.2f} (0 is a perfect match)")
            print("------------------------------")
            print("Click anywhere else to pick another color... (Ctrl+C in terminal to stop)")
            
        except Exception as e:
            # Catch errors if clicking outside active monitor bounds
            pass

def main():
    if not blocks:
        return
        
    print("=== IN-HOUSE GLOBAL DROPPER ACTIVE ===")
    print("The script is listening. Click ANYWHERE on your screen to sample a color.")
    print("Press Ctrl + C in this terminal window when you want to stop.")
    print("-----------------------------------------------------------------")

    # Start listening to global mouse inputs
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

if __name__ == "__main__":
    main()
