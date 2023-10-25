
# Import dependencies
from pathlib import Path
import os
import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from transformers import AutoTokenizer, AutoModel
import logging
from typing import Optional

## PATHS
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


## GET CHROME DRIVER
def get_chrome_driver():
    """Initializes and returns a Selenium Chrome web driver using ChromeDriverManager."""
    options = Options()
    return webdriver.Chrome()

def navigate_and_print_title(driver, url):
    """Navigates to the specified URL using the given driver and prints the page title."""
    driver.get(url)
    print(driver.title)



## CONSTANTS
CALIFORNIA_UPCODES_URL = "https://up.codes/codes/california"
LOS_ANGELES_UPCODES_URL = "https://up.codes/codes/los_angeles"
LOS_ANGELES_COUNTY_UPCODES_URL = "https://up.codes/codes/los-angeles-county"
SAN_FRANCISCO_UPCODES_URL = "https://up.codes/codes/san_francisco"
SAN_JOSE_UPCODES_URL = "https://up.codes/codes/san-jose"

tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")


## LOGGING 

def get_console_logger(name: Optional[str] = 'tutorial', level: Optional[str] = 'DEBUG') -> logging.Logger:
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Set logger level
        numeric_level = getattr(logging, level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError(f'Invalid log level: {level}')
        logger.setLevel(numeric_level)
        
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(numeric_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S %Z')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File Handler
        file_handler = logging.FileHandler('app.log')
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger