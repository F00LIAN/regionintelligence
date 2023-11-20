import pandas as pd
import requests
from src.const import zoning_dict_2016

def clean_transform_csv(df, *args, **kwargs): 
    """
    Template to clean and transform data from the extraction from api
    """
    def map_zoning_codes(df, zoning_code_column, zoning_dict, column_name):
       """
       Maps zoning codes to their descriptions in a DataFrame.

       Parameters:
       df (DataFrame): The pandas DataFrame containing the data.
       zoning_code_column (str): The name of the column with zoning codes.
       zoning_dict (dict): The dictionary mapping zoning codes to descriptions.

       Returns:
       DataFrame: The DataFrame with an additional column for zoning descriptions.
       """
       # Convert values to strings, strip whitespaces, and replace non-numeric values with NaN
       df[zoning_code_column] = pd.to_numeric(df[zoning_code_column].astype(str).str.strip(), errors='coerce')

       # Convert non-null values to integers
       df.loc[df[zoning_code_column].notnull(), zoning_code_column] = df[zoning_code_column].dropna().astype('int64')

       # Map the zoning codes to descriptions
       df[column_name] = df[zoning_code_column].map(zoning_dict)

       return df
    
    # Replace non-numeric values (like a space ' ') with NaN
    df['LAND_USE_2016'] = pd.to_numeric(df['LAND_USE_2016'], errors='coerce')
    df['LAND_USE_2016'].fillna(9999, inplace=True)
    df['LAND_USE_2016'] = df['LAND_USE_2016'].astype('int64')

    ## Create logic to fill null values for LAND_USE_2019 with a value from LAND_USE_2016, if available, else 9999
    df['LAND_USE_2019'] = pd.to_numeric(df['LAND_USE_2019'], errors='coerce')
    df['LAND_USE_2019'].fillna(df['LAND_USE_2016'], inplace=True)
    df['LAND_USE_2019'] = df['LAND_USE_2019'].astype('int64')


    strings = ['vcfcd', 'opnspc', 'nap', 'drain', 'common_p', 'common-p', 'common']

    ## Replace the string values with 00 and convert the column to int64
    df.APN_RAW_2019.replace(strings, '00', inplace=True)
    df.APN_RAW_2019.fillna('000000000', inplace=True)

    is_non_numeric = pd.to_numeric(df['APN_RAW_2019'], errors='coerce').isna()
    non_numeric_values = df[is_non_numeric]

    df.loc[is_non_numeric, 'APN_RAW_2019'] = 0
    df.APN_RAW_2019 = df.APN_RAW_2019.astype('int64')




    ## Replace the null values with 00 and convert the column to int64
    df.APN.fillna('00000', inplace=True)
    df.APN.replace(strings, '00000', inplace=True)

    is_non_numeric = pd.to_numeric(df['APN'], errors='coerce').isna()
    non_numeric_values = df[is_non_numeric]
    
    df.loc[is_non_numeric, 'APN'] = 0
    df.APN = df.APN.astype('int64')
    
    ## Map the LAND_USE_CLASS_NAME to the dictionary zoning_dict_2016
    df = map_zoning_codes(df, 'LAND_USE_2019', zoning_dict_2016, 'LAND_USE_CLASS_NAME')

     # Assuming 'zoning_code' is the name of your column with the codes
    df = map_zoning_codes(df, 'RI_ZONE_CODE', zoning_dict_2016, 'RI_ZONE_CODE_DESC_2016')
    df = map_zoning_codes(df, 'RI_GP_CODE', zoning_dict_2016, 'RI_GP_CODE_DESC_2016')
    
    
    # turn null values into strings called 'Unknown'
    df.loc[df['LAND_USE_SOURCE_2019'].apply(type) == float, 'LAND_USE_SOURCE_2019'] = 'Unknown'
    
    # turn null values into strings called 'Unknown'
    df.loc[df.CITY_GP_CODE.apply(type) == float, 'CITY_GP_CODE'] = 'Unknown'
    df.loc[df.CITY_SP_CODE.apply(type) == float, 'CITY_SP_CODE'] = 'Unknown'
    
    ## Print the string values in the column that are not nulL 
    df.loc[df.RI_SP_CODE.apply(type) == float, 'RI_SP_CODE'] = 9999
    df['RI_SP_CODE'] = pd.to_numeric(df['RI_SP_CODE'], errors='coerce')
    df['RI_SP_CODE'].fillna(9999, inplace=True)
    df['RI_SP_CODE'] = df['RI_SP_CODE'].astype('int64')
    
    ## Print the string values in the column that are not nulL 
    df.loc[df.CITY_ZONE_CODE.apply(type) == float, 'CITY_ZONE_CODE'] = 'Unknown'
    ## Print the string values in the column that are not nulL 
    df.loc[df.PUB_AGENCY_NAME.apply(type) == float, 'PUB_AGENCY_NAME'] = 'Unknown'
    ## Print the string values in the column that are not nulL 
    df.loc[df.PUBLIC_TYPE.apply(type) == float, 'PUBLIC_TYPE'] = 'Unknown'
    df.loc[df.PUBLIC_SOURCE.apply(type) == float, 'PUBLIC_SOURCE'] = 'Unknown'
    df.loc[df.EPA_BROWN_NAME.apply(type) == float, 'EPA_BROWN_NAME'] = 'Unknown'
    df.loc[df.EPA_BROWN_TYPE.apply(type) == float, 'EPA_BROWN_TYPE'] = 'Unknown'
    df.loc[df.OPPORTUNITY_LEVEL.apply(type) == float, 'OPPORTUNITY_LEVEL'] = 'Unknown'
    df.loc[df.RI_ZONE_CODE_DESC_2016.apply(type) == float, 'RI_ZONE_CODE_DESC_2016']  = 'Unknown'
    df.loc[df.RI_GP_CODE_DESC_2016.apply(type) == float, 'RI_GP_CODE_DESC_2016']  = 'Unknown'
    
    
    # Match full_df with df
    full_df = df

    # Separate main df into different tables
    parcel_columns = ['RI_PARCEL_ID', 'LAND_USE_2019', 'LAND_USE_SOURCE_2019', 'LAND_USE_2016', 'LAND_USE_CLASS_NAME', 'APN_RAW_2019', 'APN', 'ACREAGE', 'SLOPE', 'MULTIPART', 'STACK', 'Shape_Length', 'Shape_Area', 'Centroid_X', 'Centroid_Y']
    parcel_df = full_df[parcel_columns]
    parcel_df.reset_index(drop=True, inplace=True)

    # Separate main df into different tables
    building_columns = ['RI_PARCEL_ID', 'UNBUILT_SF', 'BUILDING_SQFT', 'IMPROVEMENT_RATIO', 'ADU_SPACE_POSSIBILITY', 'SETBACK_REDUCTION_ADU', 'SMALL_ADU_POSSIBILITY', 'PARKING_EXEMPTION_ADU', 'SETBACK_SMALL_ADU', 'SETBACK_PARKING_ADU', 'SMALL_PARKING_ADU', 'SETBACK_SMALL_PARKING_ADU']
    building_df = full_df[building_columns]
    building_df.reset_index(drop=True, inplace=True)

    # Separate main df into different tables  
    city_columns = ['RI_PARCEL_ID', 'CITY_ID', 'CITY_NAME']
    city_df = full_df[city_columns]
    city_df.reset_index(drop=True, inplace=True)

    # Separate main df into different tables
    county_columns = ['RI_PARCEL_ID', 'RI_COUNTY_ID', 'COUNTY_NAME']
    county_df = full_df[county_columns]
    county_df.reset_index(drop=True, inplace=True)

    # Separate main df into different tables
    commdev_columns = ['RI_PARCEL_ID', 'RI_COUNTY_ID', 'CITY_ID', 'URBANIZED_AREA', 'GROCERY_1_MILE', 'HEALTHCARE_1_MILE', 'OPENSPACE_1_MILE', 'OPPORTUNITY_LEVEL', 'HIGH_QUALITY_TRANSIT_AREA', 'JOB_CENTER', 'NEIGHBORHOOD_MOBILITY_AREA', 'ABSOLUTE_CONSTRAINT', 'VARIABLE_CONSTRAINT', 'ENVIRONMENT_JUSTICE_AREA', 'DISADVANTAGED_COMMUNITY_AREA', 'COMMUNITY_OF_CONCERN']
    commdev_df = full_df[commdev_columns]
    commdev_df.reset_index(drop=True, inplace=True)

    # Separate main df into different tables
    envhaz_columns = ['RI_PARCEL_ID', 'CITY_ID', 'RI_COUNTY_ID', 'FLOOD_PLAIN_ZONE', 'EQUAKE_ZONE', 'FIRE_HAZARD', 'PROTECTED_AREA', 'RIVER_WETLAND_AREA', 'WILDLIFE_AREA', 'WETLAND_AREA', 'CNDDB_RARE_SPECIES_AREA', 'HABITAT_RESERVE_AREA', 'LIQUAFACTION_ZONE', 'LANDSLIDE_ZONE', 'SEARISE_1_METER', 'SEARISE_2_METER']
    envhaz_df = full_df[envhaz_columns]
    envhaz_df.reset_index(drop=True, inplace=True)

    # Separate main df into different tables
    zone_columns = ['RI_PARCEL_ID', 'CITY_ID', 'CITY_GP_CODE', 'CITY_SP_CODE', 'RI_GP_CODE', 'RI_GP_CODE_DESC_2016', 'RI_SP_CODE', 'CITY_ZONE_CODE', 'RI_ZONE_CODE', 'RI_ZONE_CODE_DESC_2016'] 
    zone_df = full_df[zone_columns]
    zone_df.reset_index(drop=True, inplace=True)

    return {
    "parcel_df": parcel_df.to_dict(orient="dict"),
    "building_df": building_df.to_dict(orient="dict"),
    "city_df": city_df.to_dict(orient="dict"),
    "county_df": county_df.to_dict(orient="dict"),
    "commdev_df": commdev_df.to_dict(orient="dict"),
    "envhaz_df": envhaz_df.to_dict(orient="dict"),
    "zone_df": zone_df.to_dict(orient="dict")
}, print("done transforming")

def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block
    """
    assert output is not None, "Output is undefined"

#transformed_data, _= clean_transform_csv(df)