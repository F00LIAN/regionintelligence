import os
import sys
from pathlib import Path

# Set the current working directory to the script's directory
os.chdir(os.path.dirname(__file__))
project_root = Path(__file__).resolve().parent.parent  # Adjust based on your project structure
sys.path.append(str(project_root))

import pandas as pd
import numpy as np
from src.paths import TRANSFORMED_DATA_DIR, FINAL_DATA_DIR
from src.const import *
from src.custom import *

def clean_and_convert_strings(df, columns):
    """
    Cleans and converts specified columns in a dataframe to strings. It replaces null values and any instances
    of 'ÿ' and its repetitions with 'Unknown', then converts each column to string type.

    Args:
        df (pd.DataFrame): The dataframe to process.
        columns (list of str): The list of column names to process as string columns.

    Returns:
        pd.DataFrame: The dataframe with the processed columns.
    """
    for column in columns:
        if column in df.columns:
            # Replace 'ÿ' sequences and null values with 'Unknown'
            df[column] = df[column].replace(to_replace=r'ÿ+', value='Unknown', regex=True).fillna('Unknown')
            # Convert to string type
            df[column] = df[column].astype(str)
        else:
            print(f"Warning: Column '{column}' not found in DataFrame.")
    return df

def convert_to_datetime(df, columns, placeholder='1901-01-01'):
    """
    Converts specified columns in a dataframe to datetime. It replaces non-convertible values with a placeholder.

    Args:
        df (pd.DataFrame): The dataframe to process.
        columns (list of str): The list of column names to process as datetime columns.
        placeholder (datetime or pd.NaT): The placeholder value for non-convertible entries, default is pd.NaT.

    Returns:
        pd.DataFrame: The dataframe with the processed columns.
    """
    for column in columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors='coerce')
            # Replace any remaining NaT or other non-convertible values with the placeholder
            df[column] = df[column].dt.date
            df[column] = df[column].fillna(pd.to_datetime(placeholder).date())
        else:
            print(f"Warning: Column '{column}' not found in DataFrame.")
    return df

def convert_to_int(df, columns):
    """
    Converts specified columns in a dataframe to int64. It handles floats by converting them directly to ints,
    numeric strings are also converted to ints, and non-numeric strings or any other non-convertible values are
    replaced with 0.

    Args:
        df (pd.DataFrame): The dataframe to process.
        columns (list of str): The list of column names to process as integer columns.

    Returns:
        pd.DataFrame: The dataframe with the processed columns.
    """
    for column in columns:
        if column in df.columns:
            # Attempt to convert all values to int64, replacing non-convertible values with 0
            df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0).astype('int64')
        else:
            print(f"Warning: Column '{column}' not found in DataFrame.")

    return df

def detect_column_types_from_dict(df, column_types_dict):
    """
    Detects and verifies the data types for the specified columns using the provided dictionary.

    Args:
        df (pd.DataFrame): The dataframe to process.
        column_types_dict (dict): A dictionary mapping column names to their desired data types.

    Returns:
        dict: A dictionary mapping column names to their detected data types.
    """
    column_types = {}
    for column, expected_type in column_types_dict.items():
        if column in df.columns:
            if pd.api.types.is_dtype_equal(df[column], expected_type):
                column_types[column] = expected_type
            else:
                # Mixed type detection (this part could be more sophisticated)
                unique_types = set(df[column].apply(type))
                if expected_type == 'object' and (str in unique_types or bytes in unique_types):
                    column_types[column] = 'object'
                elif expected_type == 'int64' and (int in unique_types or float in unique_types):
                    column_types[column] = 'int64'
                elif expected_type == 'datetime64[ns]' and pd.api.types.is_datetime64_any_dtype(df[column]):
                    column_types[column] = 'datetime64'
                else:
                    column_types[column] = expected_type
        else:
            print(f"Warning: Column '{column}' not found in DataFrame.")
    return column_types

def apply_column_conversions(df, column_types):
    """
    Applies the appropriate conversions to the DataFrame columns based on a dictionary of column types.

    Args:
        df (pd.DataFrame): The DataFrame to process.
        column_types (dict): A dictionary mapping column names to their desired data types.

    Returns:
        pd.DataFrame: The DataFrame with the columns converted to the specified data types.
    """

    string_columns = []
    int_columns = []
    datetime_columns = []
    
    # Classify columns by the target data type
    for column, dtype in column_types.items():
        if dtype == 'object':
            string_columns.append(column)
        elif dtype == 'int64':
            int_columns.append(column)
        elif dtype == 'datetime64':
            datetime_columns.append(column)
    
    # Apply conversions
    if string_columns:
        df = clean_and_convert_strings(df, string_columns)
    if int_columns:
        df = convert_to_int(df, int_columns)
    if datetime_columns:
        df = convert_to_datetime(df, datetime_columns)

    return df

