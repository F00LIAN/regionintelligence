import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path

# Set the current working directory to the script's directory
os.chdir(os.path.dirname(__file__))
project_root = Path(__file__).resolve().parent.parent  # Adjust based on your project structure
sys.path.append(str(project_root))

from src.paths import TRANSFORMED_DATA_DIR, FINAL_DATA_DIR, DROPBOX_DIR

# Create a function that will perform the transformations

def perform_initial_transformations():
    """
    First gather the extracted data files from the dropbox directory and then perform transformations on them.
    """
    # Load the data files
    print("Loading the new dropbox data files...")
    DS_1 = pd.read_csv(DROPBOX_DIR / 'DS04 Part 1 Data Sales.csv')
    DS_2 = pd.read_csv(DROPBOX_DIR / 'DS04 Part 2 Data Sales.csv')
    DS_3 = pd.read_csv(DROPBOX_DIR / 'DS04 Part 3 Data Sales.csv')

    local_roll = pd.read_excel(DROPBOX_DIR / 'Local Roll Part 1 Data Sales.xlsx')
    local_roll_2 = pd.read_excel(DROPBOX_DIR / 'Local Roll Part 2 Data Sales.xlsx')
    local_roll_3 = pd.read_excel(DROPBOX_DIR / 'Local Roll Part 3 Data Sales.xlsx')
    local_roll_4 = pd.read_excel(DROPBOX_DIR / 'Local Roll Part 4 Data Sales.xlsx')
    local_roll_5 = pd.read_excel(DROPBOX_DIR / 'Local Roll Part 5 Data Sales.xlsx')

    sales_list = pd.read_excel(DROPBOX_DIR / 'SALESLIST_012424 Data Sales.xlsx')
    
    print("Transforming the data...")
    DS_1.rename(columns=lambda x: x.strip(), inplace=True)
    DS_2.rename(columns=lambda x: x.strip(), inplace=True)
    DS_3.rename(columns=lambda x: x.strip(), inplace=True)  

    local_roll.rename(columns=lambda x: x.strip(), inplace=True)
    local_roll_2.rename(columns=lambda x: x.strip(), inplace=True)
    local_roll_3.rename(columns=lambda x: x.strip(), inplace=True)
    local_roll_4.rename(columns=lambda x: x.strip(), inplace=True)
    local_roll_5.rename(columns=lambda x: x.strip(), inplace=True)

    sales_list.rename(columns=lambda x: x.strip(), inplace=True)

    DS_1 = DS_1.map(lambda x: x.strip() if isinstance(x, str) else x)
    DS_2 = DS_2.map(lambda x: x.strip() if isinstance(x, str) else x)
    DS_3 = DS_3.map(lambda x: x.strip() if isinstance(x, str) else x)

    local_roll = local_roll.map(lambda x: x.strip() if isinstance(x, str) else x)
    local_roll_2 = local_roll_2.map(lambda x: x.strip() if isinstance(x, str) else x)
    local_roll_3 = local_roll_3.map(lambda x: x.strip() if isinstance(x, str) else x)
    local_roll_4 = local_roll_4.map(lambda x: x.strip() if isinstance(x, str) else x)
    local_roll_5 = local_roll_5.map(lambda x: x.strip() if isinstance(x, str) else x)

    sales_list.rename(columns=lambda x: x.strip(), inplace=True)

    print("Concatenating the data...")
    # Concatenate the three datasets
    DS = pd.concat([DS_1, DS_2, DS_3], axis=0)  
    local_roll = pd.concat([local_roll, local_roll_2, local_roll_3, local_roll_4, local_roll_5], axis=0)
    sales_list = sales_list

    # Save the data to the transformed data directory
    DS.to_csv(TRANSFORMED_DATA_DIR / 'DS_transformed.csv', index=False)
    local_roll.to_csv(TRANSFORMED_DATA_DIR / 'local_roll_transformed.csv', index=False)
    sales_list.to_csv(TRANSFORMED_DATA_DIR / 'sales_list_transformed.csv', index=False)

    print("Transformations complete")

