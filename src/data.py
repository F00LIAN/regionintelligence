import time
import numpy as np
import pandas as pd
import re

from src.driver_config import get_chrome_driver, navigate_and_print_title
from src.const import SANTA_ANA_PLANNING_OFFICE_NAME, SANTA_ANA_PLANNING_URL, SANTA_ANA_PLANNING_OFFICE_EMAIL, SANTA_ANA_PLANNING_OFFICE_PHONE
from src.paths import RAW_DATA_DIR, PROCESSED_DATA_DIR

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from pathlib import Path
from datetime import datetime, timedelta
import requests
from pdb import set_trace as stop
import numpy as np
import pandas as pd
import pdfplumber
import glob
from tqdm import tqdm


class SantaAnaScraper:
    def __init__(self, driver):
        self.driver = driver
        self.listing_names = []
        self.project_locations = []
        self.planner_leads = []
        self.property_owner = []
        self.project_status = []
        self.project_descriptions = []
        self.contact_information = []
        self.last_project_update = []
        self.all_images_urls = []
        self.df = None

    def connect(self, url):
        self.driver.get(url)
        print(self.driver.title)

    def scrape_base_directory(self):
        try:
            main = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#projectList"))
            )
            self._scrape_titles(main)
            self._scrape_addresses(main)
            self._scrape_applicants(main)
            self._scrape_owners(main)
            self._scrape_status(main)
        finally:
            pass

    def _scrape_titles(self, main):
        titles = main.find_elements(By.CSS_SELECTOR, "#projectList tr td:first-of-type")
        for title in titles:
            self.listing_names.append(title.text)

    def _scrape_addresses(self, main):
        addresses = main.find_elements(By.CSS_SELECTOR, "#projectList tr td:nth-of-type(2)")
        for address in addresses:
            self.project_locations.append(address.text)

    def _scrape_applicants(self, main):
        applicants = main.find_elements(By.CSS_SELECTOR, "#projectList tr td:nth-of-type(3)")
        for applicant in applicants:
            self.planner_leads.append(applicant.text)

    def _scrape_owners(self, main):
        owners = main.find_elements(By.CSS_SELECTOR, "#projectList tr td:nth-of-type(4)")
        for owner in owners:
            self.property_owner.append(owner.text)

    def _scrape_status(self, main):
        status = main.find_elements(By.CSS_SELECTOR, "#projectList tr td:nth-of-type(5)")
        for stats in status:
            self.project_status.append(stats.text)

    def scrape_detailed_info(self):
        for link in self.listing_names:
            link = link.strip()
            link = self.driver.find_element(By.LINK_TEXT, link)
            self.driver.execute_script("arguments[0].scrollIntoView();", link)
            link.click()
            self._scrape_project_details()
            self.driver.back()

    def _scrape_project_details(self):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".so-widget-sow-editor.so-widget-sow-editor-base")
                )
            )
            self._scrape_project_description(element)
            self._scrape_contact_info(element)
            self._scrape_last_updated(element)
            self._scrape_image_urls()
        finally:
            pass

    def _scrape_project_description(self, element):
        try:
            description = element.find_element(By.CSS_SELECTOR, "ul:first-of-type li:first-child")
            self.project_descriptions.append(description.text)
        except:
            self.project_descriptions.append("NA")

    def _scrape_contact_info(self, element):
        try:
            contact_info = element.find_element(By.CSS_SELECTOR, "p")
            self.contact_information.append(contact_info.text)
        except:
            self.contact_information.append("NA")

    def _scrape_last_updated(self, element):
        try:
            last_updated = element.find_element(By.CSS_SELECTOR, "p > em")
            self.last_project_update.append(last_updated.text)
        except:
            self.last_project_update.append("NA")

    def _scrape_image_urls(self):
        image_url = None
        # Locate div elements
        div_elements = self.driver.find_elements(
            By.CSS_SELECTOR, "div.siteorigin-widget-tinymce.textwidget"
        )

        for div in div_elements:
            image_urls = []
            try:
                # Locate every img tag that is inside a p element following an a tag within the current div
                images_in_div = div.find_elements(By.CSS_SELECTOR, "p a img")

                # Extract the src attribute of each img tag found
                for img in images_in_div:
                    image_url = img.get_attribute("src")
                    if image_url:
                        image_urls.append(image_url)
                    else:
                        image_urls.append("NA")
            except Exception as e:
                print("Exception occurred: ", e)
                image_urls.append("NA")

            self.all_images_urls.append(image_urls)
    
    def clean_data(self):
        if self.df is None:
            raise ValueError("DataFrame not yet created. Call create_dataframe first.")
        else:
        # Split the Planner/Manager column into name and the rest
            self.df[["name", "Rest"]] = self.df["planner"].str.split(
                "Phone:", expand=True
            )

            # Now split the rest into phone and email using re.split
            # Handle potential non-string (NaN) values in the 'Rest' column
            self.df["phone"], self.df["email"] = zip(
                *self.df["Rest"].apply(
                    lambda x: re.split("E-mail:|Email:", x)
                    if isinstance(x, str)
                    else (np.nan, np.nan)
                )
            )

            # Remove unnecessary strings
            self.df["name"] = (
                self.df["name"].str.replace("Project Manager:", "").str.strip()
            )
            self.df["phone"] = self.df["phone"].str.strip()
            self.df["email"] = self.df["email"].str.strip()
            self.df['city'] = 'Santa Ana'

        # Clean Emails that did not parse correctly. Using helper method. 
        def clean_email(value):  # Helper method for cleaning emails
            if isinstance(value, str):  # Check if value is a string
                potential_email = value.split('\n')[0]
                if "@" in potential_email and "." in potential_email:
                    return potential_email
                else:
                    return None
            else:
                return None  # Return None if value is not a string (like NaN)
            
        self.df["email"] = self.df["email"].apply(clean_email)

        # Drop the 'Rest' and 'Planner/Manager' columns as they are not needed anymore
        self.df.drop(["Rest", "planner"], axis=1, inplace=True)

            # Group by 'Name', then fill missing 'Phone' and 'Email' with the mode value in each group
        self.df["phone"] = self.df.groupby("name")["phone"].transform(
                lambda x: x.fillna(x.mode().iloc[0] if not x.mode().empty else "Unknown")
            )
        self.df["email"] = self.df.groupby("name")["email"].transform(
                lambda x: x.fillna(x.mode().iloc[0] if not x.mode().empty else "Unknown")
            )

    def save_to_raw(self, file_name_prefix="santa-ana-current-projects"):
        """
        Save the DataFrame to an Excel file in the RAW_DATA_DIR / 'santana' directory.
        The saved file name will be in the format: [file_name_prefix]_YYYY-MM-DD.xlsx
        :param file_name_prefix: Prefix of the Excel file.
        """
        current_date = datetime.now().strftime('%Y-%m-%d')
        file_name = f"{file_name_prefix}_{current_date}.xlsx"
        path = RAW_DATA_DIR / 'santana' / file_name
        self.df.to_excel(path, header=True)

    def create_dataframe(self):
        self.df = pd.DataFrame(
            {
                "projectName": self.listing_names,
                "address": self.project_locations,
                "applicantName": self.planner_leads,
                "owner": self.property_owner,
                "imageURL": self.all_images_urls,
                "status": self.project_status,
                "description": self.project_descriptions,
                "planner": self.contact_information,
                "lastUpdate": self.last_project_update,
            }
        )
        return self.df
    
