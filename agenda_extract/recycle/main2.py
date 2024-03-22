import asyncio
import pprint
from pydantic import BaseModel
from scrape import ascrape_playwright
from ai_extractor import extract
from schemas import SchemaCityWebsites
from const import city_website_links, city_website_prefix_links

# Assuming city_website_links and city_website_prefix_links are defined as provided

def append_prefix_to_agenda_link(extracted_data, city_name):
    prefix_link = city_website_prefix_links.get(city_name, "")
    for item in extracted_data:
        item['agenda_link'] = prefix_link + item['agenda_link']
    return extracted_data

# Adjust your testing code accordingly
if __name__ == "__main__":
    
    # chunk size for token limit in the content
    
    token_limit = 4000  # Set a token limit for the content

    # Define an async function to scrape content and append prefix
    async def scrape_with_playwright(url: str, city_name: str, tags, **kwargs):
        # Assuming ascrape_playwright is defined and working as expected
        html_content = await ascrape_playwright(url, tags)

        print(f"Extracting {city_name} content with LLM")

        html_content_fits_context_window_llm = html_content[:token_limit]

        # Assuming extract is defined and working as expected
        extracted_content = extract(**kwargs, content=html_content_fits_context_window_llm)

        # Append prefix to 'agenda_link', now with dynamic city_name
        processed_content = append_prefix_to_agenda_link(extracted_content, city_name)

        pprint.pprint(processed_content)

    # Loop through the cities and their website links
    for city_name, city_url in city_website_links.items():
        asyncio.run(scrape_with_playwright(
            url=city_url,
            city_name=city_name,
            tags=["td", "span", "a"],
            schema_pydantic=SchemaCityWebsites # Assuming SchemaCityWebsites is defined
        ))
