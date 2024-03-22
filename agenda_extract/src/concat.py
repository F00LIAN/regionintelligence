import os
import sys
from pathlib import Path

# Set the current working directory to the script's directory
os.chdir(os.path.dirname(__file__))
project_root = Path(__file__).resolve().parent.parent  # Adjust based on your project structure
sys.path.append(str(project_root))

from src.paths import PRIMEGOV_DIR, CONCAT_DIR, LEGISTAR_DIR
from datetime import datetime
import json

# A Function that  Concatenate both the PrimeGov and Legistar JSON files from the most recent date

def concatenate_json_files():
    primegov_files = list(PRIMEGOV_DIR.glob('*.json'))
    legistar_files = list(LEGISTAR_DIR.glob('*.json'))
    
    primegov_files.sort()
    legistar_files.sort()
    
    primegov_latest = primegov_files[-1]
    legistar_latest = legistar_files[-1]
    
    with open(primegov_latest, 'r') as file:
        primegov_data = json.load(file)
    
    with open(legistar_latest, 'r') as file:
        legistar_data = json.load(file)
    
    combined_data = {**primegov_data, **legistar_data}
    
    current_time = datetime.now().strftime("%Y-%m-%d")
    
    with open(CONCAT_DIR / f'latest_agendas_{current_time}.json', 'w') as file:
        file.write(json.dumps(combined_data, indent=4))
        
    print(f'JSON files concatenated and saved as concatenated_{current_time}.json')


# concatenate_json_files(), 

# create another function that ensure the data is not duplicated
def remove_duplicate_data():
    latest_file = list(CONCAT_DIR.glob('*.json'))[-1]
    
    with open(latest_file, 'r') as file:
        data = json.load(file)
    
    for city in data:
        data[city] = [dict(t) for t in {tuple(d.items()) for d in data[city]}]
    
    with open(latest_file, 'w') as file:
        file.write(json.dumps(data, indent=4))
    
    print('Duplicate data removed')

# create a function to grab the latest agendas added to the JSON file

def grab_latest_agendas():
    """
    Grabs the latest agendas added by comparing the most recent concatenated file 
    against the previous version, if available.
    """
    json_files = sorted(CONCAT_DIR.glob('*.json'))
    if len(json_files) < 2:
        print("Not enough data to compare for new agendas.")
        return

    # Compare the two most recent files
    with open(json_files[-2], 'r') as file:  # Previous file
        prev_data = json.load(file)
    with open(json_files[-1], 'r') as file:  # Latest file
        latest_data = json.load(file)
    
    # Assuming no explicit unique identifiers, compare data based on content
    new_agendas = {}
    for city, agendas in latest_data.items():
        prev_agendas = prev_data.get(city, [])
        # Convert list of dicts to list of tuples for comparison
        prev_tuples = [tuple(sorted(d.items())) for d in prev_agendas]
        for agenda in agendas:
            if tuple(sorted(agenda.items())) not in prev_tuples:
                if city not in new_agendas:
                    new_agendas[city] = []
                new_agendas[city].append(agenda)
    
    if new_agendas:
        current_time = datetime.now().strftime("%Y-%m-%d")
        new_file_path = CONCAT_DIR / f'latest_new_agendas_{current_time}.json'
        with open(new_file_path, 'w') as file:
            json.dump(new_agendas, file, indent=4)
        print(f'New agendas saved to {new_file_path}')
    else:
        print('No new agendas found')