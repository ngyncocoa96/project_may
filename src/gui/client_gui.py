"""Manages the client registration interface, handling input validation and data persistence for new records."""

import tkinter as tk
from tkinter import messagebox

from data.record_manager import create_record, get_next_unique_id
from conf.constants import CLIENT


class ClientWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)

        self.window.title("Create Client Record")

        self.entries = {}

        fields = [
            "ID",
            "Name",
            "Address Line 1",
            "Address Line 2",
            "Address Line 3",
            "City",
            "State",
            "Zip Code",
            "Country",
            "Phone Number"
        ]

        for index, field in enumerate(fields):

            label = tk.Label(
                self.window,
                text=field
            )

            label.grid(
                row=index,
                column=0,
                padx=10,
                pady=5
            )

            entry = tk.Entry(self.window)

            entry.grid(
                row=index,
                column=1,
                padx=10,
                pady=5
            )

            self.entries[field] = entry

        self.entries["ID"].insert(0, str(get_next_unique_id()))

        save_button = tk.Button(
            self.window,
            text="Save Client",
            command=self.save_client
        )

        save_button.grid(
            row=len(fields),
            column=0,
            columnspan=2,
            pady=10
        )

    def save_client(self):
        try:
            # Collect and sanitize data (remove surrounding whitespaces)
            data = {field: entry.get().strip() for field, entry in self.entries.items()}

            # Basic validation: Check for empty mandatory fields
            if not data["Name"] or not data["Phone Number"] or not data["City"] or not data["Country"]:
                raise ValueError("Name, Country, City, and Phone Number are mandatory.")

            # Data type validation: Name should not be purely numeric
            if data["Name"].isdigit():
                raise ValueError("The Name field cannot be a number.")
            
            # Data type validation: Country should not be numeric
            if data["Country"].isdigit():
                raise ValueError("The Country field cannot be a number.")
            
            # Data type validation: City should not be numeric
            if data["City"].isdigit():
                raise ValueError("The City field cannot be a number.")

            # Data type validation: Zip Code must contain only digits
            if data["Zip Code"] and not data["Zip Code"].isdigit():
                raise ValueError("Zip Code must contain only numbers.")

            # Data type validation: Phone Number must contain digits
            if not any(char.isdigit() for char in data["Phone Number"]):
                raise ValueError("The Phone Number must contain at least one digit.")

            # Construct the final record dictionary
            record = {
                "id": int(data["ID"]), # Ensure ID is stored as an integer
                "type": CLIENT,
                "name": data["Name"],
                "address_line_1": data["Address Line 1"],
                "address_line_2": data["Address Line 2"],
                "address_line_3": data["Address Line 3"],
                "city": data["City"],
                "state": data["State"],
                "zip_code": data["Zip Code"],
                "country": data["Country"],
                "phone_number": data["Phone Number"]
            }

            # Store the record in the database
            create_record(record)

            messagebox.showinfo(
                "Success",
                "Client record created successfully"
            )

            self.window.destroy()

        except ValueError as error:
            # Handle both manual validation errors and automatic type conversion errors
            error_message = str(error)

            if "invalid literal" in error_message:
                error_message = "ID must be a valid number."

            messagebox.showerror(
                "Validation Error",
                error_message
            )