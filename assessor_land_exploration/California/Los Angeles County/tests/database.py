import unittest
from src.load import upload_to_sql
from src.paths import FINAL_DATA_DIR
import pandas as pd
from src.load import engine

class DatabaseTestCase(unittest.TestCase):
    def test_data_upload(self):
        """ Test data upload to the test database. """
        df = pd.read_csv(FINAL_DATA_DIR / 'sales_list_transformed.csv')
        upload_to_sql(df, 'sales_list')
        # Query the table
        with engine.connect() as connection:
            result = connection.execute("SELECT COUNT(*) FROM sales_list").fetchone()
            self.assertEqual(result[0], df.shape[0])

if __name__ == '__main__':
    unittest.main()