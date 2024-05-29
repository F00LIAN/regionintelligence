import os
import sys
from pathlib import Path

# Set the current working directory to the script's directory
os.chdir(os.path.dirname(__file__))
project_root = Path(__file__).resolve().parent.parent  # Adjust based on your project structure
sys.path.append(str(project_root))

# Replace DS Values to our need
def replace_DS_hazard_city_key(df, column, old_values, new_values):
    """
    A function to replace the hazard city key values
    """
    df[column] = df[column].replace(old_values, new_values)
    return df

def replace_DS_special_name_legend(df, column, old_values, new_values):
    """
    A function to fix nulls from special name legend row
    """
    df[column] = df[column].replace(old_values, new_values)
    return df

def replace_DS_doc_reason_code(df, column, old_values, new_values):
    """
    A function to fix nulls from special name legend row
    """
    df[column] = df[column].replace(old_values, new_values)
    return df

def replace_DS_tax_stat_key(df, column, old_values, new_values):
    """
    A function to fix nulls from tax stat key
    """
    df[column] = df[column].replace(old_values, new_values)
    return df

def replace_DS_exemption(df, column, old_values, new_values):
    """
    A function to fix nulls and unknown values
    """
    df[column] = df[column].replace(old_values, new_values)

    return df

def drop_DS_ownership_code(df, column, old_values, new_values):
    """
    A function to drop the ownership code column
    """
    df.drop(column, axis=1, inplace=True)
    return df

def replace_DS_pp_key(df, column, old_values, new_values):
    """
    A function to replace the pp key values
    """
    df[column] = df[column].replace(old_values, new_values)
    return df

# for a column called "Administrative Region" in a dataset, replace the string values of 'A-1' and 'B-1' with a 1 and 21 respectively
def replace_LR_administrative_values(df, column, old_values, new_values):
    """
    A custom function for the LR dataset to replace the string values of 'A-1' and 'B-1' with a 1 and 21 respectively
    """
    df[column] = df[column].replace(old_values, new_values)
    return df

def replace_LR_situs_address_key(df, column, old_values, new_values):
    """
    A custom function for the LR dataset to replace the string values of 'A-1' and 'B-1' with a 1 and 21 respectively
    """
    df[column] = df[column].replace(old_values, new_values)
    return df

def drop_LR_filler(df, column):
    """
    A custom function to drop the filler column
    """
    df = df.drop(column)

# Replace Sales List Values to change Mixed Types
def replace_SL_administrative_values(df, column, old_values, new_values):
    """
    A custom function for the SL dataset to replace the string values of 'A-1' and 'B-1' with a 1 and 21 respectively
    """
    df[column] = df[column].replace(old_values, new_values)
    return df

def replace_SL_dtt_type(df, column, old_values, new_values):
    """
    A custom function for the SL dataset to replace the string values of 'A-1' and 'B-1' with a 1 and 21 respectively
    """
    df[column] = df[column].replace(old_values, new_values)
    return df

def replace_SL_key(df, column, old_values, new_values):
    """
    A custom function for the SL dataset to replace the string values of 'A-1' and 'B-1' with a 1 and 21 respectively
    """
    df[column] = df[column].replace(old_values, new_values)
    return df

def replace_SL_design_ty(df, column, old_values, new_values):
    """
    A custom function for the SL dataset to replace the string values of 'A-1' and 'B-1' with a 1 and 21 respectively
    """
    df[column] = df[column].replace(old_values, new_values)
    return df

def replace_SL_verification(df, columns, old_values, new_values):
    """
    A function to replace the verification ÿ, np.nan
    """
    for column in columns:
        df[column] = df[column].replace(old_values, new_values)
    return df 

