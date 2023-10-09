# Import dependencies
import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_chrome_driver():
    """Initializes and returns a Selenium Chrome web driver using ChromeDriverManager."""
    options = Options()
    return webdriver.Chrome()

def navigate_and_print_title(driver, url):
    """Navigates to the specified URL using the given driver and prints the page title."""
    driver.get(url)
    print(driver.title)

"""
def main():
    # Set up the driver and target URL
    driver = get_chrome_driver()
    target_url = "https://www.santa-ana.org/major-planning-projects-and-monthly-development-project-reports/"
    
    # Navigate to the target URL and print the title
    navigate_and_print_title(driver, target_url)
    
    # Remember to close the driver when you're done (this step is important)
    driver.quit()

if __name__ == "__main__":
    main()
"""