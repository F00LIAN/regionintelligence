
# create a dictionary of city names and their respective website prefixes (legistar websites)
legistar_website_links = {
    "Fullerton, CA": "https://fullerton.legistar.com/Calendar.aspx",
    "Costa Mesa, CA": "https://costamesa.legistar.com/Calendar.aspx",
    "Orange, CA": "https://cityoforange.legistar.com/Calendar.aspx",
    "Corona, CA": "https://corona.legistar.com/Calendar.aspx",
    "Culver City, CA": "https://culver-city.legistar.com/Calendar.aspx",
    "Riverside, CA": "https://riversideca.legistar.com/Calendar.aspx",
}

primegov_website_links = {
    "Long Beach, CA": "https://longbeach.primegov.com/public/portal",
    "Santa Ana, CA": "https://santa-ana.primegov.com/public/portal",
    "Menifee, CA":  "https://cityofmenifee.primegov.com/public/portal",
    "Victorville, CA": "https://victorvilleca.primegov.com/public/portal" 
    }

city_website_prefix_links = {
    "Fullerton, CA": "https://fullerton.legistar.com/",
    "Costa Mesa, CA": "https://costamesa.legistar.com/",
    "Orange, CA": "https://cityoforange.legistar.com/",
    "Corona, CA": "https://corona.legistar.com/",
    "Culver City, CA": "https://culvercity.legistar.com/", 
    "Riverside, CA": "https://riversideca.legistar.com/",
    "Santa Ana, CA": "https://santa-ana.primegov.com",
    "Long Beach, CA": "https://longbeach.primegov.com",
    "Menifee, CA": "https://cityofmenifee.primegov.com",
    "Victorville, CA": "https://victorvilleca.primegov.com",
}


tags = [{"name": "td"},
        {"name": "a"}]

"""tags = [{"name": "div"},
        {"name": "td", "class":" meeting-title bodyTextColour"},
        {"name": "a", "class": "dropdown-document-0"},
        {"name": "a", "class": "dropdown-document-1"},
        {"name": "a", "class": "dropdown-document-2"}]"""

"""tags = [{"name": "td", "class": " meeting-title bodyTextColour"},
        {"name": "td", "class": "bodyTextColour sorting_1"},
        {"name", "td", "class", "bodyTextColour"}, 
        {"name": "a", "class": "dropdown-document-1"},
        {"name": "a", "class": "dropdown-document-2"}]"""

_EXTRACTION_TEMPLATE = """
Extract and save the relevant entities mentioned\
in the following passage together with their properties.

Only extract the properties mentioned in the 'information_extraction' function.

If a property is not present and is not required in the function parameters, do not include it in the output.

Passage:
{input}
""" 
# {"name": "div", "class": "meeting-title bodyTextColour"}