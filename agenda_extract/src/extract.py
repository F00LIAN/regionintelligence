import pandas as pd
import json
import time
import requests
from requests.exceptions import ChunkedEncodingError
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from const import city_website_prefix_links
from paths import CONCAT_DIR, FINAL_DIR, PDF_PATH


def get_latest_data():
    """
    Extracts the latest data from the CONCAT directory and returns it as a DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the latest JSON data.
    """
    latest_file = sorted(CONCAT_DIR.glob('*.json'))[-1]
    with open(latest_file, 'r') as f:
        data = json.load(f)
    
    print(f"Loaded data from {latest_file}")
    
    return data


def fetch_html(url, retry_attempts=3):
    """
    Fetches the HTML content from a given URL.
    """
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP errors

    return response.text


def is_pdf_link(url):
    """
    Checks if the URL is a direct link to a PDF file.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if it's a PDF link, False otherwise.
    """
    parsed_url = urlparse(url)


    return parsed_url.path.lower().endswith('.pdf')


def download_pdf(url):
    """

    Attempts to download a PDF from a URL and saves it in the PDF directory.
    Includes retry logic for handling incomplete downloads.

    Args:
        url (str): The URL of the PDF to download.

    """
    filename = url.split('/')[-1]
    filepath = PDF_PATH / filename
    success = False
    attempts = 0
    max_attempts = 5  # Set the maximum number of retry attempts

    while not success and attempts < max_attempts:
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Check for HTTP errors

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # Filter out keep-alive chunks
                        f.write(chunk)
            success = True  # File downloaded successfully
        except ChunkedEncodingError as e:
            attempts += 1
            print(f"Attempt {attempts} failed: {e}. Retrying...")
            time.sleep(2)  # Wait a bit before retrying to avoid hammering the server
        except Exception as e:
            print(f"Failed to download PDF from {url}. Error: {e}")
            return None

    if success:
        return filepath
    else:
        print(f"Failed to download PDF after {max_attempts} attempts.")
        return None


def extract_links(html_content, city_name):
    """
    Extracts links containing '/api' from the given HTML content and appends the city prefix to them.

    Args:
        html_content (str): HTML content of a page.
        city_name (str): The name of the city to append the correct prefix to the links.

    Returns:
        list: A list of href values from <a> tags containing '/api', with city prefixes appended.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    city_prefix = city_website_prefix_links.get(city_name, "")
    api_links = [city_prefix + a['href'] for a in soup.find_all('a', href=True) if '/api' in a['href']]
    return api_links


def update_agenda_links_with_pdfs_and_details(data):
    """
    Updates the input JSON data structure with PDF links extracted from each agenda link
    and appends city prefixes to '/api' links extracted as project details.

    Args:
        data (dict): The original JSON data structure.

    Returns:
        dict: The updated JSON data structure with PDF links or project details.
    """
    for city, agendas in data.items():
        for agenda in agendas:
            agenda_link = agenda.get('agenda_link', '')
            print(agenda_link)
            if is_pdf_link(agenda_link):
                pdf_path = download_pdf(agenda_link)
                agenda['pdf_link'] = str(pdf_path) if pdf_path else "Failed to download"
                
            else:
                html_content = fetch_html(agenda_link)
                project_details = extract_links(html_content, city)
                agenda['project_details'] = project_details
        time.sleep(1)
    return data


def main_extract():
    """
    Main function to orchestrate the extraction and update process.
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    data = get_latest_data()
    updated_data = update_agenda_links_with_pdfs_and_details(data)

    # Optionally, save the updated data back to a JSON file
    output_path = FINAL_DIR / f"city_agendas_{current_date}_data.json"
    with open(output_path, 'w') as f:
        json.dump(updated_data, f, indent=4)

    
if __name__ == "__main__":
    main_extract()
