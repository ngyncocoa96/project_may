# Record Management System

## Overview

This project is a Record Management System for a specialist travel agent.

The system manages:
- Client Records
- Airline Records
- Flight Records

The application supports:
- Create Record
- Delete Record
- Update Record
- Search and Display Record

## Record Fields

### Client Record

- ID: int
- Type: str
- Name: str
- Address Line 1: str
- Address Line 2: str
- Address Line 3: str
- City: str
- State: str
- Zip Code: str
- Country: str
- Phone Number: str

### Airline Record

- ID: int
- Type: str
- Company Name: str

### Flight Record

- Client ID: int
- Airline ID: int
- Date: date/time in DD-MM-YYYY format
- Start City: str
- End City: str

Record IDs are unique across client, airline, and flight records. Flight records use an internal ID for search, update, and delete operations.

## Technologies Used

- Python 3
- Tkinter
- CustomTkinter
- JSONL
- unittest

## Setup

Use Python 3.10 or later. The project has been tested with Python 3.13.

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

## Run Application

From the project root, run:

```bash
PYTHONPATH=src python3 src/main.py
```

If you are using the virtual environment above, you can also run:

```bash
PYTHONPATH=src ./.venv/bin/python src/main.py
```

## Run Tests

From the project root, run:

```bash
PYTHONPATH=.:src python3 -m unittest discover -s tests
```

or, with the virtual environment:

```bash
PYTHONPATH=.:src ./.venv/bin/python -m unittest discover -s tests
```

## Notes for Downloaded GitLab ZIP Files

If you download the project as a ZIP file from GitLab, unzip it, open a terminal in the extracted project folder, then follow the setup steps above before running the application. Do not commit local virtual environment folders such as `.venv/` or generated cache folders such as `__pycache__/`.
