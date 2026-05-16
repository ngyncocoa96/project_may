import json
import os

from conf.settings import RECORD_FILE #Should import from src/conf/settings, not just conf/settings


def check_file_exists():
    """
    Create the record file if it does not exist.
    """

    os.makedirs(os.path.dirname(RECORD_FILE), exist_ok=True)

    if not os.path.exists(RECORD_FILE):
        with open(RECORD_FILE, "w", encoding="utf-8"):
            pass


def load_records():
    """
    Load all records from the JSONL file.
    """

    check_file_exists()

    records = []

    with open(RECORD_FILE, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                records.append(json.loads(line))

    return records


def save_records(records):
    """
    Save records to the JSONL file.
    """

    with open(RECORD_FILE, "w", encoding="utf-8") as file:
        for record in records:
            json.dump(record, file)
            file.write("\n")