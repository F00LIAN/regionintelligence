from concurrent.futures import ThreadPoolExecutor
import src.logger as logger
from src.data import (main_anaheim, 
                      main_city_of_orange, 
                      main_santa_ana, 
                      main_city_of_fullerton,
                      main_garden_grove,
                      main_huntington_beach,
                      main_irvine_scraper)
                      
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
        executor.submit(main_irvine_scraper)
        executor.submit(main_huntington_beach)
        logger.info('All scrapers finished')
