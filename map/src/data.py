import time
import numpy as np
import pandas as pd
import re
import os

from src.driver_config import get_chrome_driver, navigate_and_print_title

from src.const import (    
    SANTA_ANA_PLANNING_OFFICE_EMAIL, 
    FULLERTON_PLANNING_OFFICE_EMAIL,
    ANAHEIM_PLANNING_OFFICE_EMAIL,
    IRVINE_PLANNING_OFFICE_EMAIL,
    HUNTINGTON_BEACH_PLANNING_OFFICE_EMAIL,
    )

from src.const import (
    HUNTINGTON_BEACH_PLANNING_OFFICE_PHONE,
    ANAHEIM_PLANNING_OFFICE_PHONE,
    SANTA_ANA_PLANNING_OFFICE_PHONE,
    IRVINE_PLANNING_OFFICE_PHONE,
)

from src.const import (
    SANTA_ANA_PLANNING_URL,
    HUNTINGTON_BEACH_PLANNING_URL,
    GARDEN_GROVE_PLANNING_URL,
    ORANGE_PLANNING_URL,
    FULLERTON_PLANNING_URL,
    IRVINE_MAJOR_PLANNING_URL,
)
from src.const import (
    SANTA_ANA_PLANNING_OFFICE_NAME, 
    ANAHEIM_PLANNING_OFFICE_NAME,
    HUNTINGTON_BEACH_PLANNING_OFFICE_NAME,
    GARDEN_GROVE_PLANNING_OFFICE_NAME,
    IRVINE_PLANNING_OFFICE_NAME,

)

from src.const import (
    orange_planner_phones, 
    orange_planner_emails, 
    orange_planner_names, 
   
    fullerton_planner_names,
    fullerton_planner_phones,

    garden_grove_planner_emails,
    garden_grove_planner_names,
    garden_grove_planner_phones,

    hb_planner_emails,
    hb_planner_names,

    anaheim_planner_emails, 
    anaheim_planner_phones, 
    anaheim_planner_names, 

    )

from src.paths import RAW_DATA_DIR, PROCESSED_DATA_DIR, FINAL_DATA_DIR, COMPANY_DATA_DIR


from src.logger import get_console_logger
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import openpyxl

from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime, timedelta
import requests
from pdb import set_trace as stop
import numpy as np
import pandas as pd
import pdfplumber
import glob
from tqdm import tqdm
from difflib import SequenceMatcher


logger = get_console_logger()

# Santa Ana Scraper
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
                self.df["name"].str.replace("Assigned Planner:", "").str.strip()
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
        self.df.drop(["Rest"], axis=1, inplace=True)

            # Group by 'Name', then fill missing 'Phone' and 'Email' with the mode value in each group
        self.df["phone"] = self.df.groupby("name")["phone"].transform(
                lambda x: x.fillna(x.mode().iloc[0] if not x.mode().empty else SANTA_ANA_PLANNING_OFFICE_PHONE)
            )
        self.df["email"] = self.df.groupby("name")["email"].transform(
                lambda x: x.fillna(x.mode().iloc[0] if not x.mode().empty else SANTA_ANA_PLANNING_OFFICE_EMAIL)
            )
    
    
    def adjust_project_columns(self):
        self.df['planner'] = self.df['name']
        self.df.drop(columns=['name'], inplace=True)
        self.df['planner'].fillna(SANTA_ANA_PLANNING_OFFICE_NAME, inplace=True)

        
    def save_to_raw(self, file_name_prefix="santa-ana-current-projects"):
        """
        Save the DataFrame to an Excel file in the RAW_DATA_DIR / 'santana' directory.
        The saved file name will be in the format: [file_name_prefix]_YYYY-MM-DD.xlsx
        :param file_name_prefix: Prefix of the Excel file.

        THIS SAVES SANTA ANA'S CURRENT PROJECTS TO RAW DATA DIRECTORY
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
                "applicantName": self.property_owner,
                "imageURL": self.all_images_urls,
                "status": self.project_status,
                "description": self.project_descriptions,
                "planner": self.contact_information,
                "recentUpdate": self.last_project_update,
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
        df['planner'] = SANTA_ANA_PLANNING_OFFICE_NAME
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
                "Date Accepted": "recentUpdate"}, inplace=True)
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
        
        THIS SAVES SANTA ANA APPROVED DATA TO RAW DATA DIRECTORY
        """
        current_date = datetime.now().strftime('%Y-%m-%d')
        # Optional Save Owner information to company database

        # drop the owner column for production
        
        
        
        file_name = f"{file_name_prefix}_{current_date}.xlsx"
        path = RAW_DATA_DIR / 'santana' / file_name
        df.to_excel(path, header=True)
        return df


