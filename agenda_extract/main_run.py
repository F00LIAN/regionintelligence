import asyncio
from playwright.async_api import async_playwright
from src.primegov import scrape_primegov_cities
from src.legistar import scrape_legistar_cities
from src.concat import concatenate_json_files
from src.extract import main_extract

def main():
    
    # Run the PrimeGov scraper
    asyncio.run(scrape_primegov_cities())

    # Run the Legistar scraper
    asyncio.run(scrape_legistar_cities())

    # Concatenate the JSON files
    concatenate_json_files()

    # Extract PDF links and project details
    main_extract()

if __name__ == "__main__":
    main()


