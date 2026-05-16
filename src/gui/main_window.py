import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from conf.constants import APP_TITLE

from data.record_manager import (
    get_all_records,
    search_record,
    delete_record,
    update_record
)
from data.validators import validate_date

from gui.client_gui import ClientWindow
from gui.airline_gui import AirlineWindow
from gui.flight_gui import FlightWindow


FIELD_LABELS = {
    "id": "ID",
    "type": "Type (type of record)",
    "name": "Name",
    "address_line_1": "Address Line 1",
    "address_line_2": "Address Line 2",
    "address_line_3": "Address Line 3",
    "city": "City",
    "state": "State",
    "zip_code": "Zip Code",
    "country": "Country",
    "phone_number": "Phone Number",
    "company_name": "Company Name",
    "client_id": "Client ID",
    "airline_id": "Airline ID",
    "date": "Date (DD-MM-YYYY)",
    "start_city": "Start City",
    "end_city": "End City"
}

UPDATE_FIELDS = {
    "airline": [
        "id",
        "type",
        "company_name"
    ],
    "flight": [
        "client_id",
        "airline_id",
        "date",
        "start_city",
        "end_city"
    ]
}


class MainWindow:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title(APP_TITLE)

        self.root.geometry("1100x600")

        self.create_widgets()

        self.refresh_records()

    def create_widgets(self):

        button_frame = tk.Frame(self.root)

        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Add Client",
            command=self.open_client_window
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Add Airline",
            command=self.open_airline_window
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Add Flight",
            command=self.open_flight_window
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            button_frame,
            text="Refresh",
            command=self.refresh_records
        ).grid(row=0, column=3, padx=5)

        self.search_entry = tk.Entry(button_frame)

        self.search_entry.grid(
            row=0,
            column=4,
            padx=5
        )

        tk.Button(
            button_frame,
            text="Search",
            command=self.search_records
        ).grid(row=0, column=5, padx=5)

        tk.Button(
            button_frame,
            text="Delete",
            command=self.delete_selected_record
        ).grid(row=0, column=6, padx=5)

        tk.Button(
            button_frame,
            text="Update",
            command=self.open_update_window
        ).grid(row=0, column=7, padx=5)

        columns = (
            "ID",
            "Type",
            "Name",
            "Details"
        )

        self.tree = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings"
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Details", text="Details")

        self.tree.column("ID", width=80)
        self.tree.column("Type", width=120)
        self.tree.column("Name", width=200)
        self.tree.column("Details", width=600)

        self.tree.bind("<Double-1>", self.open_update_window)
        self.tree.bind("<Return>", self.open_update_window)

        self.tree.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10
        )

    def open_client_window(self):

        ClientWindow(self.root)

    def open_airline_window(self):

        AirlineWindow(self.root)

    def open_flight_window(self):

        FlightWindow(self.root)

    def refresh_records(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        records = get_all_records()

        for record in records:

            record_id = record.get("id", "N/A")

            record_type = record.get("type", "Unknown")

            if record_type == "client":

                name = record.get("name", "")

            elif record_type == "airline":

                name = record.get("company_name", "")

            elif record_type == "flight":

                start_city = record.get("start_city", "")
                end_city = record.get("end_city", "")

                name = f"{start_city} → {end_city}"

            else:

                name = ""

            #details = str(record)
            # Replaced to have a clear table

            if record_type == "client":

                details = (
                    f"{record.get('city', '')}, "
                    f"{record.get('country', '')}"
                )

            elif record_type == "airline":

                details = record.get("company_name", "")

            elif record_type == "flight":

                details = (
                    f"{record.get('date', '')}"
                )

            else:

                details = ""

            self.tree.insert(
                "",
                tk.END,
                values=(
                    record_id,
                    record_type,
                    name,
                    details
                )
            )

    def search_records(self):

        record_id = self.search_entry.get().strip() #Strip remove the space issues (" 1 " will become "1" for instance)

        if not record_id.isdigit():

            messagebox.showerror(
                "Error",
                "Enter a valid ID"
            )

            return

        record = search_record(int(record_id))

        for item in self.tree.get_children():
            self.tree.delete(item)

        if record:

            record_type = record.get("type", "Unknown")

            if record_type == "client":

                name = record.get("name", "")

            elif record_type == "airline":

                name = record.get("company_name", "")

            elif record_type == "flight":

                start_city = record.get("start_city", "")
                end_city = record.get("end_city", "")

                name = f"{start_city} → {end_city}"

            else:

                name = ""

            self.tree.insert(
                "",
                tk.END,
                values=(
                    record.get("id", "N/A"),
                    record_type,
                    name,
                    str(record)
                )
            )

        else:

            messagebox.showinfo(
                "Search",
                "No record found"
            )

    def delete_selected_record(self):

        try:

            record_id = self.get_selected_record_id()

        except ValueError as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            return

        try:

            success = delete_record(record_id)

            if success:

                self.refresh_records()

                messagebox.showinfo(
                    "Success",
                    "Record deleted successfully"
                )

            else:

                messagebox.showerror(
                    "Error",
                    "Record could not be deleted"
                )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Delete failed: {error}"
            )

    def get_selected_record_id(self):

        selected_item = self.tree.selection()

        if not selected_item:
            raise ValueError("Select a record first")

        values = self.tree.item(
            selected_item[0],
            "values"
        )

        return int(values[0])

    def open_update_window(self, event=None):

        if event is not None and event.type == tk.EventType.ButtonPress:
            selected_row = self.tree.identify_row(event.y)

            if not selected_row:
                return

            self.tree.selection_set(selected_row)

        try:

            record_id = self.get_selected_record_id()

        except ValueError as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            return

        record = search_record(record_id)

        if not record:

            messagebox.showerror(
                "Error",
                "Record not found"
            )

            return

        update_window = tk.Toplevel(self.root)

        update_window.title("Update Record")

        entries = {}

        row_index = 0

        record_type = record.get("type")

        fields = UPDATE_FIELDS.get(
            record_type,
            list(record.keys())
        )

        for key in fields:

            value = record.get(key, "")

            label = tk.Label(
                update_window,
                text=FIELD_LABELS.get(key, key)
            )

            label.grid(
                row=row_index,
                column=0,
                padx=10,
                pady=5
            )

            entry = tk.Entry(update_window, width=50)

            entry.insert(0, str(value))

            entry.grid(
                row=row_index,
                column=1,
                padx=10,
                pady=5
            )

            entries[key] = entry

            row_index += 1

        def save_updated_record():

            updated_record = record.copy()

            for key, entry in entries.items():

                value = entry.get()

                if key in [
                    "id",
                    "client_id",
                    "airline_id"
                ]:

                    try:
                        value = int(value)

                    except ValueError:

                        messagebox.showerror(
                            "Error",
                            f"{key} must be an integer"
                        )

                        return

                if key == "client_id": 
                    target = search_record(value)
                    if not target or target.get("type") != "client":
                        messagebox.showerror("Error", f"Client ID {value} does not exist.")
                        return
                    
                if key == "airline_id":
                    target = search_record(value)
                    if not target or target.get("type") != "airline":
                        messagebox.showerror("Error", f"Airline ID {value} does not exist.")
                        return

                if key == "date" and not validate_date(value):

                    messagebox.showerror(
                        "Error",
                        "Date must be in DD-MM-YYYY format"
                    )

                    return

                updated_record[key] = value

            try:

                update_record(
                    record_id,
                    updated_record
                )

            except ValueError as error:

                messagebox.showerror(
                    "Error",
                    str(error)
                )

                return

            self.refresh_records()

            update_window.destroy()

            messagebox.showinfo(
                "Success",
                "Record updated successfully"
            )

        tk.Button(
            update_window,
            text="Save Changes",
            command=save_updated_record
        ).grid(
            row=row_index,
            column=0,
            columnspan=2,
            pady=10
        )

    def run(self):

        self.root.mainloop()
