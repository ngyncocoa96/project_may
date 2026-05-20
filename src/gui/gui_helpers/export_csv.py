"""Automates the export of visible table records to a structured CSV file, enabling portable data reporting and external analysis."""

import csv
from tkinter import messagebox, filedialog

def handle_export_csv(app):
    """Saves current table view to a CSV file."""
    if not app.tree.get_children():
        messagebox.showwarning("Export", "No data to export.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")]
    )

    if file_path:
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Define header row
                writer.writerow(["ID", "Type", "Name", "Details"])
                
                # Iterate through treeview rows
                for row_id in app.tree.get_children():
                    writer.writerow(app.tree.item(row_id)['values'])
                    
            messagebox.showinfo("Success", "Data exported successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")