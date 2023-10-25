import datetime
import logging
import os
from typing import List, Optional

import requests
from bytewax.inputs import DynamicInput, StatelessSource

from scrapers import (main_los_angeles_county_upcodes,
                      main_california_upcodes,
                      main_san_francisco_upcodes,
                      main_los_angeles_upcodes,
                      main_san_jose_upcodes)

from text_to_json import (los_angeles_county_json,
                        california_json,
                        san_francisco_json,
                        los_angeles_json,
                        san_jose_json)

from concat_all_json_codes import concatenate_json_files
from send_to_qdrant_vector_db import BuildingCodeProcessor, Document

from concurrent.futures import ThreadPoolExecutor
from utils import get_console_logger

logger = get_console_logger(name='main_script', level='INFO')

def run_all_code_scrapers():
    logger.info("Running all code scrapers...")
    print("Running all code scrapers...")
    with ThreadPoolExecutor() as executor:
        executor.submit(main_los_angeles_county_upcodes)
        executor.submit(main_california_upcodes)
        executor.submit(main_san_francisco_upcodes)
        executor.submit(main_los_angeles_upcodes)
        executor.submit(main_san_jose_upcodes)
    logger.info("All code scrapers have finished running.")
    print("All code scrapers have finished running.")

def turn_all_text_to_json():
    logger.info("Turning all text to JSON...")
    print("Turning all text to JSON...")
    with ThreadPoolExecutor() as executor:
        executor.submit(los_angeles_county_json)
        executor.submit(california_json)
        executor.submit(san_francisco_json)
        executor.submit(los_angeles_json)
        executor.submit(san_jose_json)
    logger.info("All text has been turned to JSON.")
    print("All text has been turned to JSON.")


if __name__ == '__main__':

    logger.info("Starting batch pipeline...")
    print("Starting batch pipeline...")
    
    run_all_code_scrapers()
    turn_all_text_to_json()

    logger.info("Concatenating all JSON files...")
    print("Concatenating all JSON files...")

    concatenate_json_files()

    logger.info("All JSON files have been concatenated.")
    print("All JSON files have been concatenated.")

    logger.info("Sending all JSON files to Qdrant Vector DB...")
    print("Sending all JSON files to Qdrant Vector DB...")

    processor = BuildingCodeProcessor()
    processor.run()

    logger.info("All JSON files have been sent to Qdrant Vector DB.")
    print("All JSON files have been sent to Qdrant Vector DB.")
    
    logger.info("Batch pipeline complete.")
    print("Batch pipeline complete.")