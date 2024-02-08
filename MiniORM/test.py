import unittest
from unittest.mock import MagicMock
from SimpleORM import *


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = Database("postgres", "pedramkarimi",
                            "pedramkarimi", "localhost", "5432") # noqa

    def test_connect(self):
        mock_connect = MagicMock()
        psycopg2.connect = mock_connect
        self.db.connect()
        mock_connect.assert_called_once_with(database="postgres", user="pedramkarimi",
                                             password="pedramkarimi", host="localhost", port="5432")

    def test_disconnect(self):
        self.db.connection = MagicMock()
        self.db.disconnect()
        self.db.connection.close.assert_called_once()

    def test_execute_query(self):
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_cursor.execute = MagicMock()
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        self.db.connection = mock_connection
        self.assertEqual(self.db.execute_query("SELECT * FROM simple"), 1) # noqa

    def test_create_table_query(self):
        self.db.execute_query = MagicMock(return_value=1)
        self.db.create_table_query()
        self.db.execute_query.assert_called_once()

    def test_insert_data(self):
        self.db.execute_query = MagicMock(return_value=1)
        self.assertEqual(self.db.insert_data("pedram", 30, "python", "maktab105"), 1)

    def test_select_data(self):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [(1, "pedram", 30, "python", "maktab105")]
        mock_cursor.execute = MagicMock()
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        self.db.connection = mock_connection
        self.db.select_data()
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchall.assert_called_once()

    def test_update_data(self):
        self.db.execute_query = MagicMock(return_value=1)
        self.assertEqual(self.db.update_data(123, 31), 1)

    def test_delete_data(self):
        self.db.execute_query = MagicMock(return_value=1)
        self.assertEqual(self.db.delete_data(123), 1)


if __name__ == "__main__":
    unittest.main()
