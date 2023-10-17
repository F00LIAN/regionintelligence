from src.gather_data import (main_los_angeles_county_upcodes,
                      main_california_upcodes,
                      main_san_francisco_upcodes,
                      main_los_angeles_upcodes,
                      main_san_jose_upcodes)

from src.send_to_json import (los_angeles_county_json,
                        california_json,
                        san_francisco_json,
                        los_angeles_json,
                        san_jose_json)

from concurrent.futures import ThreadPoolExecutor
from src.paths import DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, JSON_DATA_DIR

def run_all_code_scrapers():
    with ThreadPoolExecutor() as executor:
        executor.submit(main_los_angeles_county_upcodes)
        executor.submit(main_california_upcodes)
        executor.submit(main_san_francisco_upcodes)
        executor.submit(main_los_angeles_upcodes)
        executor.submit(main_san_jose_upcodes)

def turn_all_text_to_json():
    with ThreadPoolExecutor() as executor:
        executor.submit(los_angeles_county_json)
        executor.submit(california_json)
        executor.submit(san_francisco_json)
        executor.submit(los_angeles_json)
        executor.submit(san_jose_json)
