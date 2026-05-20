"""Constructs the main application layout, including the sidebar menu, search tools, and interactive data table."""

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

def setup_ui(app):
    # Sidebar for Navigation 
    app.sidebar_frame = ctk.CTkFrame(app.root, width=200, corner_radius=0)
    app.sidebar_frame.grid(row=0, column=0, sticky="nsew")
    
    app.logo_label = ctk.CTkLabel(app.sidebar_frame, text="RMS System", font=ctk.CTkFont(size=20, weight="bold"))
    app.logo_label.pack(pady=20, padx=20)

    actions = [
        ("Add Client", app.open_client_window),
        ("Add Airline", app.open_airline_window),
        ("Add Flight", app.open_flight_window),
        ("Delete Record", app.delete_selected_record),
        ("Update Record", app.open_update_window),
        ("Export to CSV", app.export_to_csv)
    ]

    for text, cmd in actions:
        btn = ctk.CTkButton(app.sidebar_frame, text=text, command=cmd)
        btn.pack(pady=10, padx=20, fill="x")

    # Main Content Area 
    app.main_frame = ctk.CTkFrame(app.root)
    app.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
    app.main_frame.grid_columnconfigure(0, weight=1)
    app.main_frame.grid_rowconfigure(1, weight=1)

    # Search Bar setup
    app.search_frame = ctk.CTkFrame(app.main_frame, fg_color="transparent")
    app.search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
    
    app.search_entry = ctk.CTkEntry(app.search_frame, placeholder_text="Search by ID, Name, or Phone number...", width=350) # Text to be modified here if necessary
    app.search_entry.pack(side="left", padx=(0, 10))
    
    # Bind "Enter" key to search
    app.search_entry.bind("<Return>", lambda event: app.search_records())
    
    app.search_btn = ctk.CTkButton(app.search_frame, text="Search", width=100, command=app.search_records)
    app.search_btn.pack(side="left", padx=5)
    
    app.refresh_btn = ctk.CTkButton(app.search_frame, text="Refresh All", width=100, command=app.refresh_records)
    app.refresh_btn.pack(side="left", padx=5)

    # Treeview Styling
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background="#ffffff", foreground="black", fieldbackground="#ffffff", borderwidth=0)
    style.map("Treeview", background=[('selected', '#1f538d')])

    app.table_frame = ctk.CTkFrame(app.main_frame, fg_color="transparent")
    app.table_frame.grid(row=1, column=0, sticky="nsew")
    app.table_frame.grid_columnconfigure(0, weight=1)
    app.table_frame.grid_rowconfigure(0, weight=1)

    columns = ("ID", "Type", "Name", "Details")
    app.tree = ttk.Treeview(app.table_frame, columns=columns, show="headings")
    app.tree_scrollbar = ttk.Scrollbar(
        app.table_frame,
        orient="vertical",
        command=app.tree.yview
    )
    app.tree.configure(yscrollcommand=app.tree_scrollbar.set)
    
    # This part is to modify the top GUI length
    for col in columns:
        app.tree.heading(col, text=col, command=lambda _col=col: app.sort_column(_col, False))
        
    app.tree.column("ID", width=70, stretch=False)      
    app.tree.column("Type", width=100, stretch=False)   
    app.tree.column("Name", width=200, stretch=False)   
    app.tree.column("Details", width=600, stretch=True) 

    app.tree.grid(row=0, column=0, sticky="nsew")
    app.tree_scrollbar.grid(row=0, column=1, sticky="ns")
    app.tree.bind("<Double-1>", app.open_update_window)