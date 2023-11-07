**1. Scripts contain the ETL Process**: Run parallel_scraper.py to run the extract process. The transform code is experimental still, however the map_notebook contains the code to transform the data under 01_find_insights.ipynb. 


## City Notes of Improvement of Listings

- **System Functionality** 
We should verify that we can access the most recent data for every call. So there are no duplicates and we are not missing any data. Therefore when we call the API we should be able to get the most recent data.

- **City 1**: Santa Ana, Ca

We can try and extract the images for each listing so we can use for the website listings and host images on the map. 

- **City 2**: Orange, Ca

We need to fill in the gaps of the parsing status of the PDF, the PDF can potentially be parsed again. So far it does a 85% decent job of parsing but we have to create scripts to parse and clean further. Even then it does not complete the entire job. 

- **City 3**: Anaheim, Ca

The data is already pretty clean and organized, we only need to find a way to automate the process of acquiring the data as it is currently done manually. Selenium seems to fail with this. 

Anaheim has weekly information on recent submitted applications. We can potentially use this as a resource to get the most recent data. This would be a future task. 

- **City 4**: Irvine, Ca

Irvine's current planning department has a list of projects that are recently submitted. The link is here: https://www.cityofirvine.org/community-development/planning-and-development. The list does not contain the status of each individual project and it is missing a few project locations. 

If you look at the main irvine page on the left sidebar. The left sidebar has a few "Planning Areas", I imagine these areas are currently in under review for development. We can use this as a resource to get the most recent data. This would be a future task.

Also we need to call and determine if the major development projects are still in progress or if they have been completed. 

- **City 5**: Huntington Beach, Ca

Huntington Beach has quite a few projects that are listed on their website. The data is very detailed. Enough to draw insights from. Project Images may have to be from satellite view. 

- **City 6**: Garden Grove, Ca

Garden grove was also really complete with their data. They have a list of projects that are currently in progress. The data is very detailed. Enough to draw insights from. Project Images may have to be scraped.

- **City 7**: Fullerton, Ca

Fullerton data was also very complete. They have a list of projects that are currently in progress. The data is very detailed. Enough to draw insights from. Project Images may have to be scraped.

- **City 8**: Costa Mesa, Ca

The city website does not have any information to draw insights from. We may have to circle back on this in the future. 


## Contact

For more details or business inquiries, please visit [Region Intelligence's Official Website](www.regionintelligence.com).


