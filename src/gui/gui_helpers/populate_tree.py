import tkinter as tk
from data.record_manager import search_record

def fill_tree_with_records(tree_widget, records):
    """Common logic to fill the treeview with given records."""
    # Clear current items
    for item in tree_widget.get_children(): 
        tree_widget.delete(item)

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

        # For Details text: Can be modified here
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
            company_name = record.get('company_name', '').strip()
            details = f"Airlines company : {company_name}"

        elif record_type == "flight":
            date = str(record.get('date', '')).strip()
            c_id = record.get('client_id') 
            a_id = record.get('airline_id')

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

        tree_widget.insert("", tk.END, values=(record_id, record_type, name, details))