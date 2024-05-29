######### Local Roll #################

LR_adminstrative_region = {
    0: 'Unknown',
    1: 'Antelope Valley',
    21: 'Newhall-Saugus',
    2: 'Canoga Park',
    3: 'Van Nuys',
    5: 'Pasadena',
    6: 'West Covina',
    8: 'Hollywood',
    9: 'Culver City',
    10: 'Bellflower',
    11: 'El Monte',
    14: 'Lomita',
    22: 'Possessory Interest',
    23: 'Central LOS ANGELES COUNTY OFFICE OF THE ASSESSOR SECURED LOCAL ROLL',
    28: 'Special Commercial Properties',
    29: 'Cost Appraisals',
    30: 'Natural Resources'
}

common_area_key = {
    "0": 'Unknown',
    "1": 'Common Area',
    "2": 'Common Area Land',
    "3": 'Common Area Improvements',
    "4": 'Non-Assessable Value',
}


gross_personal_property_key = {
    "0": 'No Personal Property',
    "1": 'Mobilehomes',
    "3": 'Computed (Landlords)',
    "4": 'Statement Value',
    "5": 'Constant Personal Property Value',
    "6": 'Statement Value: Bypass 14% Check',
    "7": 'Force-on Statement - Bypass All Checks'
    }

exemption_claim_type_key = {
    "1": 'Veteran Affidavit Received',
    "3": 'Church, All Exempt',
    "4": 'Welfare, All Exempt',
    "5": 'Religious, All Exempt',
    "6": "Church, Partially Exempt",
    "7": "Welfare, Partially Exempt",
    "8": "Religious, Partially Exempt"
    }


################### Sales List ####################

SL_adminstrative_region = {
    1: 'Lancaster (North District)',
    21: 'Santa Clarita (North District)',
    2: 'Chatsworth (North District)',
    3: 'Van Nuys (North District)',
    4: 'Glendale (Part East / Part West District)',
    5: 'Pasadena (East District)',
    6: 'West Covina (East District)',
    7: 'Santa Monica (West District)',
    9: 'Culver City (West District)',
    10: 'Long Beach (South District)',
    11: 'South El Monte (East District)',
    12: 'Norwalk (South District)',
    14: 'Lomita (South District)',
    22: 'PI',
    23: 'C-I Central',
    24: 'C-I North',
    25: 'C-I West',
    26: 'C-I South',
    27: 'C-I East',
    28: 'Special Commercial Properties',
    29: 'Cost Appraisal Section',
    30: 'Natural Resources',
    99: 'Main Office'
}


key = {
    0: 'No Address',
    1: 'Situs and Mail Narrative', 
    2: 'Situs only narrative',
    3: 'Situs and Mail Fixed Format',
    4: 'Situs only or Situs Mail Fixed Format'
}


document_type_key = {
    "AA" : "Restore only for 700 Transaction",
    "BB": "Enforceably Restricted",
    "CC": "CRS lease HSC 33673",
    "DD": "35 year lease reappraisal",
    "D": "Judicial decree or affidavit",
    "F": "Foreclosure",
    "H": "Reappraisal Transfer (no DTT)",
    "J": "Parcel Change - do not send COS",
    "L": "Less liens - reappraisal transfers less liens DTT",
    "M": "Parcel change - send COS",
    "N": "Land contract instrument",
    "P": "Probate sale",
    "R": "Correction to reappraise (formerly coded non-reappraisal)",
    "S": "Proposition 3",
    "U": "Unrecorded instrument",
    "W": "Legal entity control",
    "X": "HUD - grantor",
    "Y": "Sale for consideration - full DTT",
    "Z": "HUD - grantee",
    "A": "Excluded Transfer - no DTT",
    "B": "File correction",
    "C": "Affidavit of death of spouse",
    "E": "Excluded Transfer with DTT",
    "G": "Land contract instrument",
    "K": "Unrecorded instrument",
    "V": "Correction to reverse reappraisal",
    "X": "Produce FARS for HUD Properties",  
    "Z": "Produce FARS for HUD Properties"
    }

