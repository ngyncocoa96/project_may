from data.file_handler import load_records, save_records #Should import from src/data/file_handler, not just data.file_handler


def get_next_unique_id():
    """
    Return the next available ID across every record type.
    """

    records = load_records()

    existing_ids = [
        record.get("id")
        for record in records
        if isinstance(record.get("id"), int)
    ]

    if not existing_ids:
        return 1

    return max(existing_ids) + 1


def is_unique_id(record_id, excluded_record_id=None):
    """
    Check whether an ID is unused across every record type.
    """

    records = load_records()

    for record in records:
        current_id = record.get("id")

        if current_id == excluded_record_id:
            continue

        if current_id == record_id:
            return False

    return True


def create_record(record):
    """
    Create a new record.
    """

    records = load_records()

    record_id = record.get("id")

    if record_id is None:
        record["id"] = get_next_unique_id()

    elif not is_unique_id(record_id):
        raise ValueError("ID already exists")

    records.append(record)

    save_records(records)


def get_all_records():
    """
    Return all records.
    """

    return load_records()


def search_record(record_id):
    """
    Search for a record by ID.
    """

    records = load_records()

    for record in records:
        if record.get("id") == record_id:
            return record

    return None


def delete_record(record_id):
    """
    Delete a record by ID.
    """

    records = load_records()

    updated_records = []

    for record in records:
        if record.get("id") != record_id:
            updated_records.append(record)

    save_records(updated_records)

    return True


def update_record(record_id, updated_record):
    """
    Update an existing record.
    """

    records = load_records()

    updated_record_id = updated_record.get("id")

    if updated_record_id != record_id:
        for record in records:
            if record.get("id") == updated_record_id:
                raise ValueError("ID already exists")

    for index, record in enumerate(records):
        if record.get("id") == record_id:
            records[index] = updated_record

            save_records(records)

            return True

    return False
