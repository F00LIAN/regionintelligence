import os
import sys
from pathlib import Path

# Set the current working directory to the script's directory
os.chdir(os.path.dirname(__file__))
project_root = Path(__file__).resolve().parent.parent  # Adjust based on your project structure
sys.path.append(str(project_root))

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import requests
import asyncio
import pprint
import pandas as pd
import json
import time
from const import city_website_prefix_links, primegov_website_links
from datetime import datetime

# THE ORDER OF THE TAGS MATTERS
#["h1", "h2", "h3", "td", "span", "a", "div", "tbody"]
tags =  ["td", "a"]

primegov_website_links = {
    "Long Beach, CA": "https://longbeach.primegov.com/public/portal",
    "Santa Ana, CA": "https://santa-ana.primegov.com/public/portal"
    }


def extract_tags(html_content, tags: list[str]):
    """
    This takes in HTML content and a list of tags, and returns a string
    containing the text content of all elements with those tags, along with their href attribute if the
    tag is an "a" tag.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    all_titles = []
    all_hrefs = []
    for tag in tags:
        elements = soup.find_all(tag)

        for element in elements:
            print(element)
            # if the tag is a td and has a title attribute, append its title, if it has no title attribute but has a date . Append the date
            if tag == "td":
                title = element.get('title')
                if title:
                    all_titles.append(element.get_text())

            # check if the tag is 'a' 
            elif tag == "a":
                # Get class attribute and check if it starts with "dropdown-document-" 
                class_attr = element.get('class')
                if class_attr and any("dropdown-0" in c or "dropdown-document-0" in c for c in class_attr):
                    href = element.get('href')
                    all_hrefs.append(href)

    return all_titles, all_hrefs

def create_df(city_name, titles, hrefs):
    """
    Creates a pandas DataFrame from city name, titles, and hrefs.
    """
    lengths = min(len(titles), len(hrefs))  # Ensure equal length lists
    data = {"City": [city_name] * lengths, "Title": titles[:lengths], "URL": hrefs[:lengths]}
    return pd.DataFrame(data)

async def ascrape_playwright(city_name, url, tags: list[str]):
    """
    Asynchronously scrapes content from a given URL and returns a DataFrame of the results.
    """
    print(f"Started scraping {city_name}...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        page_source = await page.content()
        titles, hrefs = extract_tags(page_source, tags)
        df = create_df(city_name, titles, hrefs)
        await browser.close()
    return df

async def scrape_all_cities():
    tasks = [ascrape_playwright(city, url, ["h1", "h2", "h3", "td", "span", "a"]) for city, url in primegov_website_links.items()]
    dataframes = await asyncio.gather(*tasks)
    time.sleep(5)
    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df.to_excel('scraped_content.xlsx', index=False)
    # After you have the combined DataFrame from all cities
    grouped_data = {city: group[['Title', 'URL']].to_dict('records') 
                for city, group in combined_df.groupby('City')}

    # Convert the grouped data to JSON
    json_output = json.dumps(grouped_data, indent=4)

    # save the json output to a file
    with open('scraped_content.json', 'w') as file:
        file.write(json_output)
    return print(json_output)

# Run the scraping tasks and display the combined DataFrame
asyncio.run(scrape_all_cities())


"""   with open('scraped_content_2.txt', 'w', encoding='utf-8') as file:
        file.write(results)

    print("Results saved to scraped_content.txt")"""