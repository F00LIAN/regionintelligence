from pathlib import Path
import os

PARENT_DIR = Path(__file__).parent.resolve().parent

DATA_DIR = PARENT_DIR / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

TRAINING_DATA_DIR = DATA_DIR / "training"

JSON_DATA_DIR = DATA_DIR / "json"

# Ensure directories exist, and if not, create them
DATA_DIR.mkdir(parents=True, exist_ok=True)
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
TRAINING_DATA_DIR.mkdir(parents=True, exist_ok=True)

if not Path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

if not Path.exists(RAW_DATA_DIR):
    os.mkdir(RAW_DATA_DIR)

if not Path.exists(TRAINING_DATA_DIR):
    os.mkdir(TRAINING_DATA_DIR)
