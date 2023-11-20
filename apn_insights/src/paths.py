from pathlib import Path
import os

PARENT_DIR = Path(__file__).parent.resolve().parent
DATA_DIR = PARENT_DIR / 'data'

CONFIG_DIR = PARENT_DIR / 'config'

COMPANY_DATA_DIR = PARENT_DIR / 'map_data_company_database' 

# Ensure directories exist, and if not, create them
DATA_DIR.mkdir(parents=True, exist_ok=True)

COMPANY_DATA_DIR.mkdir(parents=True, exist_ok=True)

if not Path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

if not Path.exists(COMPANY_DATA_DIR):
    os.mkdir(COMPANY_DATA_DIR)