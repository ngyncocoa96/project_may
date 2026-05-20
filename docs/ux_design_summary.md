# UX Design Summary

## Overview

The UX design for the Travel Agent Record Management System (RMS) was prepared to support a Python customtkinter interface with a green light theme. The system allows travel agency staff to manage three types of records: Clients, Airlines, and Flights.

The design focuses on clarity, consistency, error prevention, and visible user feedback. The main required actions are:

- Create a record
- Update a record
- Delete a record
- Search and display a record

The UX documentation was created to match the implemented GUI structure and the final HTML/CSS mockups.

---

## UX Role and Purpose

My role as UX Designer was to document how the user should move through the system and how the interface should support the required record-management actions.

The UX work included:

- Designing the user flow
- Mapping the GUI to the assignment requirements
- Preparing static HTML/CSS mockups in Visual Studio Code
- Documenting the main window layout
- Explaining create, update, delete, search, and display flows
- Identifying usability strengths and future improvements

The mockups were viewed in a web browser and were designed to reflect the implemented Python customtkinter GUI. Generic sample data was used in the mockups to show the interface pattern without copying the full database contents.

---

## GUI Structure

The final GUI is organised into separate interface and helper modules. The `MainWindow` class in `main_window.py` controls the main application window and connects user actions to the relevant GUI functions.

The GUI and helper modules are:

| Module / Helper | Responsibility |
|-----------------|---------------|
| `create_widgets.py` | Builds the main window layout including sidebar, search bar, and treeview |
| `populate_tree.py` | Fills the treeview with records and formats display details per record type |
| `delete_record.py` | Handles deletion workflow including selection check and confirmation dialog |
| `search_records.py` | Filters records by ID, name, company name, or phone number |
| `sort_table.py` | Sorts treeview columns on header click with alternating direction |
| `export_csv.py` | Exports the current treeview contents to a CSV file |
| `save_updated_record.py` | Handles validation and saving logic for the update window |
| `selected_record_id.py` | Retrieves the ID of the currently selected treeview row |
| `update_record_window.py` | Manages the update popup window |

From a UX perspective, this structure keeps the interface organised while supporting the main user actions: creating records, updating records, deleting records, searching, sorting, refreshing, and exporting table data.

---

## Main Window Layout

The main window uses a sidebar on the left for navigation and a main content area on the right for search and records display. The interface is built using customtkinter with a green light theme (`ctk.set_appearance_mode("Light")`, `ctk.set_default_color_theme("green")`).

The sidebar includes:

- Add Client
- Add Airline
- Add Flight
- Delete Record
- Update Record
- Export to CSV

The main area includes:

- Search entry field (placeholder: "Search by ID, Name, or Phone number...")
- Search button
- Refresh All button
- Records table

The records table displays four columns:

- ID
- Type
- Name
- Details

The table supports column sorting by clicking any column header. Clicking the same header again reverses the sort order. Double-clicking a row opens the Update window.

The **Export to CSV** button is included in the sidebar, allowing users to export the currently visible table contents to a structured CSV file at any time.

---

## Requirement Mapping

| Requirement / Implemented Feature | UX / GUI Support |
|----------------------------------|------------------|
| Create a record | Add Client, Add Airline, and Add Flight buttons in the sidebar open popup forms |
| Update a record | Update Record button and double-click open an advanced update window with type conversion |
| Delete a record | Delete Record button shows a confirmation dialog before removing the selected record |
| Search and display a record | Search field accepts ID, name, company name, or phone number and filters the table |
| Manage Client records | Client popup includes ID, name, address fields, city, state, zip code, country, and phone number |
| Manage Airline records | Airline popup includes ID and company name, with type enforced in code |
| Manage Flight records | Flight popup includes client ID, airline ID, date, start city, and end city |
| Give user feedback | Messageboxes show success, validation error, security error, and no-result messages |
| Confirmation before delete | Yes/No dialog appears before a selected record is permanently removed |
| Export records | Export to CSV button saves the visible table to a file |
| Sort records | Clicking any column header sorts the table; clicking again reverses the order |

---

## Screen Designs

### Screen 1: Main Window

The main window uses a dark sidebar on the left and a light main area on the right. The sidebar holds the main CRUD actions plus the Export to CSV button, while the main area shows the search bar and records table.

The treeview includes a vertical scrollbar and supports column header sorting. The table columns are sized as follows: ID (70px), Type (100px), Name (200px), and Details (600px, stretches to fill). The search entry supports pressing Enter as well as clicking the Search button.

The mockup uses generic sample records to show the interface pattern. The important UX point is that the table supports many loaded records and allows row selection before update or delete.

### Screen 2: Create Client Record

The Create Client popup contains the required client fields: ID, Name, Address Lines 1-3, City, State, Zip Code, Country, and Phone Number.

The ID is auto-filled by `get_next_unique_id()` but remains editable. Validation checks that Name, City, Country, and Phone Number are not empty. Name, City, and Country must not be purely numeric. Zip Code must contain only digits. Phone Number must contain at least one digit.

### Screen 3: Create Airline Record

The Create Airline popup contains only ID and Company Name. The Type field is not shown because the record type is enforced internally as `"airline"`. Company Name must contain only letters and spaces. This prevents symbols, numbers, and wrong-type entries.

### Screen 4: Create Flight Record

The Create Flight popup contains Client ID, Airline ID, Date (DD-MM-YYYY), Start City, and End City.

The system validates that Client ID and Airline ID reference existing records of the correct type before saving. The date format is validated against DD-MM-YYYY. This prevents orphaned flight records.

### Screen 5: Update Record

