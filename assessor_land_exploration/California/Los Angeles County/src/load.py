import os
import sys
from pathlib import Path

# Set the current working directory to the script's directory
os.chdir(os.path.dirname(__file__))
project_root = Path(__file__).resolve().parent.parent  # Adjust based on your project structure
sys.path.append(str(project_root))

import pandas as pd
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from io import StringIO
from src.paths import FINAL_DATA_DIR 

# Load environment variables
load_dotenv()

# Environment configuration
DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

def create_engine_load_data(file_path, table_name, engine):
    """
    Load data from a CSV file into a DataFrame and then into a PostgreSQL database table.
    If the table exists, update it with new data; otherwise, create a new table.
    """
    # Load data from CSV file with low_memory set to False to handle mixed data types
    df = pd.read_csv(file_path, low_memory=False)

    # Create a SQLAlchemy engine
    with engine.connect() as connection:
        # Prepare and execute a query to check if the table exists
        query = text(f"SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = :table);")
        exists = connection.execute(query, {'table': table_name}).fetchone()[0]
        
        if exists:
            # Insert new data or update existing data
            df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
            print(f"Updated data in the {table_name} table.")
        else:
            # Create new table and insert data
            df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
            print(f"Created and populated the {table_name} table.")

def run_db():
    # Create an engine instance
    engine = create_engine(DB_URL)
    
    # Define file paths and table names
    data_files = {
        FINAL_DATA_DIR / 'sales_list_transformed.csv': 'sales_list',
        FINAL_DATA_DIR / 'local_roll_transformed.csv': 'local_roll',
        FINAL_DATA_DIR / 'secured_basic_transformed.csv': 'secured_basic'
    }

    # Process each file
    for file_path, table_name in data_files.items():
        create_engine_load_data(file_path, table_name, engine)
