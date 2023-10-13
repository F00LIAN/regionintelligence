from src.data import (main_los_angeles_county_upcodes,
                      main_california_upcodes,
                      main_san_francisco_upcodes,
                      main_los_angeles_upcodes,
                      main_san_jose_upcodes)

from concurrent.futures import ThreadPoolExecutor

def run_all_code_scrapers():
    with ThreadPoolExecutor() as executor:
        executor.submit(main_los_angeles_county_upcodes)
        executor.submit(main_california_upcodes)
        executor.submit(main_san_francisco_upcodes)
        executor.submit(main_los_angeles_upcodes)
        executor.submit(main_san_jose_upcodes)

                      