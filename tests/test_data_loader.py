import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from data.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.mock_db_conn = MagicMock()
        self.data_loader = DataLoader(self.mock_db_conn)

    @patch('scrap_env.data.data_loader.pd.read_sql_query')
    def test_load_books_df_success(self, mock_read_sql_query):
        # Setup mock return value
        mock_df = pd.DataFrame({'title': ['Book1', 'Book2'], 'author': ['Author1', 'Author2']})
        mock_read_sql_query.return_value = mock_df

        # Call the method
        result = self.data_loader.load_books_df()

        # Assertions
        mock_read_sql_query.assert_called_once_with("SELECT * FROM books", self.mock_db_conn)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertIn('title', result.columns)
        self.assertIn('author', result.columns)

    @patch('scrap_env.data.data_loader.pd.read_sql_query')
    def test_load_books_df_failure(self, mock_read_sql_query):
        # Setup mock to raise an exception
        mock_read_sql_query.side_effect = Exception("Database error")

        # Call the method
        result = self.data_loader.load_books_df()

        # Assertions
        mock_read_sql_query.assert_called_once_with("SELECT * FROM books", self.mock_db_conn)
        self.assertIsNone(result)

    @patch('scrap_env.data.data_loader.pd.read_sql_query')
    def test_load_table_success(self, mock_read_sql_query):
        # Setup mock return value
        mock_df = pd.DataFrame({'column1': [1, 2], 'column2': [3, 4]})
        mock_read_sql_query.return_value = mock_df

        # Call the method
        result = self.data_loader.load_table('test_table')

        # Assertions
        mock_read_sql_query.assert_called_once_with("SELECT * FROM test_table", self.mock_db_conn.conn)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertIn('column1', result.columns)
        self.assertIn('column2', result.columns)

    @patch('scrap_env.data.data_loader.pd.read_sql_query')
    def test_load_table_failure(self, mock_read_sql_query):
        # Setup mock to raise an exception
        mock_read_sql_query.side_effect = Exception("Database error")

        # Call the method
        result = self.data_loader.load_table('test_table')

        # Assertions
        mock_read_sql_query.assert_called_once_with("SELECT * FROM test_table", self.mock_db_conn.conn)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()