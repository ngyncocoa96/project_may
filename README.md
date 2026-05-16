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
- JSONL
- unittest

## Run Application

```bash
PYTHONPATH=src python3 src/main.py
```

## Run Tests

```bash
PYTHONPATH=.:src python3 -m unittest discover -s tests
```
