from concurrent.futures import ThreadPoolExecutor
from src.data import (main_anaheim, 
                      main_city_of_orange, 
                      main_santa_ana, 
                      main_city_of_fullerton,
                      main_garden_grove)

def run_all_scrapers():
    with ThreadPoolExecutor() as executor:
        executor.submit(main_anaheim)
        executor.submit(main_city_of_orange)
        executor.submit(main_santa_ana)
        executor.submit(main_city_of_fullerton)
        executor.submit(main_garden_grove)