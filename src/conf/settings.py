import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)


RECORD_FILE = os.path.join(
    BASE_DIR,
    "src", #Moved the save into /src/record instead of /record
    "record",
    "record.jsonl"
)