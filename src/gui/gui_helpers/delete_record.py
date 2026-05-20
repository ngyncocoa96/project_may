"""Manages the record deletion workflow by verifying selection, requesting user confirmation, and synchronizing the UI with the updated database."""

from tkinter import messagebox
from data.record_manager import delete_record
from gui.gui_helpers.selected_record_id import get_selected_record_id

def handle_delete_record(app):
    try:
        # We use our helper to get the ID
        record_id = get_selected_record_id(app.tree)
        
        if messagebox.askyesno("Confirm", "Delete this record?"):
            delete_record(record_id)
            # We call the refresh method of the main app
            app.refresh_records()
            
    except Exception as e: 
        messagebox.showerror("Error", str(e))