local_roll_types = {
    "Assessor Identification Number": "int64",
    "TaxRate Area": "int64",
    "Administrative Region Number": "int64",
    "Common Area Key": "int64",
    "Year Sold To State": "int64",
    "Recording Date": "datetime64",
    "Land Value": "int64",
    "Improvement Value": "int64",
    "Gross Personal Property Value": "int64",
    "Exemption Claim Type Key": "int64",
    "Gross Personal Property Value": "int64",
    "Fixture Value": "int64", 
    "Real Estate Exemption": "int64",
    "Personal Property Exemption": "int64",
    "Fixture Exemption Value": "int64",
    "Homeowner's Exemption": "int64", 
    "First Owner Assessee Name": "object",
    "First Owner Assessee Name Overflow": "object",
    "Second Owner Assessee Name": "object",
    "Special Name Assessee": "object",
    "Situs Address Key": "object",
    "Situs Address date of Last Change": "datetime64",
    "Situs Address Postal City Code": "int64",
    "Situs Address House Number": "int64",
    "Situs Address Fraction": "object",
    "Situs Address Direction": "object",
    "Situs Address Unit": "object",
    "Situs Address Zip Code": "int64",
    "Situs Address Street Name": "object",
    "Situs Address City and State": "object",
    "Mail Address Key": "object",
    "Mail Address date of Last Change": "datetime64",
    "Mail Address Postal City Code": "int64",
    "Mail Address House Number": "int64",
    "Mail Address Fraction": "object",
    "Mail Address Direction": "object",
    "Mail Address Unit": "object",
    "Mail Address Zip Code": "int64",
    "Mail Address Street Name": "object",
    "Mail Address City and State": "object",
    "Legal Description - Last LIne Narrative": "object",
    "Legal Description - Last LIne Lot": "object",
    "Legal Description - Last LIne Division": "object",
    "Legal Description - Last LIne Region": "object",
    "Legal Description Line One": "object",
    "Legal Description Line Two": "object",
    "Legal Description Line Three": "object",
    "Legal Description Line Four": "object",
    "Legal Description Line Five": "object",
    "Zoning Code": "object",
    "Use Code": "object",
    "Effective Year": "int64",
    "Year Built": "int64",
    "Building - Square Feet - Main": "int64",
}

################# Secured Basic (DS) ##################
impairment_key_dict = {
    0: 'None',
    2000: 'Being Made Inactive',
    3000: 'Water Company Parcel',
    4000: 'Imparied Water Company Parcel',
    5000: 'Water District Parcel',
    6000: 'Mineral Rights Separate Ownership',
    7000: 'Land Physical Impaired',
    8000: 'Land Legal Impaired Lease',
    9000: 'Within a Lease Unimpaired'
}

tax_status_dict = {
    0: 'Taxes paid not delinquent',
    1: 'Sold to state delinquent tax 1 to 5 years',
    2: 'Deeded to state delinquent tax 6 years and above',
    3: 'SBE or government owned and non assessable'
}

hazard_city_key = {
    1: 'Los Angeles City (Lot Cleaning Division)',
    2: 'Board of Supervisors of the County of Los Angeles',
    3: 'Monrovia',
    4: 'Commerce',
    5: 'Palos Verdes',
    6: 'Glendale',
    7: 'Arcadia',
    8: 'Sante Fe Springs',
    9: 'El Monte',
    10: 'La Habra Heights',
    11: 'La Verne',
    12: 'Azusa',
    13: 'Montebello'
}

document_reason_code = {
    "A": "Good Transfer - No Special Instruction",
    "1": "Interspousal 63 Exclusion",
    "B": "Parcel Change - New Owner Per Tract Map",
    "6": "Affiliated Corp. 64(b) Exclusion",
    "C": "Parcel Change - New Transferee",
    "R": "Transfer Not Changing % Interests 62(a)",
    "G": "Development Rights - Acquiring Parcels",
    "S": "Perfection of Title 62(b)",
    "H": "Development Rights - Transferring Parcels",
    "T": "Security Interest (any) 62(c)",
    "9": "Parcel Change - Mult. B.Y. (OWN-216)",
    "U": "Trust 62(d)",
    "M": "Partial Interest - Complete OWN-216",
    "V": "Grantor Retains Life Estate - Estate for Years 62(e)",
    "P": "Trustee Sale - May Not Be Market",
    "W": "Joint Tenancy 62(f), 65(c)",
    "Q": "Life Estate - Goes to Grantee",
    "Y": "Parent-Child Transfers 63.1 (Prop. 58)",
    "5": "Base Year Value Transfer (Prop. 3 - Public Taking) §68",
    "Z": "Other 's 62.1, 62.2, 66",
    "7": "Base Year Value Transfer (Prop. 50 - Disaster Taking) 69",
    "8": "Base Year Value Transfer (Prop. 60 - Senior Citizen - Age 55) 69.5",
    "D": "Parcel Change Old Owne",
    "0": "Filler - Used by Valuations"
}