class SantaAnaPDFParser:

    def __init__(self, data_dir: Path = RAW_DATA_DIR):
        self.data_dir = data_dir

    def download_one_file_of_raw_data(self, year: int, month: str, monthint: int) -> Path:
        """
        Downloads PDF file with the given `year` and `month` from the specified URL
        """
        URL = f'https://storage.googleapis.com/proudcity/santaanaca/uploads/{year}/{monthint:02d}/{month}-{year}-DP-List.pdf'
        response = requests.get(URL)

        if response.status_code == 200:
            path = self.data_dir / 'santana' / f'santa_ana_approved_data_{year}-{month}.pdf'
            open(path, "wb").write(response.content)
            return path
        else:
            raise Exception(f'{URL} is not available')

    def get_last_six_months(self):
        today = datetime.today()
        months = [(today - timedelta(days=30 * x)).strftime('%B') for x in range(7)]
        monthints = [(today - timedelta(days=30 * x)).month + 1 for x in range(7)]
        years = [(today - timedelta(days=30 * x)).year for x in range(7)]
        return years, months, monthints

    def load_last_six_months_data(self):
        years, months, monthints = self.get_last_six_months()
        for year, month, monthint in zip(years, months, monthints):
            local_file = self.data_dir / 'santana' / f'santa_ana_approved_data_{year}-{month}.pdf'
            if local_file.exists():
                print(f'File for {month} {year} already exists in local storage.')
            else:
                try:
                    print(f'Downloading data for {month} {year}...')
                    self.download_one_file_of_raw_data(year, month, monthint)
                except Exception as e:
                    print(e)

    def parse_pdf_to_dataframe(self, pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            all_data = []
            for page in pdf.pages:
                data = page.extract_table()
                cleaned_data = [[cell.replace('\n', ' ') if cell else cell for cell in row] for row in data]
                all_data.extend(cleaned_data)

        all_data = self._merge_rows(all_data)
        header = all_data[1]
        df = pd.DataFrame(all_data[2:], columns=header)
        df = df.dropna(thresh=(len(df.columns) - 3))
        return df

    def parse_all_pdfs_in_directory(self, directory_path=None):
        if directory_path is None:
            directory_path = self.data_dir / 'santana'
        pdf_files = glob.glob(f"{directory_path}/*.pdf")
        dataframes = [self.parse_pdf_to_dataframe(pdf_file) for pdf_file in pdf_files]
        concatenated_df = pd.concat(dataframes, ignore_index=True)
        return concatenated_df
    
    def add_name_phone_email(self, df):
        df['name'] = SANTA_ANA_PLANNING_OFFICE_NAME
        df['phone'] = SANTA_ANA_PLANNING_OFFICE_PHONE
        df['email'] = SANTA_ANA_PLANNING_OFFICE_EMAIL
        df['imageURL'] = ''
        df['city'] = 'Santa Ana'
        return df
    
    def change_column_names(self, df):
        df.rename(columns={
                "Project Name": "projectName",
                "Applicant Name": "applicantName",
                "Property Owner Name": "owner",
                "Address and Council Ward": "address",
                "Application Type": "status",
                "Description": "description",
                "Date Accepted": "lastUpdate"}, inplace=True)
        return df
    
    def _merge_rows(self, data):
        merged_data = []
        previous_row = None
        
        def convert_empty_to_nan(row):
            return [cell if cell != '' else np.nan for cell in row]

        for row in data:
            row = convert_empty_to_nan(row)
            if row.count(None) + row.count(np.nan) >= len(row) - 2:
                if not previous_row:  # if previous_row is None, assign the current row to it
                    previous_row = row
                    continue
                merged_row = []
                for prev_cell, cell in zip(previous_row, row):
                    if cell is not np.nan:
                        merged_row.append(f"{prev_cell} {cell}")
                    else:
                        merged_row.append(prev_cell)
                previous_row = merged_row
            else:
                if previous_row:
                    merged_data.append(previous_row)
                    previous_row = None
                merged_data.append(row)

        if previous_row:  # Append the last row if not appended
            merged_data.append(previous_row)

        return merged_data
    
    def save_to_raw(self, df, file_name_prefix="santa-ana-approved"):
        """
        Save the DataFrame to an Excel file in the RAW_DATA_DIR / 'santana' directory.
        The saved file name will be in the format: [file_name_prefix]_YYYY-MM-DD.xlsx
        :param file_name_prefix: Prefix of the Excel file.
        """
        current_date = datetime.now().strftime('%Y-%m-%d')
        file_name = f"{file_name_prefix}_{current_date}.xlsx"
        path = RAW_DATA_DIR / 'santana' / file_name
        df.to_excel(path, header=True)
    

def concat_and_save_all_santa_ana_data():
    files = glob.glob(f"{RAW_DATA_DIR}/santana/*.xlsx")
    dfs = [pd.read_excel(file) for file in files]
    df = pd.concat(dfs, ignore_index=True)
    df.drop(columns=['Unnamed: 0'], inplace=True)

    # Save the data to the processed data directory
    current_date = datetime.now().strftime('%Y-%m-%d')
    file_name = f"santa_ana_data_{current_date}.xlsx"
    df.to_excel(PROCESSED_DATA_DIR / 'santaana' / file_name, header=True)


def main():
    """
    SANTA ANA
    """
    # Instantiate the Chrome driver
    driver = get_chrome_driver()
    scraper = SantaAnaScraper(driver)
    scraper.connect(SANTA_ANA_PLANNING_URL)
    scraper.scrape_base_directory()

    scraper.scrape_detailed_info()
    df = scraper.create_dataframe()
    scraper.clean_data()
    scraper.save_to_raw()
    driver.close()

    # Instantiate the PDF parser
    parser = SantaAnaPDFParser()
    parser.load_last_six_months_data()
    df = parser.parse_all_pdfs_in_directory()
    df = parser.add_name_phone_email(df)
    df = parser.change_column_names(df)
    parser.save_to_raw(df)

    # Concatenate all the data and save to processed data directory
    concat_and_save_all_santa_ana_data