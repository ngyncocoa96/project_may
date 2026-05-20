import customtkinter as ctk
from tkinter import messagebox
from data.record_manager import search_record
from gui.gui_helpers.selected_record_id import get_selected_record_id
from gui.gui_helpers.save_updated_record import execute_save, FIELD_LABELS

# Defines the specific data fields required for each record category
UPDATE_FIELDS = {
    "client": ["id", "name", "address_line_1", "address_line_2", "address_line_3", "city", "state", "zip_code", "country", "phone_number"],
    "airline": ["id", "company_name"],
    "flight": ["id", "client_id", "airline_id", "date", "start_city", "end_city"]
}

"""Manages the lifecycle of the update dialog, from dynamic form generation to data persistence."""
def open_update_window(app, event=None):

    #Fix the issue where double click pops-up a message between headers/separators
    if event:
        region = app.tree.identify_region(event.x, event.y)
        if region == "heading" or region == "separator": 
            return 
    
    # Retrieves the selected record's ID and handles potential selection errors
    try:
        record_id = get_selected_record_id(app.tree)
    except ValueError as error:
        if not event: 
            messagebox.showerror("Error", str(error))
        return

    # Fetches the existing data from the database or exits if not found
    record = search_record(record_id)
    if not record: return

    # Initializes the pop-up window and ensures it appears in the foreground
    update_win = ctk.CTkToplevel(app.root)
    update_win.title("Update Record")
    update_win.geometry("650x800")
    update_win.after(100, update_win.lift)

    current_entries = {}

    # Creates the header section for record type selection
    top_frame = ctk.CTkFrame(update_win, fg_color="transparent")
    top_frame.pack(pady=10, padx=20, fill="x")
    ctk.CTkLabel(top_frame, text="Convert Record To:", font=("Arial", 14, "bold")).pack(side="left", padx=10)

    # Configures the dropdown to trigger a UI refresh upon type change
    def on_type_change(new_type):
        render_fields(new_type)

    type_combo = ctk.CTkComboBox(top_frame, values=["client", "airline", "flight"], command=on_type_change, width=200)
    type_combo.set(record.get("type"))
    type_combo.pack(side="left", padx=10)

    # Scrollable Fields Area
    scroll_frame = ctk.CTkScrollableFrame(update_win, width=600, height=550)
    scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

    """Clears and rebuilds the UI based on the selected type."""
    # Logic to clear and rebuild the form fields based on the selected type
    def render_fields(selected_type):
        for widget in scroll_frame.winfo_children():
            widget.destroy()
        current_entries.clear()

        fields = UPDATE_FIELDS.get(selected_type, [])

        for i, key in enumerate(fields):
            lbl = ctk.CTkLabel(scroll_frame, text=FIELD_LABELS.get(key, key), anchor="w")
            lbl.grid(row=i, column=0, padx=10, pady=10, sticky="w")

            entry = ctk.CTkEntry(scroll_frame, width=350)
            val = record.get(key, "")
            entry.insert(0, str(val))
            
            # Protects the unique ID by making the field read-only, can modify the color
            if key == "id":
                entry.configure(state="disabled", fg_color="gray30")

            entry.grid(row=i, column=1, padx=10, pady=10)
            current_entries[key] = entry

    # Initial Render
    render_fields(record.get("type"))

    # Button "SAVE"
    save_btn = ctk.CTkButton(
        update_win, 
        text="Save Changes", 
        command=lambda: execute_save(app, update_win, type_combo, current_entries, record, record_id),
        height=45, 
        font=("Arial", 14, "bold")
    )
    save_btn.pack(pady=20)