def concat_and_save_all_santa_ana_data():
    files = glob.glob(f"{RAW_DATA_DIR}/santana/*.xlsx")
    
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Form the file names using f-strings
    latest_approved = f"santa-ana-approved_{current_date}.xlsx"
    latest_projects = f"santa-ana-current-projects_{current_date}.xlsx"
    
    # Check if the files are in the list of files
    latest_approved = next((file for file in files if latest_approved in file), None)
    latest_projects = next((file for file in files if latest_projects in file), None)
    
    # If either of the latest files isn't found, return None
    if not latest_approved or not latest_projects:
        print("Unable to find latest Excel files for both prefixes.")
        return None

    # Load and concatenate the dataframes
    dfs = [pd.read_excel(latest_approved), pd.read_excel(latest_projects)]
    df = pd.concat(dfs, ignore_index=True)
    
    if 'Unnamed: 0' in df.columns:
        df.drop(columns=['Unnamed: 0'], inplace=True)
    
    # Assuming 'projectName' column exists and needs to be de-duplicated
    if 'projectName' in df.columns:
        df['projectName'].drop_duplicates(inplace=True)
    
    
    # save the data with the owner column to the company database
    # save the data with the applicant Name to the company database
    # Save the data to the processed data directory
    file_name = f"santa_ana_data_{current_date}.xlsx"
    path = Path(COMPANY_DATA_DIR) / 'santana' / file_name
    df.to_excel(path, header=True)

    # drop the applicantName column for production
    df.drop(columns=['owner'], inplace=True)
    df.drop(columns=['applicantName'], inplace=True)
    df.drop(columns=['imageURL'], inplace=True)

    # fill null values in planner column with Santa Ana Planning Office
    df['planner'].fillna(SANTA_ANA_PLANNING_OFFICE_NAME, inplace=True)

    # Save the data to the processed data directory
    file_name = f"santa_ana_data_{current_date}.xlsx"
    path = Path(PROCESSED_DATA_DIR) / 'santana' / file_name
    df.to_excel(path, header=True)
    
    return df


def main_santa_ana():
    """
    SANTA ANA
    """
    logger.info('Running Santa Ana scraper')
    # Instantiate the Chrome driver
    driver = get_chrome_driver()
    scraper = SantaAnaScraper(driver)
    scraper.connect(SANTA_ANA_PLANNING_URL)
    scraper.scrape_base_directory()

    scraper.scrape_detailed_info()
    df = scraper.create_dataframe()
    scraper.clean_data()
    scraper.adjust_project_columns()
    
    scraper.save_to_raw()
    driver.close()

    # Instantiate the PDF parser
    parser = SantaAnaPDFParser()
    parser.load_last_six_months_data()
    df = parser.parse_all_pdfs_in_directory()
    df = parser.add_name_phone_email(df)
    df = parser.change_column_names(df)
    parser.save_to_raw(df)

    logger.info('Concatenating and saving all Santa Ana data')
    concat_and_save_all_santa_ana_data()
    
    logger.info('Santa Ana scraper finished')
    return df

# City of Orange Scraper


