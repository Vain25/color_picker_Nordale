import os
import zipfile
import csv
from PIL import Image
import io

# 1. Update these paths to match your computer's setup!
MODS_DIR = r"C:\Users\Ali\AppData\Roaming\ATLauncher\instances\Nordalium\mods"
OUTPUT_CSV = "modded_blocks_hex.csv"

def get_average_hex(image_bytes):
    """Calculates the average hex color of a PNG image, ignoring transparent pixels."""
    try:
        with Image.open(io.BytesIO(image_bytes)) as img:
            img = img.convert("RGBA")
            pixels = list(img.getdata())
            
            # Filter out completely transparent pixels (alpha == 0)
            visible_pixels = [p for p in pixels if p[3] > 0]
            if not visible_pixels:
                return None
                
            # Sum up R, G, B channels separately
            r_total = sum(p[0] for p in visible_pixels)
            g_total = sum(p[1] for p in visible_pixels)
            b_total = sum(p[2] for p in visible_pixels)
            count = len(visible_pixels)
            
            # Calculate mathematical average integers
            r_avg = r_total // count
            g_avg = g_total // count
            b_avg = b_total // count
            
            return f"#{r_avg:02x}{g_avg:02x}{b_avg:02x}"
    except Exception:
        return None

# Prepare CSV output file
with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Mod Name", "Texture File Name", "Average Hex Code"])
    
    # 2. Iterate through all files in the mods directory
    if not os.path.exists(MODS_DIR):
        print(f"Error: The directory {MODS_DIR} does not exist. Please check your path.")
        exit()

    print("Scanning mod files for block textures... Please wait.")
    
    for filename in os.listdir(MODS_DIR):
        if filename.endswith(".jar"):
            jar_path = os.path.join(MODS_DIR, filename)
            
            try:
                # Open the mod .jar file as a standard ZIP archive
                with zipfile.ZipFile(jar_path, 'r') as jar:
                    for file_info in jar.infolist():
                        # 1.12.2 target paths usually look like: assets/mod_id/textures/blocks/item_name.png
                        if "assets/" in file_info.filename and "/textures/blocks/" in file_info.filename and file_info.filename.endswith(".png"):
                            
                            # Read raw image data directly from memory without extracting to disk
                            img_data = jar.read(file_info.filename)
                            hex_code = get_average_hex(img_data)
                            
                            if hex_code:
                                # Clean up the visual names for the CSV output
                                clean_name = os.path.basename(file_info.filename)
                                writer.writerow([filename, clean_name, hex_code])
                                
            except (zipfile.BadZipFile, PermissionError):
                # Skip corrupt mods or files currently locked by the game
                continue

print(f"\nSuccess! Every extracted block hex code has been saved to: {os.path.abspath(OUTPUT_CSV)}")


