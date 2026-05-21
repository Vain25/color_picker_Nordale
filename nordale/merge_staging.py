import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
master_path = os.path.join(script_dir, "dictionary.json")
staging_path = os.path.join(script_dir, "..", "nordalian_staging.json")  # one level up
backup_path = os.path.join(script_dir, "dictionary_backup.json")

# 1. Backup the current master
print("Backing up master dictionary...")
with open(master_path, 'r', encoding='utf-8') as f:
    master = json.load(f)
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(master, f, ensure_ascii=False, indent=4)
print(f"  Backup saved ({len(master)} entries)")

# 2. Load the staging file
print("Loading staging file...")
with open(staging_path, 'r', encoding='utf-8') as f:
    staging = json.load(f)

auto_approved = staging.get("auto_approved", {})
print(f"  Auto‑approved entries: {len(auto_approved)}")

# 3. Merge (existing entries are NEVER overwritten)
added = 0
for eng, nord in auto_approved.items():
    if eng not in master:
        master[eng] = nord
        added += 1

print(f"  New entries added: {added}")
print(f"  Final dictionary size: {len(master)}")

# 4. Save the expanded master
with open(master_path, 'w', encoding='utf-8') as f:
    json.dump(master, f, ensure_ascii=False, indent=4)

print("✅ Master dictionary updated successfully!")
print(f"  Backup: {backup_path}")
print(f"  Master: {master_path}")