import tkinter as tk
from tkinter import messagebox

from data.record_manager import create_record, get_next_unique_id
from conf.constants import AIRLINE


class AirlineWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)

        self.window.title("Create Airline Record")

        tk.Label(
            self.window,
            text="ID"
        ).grid(row=0, column=0, padx=10, pady=5)

        tk.Label(
            self.window,
            text="Company Name"
        ).grid(row=2, column=0, padx=10, pady=5)

        tk.Label(
            self.window,
            text="Type"
        ).grid(row=1, column=0, padx=10, pady=5)

        self.id_entry = tk.Entry(self.window)

        self.id_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=5
        )

        self.id_entry.insert(0, str(get_next_unique_id()))

        self.type_entry = tk.Entry(self.window)

        self.type_entry.insert(0, AIRLINE)

        self.type_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=5
        )

        self.company_entry = tk.Entry(self.window)

        self.company_entry.grid(
            row=2,
            column=1,
            padx=10,
            pady=5
        )

        save_button = tk.Button(
            self.window,
            text="Save Airline",
            command=self.save_airline
        )

        save_button.grid(
            row=3,
            column=0,
            columnspan=2,
            pady=10
        )

    def save_airline(self):

        try:

            record = {
                "id": int(self.id_entry.get()),
                "type": self.type_entry.get(),
                "company_name": self.company_entry.get()
            }

            create_record(record)

            messagebox.showinfo(
                "Success",
                "Airline record created successfully"
            )

            self.window.destroy()

        except ValueError as error:

            error_message = str(error)

            if error_message.startswith("invalid literal"):
                error_message = "ID must contain numbers only"

            messagebox.showerror(
                "Error",
                error_message
            )