tax_stat_key = {
    0: 'Taxes Paid (Not Delinquent)',
    1: 'Sold to State',
    2: 'Deeded to state (delinquent 6 years and over)',
    3: 'SBE or government owned (non-assessable)',
    4: 'Unknown'
}

exemption_claim_type = {
  '0': "Veteran number on file, no claim",
  '1': "Veteran",
  '2': "Delete veteran exemption",
  '3': "Church, wholly exempt",
  '4': "Welfare, wholly exempt",
  '5': "Full religious",
  '6': "Church, partially exempt",
  '7': "Welfare, partially exempt",
  '8': "Religious, partially exempt",
  '9': "Delete real estate exemption",
  '10': "No Exemption"
}

personal_property = {
    3: "Computed (landlords)",
    4: "Statement value",
    5: "Constant personal property value",
    6: "Bypass 14 percent check (statement)",
    7: 'Force-on statement - bypass all checks',
    0: "Unknown"
}


secured_roll_types = {
    'AIN': 'int64',
    'TRA': 'int64',
    'Agency Number': 'int64',
    'Land Roll Year': 'int64',
    'Land Current Value': 'int64',
    'Imp Current Roll Year': 'int64',
    'Imp Current Value': 'int64',
    'Situs House No': 'int64',
    'Fraction': 'object',
    'Direction': 'object',
    'Street Name': 'object',
    'Unit': 'object',
    'City State': 'object',
    'Zip': 'int64',
    'Mail House No': 'int64',
    'M Fraction': 'object',
    'M Direction': 'object',
    'M Street Name': 'object',
    'M Unit': 'object',
    'M City State': 'object',
    'M Zip': 'int64',
    'First Owner Name': 'object',
    'First Owner Name Overflow': 'object',
    'Special Name Legend': 'object',
    'Special Name Assessee': 'object',
    'Second Owner Name': 'object',
    'Recording Date': 'datetime64',
    'Tax Stat Key': 'int64',
    'Year Sold to State': 'int64',
    'Hazard City Key': 'int64',
    'Hazard Info': 'object',
    'Zoning Code': 'object',
    'Use Code': 'object',
    'Partial Interest': 'int64',
    'Doc Reason Code': 'object',
    #'Ownership Code': 'object',
    'Exemption Type': 'int64',
    'PP Key': 'int64',
    'PP Value': 'int64',
    'PP Exemption Val': 'int64',
    'Fixture Val': 'int64',
    'Fixture Exemption Val': 'int64',
    'Num Howmowner Exemption': 'int64',
    'Homeowner Exemption Val': 'int64',
    'Real Estate Exemption Val': 'int64',
    'Last Sale Verif Key': 'int64',
    'Last Sale Amount': 'int64',
    'Last Sale Date': 'datetime64',
    'Sale Two Verif Key': 'int64',
    'Sale Two Amount': 'int64',
    'Sale Two Date': 'datetime64',
    'Sale Three Verif Key': 'int64',
    'Sale Three Amount': 'int64',
    'Sale Three Date': 'datetime64',
    'BD1 Subpart': 'int64',
    'BD1 Design': 'int64',
    'BD1 Quality': 'int64',
    'BD1 Year Built': 'int64',
    'BD1 Units': 'int64',
    'BD1 Bedrooms': 'int64',
    'BD1 Baths': 'int64',
    'BD1 Square Feet': 'int64',
    'BD2 Subpart': 'int64',
    'BD2 Design': 'int64',
    'BD2 Quality': 'int64',
    'BD2 Year Built': 'int64',
    'BD2 Units': 'int64',
    'BD2 Bedrooms': 'int64',
    'BD2 Baths': 'int64',
    'BD2 Square Feet': 'int64',
    'BD3 Subpart': 'int64',
    'BD3 Design': 'int64',
    'BD3 Quality': 'int64',
    'BD3 Year Built': 'int64',
    'BD3 Units': 'int64',
    'BD3 Bedrooms': 'int64',
    'BD3 Baths': 'int64',
    'BD3 Square Feet': 'int64',
    'BD4 Subpart': 'int64',
    'BD4 Design': 'int64',
    'BD4 Quality': 'int64',
    'BD4 Year Built': 'int64',
    'BD4 Units': 'int64',
    'BD4 Bedrooms': 'int64',
    'BD4 Baths': 'int64',
    'BD4 Square Feet': 'int64',
    'BD5 Subpart': 'int64',
    'BD5 Design': 'int64',
    'BD5 Quality': 'int64',
    'BD5 Year Built': 'int64',
    'BD5 Units': 'int64',
    'BD5 Bedrooms': 'int64',
    'BD5 Baths': 'int64',
    'BD5 Square Feet': 'int64',
    'Legal First Line': 'object',
    'Legal Second Line': 'object',
    'Legal Third Line': 'object',
    'Legal Fourth Line': 'object',
    'Legal Fifth Line': 'object',
    'Legal Last Line': 'object',
    'Land Base Year': 'int64',
    'Imp Base Year': 'int64',
    'Land Base Val': 'int64',
    'Imp Base Val': 'int64',
    "Cluster Location": "int64",
    "Cluster Type": "int64",
    "Cluster Appraisal Unit": "int64",
    "Land Reason Key": "int64",
    "Impairment Key": "int64",
    "DDT Amount": "int64",
    "BD1 Year Change": "int64",
    "BD1 Unit Cost": "int64",
    "BD1 RCN Main": "int64",
    "BD2 Year Change": "int64",
    "BD2 Unit Cost": "int64",
    "BD2 RCN Main": "int64",
    "BD3 Year Change": "int64",
    "BD3 Unit Cost": "int64",
    "BD3 RCN Main": "int64",
    "BD4 Year Change": "int64",
    "BD4 Unit Cost": "int64",
    "BD4 RCN Main": "int64",
    "BD5 Year Change": "int64",
    "BD5 Unit Cost": "int64",
    "BD5 RCN Main": "int64",
    "Landlord Reappraisal Year": "int64",
    "Landlord Units": "int64",
    "First Transfree Name": "object",
    "First Transfree Overflow": "object",
    "Second Transfree Name": "int64",
    "Document Key": "int64",
    "Document Number": "int64"
}


