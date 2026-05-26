import csv
import json

blocks = []
with open("modded_blocks_hex.csv", mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        if len(row) >= 3:
            blocks.append({
                "mod": row[0],
                "texture": row[1].replace(".png", ""),
                "hex": row[2]
            })

with open("blocks.json", "w", encoding="utf-8") as f:
    json.dump(blocks, f, indent=4)
print("Converted data to blocks.json!")