class OrangeScraper:

    # Define current_date as a class variable
    current_date = datetime.now().strftime('%Y-%m-%d')

    def __init__(self, driver):
        self.driver = driver
        self.pdf_urls = []

    def connect(self, url):
        self.driver.get(url)
        print(self.driver.title)

    def scrape_pdf(self):
        try:
            accordion_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "accordion-heading"))
            )

            accordion_link.click()
            time.sleep(3)
            pdf_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Current Pending Land Use Applications List"))
            )
            time.sleep(3)
            pdf_link.click()
            time.sleep(3)
            pdf_url = pdf_link.get_attribute("href")
            self.pdf_urls.append(pdf_url)
            
        except Exception as e:
            print(f"An error occurred: {e}")

    def parse_orange_pdf(self, pdf_path=None):
        if not pdf_path:
            pdf_path = RAW_DATA_DIR / 'orange' / f'orange_city_data_{OrangeScraper.current_date}.pdf'
        time.sleep(3)    
        # Open the PDF
        with pdfplumber.open(pdf_path) as pdf:
            all_data = []
            
            for page in pdf.pages:
                data = page.extract_table()
                filtered_data = [ 
                    [row[1], row[3], row[4], row[5], ' '.join([str(cell) for cell in row[6:20] if cell is not None]), ' '.join([str(cell) for cell in row[22:27] if cell is not None])]
                    for row in data[1:]  # Skipping the header
                ]
                all_data.extend(filtered_data)

        # Convert the extracted data into a DataFrame
        columns = ['address', 'projectName', 'description', 'planner', 'status', 'recentUpdate/owner']
        df = pd.DataFrame(all_data, columns=columns)
        
        return df

    def download_pdf(self, directory):
        if not self.pdf_urls:
            print("No PDFs found to download!")
            return

        file_name = f"orange_city_data_{OrangeScraper.current_date}.pdf"
        orange_dir = os.path.join(directory, 'orange')
        if not os.path.exists(orange_dir):
            os.makedirs(orange_dir)

        for url in self.pdf_urls:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3'}
            response = requests.get(url, headers=headers, stream=True)

            # Check if the request was successful
            response.raise_for_status()

            with open(os.path.join(orange_dir, file_name), "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

        return os.path.join(orange_dir, file_name)

    
    def clean_orange_pdf(self, df):
        # Convert all None values to NaN
        df = df.where(pd.notna(df), None)

        # Drop rows where at least 4 columns are NaN
        df = df[df.apply(lambda x: x.isna().sum() < 3, axis=1)]

        # Cleaning operations
        df['status'] = df['status'].str.replace('\n', '', regex=False)
        
        for column in df.columns:
            if column != 'status':
                df[column] = df[column].str.replace('\n', ' ', regex=False)

        return df
    
    def move_text_from_status_to_planner(self, row):
        # Extract text other than "Pending" or "Approved"
        extraneous_text = re.sub(r'Pending|Approved', '', row['status']).strip()

        # If there's extraneous text and the planner is None, update the planner column
        if extraneous_text and (row['planner'] == 'None' or pd.isna(row['planner'])):
            row['planner'] = extraneous_text

        # Remove extraneous text from the status column
        row['status'] = row['status'].replace(extraneous_text, '').strip()

        # If status contains both "Pending" and "Approved", set it to "Pending"
        if "Approved" in row['status'] and "Pending" in row['status']:
            row['status'] = "Pending"
        elif "Pending" in row['status']:
            row['status'] = "Pending"
        elif "Approved" in row['status']:
            row['status'] = "Approved"
        else:
            row['status'] = "Denied"

        return row
    
    def process_plannernames(self, df):
        df = df.apply(self.move_text_from_status_to_planner, axis=1)
        def extract_planner_name(row):
            names_set = set(orange_planner_names.values()) # Set of all planner names
            for name in names_set:
                if name in row:
                    return name
            return None
        
        df['planner'] = df['planner'].apply(extract_planner_name)
        df['phone'] = df['planner'].map(orange_planner_phones)
        df['email'] = df['planner'].map(orange_planner_emails)
        return df
    
    def update_description_based_on_project(self, row):
        # If 'ADU' is in projectName and description is empty or NaN
        if "ADU" in str(row['projectName']) and (pd.isnull(row['description']) or row['description'] == ''):
            row['description'] = "Applicant has requested to build an ADU"
        return row

    def refine_drop_empty_name_rows(self, df):
        df = df.apply(self.update_description_based_on_project, axis=1)
        df = df[df['projectName'].astype(str).str.strip() != '']
        df = df[df['projectName'].astype(str).str.strip() != ' ']
        df = df.dropna(subset=['projectName'])
        return df
    
    def save_to_company_database(self, df, path=None):
        if not path:
            path = COMPANY_DATA_DIR / 'orange' / f'orange_city_data_{OrangeScraper.current_date}.xlsx'
        df.to_excel(path, index=False)
    
    def save_to_processed(self, df):
        # Use the class variable here
        file_name = f"orange_city_data_{OrangeScraper.current_date}.xlsx"
        path = PROCESSED_DATA_DIR / 'orange' / file_name
        df.to_excel(path, header=True)
    
    def extract_recent_date_and_owner(self, s):
        # Extract all dates in the format MM/DD/YYYY
        dates = re.findall(r'\d{1,2}/\d{1,2}/\d{4}', s)
        recent_date = None
        if dates:
            # Convert strings to datetime objects to find the most recent date
            recent_date = max(pd.to_datetime(dates)).strftime('%m/%d/%Y')
    
        # Assuming names are capitalized words. Extract them
        name_list = re.findall(r'\b[A-Z][a-z]+\b', s)
        owner = ' '.join(name_list[:2]) if name_list else None  # Considering first and last names only

        return recent_date, owner
    
    def process_recentUpdate_owner_column(self, df):
        # Apply the extraction function to the 'recentUpdate/owner' column
        df['recentUpdate'], df['owner'] = zip(*df['recentUpdate/owner'].apply(self.extract_recent_date_and_owner))
        
        # Drop the original 'recentUpdate/owner' column
        df.drop(columns=['recentUpdate/owner'], inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

def main_city_of_orange():
    """
    CITY OF ORANGE
    """
    logger.info('Running Orange scraper')
    # Instantiate the Chrome driver
    driver = get_chrome_driver()
    scraper = OrangeScraper(driver)
    scraper.connect(ORANGE_PLANNING_URL)
    scraper.scrape_pdf()
    pdf_path = scraper.download_pdf(RAW_DATA_DIR)
    df = scraper.parse_orange_pdf(pdf_path)
    df = scraper.clean_orange_pdf(df)
    df = scraper.refine_drop_empty_name_rows(df)
    df = scraper.process_plannernames(df)
    df = scraper.process_recentUpdate_owner_column(df)

    # add city column
    df['city'] = 'Orange'

    # Optional Save owner information to company database
    scraper.save_to_company_database(df)

    # drop the owner column 
    df.drop(columns=['owner'], inplace=True)
    

    scraper.save_to_processed(df)
    driver.close()
    logger.info('Orange scraper finished')
    return df

# City of Anaheim Scraper
class AnaheimScraper:

    current_date = datetime.now().strftime('%Y-%m-%d')

    def __init__(self):
        # Initializing some attributes
        self.current_projects_df = None
        self.current_applications_df = None
        self.driver = None

    @staticmethod
    def get_most_recent_file(path, file_startswith):
        list_of_files = [f for f in os.listdir(path) if f.startswith(file_startswith)]
        if not list_of_files:
            return None
        latest_file = max(list_of_files, key=lambda x: os.path.getctime(os.path.join(path, x)))
        return os.path.join(path, latest_file)

    def read_anaheim_csv(self):
        anaheim_path = self.get_most_recent_file(RAW_DATA_DIR / 'anaheim', 'AndysMap.csv')
        dev_apps_path = self.get_most_recent_file(RAW_DATA_DIR / 'anaheim', 'dev_apps.csv')
        if not anaheim_path or not dev_apps_path:
            raise Exception("Couldn't find the required files!")
        self.current_projects_df = pd.read_csv(anaheim_path)
        self.current_applications_df = pd.read_csv(dev_apps_path)

    def process_the_dataframe(self, df):
        if 'Staff Name' in df.columns:
            df['email'] = df['Staff Name'].map(anaheim_planner_emails)
            df['phone'] = df['Staff Name'].map(anaheim_planner_phones)
            df['planner'] = df['Staff Name'].map(anaheim_planner_names) 
            df['email'].fillna(ANAHEIM_PLANNING_OFFICE_EMAIL, inplace=True)
            df['phone'].fillna(ANAHEIM_PLANNING_OFFICE_PHONE, inplace=True)
            df['planner'] = df['planner'].fillna(ANAHEIM_PLANNING_OFFICE_NAME)
        else:
            df['email'] = ANAHEIM_PLANNING_OFFICE_EMAIL
            df['phone'] = ANAHEIM_PLANNING_OFFICE_PHONE
            df['planner'] = ANAHEIM_PLANNING_OFFICE_NAME
        df.rename(columns={
            'Address': 'address',
            'Description': 'description',
            'Application Name': 'projectName',
            'Type of Use': 'typeOfUse',
            'Case Status': 'status',
            'Applicant': 'owner',
            'Opened Date': 'recentUpdate'
        }, inplace=True)
        df['city'] = 'Anaheim'
        df = df[['address', 'description', 'projectName', 'typeOfUse', 'status', 'owner', 'recentUpdate', 'email', 'phone', 'city', 'planner']]
        #df['projectName'] = df['projectName'].apply(lambda x: re.sub(r'\[.*?\]\s*', '', x))

        # Optional Save owner information to company database
        path = COMPANY_DATA_DIR / 'anaheim' / f'anaheim_city_data_{AnaheimScraper.current_date}.xlsx'
        df.to_excel(path, index=False)

        df.drop(columns=['owner'], inplace=True)
        return df
    
    def save_to_processed(self, df, path):   
        df.to_excel(path, header=True)

    def run(self):

        # define the path and file name
        file_name = f"anaheim_city_data_{AnaheimScraper.current_date}.xlsx"
        path = PROCESSED_DATA_DIR / 'anaheim' / file_name

        # Reads the CSV
        self.read_anaheim_csv()

        # Processes the first dataframe
        self.current_projects_df = self.process_the_dataframe(self.current_projects_df)
        self.save_to_processed(self.current_projects_df, path)
        
        # (Optional) Processes the second dataframe, etc.

        # Returns the processed dataframe for further operations or analysis
        return self.current_projects_df


def main_anaheim():
    """
    CITY OF ANAHEIM
    """
    logger.info('Running Anaheim scraper')
    scraper = AnaheimScraper()
    df = scraper.run()
    logger.info('Anaheim scraper finished')
    return df



# City of Fullertron Scraper


class FullertonScraper:

    # Define current_date as a class variable
    current_date = datetime.now().strftime('%Y-%m-%d')

    def __init__(self, driver):
        self.driver = driver
        self.heading_name = []
        self.listing_names = []
        self.case_number_texts = []
        self.project_locations = []
        self.type_of_use = []
        self.planner_leads = []
        self.project_descriptions = []
        self.project_status = []
        self.image_urls = []

    def connect(self, url):
        self.driver.get(url)
        print(self.driver.title)

    def scrape_data(self):
        time.sleep(3)
        try:
            main = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "govAccess-reTable-4"))
            )

            headers = main.find_elements(By.CSS_SELECTOR, "tr:first-of-type td")
            for header in headers:
                self.heading_name.append(header.text)

            types = main.find_elements(By.CSS_SELECTOR, "tr:nth-of-type(n+2)")
            for type in types:
                first_td = type.find_element(By.CSS_SELECTOR, "td:first-of-type")
                self.type_of_use.append(first_td.text)

            listings = main.find_elements(By.CSS_SELECTOR, "tr:nth-of-type(n+2)")
            for listing in listings:
                second_td = listing.find_element(By.CSS_SELECTOR, "td:nth-of-type(2)")
                self.listing_names.append(second_td.text)

                third_td = listing.find_element(By.CSS_SELECTOR, "td:nth-of-type(3)")
                self.project_locations.append(third_td.text)

                fourth_td = listing.find_element(By.CSS_SELECTOR, "td:nth-of-type(4)")
                self.project_status.append(fourth_td.text)

                fifth_td = listing.find_element(By.CSS_SELECTOR, "td:nth-of-type(5)")
                self.case_number_texts.append(fifth_td.text)

                sixth_td = listing.find_element(By.CSS_SELECTOR, "td:nth-of-type(6)")
                self.planner_leads.append(sixth_td.text)

        except Exception as e:
            print(f"An error occurred: {e}")

    def create_dataframe(self):
        listing_names = [item.split("\n")[0] for item in self.listing_names]
        description = [item.split("\n")[1] if '\n' in item else '' for item in self.listing_names]

        df = pd.DataFrame(
            {
                "projectName": listing_names,
                "address": self.project_locations,
                "planner": self.planner_leads,
                "status": self.project_status,
                "typeOfUse": self.type_of_use,
                "description": description
            }
        )

        df['planner'] = df['planner'].str.strip()
        
        # Helper function to get the closest match from the dictionary
        def get_closest_match(name):
            max_ratio = 0
            best_match = None
            for key, value in fullerton_planner_names.items():
                ratio = SequenceMatcher(None, name, value).ratio()
                if ratio > max_ratio:
                    max_ratio = ratio
                    best_match = value
        
        # If similarity is more than 30%, return the matched name, otherwise return the original name
            return best_match if max_ratio > 0.3 else name

        df["planner"] = df["planner"].apply(get_closest_match)
    
        # Assuming you have another dictionary called fullerton_planner_phones which maps names to phone numbers
        df["phone"] = df["planner"].map(fullerton_planner_phones)

        # Replace '\n' with ' ' in the 'status' column
        df["status"] = df["status"].str.replace('\n', ' ')

        # add the city column
        df['city'] = 'Fullerton'

        # add the email column
        df['email'] = FULLERTON_PLANNING_OFFICE_EMAIL

        # Add recentUpdate column with the first day of the current month for every row
        df['recentUpdate'] = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        return df
    
    def save_to_company_database(self, path=None):
        if not path:
            path = COMPANY_DATA_DIR / 'fullerton' / f'fullerton_city_data_{FullertonScraper.current_date}.xlsx'
        df = self.create_dataframe()
        df.to_excel(path, index=False)
    
    def save_to_processed(self, path=None):
        if not path:
            path = PROCESSED_DATA_DIR / 'fullerton' / f'fullerton_city_data_{FullertonScraper.current_date}.xlsx'
        df = self.create_dataframe()
        df.to_excel(path, index=False)

