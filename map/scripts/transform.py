import pandas as pd
import numpy as np
import os
from dotenv import loadenv
import psycopg2
from src.paths import FINAL_DATA_DIR
from pathlib import Path
import openai 


def load_dataframes_from_directory(base_dir_path):
    """
    Load all Excel files from subdirectories of the given directory into dataframes.
    """
    base_dir = Path(base_dir_path)
    dataframes = {}

    for subdir in base_dir.iterdir():
        if subdir.is_dir():
            dataframes[subdir.name] = {}
            for file in subdir.iterdir():
                if file.suffix == '.xlsx':
                    try:
                        dataframes[subdir.name][file.stem] = pd.read_excel(file, engine='openpyxl')
                    except Exception as e:
                        print(f"Error reading {file}: {e}")
    
    return dataframes

def unpack_dataframes_to_globals(dataframes):
    """
    Unpack each dataframe from the nested dictionary and set them as global variables based on the subdirectory name.
    """
    for subdir_name, subdict in dataframes.items():
        for file_name, df in subdict.items():
            formatted_name = subdir_name.lower() + "_df"
            globals()[formatted_name] = df

def clean_dataframe(df):
    """
    Clean a dataframe by:
    - Dropping the "Unnamed: 0" column if it exists.
    - Replacing every '\n' occurrence with a space.
    """
    # Drop "Unnamed: 0" column
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    # Replace every '\n' with space
    df = df.replace('\n', ' ', regex=True)
    return df

def concatenate_dataframes(dfs_list):
    """
    Concatenate all dataframes in the list into a single dataframe, regardless of whether columns have different names.
    """
    concatenated_df = pd.concat(dfs_list, axis=0, ignore_index=True)
    return concatenated_df

# Pipeline
def process_pipeline(directory_path):
    # Load dataframes from directory
    dfs = load_dataframes_from_directory(directory_path)
    
    # Unpack dataframes to global variables
    unpack_dataframes_to_globals(dfs)
    
    cleaned_dfs = []

    # Clean each dataframe
    for subdir_name, subdict in dfs.items():
        for _, df in subdict.items():
            cleaned_df = clean_dataframe(df)
            cleaned_dfs.append(cleaned_df)

    # Concatenate all cleaned dataframes into a single dataframe
    final_df = concatenate_dataframes(cleaned_dfs)
    return final_df

# Execute the pipeline
final_dataframe = process_pipeline(PROCESSED_DATA_DIR)

openai.api_key = os.getenv("OPENAI_API_KEY")


load_dotenv()

prompt_template = "{description}. If it falls into 'Commercial', 'Residential', 'Industrial', or 'Mixed Use', please specify. Otherwise, label it 'Other'"

# Fictional Langchain interaction
def get_response_from_langchain(description):
    try:
        # Fictionally using Langchain to get the response (This is a mock and won't run in reality)
        messages = [{"role": "user", "content": prompt_template.format(description=description)}]
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        
        # Extract the model's message from the returned messages
        answer = response['choices'][0]['message']['content'].strip()
        
        # Check if the response starts with "Other" and then extract the two-word description
        if answer.startswith("Other"):
            return answer
        # If the response doesn't start with "Other", return just the category
        return answer.split()[0]
    except Exception as e:
        print(f"Error: {e}")
        return None

# Apply only to rows where 'typeOfUse' is NaN
mask = final_dataframe['typeOfUse'].isna()
final_dataframe.loc[mask, 'typeOfUse'] = final_dataframe.loc[mask, 'description'].apply(get_response_from_langchain)

print(final_dataframe)
