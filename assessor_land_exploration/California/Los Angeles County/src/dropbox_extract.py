import os
import sys
from pathlib import Path

# Set the current working directory to the script's directory
os.chdir(os.path.dirname(__file__))
project_root = Path(__file__).resolve().parent.parent  # Adjust based on your project structure
sys.path.append(str(project_root))

import os 
from dotenv import load_dotenv
from src.paths import DROPBOX_DIR
import dropbox
import dropbox.files
import hashlib

load_dotenv()

token = os.getenv('DROPBOX_ACCESS_TOKEN')
dbx = dropbox.Dropbox(token)

def upload_all_local_files():
    for file in os.listdir(DROPBOX_DIR):
        with open(os.path.join(DROPBOX_DIR, file), 'rb') as f:
            data = f.read()
            dbx.files_upload(data, f"/{file}")


def download_all_files():
    for entry in dbx.files_list_folder('').entries:
        dbx.files_download_to_file(os.path.join(DROPBOX_DIR, entry.name), f"/{entry.name}")


def dropbox_content_hash(file):
    hash_chunk_size = 4 * 1024 * 1024
    with open(file, 'rb') as f:
        block_hashes = bytes()
        while True:
            chunk = f.read(hash_chunk_size)
            if not chunk:
                break
            block_hashes += hashlib.sha256(chunk).digest()
        
        return hashlib.sha256(block_hashes).hexdigest()
    

def download_changed():
    for entry in dbx.files_list_folder('').entries:
        if  os.path.exists(os.path.join(DROPBOX_DIR, entry.name)):
           local_hash = dropbox_content_hash(os.path.join(DROPBOX_DIR, entry.name))
           if local_hash != entry.content_hash:
               print(f"Downloading changed file {entry.name}")
               dbx.files_download_to_file(os.path.join(DROPBOX_DIR, entry.name), f"/{entry.name}")
           else:
               print("Unchanged", entry.name)
        else:
            print("Downloading New File", entry.name)
            dbx.files_download_to_file(os.path.join(DROPBOX_DIR, entry.name), f"/{entry.name}")

#def upload_changed():
"""           
if __name__ == "__main__":
    download_changed()
    print("Done")"""