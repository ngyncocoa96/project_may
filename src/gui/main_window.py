import customtkinter as ctk
from conf.constants import APP_TITLE
from data.record_manager import get_all_records

# Bridge Imports
from gui.create_widgets import setup_ui
from gui.gui_helpers.populate_tree import fill_tree_with_records
from gui.gui_helpers.delete_record import handle_delete_record
from gui.gui_helpers.search_records import handle_search
from gui.gui_helpers.sort_table import handle_sort_column
from gui.gui_helpers.export_csv import handle_export_csv
from gui.update_record_window import open_update_window

# Window Imports
from gui.client_gui import ClientWindow
from gui.airline_gui import AirlineWindow
from gui.flight_gui import FlightWindow

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

class MainWindow:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title(f"{APP_TITLE}")
        self.root.geometry("1200x700")

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.create_widgets()
        self.refresh_records()

    def create_widgets(self):
        # Bridge to create_widgets func
        setup_ui(self)

    def open_client_window(self): ClientWindow(self.root)
    def open_airline_window(self): AirlineWindow(self.root)
    def open_flight_window(self): FlightWindow(self.root)    

    def refresh_records(self):
        # Refresh treeview with latest data
        self.populate_tree(get_all_records())

    def populate_tree(self, records):
        # Bridge to populate_tree func
        fill_tree_with_records(self.tree, records)

    def delete_selected_record(self):
        # Bridge to delete_selected_record func
        handle_delete_record(self)

    def search_records(self):
        # Bridge to search_record func
        handle_search(self)

    def sort_column(self, col, reverse):
        # Bridge to sort_column func
        handle_sort_column(self, col, reverse)

    def export_to_csv(self):
        # Bridge to export_to_csv func
        handle_export_csv(self)

    def open_update_window(self, event=None):
        # Bridge to open_update_window func
        open_update_window(self, event)

    def run(self):
        self.root.mainloop()