impairment_key_dict = {
    0: 'Not Impaired',
    2000: 'Being Made Inactive',
    3000: 'Water Company Parcel',
    4000: 'Imparied Water Company Parcel',
    5000: 'Water District Parcel',
    6000: 'Mineral Rights Separate Ownership',
    7000: 'Land Physical Impaired',
    8000: 'Land Legal Impaired Lease',
    9000: 'Within a Lease Unimpaired'
}

tax_status_dict = {
    0: 'Taxes paid not delinquent',
    1: 'Sold to state delinquent tax 1 to 5 years',
    2: 'Deeded to state delinquent tax 6 years and above',
    3: 'SBE or government owned and non assessable'
}
################# Sales List ##################
sales_list_types = {
    "Assessor Identification Number": "int64",
    "Administrative Region": "int64",
    "Cluster Code": "int64",
    "Key": "int64",
    "House Number": "int64",
    "Direction": "object",
    "street name": "object",
    "first owner": "object",
    "first owner tr": "object",
    "use code": "object",
    "Reorders": "int64",
    "zone": "object",
    "transferee": "datetime64",
    "doc type": "object",
    "dtt type": "object",
    "dttt amount": "int64",
    "asss rec": "datetime64",
    "bdl1 yb": "int64",
    "bdl1 eff y": "int64",
    "bdl1 bath": "int64",
    "bdl1 bed": "int64",
    "design ty": "object",
    "bdl1 sq ft": "int64",
    "last sale1 ver": "int64",
    "last 1 sale date": "datetime64",  # Assuming it's stored as a string for now
    "last 1 amount": "int64",
    "2 verification": "int64",
    "2 dat": "datetime64",  # Assuming it's stored as a string for now
    "2 amoun": "int64",
    "3 verif": "int64",
    "3 sal da": "datetime64",  # Assuming it's stored as a string for now
    "3 sal amou": "int64",
    "fill": "object"
}


################# Land Use/Hazards ##################
hazard_column_types = {
    "EPA_BROWN_NAME": "object",
    "EPA_BROWN_TYPE": "object",
}

