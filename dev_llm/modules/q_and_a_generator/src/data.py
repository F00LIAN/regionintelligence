import selenium 
# Import driver configuration
import time
import numpy as np
from src.driver_config import get_chrome_driver, navigate_and_print_title

from src.const import CALIFORNIA_UPCODES_URL, LOS_ANGELES_UPCODES_URL, LOS_ANGELES_COUNTY_UPCODES_URL, SAN_FRANCISCO_UPCODES_URL, SAN_JOSE_UPCODES_URL
from src.paths import RAW_DATA_DIR, PROCESSED_DATA_DIR

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os
from datetime import datetime

# Scrape California Codes
class CaliforniaUpCodesScraper:
    def __init__(self, base_url):
        self.driver = get_chrome_driver()
        self.base_url = base_url
        
    def navigate_and_get_title(self):
        print(f"Navigating to {self.base_url}...")
        navigate_and_print_title(self.driver, self.base_url)

    def extract_links_from_main(self, css_selector):
        print("Extracting main links...")
        main = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        time.sleep(1)
        links = main.find_elements(By.CSS_SELECTOR, ".group.font-inter")
        extracted_links = [link.get_attribute("href") for link in links]
        print(f"Extracted {len(extracted_links)} links from main page.")
        return extracted_links

    def extract_text_from_sublinks(self, urls):
        timestamp_str = datetime.now().strftime("%Y%m%d")
        self.output_file_path = RAW_DATA_DIR / 'california_building_codes' / f"california_{timestamp_str}.txt"
        section_div = []
        for index, url in enumerate(urls):
            print(f"Processing URL {index + 1}/{len(urls)}: {url}")
            self.driver.get(url)
            elements = self.driver.find_elements(By.CSS_SELECTOR, "a.block.w-full")
            sublinks = [element.get_attribute("href") for element in elements]
            
            for sublink in sublinks:
                self.driver.get(sublink)
                elements = self.driver.find_elements(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div/main/div[1]/div/div[2]")
                new_sections = [element.text for element in elements]
                if new_sections:
                    print(f"Extracted {len(new_sections)} section(s) from {sublink}")
                else:
                    print(f"No sections extracted from {sublink}. This might indicate a scraping issue.")
                section_div.extend(new_sections)
                self._print_sections(new_sections)
            
            #self._save_sections_to_file(section_div, index)
        #self._combine_files(len(urls))
        self._save_all_sections_to_file(section_div)
        
    def _print_sections(self, sections):
        print("Printing extracted sections...")

    def _save_all_sections_to_file(self, sections):
        print(f"Saving data to {self.output_file_path}...")
        with open(self.output_file_path, "w", encoding="utf-8") as f:
            for section in sections:
                f.write(section + "\n\n")
        print("Data saved successfully!")
                
    def _combine_files(self, num_files):
        timestamp_str = datetime.now().strftime("%Y%m%d")
        directory_path = str(RAW_DATA_DIR / 'california_building_codes')
        output_file_path = os.path.join(directory_path, f"california_{timestamp_str}.txt")
        
        with open(output_file_path, "w", encoding="utf-8") as outfile:
            for i in range(num_files):
                file_path = os.path.join(directory_path, f"testing{i}.txt")
                
                if not os.path.exists(file_path):
                    print(f"File {file_path} does not exist. Skipping.")
                    continue
                
                with open(file_path, "r", encoding="utf-8") as infile:
                    outfile.write(infile.read())
                    
        print(f"Combined file saved to {output_file_path}")
    
    def close(self):
        print("Closing the browser...")
        self.driver.quit()
        print("Browser closed successfully!")

def main_california_upcodes():
    scraper = CaliforniaUpCodesScraper(CALIFORNIA_UPCODES_URL)
    scraper.navigate_and_get_title()
    urls = scraper.extract_links_from_main("div.flex.flex-row")
    scraper.extract_text_from_sublinks(urls)
    scraper.close()

# Scrape Los Angeles Codes
class LosAngelesUpCodesScraper:
    def __init__(self, base_url):
        self.driver = get_chrome_driver()
        self.base_url = base_url
        
    def navigate_and_get_title(self):
        print(f"Navigating to {self.base_url}...")
        navigate_and_print_title(self.driver, self.base_url)

    def extract_links_from_main(self, css_selector):
        print("Extracting main links...")
        main = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        time.sleep(1)
        links = main.find_elements(By.CSS_SELECTOR, ".group.font-inter")
        extracted_links = [link.get_attribute("href") for link in links]
        print(f"Extracted {len(extracted_links)} links from main page.")
        return extracted_links

    def extract_text_from_sublinks(self, urls):
        timestamp_str = datetime.now().strftime("%Y%m%d")
        self.output_file_path = RAW_DATA_DIR / 'los_angeles_building_codes' / f"los_angeles_{timestamp_str}.txt"
        section_div = []
        for index, url in enumerate(urls):
            print(f"Processing URL {index + 1}/{len(urls)}: {url}")
            self.driver.get(url)
            elements = self.driver.find_elements(By.CSS_SELECTOR, "a.block.w-full")
            sublinks = [element.get_attribute("href") for element in elements]
            
            for sublink in sublinks:
                self.driver.get(sublink)
                elements = self.driver.find_elements(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div/main/div[1]/div/div[2]")
                new_sections = [element.text for element in elements]
                if new_sections:
                    print(f"Extracted {len(new_sections)} section(s) from {sublink}")
                else:
                    print(f"No sections extracted from {sublink}. This might indicate a scraping issue.")
                section_div.extend(new_sections)
                self._print_sections(new_sections)
            
            #self._save_sections_to_file(section_div, index)
        #self._combine_files(len(urls))
        self._save_all_sections_to_file(section_div)
        
    def _print_sections(self, sections):
        print("Printing extracted sections...")

    def _save_all_sections_to_file(self, sections):
        print(f"Saving data to {self.output_file_path}...")
        with open(self.output_file_path, "w", encoding="utf-8") as f:
            for section in sections:
                f.write(section + "\n\n")
        print("Data saved successfully!")
                
    def _combine_files(self, num_files):
        timestamp_str = datetime.now().strftime("%Y%m%d")
        directory_path = str(RAW_DATA_DIR / 'los_angeles_building_codes')
        output_file_path = os.path.join(directory_path, f"los_angeles_{timestamp_str}.txt")
        
        with open(output_file_path, "w", encoding="utf-8") as outfile:
            for i in range(num_files):
                file_path = os.path.join(directory_path, f"testing{i}.txt")
                
                if not os.path.exists(file_path):
                    print(f"File {file_path} does not exist. Skipping.")
                    continue
                
                with open(file_path, "r", encoding="utf-8") as infile:
                    outfile.write(infile.read())
                    
        print(f"Combined file saved to {output_file_path}")
    
    def close(self):
        print("Closing the browser...")
        self.driver.quit()
        print("Browser closed successfully!")

def main_los_angeles_upcodes():
    scraper = LosAngelesUpCodesScraper(LOS_ANGELES_UPCODES_URL)
    scraper.navigate_and_get_title()
    urls = scraper.extract_links_from_main("div.flex.flex-row")
    scraper.extract_text_from_sublinks(urls)
    scraper.close()

# Scrape Los Angeles County Codes
class LosAngelesCountyUpCodesScraper:
    def __init__(self, base_url):
        self.driver = get_chrome_driver()
        self.base_url = base_url
        
    def navigate_and_get_title(self):
        print(f"Navigating to {self.base_url}...")
        navigate_and_print_title(self.driver, self.base_url)

    def extract_links_from_main(self, css_selector):
        print("Extracting main links...")
        main = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        time.sleep(1)
        links = main.find_elements(By.CSS_SELECTOR, ".group.font-inter")
        extracted_links = [link.get_attribute("href") for link in links]
        print(f"Extracted {len(extracted_links)} links from main page.")
        return extracted_links

    def extract_text_from_sublinks(self, urls):
        timestamp_str = datetime.now().strftime("%Y%m%d")
        self.output_file_path = RAW_DATA_DIR / 'los_angeles_county_building_codes' / f"los_angeles_county_{timestamp_str}.txt"
        section_div = []
        for index, url in enumerate(urls):
            print(f"Processing URL {index + 1}/{len(urls)}: {url}")
            self.driver.get(url)
            elements = self.driver.find_elements(By.CSS_SELECTOR, "a.block.w-full")
            sublinks = [element.get_attribute("href") for element in elements]
            
            for sublink in sublinks:
                self.driver.get(sublink)
                elements = self.driver.find_elements(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div/main/div[1]/div/div[2]")
                new_sections = [element.text for element in elements]
                if new_sections:
                    print(f"Extracted {len(new_sections)} section(s) from {sublink}")
                else:
                    print(f"No sections extracted from {sublink}. This might indicate a scraping issue.")
                section_div.extend(new_sections)
                self._print_sections(new_sections)
            
            #self._save_sections_to_file(section_div, index)
        #self._combine_files(len(urls))
        self._save_all_sections_to_file(section_div)
        
    def _print_sections(self, sections):
        print("Printing extracted sections...")

    def _save_all_sections_to_file(self, sections):
        print(f"Saving data to {self.output_file_path}...")
        with open(self.output_file_path, "w", encoding="utf-8") as f:
            for section in sections:
                f.write(section + "\n\n")
        print("Data saved successfully!")
                
    def _combine_files(self, num_files):
        timestamp_str = datetime.now().strftime("%Y%m%d")
        directory_path = str(RAW_DATA_DIR / 'los_angeles_county_building_codes')
        output_file_path = os.path.join(directory_path, f"los_angeles_county_{timestamp_str}.txt")
        
        with open(output_file_path, "w", encoding="utf-8") as outfile:
            for i in range(num_files):
                file_path = os.path.join(directory_path, f"testing{i}.txt")
                
                if not os.path.exists(file_path):
                    print(f"File {file_path} does not exist. Skipping.")
                    continue
                
                with open(file_path, "r", encoding="utf-8") as infile:
                    outfile.write(infile.read())
                    
        print(f"Combined file saved to {output_file_path}")
    
    def close(self):
        print("Closing the browser...")
        self.driver.quit()
        print("Browser closed successfully!")

def main_los_angeles_county_upcodes():
    scraper = LosAngelesCountyUpCodesScraper(LOS_ANGELES_COUNTY_UPCODES_URL)
    scraper.navigate_and_get_title()
    urls = scraper.extract_links_from_main("div.flex.flex-row")
    scraper.extract_text_from_sublinks(urls)
    scraper.close()

# Scrape San Francisco Codes

class SanFranciscoUpCodesScraper:
    def __init__(self, base_url):
        self.driver = get_chrome_driver()
        self.base_url = base_url
        
    def navigate_and_get_title(self):
        print(f"Navigating to {self.base_url}...")
        navigate_and_print_title(self.driver, self.base_url)

    def extract_links_from_main(self, css_selector):
        print("Extracting main links...")
        main = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        time.sleep(1)
        links = main.find_elements(By.CSS_SELECTOR, ".group.font-inter")
        extracted_links = [link.get_attribute("href") for link in links]
        print(f"Extracted {len(extracted_links)} links from main page.")
        return extracted_links

    def extract_text_from_sublinks(self, urls):
        timestamp_str = datetime.now().strftime("%Y%m%d")
        self.output_file_path = RAW_DATA_DIR / 'san_francisco_building_codes' / f"san_francisco_{timestamp_str}.txt"
        section_div = []
        for index, url in enumerate(urls):
            print(f"Processing URL {index + 1}/{len(urls)}: {url}")
            self.driver.get(url)
            elements = self.driver.find_elements(By.CSS_SELECTOR, "a.block.w-full")
            sublinks = [element.get_attribute("href") for element in elements]
            
            for sublink in sublinks:
                self.driver.get(sublink)
                elements = self.driver.find_elements(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div/main/div[1]/div/div[2]")
                new_sections = [element.text for element in elements]
                if new_sections:
                    print(f"Extracted {len(new_sections)} section(s) from {sublink}")
                else:
                    print(f"No sections extracted from {sublink}. This might indicate a scraping issue.")
                section_div.extend(new_sections)
                self._print_sections(new_sections)
            
            #self._save_sections_to_file(section_div, index)
        #self._combine_files(len(urls))
        self._save_all_sections_to_file(section_div)
        
    def _print_sections(self, sections):
        print("Printing extracted sections...")

    def _save_all_sections_to_file(self, sections):
        print(f"Saving data to {self.output_file_path}...")
        with open(self.output_file_path, "w", encoding="utf-8") as f:
            for section in sections:
                f.write(section + "\n\n")
        print("Data saved successfully!")
                
    def _combine_files(self, num_files):
        timestamp_str = datetime.now().strftime("%Y%m%d")
        directory_path = str(RAW_DATA_DIR / 'san_francisco_building_codes')
        output_file_path = os.path.join(directory_path, f"san_francisco_{timestamp_str}.txt")
        
        with open(output_file_path, "w", encoding="utf-8") as outfile:
            for i in range(num_files):
                file_path = os.path.join(directory_path, f"testing{i}.txt")
                
                if not os.path.exists(file_path):
                    print(f"File {file_path} does not exist. Skipping.")
                    continue
                
                with open(file_path, "r", encoding="utf-8") as infile:
                    outfile.write(infile.read())
                    
        print(f"Combined file saved to {output_file_path}")
    
    def close(self):
        print("Closing the browser...")
        self.driver.quit()
        print("Browser closed successfully!")

def main_san_francisco_upcodes():
    scraper = SanFranciscoUpCodesScraper(SAN_FRANCISCO_UPCODES_URL)
    scraper.navigate_and_get_title()
    urls = scraper.extract_links_from_main("div.flex.flex-row")
    scraper.extract_text_from_sublinks(urls)
    scraper.close()

# Scrape San Jose Codes

class SanJoseUpCodesScraper:
    def __init__(self, base_url):
        self.driver = get_chrome_driver()
        self.base_url = base_url
        
    def navigate_and_get_title(self):
        print(f"Navigating to {self.base_url}...")
        navigate_and_print_title(self.driver, self.base_url)

    def extract_links_from_main(self, css_selector):
        print("Extracting main links...")
        main = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        time.sleep(1)
        links = main.find_elements(By.CSS_SELECTOR, ".group.font-inter")
        extracted_links = [link.get_attribute("href") for link in links]
        print(f"Extracted {len(extracted_links)} links from main page.")
        return extracted_links

    def extract_text_from_sublinks(self, urls):
        timestamp_str = datetime.now().strftime("%Y%m%d")
        self.output_file_path = RAW_DATA_DIR / 'san_jose_building_codes' / f"san_jose_{timestamp_str}.txt"
        section_div = []
        for index, url in enumerate(urls):
            print(f"Processing URL {index + 1}/{len(urls)}: {url}")
            self.driver.get(url)
            elements = self.driver.find_elements(By.CSS_SELECTOR, "a.block.w-full")
            sublinks = [element.get_attribute("href") for element in elements]
            
            for sublink in sublinks:
                self.driver.get(sublink)
                elements = self.driver.find_elements(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div/main/div[1]/div/div[2]")
                new_sections = [element.text for element in elements]
                if new_sections:
                    print(f"Extracted {len(new_sections)} section(s) from {sublink}")
                else:
                    print(f"No sections extracted from {sublink}. This might indicate a scraping issue.")
                section_div.extend(new_sections)
                self._print_sections(new_sections)
            
            #self._save_sections_to_file(section_div, index)
        #self._combine_files(len(urls))
        self._save_all_sections_to_file(section_div)
        
    def _print_sections(self, sections):
        print("Printing extracted sections...")

    def _save_all_sections_to_file(self, sections):
        print(f"Saving data to {self.output_file_path}...")
        with open(self.output_file_path, "w", encoding="utf-8") as f:
            for section in sections:
                f.write(section + "\n\n")
        print("Data saved successfully!")
                
    def _combine_files(self, num_files):
        timestamp_str = datetime.now().strftime("%Y%m%d")
        directory_path = str(RAW_DATA_DIR / 'san_jose_building_codes')
        output_file_path = os.path.join(directory_path, f"san_jose_{timestamp_str}.txt")
        
        with open(output_file_path, "w", encoding="utf-8") as outfile:
            for i in range(num_files):
                file_path = os.path.join(directory_path, f"testing{i}.txt")
                
                if not os.path.exists(file_path):
                    print(f"File {file_path} does not exist. Skipping.")
                    continue
                
                with open(file_path, "r", encoding="utf-8") as infile:
                    outfile.write(infile.read())
                    
        print(f"Combined file saved to {output_file_path}")
    
    def close(self):
        print("Closing the browser...")
        self.driver.quit()
        print("Browser closed successfully!")
    
def main_san_jose_upcodes():
    scraper = SanJoseUpCodesScraper(SAN_JOSE_UPCODES_URL)
    scraper.navigate_and_get_title()
    urls = scraper.extract_links_from_main("div.flex.flex-row")
    scraper.extract_text_from_sublinks(urls)
    scraper.close()