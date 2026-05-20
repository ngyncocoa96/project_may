"""Sorts the treeview content by clicking headers."""

def handle_sort_column(app, col, reverse):
    
    # We extract the data from the tree
    data = [(app.tree.set(child, col), child) for child in app.tree.get_children('')]
    
    # Try to sort numerically if possible (for IDs), otherwise alphabetical
    try:
        data.sort(key=lambda x: int(x[0]), reverse=reverse)
    except ValueError:
        data.sort(reverse=reverse)

    # Rearrange items in the treeview
    for index, (val, child) in enumerate(data):
        app.tree.move(child, '', index)

    # Update the heading command to toggle the sort direction
    # Toggles the sorting direction for the next interaction, enabling alternating ascending and descending orders.
    app.tree.heading(col, command=lambda: app.sort_column(col, not reverse))