def main_city_of_fullerton():
    logger.info('Running Fullerton scraper')
    driver = get_chrome_driver()
    scraper = FullertonScraper(driver)
    scraper.connect(FULLERTON_PLANNING_URL)
    time.sleep(3)
    scraper.scrape_data()
    scraper.create_dataframe()
    scraper.save_to_processed()
    driver.quit()
    logger.info('Fullerton scraper finished')
    scraper.save_to_company_database()
    

# City of Garden Grove Scraper

class GardenGroveScraper:

    current_date = datetime.now().strftime('%Y-%m-%d')

    def __init__(self, driver):
        self.driver = driver
        self.listing_names = []
        self.case_number_texts = []
        self.project_locations = []
        self.planner_leads = []
        self.project_descriptions = []
        self.project_status = []
        self.image_urls = []

    def connect(self, url):
        self.driver.get(url)
        print(self.driver.title)

    def scrape_data(self):
        try:
            main = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "section.main-content-w-aside"))
            )
            # Scraping listing names
            headers = main.find_elements(By.CSS_SELECTOR, "div.h2")
            for header in headers:
                self.listing_names.append(header.text)

            # Scraping image URLs
            urls = main.find_elements(
            By.CSS_SELECTOR,
            "div.paragraph.paragraph--type--hero-image.paragraph--view-mode--default"
            )
            for url in urls:
                img_url = []
                try:
                    images_in_div = url.find_elements(By.TAG_NAME, "img")
                    for img in images_in_div:
                        image_src = img.get_attribute("src")
                    if image_src:
                        img_url.append(image_src)
                    else:
                        img_url.append("NA")
                except:
                    img_url.append("NA")
                self.image_urls.append(img_url)

            # Scraping case numbers
            case_numbers = main.find_elements(By.CSS_SELECTOR, "div.paragraph-text p:first-of-type")
            for case_number in case_numbers:
                self.case_number_texts.append(case_number.text)

            # Scraping project locations
            locations = main.find_elements(By.CSS_SELECTOR, "div.paragraph-text p:nth-of-type(2)")
            for location in locations:
                self.project_locations.append(location.text)

            # Scraping planner leads
            planners = main.find_elements(By.CSS_SELECTOR, "div.paragraph-text p:nth-of-type(3)")
            for planner in planners:
                self.planner_leads.append(planner.text)

            # Scraping project descriptions
            descriptions = main.find_elements(By.CSS_SELECTOR, "div.paragraph-text p:nth-of-type(4)")
            for description in descriptions:
                self.project_descriptions.append(description.text)

            # Scraping project status
            status = main.find_elements(By.CSS_SELECTOR, "div.paragraph-text p:nth-of-type(5)")
            for stats in status:
                self.project_status.append(stats.text)
           

        except Exception as e:
            print(f"An error occurred: {e}")
        print(self.listing_names)
        
    def create_dataframe(self):
        df = pd.DataFrame(
            {
                "projectName": self.listing_names,
                "Image_URLs": self.image_urls,
                "caseNumbers": self.case_number_texts,
                "address": self.project_locations,
                "planner": self.planner_leads,
                "description": self.project_descriptions,
                "status": self.project_status,
            }
        )
        # Helper function to get the closest match from the dictionary
        def get_closest_match(name):
            max_ratio = 0
            best_match = None
            for key, value in garden_grove_planner_names.items():
                ratio = SequenceMatcher(None, name, value).ratio()
                if ratio > max_ratio:
                    max_ratio = ratio
                    best_match = value
        
        # If similarity is more than 30%, return the matched name, otherwise return the original name
            return best_match if max_ratio > 0.3 else name
        
        # Apply the function to the planner column
        df['planner'] = df['planner'].apply(get_closest_match)

        # Add email and phone columns
        df['email'] = df['planner'].map(garden_grove_planner_emails)
        df['phone'] = df['planner'].map(garden_grove_planner_phones)
        
        # Add city and recent update columns
        df['city'] = 'Garden Grove'
        df['recentUpdate'] = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        return df
    
    def save_to_company_database(self, path=None):
        if not path:
            path = COMPANY_DATA_DIR / 'gardengrove' / f'garden_grove_data_{GardenGroveScraper.current_date}.xlsx'
        df = self.create_dataframe()
        df.to_excel(path, index=False)

    def save_to_processed(self, path=None):
        if not path:
            path = PROCESSED_DATA_DIR / 'gardengrove' / f'garden_grove_data_{GardenGroveScraper.current_date}.xlsx'
        df = self.create_dataframe()
        # drop the image urls, case numbers columns for production
        df.drop(columns=['imageURLs', 'caseNumbers'], inplace=True)
        df.to_excel(path, index=False)


