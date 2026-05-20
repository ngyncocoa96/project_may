import unittest

from src.data.file_handler import load_records


class TestFileHandler(unittest.TestCase):

    def test_load_records_returns_list(self):
        records = load_records()
        self.assertIsInstance(records, list)


if __name__ == "__main__":
    unittest.main()