def clean_column_names(df):
    """
    Cleans the column names by making them lowercase, replacing spaces with underscores, and removing dashes.

    Args:
        df (pd.DataFrame): The DataFrame to process.

    Returns:
        pd.DataFrame: The DataFrame with cleaned column names.
    """
    df.columns = df.columns.str.replace('-', '', regex=False)
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')
    return df
    


def perform_cleaning():
    
    # Load in the Data from the transformed directory
    DS = pd.read_csv(TRANSFORMED_DATA_DIR / 'DS_transformed.csv')
    LR = pd.read_csv(TRANSFORMED_DATA_DIR / 'local_roll_transformed.csv')
    SL = pd.read_csv(TRANSFORMED_DATA_DIR / 'sales_list_transformed.csv')
    HZ = pd.read_csv(TRANSFORMED_DATA_DIR / 'hazards_city.csv')
    LU = pd.read_csv(TRANSFORMED_DATA_DIR / 'land_use.csv')

    DS = replace_DS_hazard_city_key(DS, 'Hazard City Key', ['A', 'B', 'C', 'D', np.nan], [10, 11, 12, 13, 0])
    DS = replace_DS_special_name_legend(DS, 'Special Name Legend', [np.nan, 'ÿÿÿÿÿ'], ['Unknown', 'Unknown'])
    DS = replace_DS_doc_reason_code(DS, 'Doc Reason Code', [np.nan, 'ÿ'], ['0', '0'])
    DS = replace_DS_tax_stat_key(DS, 'Tax Stat Key', [np.nan, 'ÿ'], ['4', '4'])
    DS = replace_DS_exemption(DS, 'Exemption Type', [np.nan, 'ÿ'], ['10', '10'])
    #DS = drop_DS_ownership_code(DS, 'Ownership Code')
    #DS = replace_DS_pp_key(DS, 'PP Key', [np.nan, 'ÿ'], [0, 0])
    DS['county_name'] = 'Los Angeles'
    
    DS['state_name'] = 'California'
    
    LR = replace_LR_administrative_values(LR, 'Administrative Region Number', ['A1', 'B1', np.nan], [1, 21, 0])
    LR = replace_LR_situs_address_key(LR, 'Situs Address Key', [np.nan], ['O'])
    LR['county_name'] = 'Los Angeles'
    LR['state_name'] = 'California'
    
    SL = replace_SL_administrative_values(SL, 'Administrative Region', ['A1', 'B1', 'ÿÿ', np.nan], [1, 21, 99, 99])
    SL = replace_SL_dtt_type(SL, 'dtt type', [np.nan, 'nan', 'ÿ'], [0, 0, 0])
    SL = replace_SL_key(SL, 'Key', ['ÿ'], [0])
    SL = replace_SL_design_ty(SL, 'design ty', [np.nan], [0])
    SL = replace_SL_verification(SL, ['last sale1 ver', '2 verification', '3 verif'], ['ÿ', np.nan], ['0','0S'])
    SL['county_name'] = 'Los Angeles'
    SL['state_name'] = 'California'
    
    # Keep only instances of LA County for both HZ and LU
    HZ = HZ[HZ['COUNTY_NAME'] == 'Los Angeles']
    HZ['state_name'] = 'California'
    
    LU = LU[LU['COUNTY_NAME'] == 'Los Angeles']
    LU['state_name'] = 'California'

    column_types_DS = detect_column_types_from_dict(DS, secured_roll_types)
    DS = apply_column_conversions(DS, column_types_DS)

    column_types_LR = detect_column_types_from_dict(LR, local_roll_types)
    LR = apply_column_conversions(LR, column_types_LR)

    column_types_SL = detect_column_types_from_dict(SL, sales_list_types)
    SL = apply_column_conversions(SL, column_types_SL)

    
    # Drop columns that are not needed and rename the columns
    DS = DS.drop(columns=DS_columns_to_drop)
    DS = DS.rename(columns=dict(zip(DS_columns_to_rename, DS_renamed_columns)))

    SL = SL.drop(columns=SL_columns_to_drop)
    SL = SL.rename(columns=dict(zip(SL_columns_to_rename, SL_renamed_columns)))

    LR = LR.drop(columns=LR_columns_to_drop)
    LR = LR.rename(columns=dict(zip(LR_columns_to_rename, LR_renamed_columns)))

    # structure the column names in a way they are compatable with postgres
    DS = clean_column_names(DS)
    LR = clean_column_names(LR)
    SL = clean_column_names(SL)

    # save the data to the final directory
    DS.to_csv(FINAL_DATA_DIR / 'secured_basic_transformed.csv')
    LR.to_csv(FINAL_DATA_DIR / 'local_roll_transformed.csv')
    SL.to_csv(FINAL_DATA_DIR / 'sales_list_transformed.csv')