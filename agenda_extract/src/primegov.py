import os
import sys
from pathlib import Path

# Set the current working directory to the script's directory
os.chdir(os.path.dirname(__file__))
project_root = Path(__file__).resolve().parent.parent  # Adjust based on your project structure
sys.path.append(str(project_root))


import asyncio
from bs4 import BeautifulSoup
import pandas as pd
from playwright.async_api import async_playwright
import json
import time
import os
from src.scrape import  (ascrape_primegov_playwright, append_prefix_to_agenda_link, filter_primegov_commissions, remove_no_agenda_link)
from src.const import primegov_website_links
from src.paths import EXCEL_DIR, PRIMEGOV_DIR
from datetime import datetime

async def scrape_primegov_cities():
    current_time = datetime.now().strftime("%Y-%m-%d")
    tasks = [ascrape_primegov_playwright(city, url, ["a", "h1", "h2", "h3", "td", "span"]) for city, url in primegov_website_links.items()]
    dataframes = await asyncio.gather(*tasks)
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    combined_df.to_excel(EXCEL_DIR / f'primegov_commissions_{current_time}.xlsx', index=False)
    grouped_data = {city: group[['commission_name', 'agenda_link']].to_dict('records') for city, group in combined_df.groupby('City')}

    # Iterate through each city and update the agenda links individually
    for city in grouped_data:
        grouped_data[city] = remove_no_agenda_link(filter_primegov_commissions(append_prefix_to_agenda_link(grouped_data[city], city)))
        
    time.sleep(2)
    json_output = json.dumps(grouped_data, indent=4)

    with open(PRIMEGOV_DIR / f'primegov_commissions_{current_time}.json', 'w') as file:
        file.write(json_output)

    return json_output

# asyncio.run is not needed in Jupyter Notebooks, use it if running as a script
# asyncio.run(scrape_primegov_cities())