land_use_column_types = {
    "LAND_USE_SOURCE_2019": "object",
    "EPA_BROWN_NAME": "object",
    "EPA_BROWN_TYPE": "object",
    "RI_DEM_GEO_ID_20": "int64",
    "APN_DUP": "int64",
    "IMPROVEMENT_RATIO": "float64",
    "LAND_USE_SOURCE_2019": "object",
    "RI_UNIQUE_PARCEL_ID_2016": "int64",
    "SP_INDEX": "int64",
    "BUILDING_SQFT": "float64",
}


DS_unknown_object_columns = ['Fraction', 'Direction', 'Street Name', 'Unit', 'City State', 'M Fraction', 'M Direction', 'M Street Name', 'M Unit', 'M City State', 
'First Owner Name Overflow', 'Special Name Assessee', 'Second Owner Name', 'Use Code', 'BD1 Quality',
'BD2 Quality', 'BD3 Quality', 'BD4 Quality', 'BD5 Quality', 'BD1 Design', 'BD2 Design', 'BD3 Design', 
'BD4 Design', 'BD5 Design', 'Legal First Line', 'Legal Second Line', 'Legal Third Line', 'Legal Fourth Line',
'Legal Fifth Line', 'Legal Last Line', 'Land Reason Key', 'Impairment Key', 'First Transfree Overflow', 'Second Transfree Name']

SL_unknown_object_columns = [ 'Direction', 'street name', 'first owner', 'first owner tr', 'use code', 'zone', 'doc type', 'design ty', 'last sale1 ver', '2 verification', '3 verif'] 

LR_unknown_object_columns = ['First Owner Assessee Name', 'First Owner Assessee Name Overflow', 'Second Owner Assessee Name', 'Special Name Assessee', 'Situs Address Key', 'Situs Address Fraction', 'Situs Address Direction', 
'Situs Address Street Name', 'Situs Address City and State', 'Mail Address Key', 'Mail Address Unit', 'Situs Address Unit', 'Mail Address Direction', 'Mail Address Fraction', 'Mail Address Street Name', 'Mail Address City and State',
'Legal Description - Last LIne Narrative', 'Legal Description - Last LIne Lot', 'Legal Description - Last LIne Division', 'Legal Description - Last LIne Region', 'Legal Description Line One', 
'Legal Description Line Two', 'Legal Description Line Three', 'Legal Description Line Four', 'Legal Description Line Five', 'Zoning Code', 'Use Code']

DS_datetime_columns = ['Recording Date', 'Last Sale Date', 'Sale Two Date', 'Sale Three Date']

SL_datetime_columns = ['transferee', 'last 1 sale date', '2 dat', '3 sal da']

LR_datetime_columns = ['Recording Date', 'Situs Address date of Last Change', 'Mail Address date of Last Change']

# rename columns, add a county column, and drop columns that are not needed
DS_columns_to_drop = ['Special Name Legend', 'Ownership Code', 'Special Name Assessee', 'Hazard City Key', 'Hazard Info', 'Fraction', 'Direction','M Fraction', 'M Direction', 'M Street Name', 'M Unit', 'M City State', 'M Zip', 'Mail House No']
DS_columns_to_rename = ['ain', 'TRA', 'BD1 Subpart', 'BD1 Design', 'BD1 Quality', 'BD1 Year Built', 'BD1 Units', 'BD1 Bedrooms', 'BD1 Baths', 'BD1 Square Feet', 'BD2 Subpart', 'BD2 Design', 'BD2 Quality', 
                        'BD2 Year Built', 'BD2 Units', 'BD2 Bedrooms', 'BD2 Baths', 'BD2 Square Feet', 'BD3 Subpart', 'BD3 Design', 'BD3 Quality', 'BD3 Year Built', 'BD3 Units', 'BD3 Bedrooms', 'BD3 Baths', 
                        'BD3 Square Feet', 'BD4 Subpart', 'BD4 Design','BD4 Quality', 'BD4 Year Built', 'BD4 Units', 'BD4 Bedrooms', 'BD4 Baths', 'BD4 Square Feet', 'BD5 Subpart', 'BD5 Design', 'BD5 Quality', 'BD5 Year Built',
                        'BD5 Units', 'BD5 Bedrooms', 'BD5 Baths', 'BD5 Square Feet''BD1 Year Change', 'BD1 Unit Cost', 'BD1 RCN Main', 'BD2 Year Change', 'BD2 Unit Cost', 'BD2 RCN Main', 'BD3 Year Change', 'BD3 Unit Cost', 'BD3 RCN Main', 'BD4 Year Change', 
                        'BD4 Unit Cost', 'BD4 RCN Main', 'BD5 Year Change', 'BD5 Unit Cost', 'BD5 RCN Main']

