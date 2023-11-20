import re 
import sys 
sys.path.append('/Projects/regionintelligence/apn_insights/')
import pandas as pd 
import requests
from src.const import zoning_dict_2016
import pandas as pd
from os import path
import yaml
from pandas import DataFrame
from google.oauth2 import service_account
from google.cloud import bigquery

def grab_apn_from_csv():
    url = 'https://storage.googleapis.com/ri-lnd-use/2019_RI_LAND_USE.csv'
    df = pd.read_csv(url)
    print('Done Extracting')
    return df
df = grab_apn_from_csv()