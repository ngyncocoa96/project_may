from datetime import datetime


def validate_phone(phone_number):
    """
    Validate phone number.
    """

    return phone_number.isdigit() and len(phone_number) >= 10


def validate_date(date_string):
    """
    Validate date format DD-MM-YYYY.
    """

    try:
        datetime.strptime(date_string, "%d-%m-%Y")
        return True

    except ValueError:
        return False


def validate_required_fields(record, required_fields):
    """
    Ensure required fields are not empty.
    """

    for field in required_fields:
        if field not in record:
            return False

        if record[field] == "":
            return False

    return True
