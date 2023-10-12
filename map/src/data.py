import time
import numpy as np
import pandas as pd
import re
import os

from src.driver_config import get_chrome_driver, navigate_and_print_title
from src.const import SANTA_ANA_PLANNING_OFFICE_NAME, SANTA_ANA_PLANNING_URL, SANTA_ANA_PLANNING_OFFICE_EMAIL, SANTA_ANA_PLANNING_OFFICE_PHONE
from src.paths import RAW_DATA_DIR, PROCESSED_DATA_DIR

from src.const import (
    orange_planner_phones, 
    orange_planner_emails, 
    orange_planner_names, 
    ORANGE_PLANNING_URL)
from src.const import (
    anaheim_planner_emails, 
    anaheim_planner_phones, 
    anaheim_planner_names, 
    ANAHEIM_PLANNING_OFFICE_EMAIL, 
    ANAHEIM_PLANNING_OFFICE_PHONE
)
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


def main_santa_ana():
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

            pdf_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Current Pending Land Use Applications List"))
            )
            pdf_link.click()

            pdf_url = pdf_link.get_attribute("href")
            self.pdf_urls.append(pdf_url)
            
        except Exception as e:
            print(f"An error occurred: {e}")

    def parse_orange_pdf(self, pdf_path=None):
        if not pdf_path:
            pdf_path = RAW_DATA_DIR / 'orange' / f'orange_city_data_{OrangeScraper.current_date}.pdf'
            
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

        # Use the class variable here
        file_name = f"orange_city_data_{OrangeScraper.current_date}.pdf"

        orange_dir = os.path.join(directory, 'orange')
        if not os.path.exists(orange_dir):
            os.makedirs(orange_dir)

        for url in self.pdf_urls:
            response = requests.get(url)
            with open(os.path.join(orange_dir, file_name), "wb") as f:
                f.write(response.content)
        
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
    scraper.save_to_processed(df)
    driver.close()


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
        anaheim_path = self.get_most_recent_file(RAW_DATA_DIR / 'anaheim', 'AndysMap')
        dev_apps_path = self.get_most_recent_file(RAW_DATA_DIR / 'anaheim', 'dev_apps')
        if not anaheim_path or not dev_apps_path:
            raise Exception("Couldn't find the required files!")
        self.current_projects_df = pd.read_csv(anaheim_path)
        self.current_applications_df = pd.read_csv(dev_apps_path)

    def process_the_dataframe(self, df):
        if 'Staff Name' in df.columns:
            df['email'] = df['Staff Name'].map(anaheim_planner_emails)
            df['phone'] = df['Staff Name'].map(anaheim_planner_phones)
            df['email'].fillna(ANAHEIM_PLANNING_OFFICE_EMAIL, inplace=True)
            df['phone'].fillna(ANAHEIM_PLANNING_OFFICE_PHONE, inplace=True)
        else:
            df['email'] = ANAHEIM_PLANNING_OFFICE_EMAIL
            df['phone'] = ANAHEIM_PLANNING_OFFICE_PHONE
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
        df = df[['address', 'description', 'projectName', 'typeOfUse', 'status', 'owner', 'recentUpdate', 'email', 'phone', 'city']]
        #df['projectName'] = df['projectName'].apply(lambda x: re.sub(r'\[.*?\]\s*', '', x))
        return df

    def run(self):
        # Reads the CSV
        self.read_anaheim_csv()

        # Processes the first dataframe
        self.current_projects_df = self.process_the_dataframe(self.current_projects_df)

        # (Optional) Processes the second dataframe, etc.

        # Returns the processed dataframe for further operations or analysis
        return self.current_projects_df

def main_anaheim():
    """
    CITY OF ANAHEIM
    """
    scraper = AnaheimScraper()
    df = scraper.run()
    file_name = f"anaheim_city_data_{AnaheimScraper.current_date}.xlsx"
    path = PROCESSED_DATA_DIR / 'anaheim' / file_name
    df.to_excel(path, header=True)