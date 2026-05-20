"""Searches by ID, Name, or Phone."""

from tkinter import messagebox
from data.record_manager import get_all_records

def handle_search(app):

    query = app.search_entry.get().strip().lower()
    
    if not query:
        app.refresh_records()
        return

    all_records = get_all_records()
    filtered_results = []


    for record in all_records:
        record_id = str(record.get("id", "")) # Transform id from int to str to be able to search for it
        client_name = record.get("name", "").lower() # Lower enables to find name from capital letters (ex: AIR FRANCE -> air france)
        company_name = record.get("company_name", "").lower() 
        phone = str(record.get("phone_number", "")).lower() # Transform phone number from int to str to be able to search for it
        
        #Name, phone can be partial 
        if (query == record_id or 
            query in client_name or  #Ex: find Emilie if you only type mil
            query in company_name or 
            query in phone):
            filtered_results.append(record)

    #If no result is found
    if not filtered_results:
        messagebox.showinfo("Search Results", f"No records found for: '{query}'")
    else:
        app.populate_tree(filtered_results)