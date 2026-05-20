"""Handles validation and saving logic."""

import re
from tkinter import messagebox
from data.record_manager import search_record, update_record
from data.validators import validate_date

# Labels used for error messages and UI headers
FIELD_LABELS = {
    "id": "ID", "type": "Record Type", "name": "Name", "address_line_1": "Address Line 1",
    "address_line_2": "Address Line 2", "address_line_3": "Address Line 3", "city": "City",
    "state": "State", "zip_code": "Zip Code", "country": "Country", "phone_number": "Phone Number",
    "company_name": "Company Name", "client_id": "Client ID", "airline_id": "Airline ID",
    "date": "Date (DD-MM-YYYY)", "start_city": "Start City", "end_city": "End City"
}

def execute_save(app, update_win, type_combo, current_entries, record, record_id):
    
    #  Function for the save logic
    new_type = type_combo.get()
    # Start with a fresh record to ensure old type-specific fields are removed
    updated_data = {"type": new_type}

    for key, entry in current_entries.items():
        # Handling value extraction (handling disabled ID field)
        if entry.cget("state") == "disabled":
            val = str(record.get(key))
        else:
            val = entry.get().strip()

        # Stop if critical fields are left empty
        if not val and key in ["name", "company_name", "date", "client_id", "airline_id"]:
            messagebox.showerror("Validation Error", f"The field '{FIELD_LABELS.get(key, key)}' cannot be empty.")
            return

        # Checks if client_id and airline_id are integer
        if key in ["id", "client_id", "airline_id"]:
            try:
                val = int(val)
            except ValueError:
                messagebox.showerror("Format Error", f"{FIELD_LABELS.get(key, key)} must be a number.")
                return
            
        # Ensure client_id exist
        if key == "client_id":
            target = search_record(val)
            if not target or target.get("type") != "client":
                messagebox.showerror("Security Error", f"Client ID {val} does not exist.")
                return
            
        # Ensure the airline_id exist
        if key == "airline_id":
            target = search_record(val)
            if not target or target.get("type") != "airline":
                messagebox.showerror("Security Error", f"Airline ID {val} does not exist.")
                return

        # Ensure fields like Name or City only contain letters
        if key in ["name", "city", "country", "state", "start_city", "end_city", "company_name"]:
            if val and not re.match(r"^[a-zA-ZÀ-ÿ\s\-\']+$", str(val)):
                messagebox.showerror("Format Error", f"Field '{FIELD_LABELS.get(key, key)}' can only contain letters.")
                return

        # Phone number format check
        if key == "phone_number" and val and not re.match(r"^\+?[\d\s\-]+$", str(val)):
            messagebox.showerror("Format Error", "Invalid phone number format.")
            return

        # Date format check (DD-MM-YYYY)
        if key == "date" and not validate_date(str(val)):
            messagebox.showerror("Format Error", "Date must follow the format: DD-MM-YYYY")
            return

        # If all checks pass, add to the dictionary
        updated_data[key] = val

    try:
        # Replace the record using the original record_id
        update_record(record_id, updated_data)
        
        # Refresh main interface
        app.refresh_records()
        
        # Close the pop-up window
        update_win.destroy()
        
        messagebox.showinfo("Success", f"Record successfully saved as {new_type.upper()}.")
        
    except Exception as e:
        messagebox.showerror("System Error", f"Failed to save record: {str(e)}")