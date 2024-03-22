import asyncio
import pprint
import pandas as pd
from bs4 import BeautifulSoup
import playwright
from playwright.async_api import async_playwright
from src.const import city_website_prefix_links
import time
import tqdm as tqdm


################### Legistar ############################


def extract_legistar_tags(html_content):
    """
    Parses HTML content to find 'a' tags within "tr" elements with classes "rgRow" and "rgAltRow",
    specifically looking for tags with "hypBody", "AgendaPacket", or "Agenda" in their IDs.
    It aims to associate 'hypBody' tags directly with either 'AgendaPacket' or 'Agenda' based on their presence,
    updating the association if an 'AgendaPacket' is found after an 'Agenda'.
    """

    soup = BeautifulSoup(html_content, 'html.parser')
    
    #print("Soup object created. Starting to parse 'a' tags...")

    all_titles = [] 
    all_hrefs = []  

    tr_tags = soup.find_all("tr", class_=["rgRow", "rgAltRow"])
    
    for tr in tr_tags:
        hypBody_title = None
        hypBody_href = None
        
        a_tags = tr.find_all("a")

        for a in a_tags:

            # Check for "hypBody" and capture its text and href
            if "hypBody" in a.get("id", ""):
                hypBody_title = a.text.strip()  # Capture the title
                hypBody_href = "no Agenda"  # Default href value
                       
            # Update href if "AgendaPacket" or "Agenda" is found
            if "AgendaPacket" in a.get("id", "") and hypBody_title:
                hypBody_href = a.get("href")

            elif "Agenda" in a.get("id", "") and hypBody_title and hypBody_href == "no Agenda":
                hypBody_href = a.get("href")

        # After processing all 'a' tags in the row, append the results
        if hypBody_title:
            all_titles.append(hypBody_title)
            all_hrefs.append(hypBody_href)

    # make sure the lengths are the same
    #assert len(all_titles) == len(all_hrefs), "Lengths of titles and hrefs are not the same"
            
    print("Parsing complete")
    return all_titles, all_hrefs 


def filter_legistar_commissions(commissions):
    """
    This function filters a list of commissions to only include those with names, if none are present replace with a default value.
    """

    filtered_commissions = [
    item for item in commissions 
    if item['commission_name'] and ("plann" in item['commission_name'].lower() or "hous" in item['commission_name'].lower())]
    
    print("Commissions filtered")

    return filtered_commissions


def remove_no_agenda_link(commissions):
    """
    This function filters a list of commissions to only include those with names, if none are present replace with a default value.
    """
    filtered_commissions = [
    item for item in commissions 
    if item['agenda_link'] != "No Agenda Link Available"]
    
    print("Commissions filtered")

    return filtered_commissions


def filter_primegov_commissions(commissions):
    """
    This function filters a list of commissions to only include those with names, if none are present replace with a default value.
    """
    filtered_commissions = [
    item for item in commissions 
    if item['commission_name'] and ("plann" in item['commission_name'].lower() or "hous" in item['commission_name'].lower())]
    
    print("Commissions filtered")

    return filtered_commissions


def create_df(city_name, titles, hrefs, dates):
    lengths = min(len(titles), len(hrefs))
    data = {"City": [city_name] * lengths, "commission_name": titles[:lengths], "agenda_link": hrefs[:lengths]}
    return pd.DataFrame(data)


def append_prefix_to_agenda_link(extracted_data, city_name):
    prefix_link = city_website_prefix_links.get(city_name, "")
    for item in extracted_data:
        
        if item.get('agenda_link') is not None:
            item['agenda_link'] = prefix_link + item['agenda_link']
        else:
           
            item['agenda_link'] = "No Agenda Link Available"  # or "No agenda link available"

    return extracted_data


