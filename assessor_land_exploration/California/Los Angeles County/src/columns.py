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
