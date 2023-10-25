import os
import json
import datetime
from utils import JSON_DATA_DIR, TRAINING_DATA_DIR

def concatenate_json_files(source_dir=JSON_DATA_DIR, destination_dir=TRAINING_DATA_DIR):
    """
    Concatenate all JSON files from the source directory and save the combined content to the destination directory.
    
    Args:
        source_dir (str): Directory containing the source JSON files.
        destination_dir (str): Directory where the concatenated JSON file will be saved.
    """
    print(f"Source directory: {source_dir}")
    print(f"Destination directory: {destination_dir}")

    # Get the current date and format it
    current_date = datetime.datetime.now().strftime('%Y%m%d')
    
    # Destination file name with date appended
    destination_file = f'concatenated_california_building_code_data_{current_date}.json'

    # List of all JSON files in the source directory including subdirectories
    json_files = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    
    print(f"Detected JSON files: {json_files}")

    # Placeholder for concatenated data
    concatenated_data = []

    # Iterate over each JSON file
    for json_file in json_files:
        with open(json_file, 'r') as f:
            data = json.load(f)
            concatenated_data.extend(data)

    # Write concatenated data to destination file
    with open(os.path.join(destination_dir, destination_file), 'w') as f:
        json.dump(concatenated_data, f, indent=4)

    print(f"Data from {len(json_files)} JSON files has been concatenated and saved to {destination_file}.")


