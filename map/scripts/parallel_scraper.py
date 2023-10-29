from concurrent.futures import ThreadPoolExecutor
import src.logger as logger
from src.data import (main_anaheim, 
                      main_city_of_orange, 
                      main_santa_ana, 
                      main_city_of_fullerton,
                      main_garden_grove)
                      
logger = logger.get_console_logger()

def run_all_scrapers():
    """Run all scrapers in parallel"""
    logger.info('Running all scrapers in parallel')
    with ThreadPoolExecutor() as executor:
        executor.submit(main_anaheim)
        executor.submit(main_city_of_orange)
        executor.submit(main_santa_ana)
        executor.submit(main_city_of_fullerton)
        executor.submit(main_garden_grove)
    logger.info('All scrapers finished')

run_all_scrapers()