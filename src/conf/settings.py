import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

RECORD_FILE = os.path.join(
    BASE_DIR,
    "record",
    "record.jsonl"
)