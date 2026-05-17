import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import re

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

ctk.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue")

FIELD_LABELS = {
    "id": "ID",
    "type": "Record Type",
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
    "client": [
        "id", "name", "address_line_1", "address_line_2", 
        "address_line_3", "city", "state", "zip_code", 
        "country", "phone_number"
    ],
    "airline": [
        "id", "company_name"
    ],
    "flight": [
        "id", "client_id", "airline_id", "date", "start_city", "end_city"
    ]
}
class MainWindow:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title(f"{APP_TITLE}")
        self.root.geometry("1200x700")

        # Layout configuration
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.create_widgets()
        self.refresh_records()

    def create_widgets(self):
        # Sidebar for Navigation 
        self.sidebar_frame = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="RMS System", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=20, padx=20)

        actions = [
            ("Add Client", self.open_client_window),
            ("Add Airline", self.open_airline_window),
            ("Add Flight", self.open_flight_window),
            ("Delete Record", self.delete_selected_record),
            ("Update Record", self.open_update_window)
        ]

        for text, cmd in actions:
            btn = ctk.CTkButton(self.sidebar_frame, text=text, command=cmd)
            btn.pack(pady=10, padx=20, fill="x")

        # Main Content Area 
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # Search Bar
        self.search_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Enter ID to search...", width=300)
        self.search_entry.pack(side="left", padx=(0, 10))
        
        self.search_btn = ctk.CTkButton(self.search_frame, text="Search", width=100, command=self.search_records)
        self.search_btn.pack(side="left", padx=5)
        
        self.refresh_btn = ctk.CTkButton(self.search_frame, text="Refresh All", width=100, command=self.refresh_records)
        self.refresh_btn.pack(side="left", padx=5)

        # Treeview Styling
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#ffffff", foreground="black", fieldbackground="#ffffff", borderwidth=0)
        style.map("Treeview", background=[('selected', '#1f538d')])

        columns = ("ID", "Type", "Name", "Details")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings")
        
        # This part is to modify the top GUI lenght
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column("ID", width=70, stretch=False)      
            self.tree.column("Type", width=100, stretch=False)   
            self.tree.column("Name", width=200, stretch=False)   
            self.tree.column("Details", width=600, stretch=True) 

        self.tree.grid(row=1, column=0, sticky="nsew")
        self.tree.bind("<Double-1>", self.open_update_window)

    def open_client_window(self): ClientWindow(self.root)
    def open_airline_window(self): AirlineWindow(self.root)
    def open_flight_window(self): FlightWindow(self.root)

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
                name = f"{record.get('start_city', '')} → {record.get('end_city', '')}"
            else:
                name = "Unknown"

            # For Details text: Can be modified
            if record_type == "client":
                # Gather the data of city, country and phone number
                city = record.get('city', '').strip()
                country = record.get('country', '').strip()
                phone = record.get('phone_number', '').strip()

                loc_list = [p for p in [city, country] if p]
                location = ", ".join(loc_list) 

                final_list = [p for p in [location, phone] if p]
                details = " | ".join(final_list)

            elif record_type == "airline":
                details = record.get('company_name', '')

            elif record_type == "flight":
                date = str(record.get('date', '')).strip()
                c_id = record.get('client_id') 
                a_id = record.get('airline_id')
                f_id = record.get('flight_id')

                parts = []
                
                if c_id:
                    client_data = search_record(c_id)
                    if client_data:
                        c_name = client_data.get('name', 'Unknown')
                        parts.append(f"Mr/Ms: {c_name} (ID #{c_id})")
                    else:
                        parts.append(f" Client: ID #{c_id} (Not Found)")

                if a_id:
                    airline_data = search_record(a_id)
                    if airline_data:
                        a_name = airline_data.get('company_name', 'Unknown')
                        parts.append(f"Airline: {a_name} (ID #{a_id})")
                    else:
                        parts.append(f"Airline: #{a_id}")

                if date:
                    parts.append(f"Departure date: {date}")

                details = " ; ".join(parts)

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

    def get_selected_record_id(self):
        selected = self.tree.selection()
        if not selected: raise ValueError("Please select a record first")
        return int(self.tree.item(selected[0], "values")[0])

    def delete_selected_record(self):
        try:
            record_id = self.get_selected_record_id()
            if messagebox.askyesno("Confirm", "Delete this record?"):
                delete_record(record_id)
                self.refresh_records()
        except Exception as e: messagebox.showerror("Error", str(e))

    def search_records(self):
        search_id = self.search_entry.get().strip()
        if not search_id.isdigit():
            messagebox.showerror("Error", "Enter a valid ID")
            return
        record = search_record(int(search_id))
        for item in self.tree.get_children(): self.tree.delete(item)
        if record: self.tree.insert("", tk.END, values=(record.get("id"), record.get("type"), "Found", str(record)))
        else: messagebox.showinfo("Search", "No record found")

    def open_update_window(self, event=None):
        try:
            record_id = self.get_selected_record_id()
        except ValueError as error:
            messagebox.showerror("Error", str(error))
            return

        record = search_record(record_id)
        if not record: return

        update_win = ctk.CTkToplevel(self.root)
        update_win.title("Update Record")
        update_win.geometry("650x800")
        update_win.after(100, update_win.lift)

        current_entries = {}

        # Top Selection Area 
        top_frame = ctk.CTkFrame(update_win, fg_color="transparent")
        top_frame.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(top_frame, text="Convert Record To:", font=("Arial", 14, "bold")).pack(side="left", padx=10)

        # Dynamic Render Function
        def on_type_change(new_type):
            render_fields(new_type)

        type_combo = ctk.CTkComboBox(top_frame, values=["client", "airline", "flight"], command=on_type_change, width=200)
        type_combo.set(record.get("type"))
        type_combo.pack(side="left", padx=10)

        # Scrollable Fields Area
        scroll_frame = ctk.CTkScrollableFrame(update_win, width=600, height=550)
        scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        def render_fields(selected_type):
            """Clears and rebuilds the UI based on the selected type."""
            # Clear previous widgets
            for widget in scroll_frame.winfo_children():
                widget.destroy()
            current_entries.clear()

            # Get fields for the chosen type (now including client!)
            fields = UPDATE_FIELDS.get(selected_type, [])

            for i, key in enumerate(fields):
                # Label
                lbl = ctk.CTkLabel(scroll_frame, text=FIELD_LABELS.get(key, key), anchor="w")
                lbl.grid(row=i, column=0, padx=10, pady=10, sticky="w")

                # Entry
                entry = ctk.CTkEntry(scroll_frame, width=350)
                
                # Logic: If we switch type, we keep the data if the keys match
                # (e.g., ID stays the same, but 'name' might be new/empty)
                val = record.get(key, "")
                entry.insert(0, str(val))
                
                # Special Case: ID should usually be read-only in update
                if key == "id":
                    entry.configure(state="disabled", fg_color="gray30")

                entry.grid(row=i, column=1, padx=10, pady=10)
                current_entries[key] = entry

        # Initial Render
        render_fields(record.get("type"))

    #  Function for the save logic
        def save_updated_record():

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
                    
                # Ensure client_id and airline_id exist
                if key == "client_id":
                    target = search_record(val)
                    if not target or target.get("type") != "client":
                        messagebox.showerror("Security Error", f"Client ID {val} does not exist in the database.")
                        return

                if key == "airline_id":
                    target = search_record(val)
                    if not target or target.get("type") != "airline":
                        messagebox.showerror("Security Error", f"Airline ID {val} does not exist in the database.")
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
                self.refresh_records()
                
                # Close the pop-up window
                update_win.destroy()
                
                messagebox.showinfo("Success", f"Record successfully saved as {new_type.upper()}.")
                
            except Exception as e:
                messagebox.showerror("System Error", f"Failed to save record: {str(e)}")

        # Button "SAVE"
        save_btn = ctk.CTkButton(
            update_win, 
            text="Save Changes", 
            command=save_updated_record, 
            height=45, 
            font=("Arial", 14, "bold")
        )
        save_btn.pack(pady=20)

    def run(self):
        self.root.mainloop()