def main_garden_grove():
    logger.info('Running Garden Grove scraper')
    driver = get_chrome_driver()
    scraper = GardenGroveScraper(driver)
    scraper.connect(GARDEN_GROVE_PLANNING_URL)
    scraper.scrape_data()
    df = scraper.create_dataframe()
    scraper.save_to_company_database()
    scraper.save_to_processed()
    driver.quit()
    logger.info('Garden Grove scraper finished')
    
    return df

# City of Huntington Beach Scraper


class HuntingtonBeachScraper:
    current_date = datetime.now().strftime("%Y-%m-%d")

    def __init__(self, driver, url, original_df):
        self.driver = driver
        self.url = url
        self.original_df = original_df
    
    def fetch_initial_data(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        response = requests.get(self.url, headers=headers)

        if response.status_code == 200:
            df_list = pd.read_html(response.text)
            self.original_df = df_list[2]
        else:
            print("Failed to retrieve the webpage. Status Code:", response.status_code)
            self.original_df = pd.DataFrame()

    def extract_project_info(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "middle"))
        )
        
        project_data = {}
        middle_div = self.driver.find_element(By.ID, 'middle')
        middle_div_text = middle_div.text
        project_summary_match = re.search(r'Project Summary\s*(.*)', middle_div_text, re.DOTALL)
        paragraphs = middle_div.find_elements(By.TAG_NAME, 'p')
        
        for paragraph in paragraphs:
            text = paragraph.text
            if 'Last Updated:' in text:
                project_data['recentUpdate'] = text.split('Last Updated:', 1)[1].strip()
            elif 'Project Planner:' in text:
                project_data['planner'] = text.split('Project Planner:', 1)[1].strip()
            elif 'Project Status:' in text:
                project_data['projectStatus'] = text.split('Project Status:', 1)[1].strip()

        if project_summary_match:
            project_data['description'] = project_summary_match.group(1).strip()

        return pd.DataFrame([project_data])

    def click_project_titles(self):
        all_project_data = pd.DataFrame()
        
        for title in self.original_df['Project Title'].tolist():
            try:
                link = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.LINK_TEXT, title))
                )
                link.click()
                project_df = self.extract_project_info()
                all_project_data = pd.concat([all_project_data, project_df], ignore_index=True)
                self.driver.back()
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'middle'))
                )
                time.sleep(2)
                
            except Exception as e:
                print(f"An error occurred while trying to click on the title '{title}': {e}")
        
        return all_project_data

    def merge_and_clean(self):
        self.driver.get(self.url)
        collected_data = self.click_project_titles()
        collected_data.set_index(self.original_df.index, inplace=True)
        final_df = self.original_df.join(collected_data)
        final_df.drop(columns=[col for col in final_df.columns if col not in ['Project Title', 'planner', 'projectStatus', 'description', 'recentUpdate']], inplace=True)
        final_df.rename(columns={'Project Title': 'projectName', 'Applicant': 'owner', 'Address': 'address', 'Project Planner': 'planner', 'Project Status': 'projectStatus', 'Project Summary': 'description', 'Last Updated': 'recentUpdate'}, inplace=True)
        final_df['city'] = 'Huntington Beach'
        final_df['phone'] = HUNTINGTON_BEACH_PLANNING_OFFICE_PHONE
        final_df['email'] = final_df['planner'].map(hb_planner_emails)
        self.final_df = final_df
    
    def save_to_company(self, path = None):
        if not Path: 
            path = COMPANY_DATA_DIR / 'huntingtonbeach' / f'huntington_beach_data_{HuntingtonBeachScraper.current_date}.xlsx' 
        self.final_df.to_excel(path, index=False)

    def save_to_processed(self, path = None):
        if not Path: 
            path = PROCESSED_DATA_DIR / 'huntingtonbeach' / f'huntington_beach_data_{HuntingtonBeachScraper.current_date}.xlsx' 
        self.final_df.to_excel(path, index=False)

