import unittest

from src.data.validators import (
    validate_phone,
    validate_date
)


class TestValidators(unittest.TestCase):

    def test_validate_phone(self):
        self.assertTrue(validate_phone("0123456789"))


    def test_validate_invalid_phone(self):
        self.assertFalse(validate_phone("abc"))


    def test_validate_date(self):
        self.assertTrue(validate_date("01-01-2026"))


    def test_validate_invalid_date(self):
        self.assertFalse(validate_date("2026-01-01"))


if __name__ == "__main__":
    unittest.main()
