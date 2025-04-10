import unittest
import pandas as pd

# Function to test: checking if a DataFrame contains required columns
def validate_columns(df, required_columns):
    return all(col in df.columns for col in required_columns)

class TestLoanData(unittest.TestCase):
    def setUp(self):
        # Sample test data
        self.test_df = pd.DataFrame({
            "Register Code": ["BOR123", "BOR456"],
            "Id Borrower Loan": ["LN789", "LN012"],
            "Bio Fullname": ["Alice", "Bob"],
            "Pinjaman": [5000, 10000]
        })
    
    def test_validate_columns_success(self):
        required_columns = ["Register Code", "Id Borrower Loan", "Bio Fullname", "Pinjaman"]
        self.assertTrue(validate_columns(self.test_df, required_columns))

    def test_validate_columns_failure(self):
        required_columns = ["Register Code", "Id Borrower Loan", "Bio Fullname", "Tenor"]
        self.assertFalse(validate_columns(self.test_df, required_columns))

if __name__ == '__main__':
    unittest.main()