async def ascrape_legistar_playwright(city_name, url, tags: list[str]):
    print(f"Started scraping {city_name}...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        print(f"Scraping {city_name}...")
        page_source = await page.content()
        titles, hrefs = extract_legistar_tags(page_source)
        print(f"Scraping {city_name} complete")
        time.sleep(1)
        df = create_df(city_name, titles, hrefs)
        await browser.close()
    return df


###################### Prime Gov ############################


def extract_primegov_tags(html_content, tags: list[str]):
    """
    This takes in HTML content and a list of tags, and returns a string
    containing the text content of all elements with those tags, along with their href attribute if the
    tag is an "a" tag.
    """
    
    soup = BeautifulSoup(html_content, 'html.parser')

    # Generate Lists to return the titles of commissions and href links
    all_titles = []
    all_hrefs = []

    # Iterate through each tag in the list defined in the arguments
    for tag in tags:

        # Find all elements with the tag
        elements = soup.find_all(tag)

        # For all elements found within the tag, iterate through each element
        for element in elements:

            print(element.get_text())

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

    # make sure the lengths are the same
        #assert len(all_titles) == len(all_hrefs), "Lengths of titles and hrefs are not the same"
        #assert len(all_titles) == len(all_dates), "Lengths of titles and dates are not the same"

    return all_titles, all_hrefs


def create_df(city_name, titles, hrefs):
    lengths = min(len(titles), len(hrefs))
    data = {"City": [city_name] * lengths, "commission_name": titles[:lengths], "agenda_link": hrefs[:lengths]}
    return pd.DataFrame(data)


def append_prefix_to_agenda_link(extracted_data, city_name):

    prefix_link = city_website_prefix_links.get(city_name, "")

    for item in extracted_data:
        # Check if 'agenda_link' exists and is not None before concatenating
        if item.get('agenda_link') is not None:
            item['agenda_link'] = prefix_link + item['agenda_link']

        else:
            # Handle the case where 'agenda_link' is missing or None. 
            # Decide on appropriate action, such as setting a default value, skipping, or logging.
            # For example, setting a default value or placeholder (adjust as needed):
            item['agenda_link'] = "No Agenda Link Available"  # or "No agenda link available"

    return extracted_data


def filter_primegov_commissions(commissions):
    """
    This function filters a list of commissions to only include those with names, if none are present replace with a default value.
    """
    filtered_commissions = [
    item for item in commissions 
    if item['commission_name'] and ("plann" in item['commission_name'].lower() or "hous" in item['commission_name'].lower())]
    
    print("Commissions filtered")

    return filtered_commissions


async def wait_for_selectors_with_retry(page, selectors, retries=3, delay=2):
    """
    Wait for multiple selectors, retrying with a delay if not found.

    :param page: Playwright page object.
    :param selectors: List of selector strings to wait for.
    :param retries: Number of retry attempts.
    :param delay: Delay between retries in seconds.
    """

    for attempt in range(retries):
        try:
            await asyncio.gather(*(page.wait_for_selector(selector) for selector in selectors))
            return  # If all selectors are found, exit the function
        except TimeoutError:
            if attempt < retries - 1:  # Don't wait after the last attempt
                print(f"Selector not found, retrying... (Attempt {attempt + 1} of {retries})")
                await asyncio.sleep(delay)
            else:
                raise  # Re-raise the exception if all retries fail


async def ascrape_primegov_playwright(city_name, url, tags: list[str]):
    #print(f"Started scraping {city_name}...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        print(f"Scraping {city_name}...")
        page_source = await page.content()
        titles, hrefs = extract_primegov_tags(page_source, tags)
        print(f"Scraping {city_name} complete")
        time.sleep(2)
        df = create_df(city_name, titles, hrefs)
        await browser.close()
    
    return df


"""
async def ascrape_primegov_playwright(city, url, selectors):
    print(f"Scraping {city}...")

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        # Replace direct wait_for_selectors calls with the retry function
        await wait_for_selectors_with_retry(page, selectors, retries=3, delay=2)

        # Wait for all the tags to appear in the page. Assuming tags are CSS selectors
        for tag in tags:
            await page.wait_for_selector(tag, state="attached")

        # Once all elements are loaded, proceed with extracting the content
        page_content = await page.content()
        titles, hrefs = extract_primegov_tags(page_content, tags)

        print(f"Scraping {city} complete")
        await asyncio.sleep(2)

        # create a dataframe from the extracted data
        df = create_df(city, titles, hrefs)
        await browser.close()
    return df
"""