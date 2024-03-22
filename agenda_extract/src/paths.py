from pathlib import Path
import os

PARENT_DIR = Path(__file__).parent.resolve().parent
DATA_DIR = PARENT_DIR / 'data'
NOTEBOOK_DIR = PARENT_DIR / 'notebooks'
SRC_DIR = PARENT_DIR / 'src'
JSON_DIR = DATA_DIR / 'json'
EXCEL_DIR = DATA_DIR / 'excel'
LOGGER_DIR = PARENT_DIR / 'logs'
CONCAT_DIR = DATA_DIR / 'concatenated'
FINAL_DIR = DATA_DIR / 'final'
PRIMEGOV_DIR = JSON_DIR / 'primegov'
LEGISTAR_DIR = JSON_DIR / 'legistar'

PDF_PATH = DATA_DIR / 'pdfs'

# Create the data directory if it doesn't exist

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Create the notebooks directory if it doesn't exist
if not os.path.exists(NOTEBOOK_DIR):
    os.makedirs(NOTEBOOK_DIR)

# Create the src directory if it doesn't exist
if not os.path.exists(SRC_DIR):
    os.makedirs(SRC_DIR)

# Create the json directory if it doesn't exist
if not os.path.exists(JSON_DIR):
    os.makedirs(JSON_DIR)

if not os.path.exists(EXCEL_DIR):
    os.makedirs(EXCEL_DIR)

if not os.path.exists(LOGGER_DIR):
    os.makedirs(LOGGER_DIR)

if not os.path.exists(CONCAT_DIR):
    os.makedirs(CONCAT_DIR)

if not os.path.exists(PRIMEGOV_DIR):
    os.makedirs(PRIMEGOV_DIR)

if not os.path.exists(LEGISTAR_DIR):
    os.makedirs(LEGISTAR_DIR)

if not os.path.exists(FINAL_DIR):
    os.makedirs(FINAL_DIR)

if not os.path.exists(PDF_PATH):
    os.makedirs(PDF_PATH)