import asyncio
import json
from pydantic import BaseModel
from typing import Optional
from src.scrape import ascrape_playwright, append_prefix_to_agenda_link, filter_commissions
from src.ai_extractor import extract
from src.const import city_website_prefix_links, legistar_website_links, primegov_website_links, tags
from src.schemas import SchemaCityWebsites, PrimegovCityInfo
import pprint
from datetime import datetime
from src.paths import JSON_DIR, EXCEL_DIR
import logging
from src.validation import validate_item

async def scrape_legistar_cities(url: str, city_name: str, tags=tags, **kwargs):
    city_commissions_results = {}
    loop = asyncio.get_event_loop()
    current_time = datetime.now().strftime("%Y-%m-%d")
    html_content = await ascrape_playwright(url, tags)

    logging.info(f"Extracting legistar {city_name} content with LLM")

    all_extracted_content = []
    token_limit = 4000  # Set a token limit for the content

    num_chunks = len(html_content) // token_limit + (1 if len(html_content) % token_limit > 0 else 0)
    for i in range(num_chunks):
        start_index = i * token_limit
        end_index = start_index + token_limit
        html_content_chunk = html_content[start_index:end_index]

        extracted_content = extract(**kwargs, content=html_content_chunk)
        processed_content = filter_commissions(append_prefix_to_agenda_link(extracted_content, city_name))
        all_extracted_content.extend(processed_content)

        await asyncio.sleep(2) 
    
    logging.info(f"Finished extracting {city_name} content with LLM")
    
    # Legistar website links legistar_website_prefix_links, legistar_, primegov,legistar,primegov,["td", "span", "a"]
    logging.info(f"Scraping {city_name} with Playwright")
    for city_name, city_url in legistar_website_links.items():
        commissions = loop.run_until_complete(scrape_legistar_cities(city_url, city_name, tags=tags, schema_pydantic=SchemaCityWebsites))
        city_commissions_results[city_name] = commissions
        logging.info(f"Finished scraping {city_name} with Playwright")
    # Save the results to a JSON file
    with open(JSON_DIR / f'legistar_commissions_{current_time}.json', 'w', encoding='utf-8') as file:
        json.dump(city_commissions_results, file, ensure_ascii=False, indent=4, default=lambda x: x.dict() if isinstance(x, BaseModel) else x)
   

    return all_extracted_content
    

