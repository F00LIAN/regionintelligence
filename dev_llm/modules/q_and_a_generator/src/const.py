from transformers import AutoTokenizer, AutoModel



CALIFORNIA_UPCODES_URL = "https://up.codes/codes/california"
LOS_ANGELES_UPCODES_URL = "https://up.codes/codes/los_angeles"
LOS_ANGELES_COUNTY_UPCODES_URL = "https://up.codes/codes/los-angeles-county"
SAN_FRANCISCO_UPCODES_URL = "https://up.codes/codes/san_francisco"
SAN_JOSE_UPCODES_URL = "https://up.codes/codes/san-jose"


# tokenizer and LLM we use to embed the document text
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")