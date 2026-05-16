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

            record = {
                "id": int(self.entries["ID"].get()),
                "type": CLIENT,
                "name": self.entries["Name"].get(),
                "address_line_1": self.entries["Address Line 1"].get(),
                "address_line_2": self.entries["Address Line 2"].get(),
                "address_line_3": self.entries["Address Line 3"].get(),
                "city": self.entries["City"].get(),
                "state": self.entries["State"].get(),
                "zip_code": self.entries["Zip Code"].get(),
                "country": self.entries["Country"].get(),
                "phone_number": self.entries["Phone Number"].get()
            }

            create_record(record)

            messagebox.showinfo(
                "Success",
                "Client record created successfully"
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
