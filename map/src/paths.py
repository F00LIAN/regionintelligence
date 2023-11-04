from pathlib import Path
import os

PARENT_DIR = Path(__file__).parent.resolve().parent
DATA_DIR = PARENT_DIR / 'map_data_production'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
FINAL_DATA_DIR = DATA_DIR / 'final'

COMPANY_DATA_DIR = PARENT_DIR/ 'map_data_company_database' 

# Ensure directories exist, and if not, create them
DATA_DIR.mkdir(parents=True, exist_ok=True)
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
FINAL_DATA_DIR.mkdir(parents=True, exist_ok=True)
COMPANY_DATA_DIR.mkdir(parents=True, exist_ok=True)

if not Path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

if not Path.exists(RAW_DATA_DIR):
    os.mkdir(RAW_DATA_DIR)

if not Path.exists(PROCESSED_DATA_DIR):
    os.mkdir(PROCESSED_DATA_DIR)

if not Path.exists(FINAL_DATA_DIR):
    os.mkdir(FINAL_DATA_DIR)

if not Path.exists(COMPANY_DATA_DIR):
    os.mkdir(COMPANY_DATA_DIR)