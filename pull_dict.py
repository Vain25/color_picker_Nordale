# Change this:
# from Nordale import NordaleEngine, ai_translate

# To this:
import sys
# Add current directory to path so it can find Nordale.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Nordale import NordaleEngine, ai_translate

# Base paths
base_dir = os.path.dirname(os.path.abspath(__file__))
local_json_path = os.path.join(base_dir, "nordale", "dictionary.json")

# URL of your live app's dictionary raw endpoint or temporary file backup
# Since Streamlit Cloud doesn't expose an open write API back to git,
# we can fetch the state or manually paste your live additions to lock them down.
print("Checking local sync status...")

