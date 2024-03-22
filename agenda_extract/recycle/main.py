import asyncio
import pprint

from ai_extractor import extract
from schemas import SchemaNewsWebsites, ecommerce_schema, SchemaCityWebsites
from scrape import ascrape_playwright
from const import city_website_links, city_website_prefix_links


def append_prefix_to_agenda_link(extracted_data, prefix_link="https://fullerton.legistar.com/"):
    for item in extracted_data:
        item['agenda_link'] = prefix_link + item['agenda_link']
    return extracted_data

# TESTING
if __name__ == "__main__":
    token_limit = 4000

    # News sites mostly have <span> tags to scrape
    city_url = "https://fullerton.legistar.com/Calendar.aspx"

    async def scrape_with_playwright(url: str, tags, **kwargs):
        html_content = await ascrape_playwright(url, tags)

        print("Extracting content with LLM")

        html_content_fits_context_window_llm = html_content[:token_limit]

        extracted_content = extract(**kwargs,
                                    content=html_content_fits_context_window_llm)
            # Append prefix to 'agenda_link'
        processed_content = append_prefix_to_agenda_link(extracted_content)

        pprint.pprint(processed_content)

    # Scrape and Extract with LLM
    asyncio.run(scrape_with_playwright(
        url=city_url,
        tags=["span", "a"],
        schema_pydantic=SchemaCityWebsites
    ))