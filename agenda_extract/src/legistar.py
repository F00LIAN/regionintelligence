import os
import sys
from pathlib import Path
import asyncio
from bs4 import BeautifulSoup
import pandas as pd
from playwright.async_api import async_playwright
import json
import time
import os

# Set the current working directory to the script's directory
os.chdir(os.path.dirname(__file__))
project_root = Path(__file__).resolve().parent.parent  # Adjust based on your project structure
sys.path.append(str(project_root))



from src.const import legistar_website_links
from src.scrape import (ascrape_legistar_playwright, filter_legistar_commissions, append_prefix_to_agenda_link, remove_no_agenda_link)
from src.paths import EXCEL_DIR, LEGISTAR_DIR
from datetime import datetime
import logging

async def scrape_legistar_cities():
    #logging.info("Scraping Legistar Cities")

    current_time = datetime.now().strftime("%Y-%m-%d")
    tasks = [ascrape_legistar_playwright(city, url, ["a", "h1", "h2", "h3", "td", "span"]) for city, url in legistar_website_links.items()]
    dataframes = await asyncio.gather(*tasks)
    combined_df = pd.concat(dataframes, ignore_index=True)

    combined_df.to_excel(EXCEL_DIR / f'legistar_commissions_{current_time}.xlsx', index=False)
    grouped_data = {city: group[['commission_name', 'agenda_link']].to_dict('records') for city, group in combined_df.groupby('City')}

    # Iterate through each city and update the agenda links individually
    for city in grouped_data:
        grouped_data[city] = remove_no_agenda_link(filter_legistar_commissions(append_prefix_to_agenda_link(grouped_data[city], city)))
    
    json_output = json.dumps(grouped_data, indent=4)

    with open(LEGISTAR_DIR / f'legistar_commissions_{current_time}.json', 'w') as file:
        file.write(json_output)

#asyncio.run is not needed in Jupyter Notebooks, use it if running as a script
#asyncio.run(scrape_legistar_cities())
