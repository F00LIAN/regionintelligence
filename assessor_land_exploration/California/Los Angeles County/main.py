import pandas as pd
import numpy as np
from src.dropbox_extract import download_all_files
from src.cleaning import perform_cleaning
from src.load import run_db
from src.transform import perform_initial_transformations

# GEt the dropbox files
def main():

    # Run the file download
    print("Downloading the most recent files")
    #download_all_files()
    print("Files downloaded")

    print("Performing Transformations...")
    # Perform transformations
    perform_initial_transformations()
    print("Transformations complete")

    print("Performing Cleaning...")
    # Perform transformations
    perform_cleaning()

    #print("Updating Database...")
    # Update the database
    #run_db()
    
    print("Done")

if __name__ == "__main__":
    main()