DS_renamed_columns = ['assessor_identification_number', 'taxrate_area', 'Building Subpart 1', 'Building Design 1', 'Building Quality 1', 'Building Year Built 1', 'Building Units 1', 'Building Bedrooms 1', 'Building Baths 1', 'Building Square Feet 1', 'Building Subpart 2', 'Building Design 2', 'Building Quality 2',
                      'Building Year Built 2', 'Building Units 2', 'Building Bedrooms 2', 'Building Baths 2', 'Building Square Feet 2', 'Building Subpart 3', 'Building Design 3', 'Building Quality 3', 'Building Year Built 3', 'Building Units 3', 'Building Bedrooms 3', 'Building Baths 3',
                      'Building Square Feet 3', 'Building Subpart 4', 'Building Design 4', 'Building Quality 4', 'Building Year Built 4', 'Building Units 4', 'Building Bedrooms 4', 'Building Baths 4', 'Building Square Feet 4', 'Building Subpart 5', 'Building Design 5', 'Building Quality 5'
                      'Building Year Built 5', 'Building Units 5', 'Building Bedrooms 5', 'Building Baths 5', 'Building Square Feet 5', 'Building Year Change 1', 'Building Unit Cost 1', 'Building RCN Main 1', 'Building Year Change 2', 'Building Unit Cost 2', 'Building RCN Main 2',
                      'Building Year Change 3', 'Building Unit Cost 3', 'Building RCN Main 3', 'Building Year Change 4', 'Building Unit Cost 4', 'Building RCN Main 4', 'Building Year Change 5', 'Building Unit Cost 5', 'Building RCN Main 5']


SL_columns_to_drop = ['fill', 'Direction', 'dttt amount']
SL_columns_to_rename = ['first owner tr', 'bdl1 eff y', 'asss rec', 'bdl1 yb', 'bdl1 eff y', 'bdl1 bath', 'bdl1 bed', 'design ty', 'bdl1 sq ft', 'last sale1 ver', 'last 1 sale date', 'last 1 amount', '2 verification', '2 dat', '2 amoun', '3 verif', '3 sal da', '3 sal amou']

SL_renamed_columns = ['First Owner Transfer', 'Building Effective Year', 'Assessee Recording Date', 'Building Year Built 1', 'Building Effective Year 1', 'Building Baths 1', 'Building Bedrooms 1', 'Design Type', 'Building Square Feet', 'Last Sale Verification', 'Last Sale Date', 'Last Sale Amount', 'Second Sale Verification', 'Second Sale Date', 'Second Sale Amount', 'Third Sale Verification', 'Third Sale Date', 'Third Sale Amount']


LR_columns_to_drop = ['Mail Address Unit', 'Mail Address Zip Code', 'Mail Address Street Name', 'Mail Address City and State', 'Mail Address Key', 'Mail Address date of Last Change', 'Mail Address Postal City Code', 'Mail Address House Number', 'Mail Address Fraction', 'Mail Address Direction',
                      'Situs Address Fraction', 'Situs Address Direction', 'Filler']
LR_columns_to_rename = ['Situs Address Key', 'Situs Address date of Last Change', 'Situs Address Postal City Code', 'Situs Address House Number',
                         'Situs Address Fraction', 'Situs Address Direction', 'Situs Address Unit', 'Situs Address Zip Code', 'Situs Address Street Name', 'Situs Address City and State',
                         'Building - Square Feet - Main', 'Legal Description - Last LIne Narrative', 'Legal Description - Last LIne Lot', 'Legal Description - Last LIne Division',	'Legal Description - Last LIne Region']

LR_renamed_columns = ['Address Key', 'Address Date of Last Change', 'Postal City Code', 'Situs House Number', 'Address Fraction', 'Address Direction', 'Unit', 'Zip', 'Street Name', 'City', 'Main Building Square Feet', 'Legal Description Narrative', 'Legal Description Lot', 'Legal Description Division', 'Legal Description Region']