# Example usage
def main_huntington_beach():
    url = HUNTINGTON_BEACH_PLANNING_URL
    # Example usage
    driver = get_chrome_driver()
    collector = HuntingtonBeachScraper(driver, url)
    collector.merge_and_clean()
    collector.save_to_company()  # Save without specifying a path will use the default
    collector.save_to_processed()  # Save without specifying a path will use the default
    driver.quit()

# City of Irvine Scraper

class IrvineScraper:
    def __init__(self, driver):
        self.driver = driver
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.raw_data_dir = RAW_DATA_DIR / 'irvine'
        self.processed_data_dir = PROCESSED_DATA_DIR / 'irvine'
    
    def ensure_directories_exist(self):
        if not os.path.exists(self.raw_data_dir):
            os.makedirs(self.raw_data_dir)
        if not os.path.exists(self.processed_data_dir):
            os.makedirs(self.processed_data_dir)
    
    def connect(self, url):
        self.driver.get(url)
        print(self.driver.title)

    @staticmethod
    def contains_date(s):
        return bool(re.match(r'\d{1,2}/\d{1,2}/\d{4}', s))
    
    @staticmethod
    def extract_schedule_decision_planner(details):
        # Indices for 'Schedule', 'Decision Maker', and 'Planner' assuming they are at the end
        # The -1 index will fetch the last word from the list which is assumed to be 'Planner'
        planner_index = -1
        # The -2 index will fetch the second last word from the list which is assumed to be 'Decision Maker'
        decision_maker_index = -2
        # The -3 index will fetch the third last word from the list which is assumed to be 'Schedule'
        schedule_index = -3
    
        #    We want everything before 'Schedule' to be part of the project description
        project_description = ' '.join(details[:schedule_index])
        schedule = details[schedule_index]
        decision_maker = details[decision_maker_index]
        planner = details[planner_index]
    
        return project_description, schedule, decision_maker, planner
    
    @staticmethod
    def process_text(text):
        lines = text.strip().split("\n")
        projects = []
        project_title = None

        for line in lines:
            if line.startswith("CURRENT DISCRETIONARY PROJECTS UNDER REVIEW"):
                continue
            if not IrvineScraper.contains_date(line.strip()):
                project_title = line.strip()
            else:
                details = line.strip().split()
                if len(details) > 3 and project_title:
                    project_description, schedule, decision_maker, planner = IrvineScraper.extract_schedule_decision_planner(details)
                    project_data = {
                    'Submittal Date': details[0],
                    'File #': details[1],
                    'PA': details[2],
                    'Project Description': project_description,
                    'Schedule': schedule,
                    'Decision Maker': decision_maker,
                    'Planner': planner,
                    'Project Title': project_title
                    }
                    projects.append(project_data)
                    project_title = None  # Reset project title for the next block

        return projects

    @staticmethod
    def create_dataframe(projects):
        return pd.DataFrame(projects)


    def scrape_pdf(self):
        try:
            # Click the link to open in a new tab
            link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Discretionary Project List"))
            )
            link.click()
            print("Navigated to the Discretionary Project List")

            # Switch to the new tab and wait for it to load
            WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)
            self.driver.switch_to.window(self.driver.window_handles[1])
            time.sleep(5)  # Adjust time as needed

            # Get the URL of the new tab
            pdf_url = self.driver.current_url

            # Sanitize the URL if it has been duplicated
            if pdf_url.count('BlobID=') > 1:
                pdf_url = pdf_url.split('&')[0]

            print(f"PDF should be available at: {pdf_url}")

            # Send a GET request to the PDF URL using requests
            response = requests.get(pdf_url)
            
            
            if response.status_code == 200:
                if not os.path.exists(self.raw_data_dir):
                    os.makedirs(self.raw_data_dir)

                    filename = f"irvine_major_planning_{self.current_date}.pdf"

                    # Write the PDF content to a file in RAW_DATA_DIR
                    file_path = os.path.join(self.raw_data_dir, filename)

                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    print(f"PDF has been saved to {file_path}")
                else:
                    print(f"Failed to download the PDF. Status code: {response.status_code}")
            
            # Close the PDF tab
            self.driver.close()

            # Switch back to the original tab
            self.driver.switch_to.window(self.driver.window_handles[0])
                
        except Exception as e:
            print(f"An error occurred: {e}")

    def wait_for_download_to_complete(self, file_pattern):
        """ Wait for the download to complete """
        print("Waiting for download to complete...")
        timeout = 120  # 2 minutes timeout
        while timeout > 0:
            files = os.listdir()
            if any(f.startswith(file_pattern) for f in files):
                print("Download completed.")
                return
            time.sleep(1)
            timeout -= 1
        print("Download did not complete within the allotted time.")
    
    @staticmethod
    def parse_pdf(pdf_filename):
        try:
            with pdfplumber.open(pdf_filename) as pdf:
                full_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            print(full_text)
        except Exception as e:
            print(f"An error occurred while parsing the PDF: {e}")
    
    def clean_and_rename_data(self, df):
        """Clean and rename the data of the DataFrame."""
        self.rename_columns(df)
        self.clean_description_column(df)
        self.add_additional_columns(df)
        self.fix_project_titles(df)
        self.drop_unnecessary_columns_and_clean(df)

    def drop_unnecessary_columns_and_clean(self, df):
         # Drop Columns 
        df.drop(columns=['Submittal Date', 'file_number', 'pa'], inplace=True)

    def rename_columns(self, df):
        """Rename columns in the DataFrame."""
        df.rename(columns={
            'Submittal Date': 'recentUpdate',
            'File #': 'file_number',
            'PA': 'pa',
            'Project Description': 'description',
            'Schedule': 'schedule',
            'Decision Maker': 'decision_maker',
            'Planner': 'planner',
            'Project Title': 'projectName'
        }, inplace=True)

    def save_to_company_database(self, df, path=None):
        """Save the DataFrame to a CSV file."""
        if not path:
            path = COMPANY_DATA_DIR / 'irvine' / f'irvine_city_data_{self.current_date}.xlsx'
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_excel(path, index=False)
        print(f"Company file saved to {path}")

    def clean_description_column(self, df):
        """Clean the 'description' column in the DataFrame."""
        df['description'] = df['description'].apply(self.clean_description)

        # Drop rows with empty 'description', if required
        df.drop(df[df['description'] == ''].index, inplace=True)

    def add_additional_columns(self, df):
        """Add additional columns to the DataFrame."""
        df['city'] = 'Irvine'
        df['planner'] = df['plannerFirst'] + ' ' + df['plannerLast']
        df['email'] = IRVINE_PLANNING_OFFICE_EMAIL
        df['phone'] = IRVINE_PLANNING_OFFICE_PHONE
        df['address'] = df['projectName']

        # project status is unknown
        df['status'] = 'Unknown'

        # drop project planner first and last name columns
        df.drop(columns=['plannerFirst', 'plannerLast'], inplace=True)

    def fix_project_titles(self, df):
        """Fix 'projectName' column in the DataFrame."""
        df['projectName'] = df.apply(self.fix_project_title, axis=1)
    
    # Function to clean the description
    @staticmethod
    def clean_description(description):
    # Remove 'TBD'
        description = description.replace('TBD', '')
    # Remove the date using regex
        description = re.sub(r'\d+/\d+/\d+', '', description).strip()
        # Remove file number using regex
        description = re.sub(r'\b\d{8}-[A-Z]{3,4}\b', '', description).strip()
        # Remove PA number using regex
        description = re.sub(r'^\d+\s+(?=[A-Z])', '', description)

        return description

    @staticmethod
    def fix_project_title(row):
    # Check if the project_title is the exact problematic string
        if row['project_title'] == 'Submittal Date File # PA Project Description Schedule Decision Maker Planner':
        # Replace with 'PA #' followed by the pa value
            return 'PA ' + str(row['pa'])
        else:
        # If not, return the original project_title
            return row['project_title']
        
    def process_and_save_dataframe(self, projects):
        try:
            project_df = self.create_dataframe(projects)
            self.clean_and_rename_data(project_df)
            self.save_to_processed(project_df)
        except Exception as e:
            print(f"An error occurred while processing data: {e}")
    
    def save_to_processed(self, df):
        """Save the DataFrame to a CSV file."""
        save_path = os.path.join(self.processed_data_dir, 'irvine', f'irvine_city_data_{self.current_date}.xlsx')
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df.to_excel(save_path, index=False)
        print(f"Processed file saved to {save_path}")
    
def main_irvine_scraper():
    current_date = datetime.now().strftime("%Y-%m-%d")
    logger.info('Running Irvine scraper')
    driver = get_chrome_driver()
    scraper = IrvineScraper(driver)
    scraper.connect(IRVINE_MAJOR_PLANNING_URL)
    scraper.scrape_pdf()
    scraper.wait_for_download_to_complete('irvine_major_planning')
    scraper.parse_pdf(f'irvine_major_planning_{current_date}.pdf')
    projects = scraper.process_text(f'irvine_major_planning_{current_date}.pdf')
    scraper.save_to_company_database(projects)
    scraper.process_and_save_dataframe(projects)
    driver.quit()
    logger.info('Irvine scraper finished') 