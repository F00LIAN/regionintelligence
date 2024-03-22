import asyncio
import pprint
from pydantic import BaseModel
from scrape import ascrape_playwright, append_prefix_to_agenda_link, filter_commissions
from ai_extractor import extract
from schemas import SchemaCityWebsites
from const import city_website_links, city_website_prefix_links
import time



# Adjust your testing code accordingly
if __name__ == "__main__":
    
    token_limit = 4000  # Set a token limit for the content

    async def scrape_with_playwright(url: str, city_name: str, tags, **kwargs):
        # Assuming ascrape_playwright is defined and working as expected
        html_content = await ascrape_playwright(url, tags)

        print(f"Extracting {city_name} content with LLM")

        all_extracted_content = []
        
        # Calculate the number of chunks needed
        num_chunks = len(html_content) // token_limit + (1 if len(html_content) % token_limit > 0 else 0)

        for i in range(num_chunks):
            start_index = i * token_limit
            end_index = start_index + token_limit
            html_content_chunk = html_content[start_index:end_index]

            # Assuming extract is defined and working as expected
            extracted_content = extract(**kwargs, content=html_content_chunk)

            # Append prefix to 'agenda_link', now with dynamic city_name
            processed_content = filter_commissions(append_prefix_to_agenda_link(extracted_content, city_name))

            # Add the processed content to the all_extracted_content list
            all_extracted_content.extend(processed_content)

            asyncio.sleep(2)

        pprint.pprint(all_extracted_content)

    # Loop through the cities and their website links
    for city_name, city_url in city_website_links.items():
        asyncio.run(scrape_with_playwright(
            url=city_url,
            city_name=city_name,
            tags=["td", "span", "a"],
            schema_pydantic=SchemaCityWebsites # Assuming SchemaCityWebsites is defined
        ))
