import pandas as pd
from os import path
import yaml
from pandas import DataFrame
from google.oauth2 import service_account
from google.cloud import bigquery


from src.paths import PARENT_DIR

def export_data_to_big_query(data, **kwargs) -> None:

    # The path to the config.yaml file.
    config_path = path.join(PARENT_DIR, 'config.yaml')

    # Read the YAML config file.
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Extract the configuration from the config file.
    bigquery_creds = config['default']['GOOGLE_SERVICE_ACC_KEY']

    # Remove newlines from the private key (if present)
    if 'private_key' in bigquery_creds:
        bigquery_creds['private_key'] = bigquery_creds['private_key'].replace('\\n', '\n')
    
    # Construct the BigQuery client object using the service account info
    credentials = service_account.Credentials.from_service_account_info(
        bigquery_creds,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    client = bigquery.Client(credentials=credentials, project=bigquery_creds['project_id'])

    # The dataset ID and table ID in BigQuery.
    dataset_id = 'ri_land_use_dashboard'
   

    for key, inner_dict in data.items():
        # Convert the inner dictionary to a DataFrame
        if isinstance(inner_dict, dict):
            dataframe = pd.DataFrame.from_dict(inner_dict)
            table_id = f"{dataset_id}.{key}"  # Modify this to fit your naming convention
            table_ref = f"{client.project}.{table_id}"

            job_config = bigquery.LoadJobConfig(
                autodetect=True,
                write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE  # Replace existing table
            )

            # Load the DataFrame to BigQuery
            job = client.load_table_from_dataframe(
                dataframe=dataframe,
                destination=table_ref,
                job_config=job_config
            )

            # Wait for the load job to complete
            job.result()
        else:
            print(f"Warning: The item with key '{key}' is not in the expected format and was skipped.")

    return print("Done exporting")

"""
# Assuming transformed_data is defined earlier
if transformed_data and isinstance(transformed_data, dict):
    export_data_to_big_query(transformed_data)
else:
    print("Error: The data transformation did not return the expected output.")
    """