The Update Record window opens as a scrollable popup (650x800px). It includes a dropdown at the top to convert the selected record to a different type: client, airline, or flight.

Changing the dropdown re-renders the correct fields for the chosen type. The ID field is locked (read-only, grey background) to protect record identity. Other fields are pre-filled with existing values where available. Full validation runs before saving, including existence checks for Client ID and Airline ID in flight records.

After a successful save, the main window table refreshes automatically and the popup closes.

### Screen 6: Delete Confirmation

When the user clicks Delete Record, the system first checks that a row is selected. If nothing is selected, an error message appears. If a record is selected, a Yes/No confirmation dialog appears before removal. This prevents accidental data loss.

### Screen 7: Search and Display Records

The search function accepts partial matches. Users can search by exact ID, partial name, partial company name, or partial phone number. The search is case-insensitive, so searching "air france" finds "AIR FRANCE". If no results are found, an info messagebox appears. The Refresh All button restores the full record list.

### Screen 8: Column Sorting

Clicking any column header sorts the table by that column. The system attempts numeric sorting first for the ID column and falls back to alphabetical sorting for text columns. Clicking the same header again reverses the order.

### Screen 9: Export to CSV

Clicking Export to CSV opens a Save As dialog. The exported file contains headers: ID, Type, Name, Details. Each visible row in the treeview is written as a CSV row. If the table is empty, a warning appears instead of opening the dialog.

### Screen 10: Messagebox Feedback

The interface uses messageboxes to give feedback after user actions:

- **Success messages**: shown after records are created, updated, or exported successfully
- **Validation / Format errors**: shown when required fields are empty, IDs are not numeric, dates use the wrong format, or text fields contain invalid values
- **Security errors**: shown when a flight refers to a Client ID or Airline ID that does not exist
- **Search result information**: shown when no records match the search query
- **Export warnings or errors**: shown when there is no data to export or when CSV export fails
- **System errors**: shown if saving or exporting fails unexpectedly

This feedback helps users understand whether an action worked, failed, or needs correction.

---

## Design Decisions and Rationale

| Design Decision | Rationale |
|----------------|-----------|
| Sidebar navigation | Keeps all CRUD actions permanently visible without cluttering the records table |
| customtkinter green light theme | Gives the application a clean, modern appearance suited to a professional internal tool |
| Type field removed from Airline form | Prevents accidental wrong-type entries because type is enforced in code |
| Delete confirmation dialog | Prevents accidental data loss before a destructive action |
| Type conversion in Update window | Allows staff to correct a mis-categorised record without deleting and recreating it |
| Flight details show client and airline name | Gives richer context in the table without needing to open a separate view |
| Database existence check for Client/Airline ID | Prevents orphaned flight records referencing non-existent records |
| Scrollable update form | Handles longer forms cleanly without overflowing the update window |
| Double-click to update | Supports faster editing for repeated use |
| Messagebox feedback | Every action produces a visible success, error, or information response |
| Organised helper files | Separates interface actions clearly while keeping the user-facing behaviour consistent |
| Column sorting on header click | Allows users to quickly reorder records by ID, type, or name |
| Partial search matching | Allows users to find records without needing the exact full value |
| Export to CSV in sidebar | Makes data export consistently accessible from the main navigation |
| Refresh All button | Allows users to restore the full record list after a search without restarting |
| Scrollbar on treeview | Supports viewing many records without resizing the window |

---

## Usability Principles Applied

### Clarity

The sidebar uses direct action labels. Users can immediately see all available operations without searching through menus.

### Consistency

All create windows follow the same label-entry-save-button structure. The update window follows the same pattern with an additional type selector at the top.

### Error Prevention

The UX supports error prevention through:

- Auto-filled ID fields
- Required field checks for key client, airline, and flight inputs
- Date validation using DD-MM-YYYY format
- Numeric checks for ID, Client ID, Airline ID, and Zip Code fields where required
- Client creation checks to prevent purely numeric Name, City, or Country values
- Airline creation checks so Company Name contains only letters and spaces
- Update-window checks for letter-based fields, phone number format, numeric IDs, and linked Client/Airline IDs
- Database existence checks for Client ID and Airline ID in flight records
- Delete confirmation before removing a selected record
- Read-only ID field in the update window

### Feedback

The interface produces visible responses through success messageboxes, validation and format error dialogs, security error dialogs, search-result information, export warnings, and system error messages.

### Efficiency

The sidebar keeps actions visible, the Refresh All button reloads the records table, double-clicking a selected row opens the update workflow quickly, pressing Enter in the search field triggers a search, and column sorting allows rapid reordering without any additional navigation.

---

## Strengths of the Current UX

The GUI is simple, clear, and safe for a small internal travel agency system. The sidebar layout makes the main actions easy to find. The delete confirmation protects users from accidental loss. The flight form validates referenced records before saving. The update form allows record type correction without deleting and recreating data. The organised GUI structure makes the codebase easier to maintain. Partial search matching reduces friction for users who do not know exact values. Column sorting allows quick reordering of the displayed records.

---

## Future UX Improvements

- Show the client name next to the Client ID input in the Flight form as helper text.
- Add a short save-status message or visual indicator after records are created, updated, deleted, or exported.
- Add a status bar at the bottom of the main window showing the total number of loaded records.
- Consider adding a filter dropdown to show only clients, airlines, or flights at once.

---

## UX Contribution Summary

My UX contribution was to prepare the design documentation and mockups for the Record Management System. This included the main window layout, sidebar navigation, user flow, requirement mapping, create/edit popup designs, delete confirmation flow, update window, search and display flow, messagebox feedback, column sorting, CSV export, and future usability improvements.

The UX documentation was prepared to match the final GUI structure.
