"""Manages the flight registration interface, handling input validation and data persistence for new records."""


import tkinter as tk
from tkinter import messagebox

from data.record_manager import create_record, search_record
from data.validators import validate_date
from conf.constants import FLIGHT


class FlightWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)

        self.window.title("Create Flight Record")

        labels = [
            "Client ID",
            "Airline ID",
            "Date (DD-MM-YYYY)",
            "Start City",
            "End City"
        ]

        self.entries = {}

        for index, label_text in enumerate(labels):

            label = tk.Label(
                self.window,
                text=label_text
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

            self.entries[label_text] = entry

        save_button = tk.Button(
            self.window,
            text="Save Flight",
            command=self.save_flight
        )

        save_button.grid(
            row=len(labels),
            column=0,
            columnspan=2,
            pady=10
        )

    def save_flight(self):

        try:

            # Get the IDs
            raw_client_id = self.entries["Client ID"].get().strip()
            raw_airline_id = self.entries["Airline ID"].get().strip()
            date = self.entries["Date (DD-MM-YYYY)"].get().strip()

            #Verify empty inputs
            if not raw_client_id or not raw_airline_id or not date:
                raise ValueError("Client ID, Airline ID and Date are required.")

            client_id = int(raw_client_id)
            airline_id = int(raw_airline_id)

            date = self.entries["Date (DD-MM-YYYY)"].get()

            if not validate_date(date):
                raise ValueError("Date must be in DD-MM-YYYY format")

            #Checks if client exist
            client_record = search_record(client_id)
            if not client_record or client_record.get("type") != "client":
                raise ValueError(f"Client ID {client_id} do not exist in database.")

            #Checks if the company exist
            airline_record = search_record(airline_id)
            if not airline_record or airline_record.get("type") != "airline":
                raise ValueError(f"Airline ID {airline_id} do not exist in database.")
            
            record = {
                "client_id": client_id,   
                "airline_id": airline_id,  
                "type": FLIGHT,
                "date": date,
                "start_city": self.entries["Start City"].get().strip(),
                "end_city": self.entries["End City"].get().strip()
            }


            create_record(record)

            messagebox.showinfo(
                "Success",
                "Flight record created successfully"
            )

            self.window.destroy()

        except ValueError as error:

            error_message = str(error)

            if error_message.startswith("invalid literal"):
                error_message = "Client ID and Airline ID must contain numbers only"

            messagebox.showerror(
                "Error",
                error_message
            )
