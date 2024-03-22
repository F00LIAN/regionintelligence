import unittest

import unittest
from src.scrape import (remove_unwanted_tags, 
                        extract_tags, 
                        remove_unnecessary_lines,
                        append_prefix_to_agenda_link,
                        filter_commissions,
                        ascrape_playwright)


class TestScraper1(unittest.TestCase):
    # Create Example Input to test the functions
    def setUp(self):
        self.html_content = "<html><body><h1>Test input</h1></body></html>"
        self.tags = ["td", "span", "a"]
        self.commissions = [{"commission_name": "Test Commission", "agenda_link": "Test link"}]
    
    # Test case for remove_unwanted_tags
    def test_extract_tags(self):
        # Test case for my_function
        expected = "Expected output"
        result = remove_unwanted_tags("Test input")
        self.assertEqual(result, expected)
    
    def test_extract_tags(self):
        # Test case for my_function
        expected = "Expected output"
        result = extract_tags("Test input")
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()