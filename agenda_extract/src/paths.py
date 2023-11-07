from pathlib import Path
import os

PARENT_DIR = Path(__file__).parent.resolve().parent
DATA_DIR = PARENT_DIR / 'data'

# Ensure directories exist, and if not, create them
DATA_DIR.mkdir(parents=True, exist_ok=True)

if not Path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)
