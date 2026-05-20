"""Retrieves the ID of the currently selected row in the treeview."""

#Identifies the selected row in the table and extracts its unique ID as an integer
def get_selected_record_id(tree_widget):
    selected = tree_widget.selection()
    if not selected: 
        raise ValueError("Please select a record first")
    return int(tree_widget.item(selected[0], "values")[0])