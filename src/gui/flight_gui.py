import tkinter as tk
from tkinter import messagebox

from data.record_manager import create_record
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

            date = self.entries["Date (DD-MM-YYYY)"].get()

            if not validate_date(date):
                raise ValueError("Date must be in DD-MM-YYYY format")

            record = {
                "client_id": int(self.entries["Client ID"].get()),
                "airline_id": int(self.entries["Airline ID"].get()),
                "type": FLIGHT,
                "date": date,
                "start_city": self.entries["Start City"].get(),
                "end_city": self.entries["End City"].get()
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
