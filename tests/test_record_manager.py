import unittest
from unittest.mock import patch

from src.data.record_manager import (
    create_record,
    get_next_unique_id,
    search_record,
    update_record
)


class TestRecordManager(unittest.TestCase):

    def test_search_non_existing_record(self):
        result = search_record(99999)
        self.assertIsNone(result)

    @patch("src.data.record_manager.save_records")
    @patch("src.data.record_manager.load_records")
    def test_create_record_rejects_duplicate_id_across_types(
        self,
        mock_load_records,
        mock_save_records
    ):
        mock_load_records.return_value = [
            {"id": 1, "type": "client", "name": "Test Client"}
        ]

        with self.assertRaises(ValueError):
            create_record({
                "id": 1,
                "type": "airline",
                "company_name": "Test Airline"
            })

        mock_save_records.assert_not_called()

    @patch("src.data.record_manager.load_records")
    def test_get_next_unique_id_uses_all_record_types(
        self,
        mock_load_records
    ):
        mock_load_records.return_value = [
            {"id": 1, "type": "client"},
            {"id": 2, "type": "airline"},
            {"id": 3, "type": "flight"}
        ]

        self.assertEqual(get_next_unique_id(), 4)

    @patch("src.data.record_manager.save_records")
    @patch("src.data.record_manager.load_records")
    def test_create_record_assigns_missing_id(
        self,
        mock_load_records,
        mock_save_records
    ):
        mock_load_records.return_value = [
            {"id": 1, "type": "client"}
        ]

        create_record({
            "type": "flight",
            "client_id": 1,
            "airline_id": 2
        })

        saved_records = mock_save_records.call_args.args[0]

        self.assertEqual(saved_records[-1]["id"], 2)

    @patch("src.data.record_manager.save_records")
    @patch("src.data.record_manager.load_records")
    def test_update_record_rejects_duplicate_new_id(
        self,
        mock_load_records,
        mock_save_records
    ):
        mock_load_records.return_value = [
            {"id": 1, "type": "client"},
            {"id": 2, "type": "airline"}
        ]

        with self.assertRaises(ValueError):
            update_record(1, {"id": 2, "type": "client"})

        mock_save_records.assert_not_called()


if __name__ == "__main__":
    unittest.main()
