from pathlib import Path
import os

PARENT_DIR = Path(__file__).parent.resolve().parent
DATA_DIR = PARENT_DIR / 'data'
#RAW_DATA_DIR = PARENT_DIR / 'data' / 'raw'
TRANSFORMED_DATA_DIR = PARENT_DIR / 'data' / 'transformed'
FINAL_DATA_DIR = PARENT_DIR / 'data' / 'final'
DATA_CACHE_DIR = PARENT_DIR / 'data' / 'cache'
DROPBOX_DIR = DATA_DIR/ 'dropbox'
MODELS_DIR = PARENT_DIR / 'models'
FRONTEND_DIR = DATA_DIR / 'frontend'
CLEANED_DATA_DIR = DATA_DIR / 'cleaned'
VALIDATION_DIR = DATA_DIR / 'validation'
NORMALIZED_DATA_DIR = DATA_DIR / 'normalized'


if not Path(DATA_DIR).exists():
    os.mkdir(DATA_DIR)

#if not Path(RAW_DATA_DIR).exists():
#    os.mkdir(RAW_DATA_DIR)

if not Path(TRANSFORMED_DATA_DIR).exists():
    os.mkdir(TRANSFORMED_DATA_DIR)

if not Path(MODELS_DIR).exists():
    os.mkdir(MODELS_DIR)

if not Path(DATA_CACHE_DIR).exists():
    os.mkdir(DATA_CACHE_DIR)

if not Path(DROPBOX_DIR).exists():
    os.mkdir(DROPBOX_DIR)

if not Path(FINAL_DATA_DIR).exists():
    os.mkdir(FINAL_DATA_DIR)

if not Path(FRONTEND_DIR).exists():
    os.mkdir(FRONTEND_DIR)

if not Path(CLEANED_DATA_DIR).exists():
    os.mkdir(CLEANED_DATA_DIR)

if not Path(VALIDATION_DIR).exists():
    os.mkdir(VALIDATION_DIR)

if not Path(NORMALIZED_DATA_DIR).exists():
    os.mkdir(NORMALIZED_DATA_DIR)

