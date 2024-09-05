import tkinter as tk
from tkinter import ttk
import sqlite3
import pandas as pd
import json

import sys
sys.path.append('D:/programok/py_ui/')

# Initialize the ErrorLogger with the name 'Main'


# Now import the modules
from utils.logger import ErrorLogger, changeLogger
from utils import db_helper, csv_reader
from utils.config_parser import get_config_value


error_logger = ErrorLogger(name='Main')

# Get the file paths for the CSV and SQLite database from the configuration
csv_path = get_config_value('data_csv', 'path')
db_path = get_config_value('data_db', 'path')

# Define styles for light and dark modes
STYLES = {
    'light': {
        'bg': 'white',
        'fg': 'black',
        'btn_bg': 'lightgrey',
        'btn_fg': 'black'
    },
    'dark': {
        'bg': 'black',
        'fg': 'white',
        'btn_bg': 'grey',
        'btn_fg': 'white'
    }
}

# Main Application Class
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Viewer")
        self.geometry("800x600")
        self.current_style = 'light'  # Set default style

        # Create components
        self.navbar = Navbar(self)
        self.data_view = DataView(self)
        self.bottom_bar = BottomBar(self)

        # Apply initial style
        self.apply_style()

    def apply_style(self):
        """Applies the current style to all widgets."""
        style = STYLES[self.current_style]
        self.configure(bg=style['bg'])
        self.navbar.apply_style(style)
        self.data_view.apply_style(style)
        self.bottom_bar.apply_style(style)

    def toggle_mode(self):
        """Switches between light and dark mode."""
        self.current_style = 'dark' if self.current_style == 'light' else 'light'
        self.apply_style()

# Navbar Component
class Navbar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(side=tk.TOP, fill=tk.X)

        self.name_entry = tk.Entry(self)
        self.name_entry.pack(side=tk.RIGHT, padx=10, pady=5)

        self.age_entry = tk.Entry(self)
        self.age_entry.pack(side=tk.RIGHT, padx=10, pady=5)

        self.gender_entry = tk.Entry(self)
        self.gender_entry.pack(side=tk.RIGHT, padx=10, pady=5)

        self.city_entry = tk.Entry(self)
        self.city_entry.pack(side=tk.RIGHT, padx=10, pady=5)

        self.state_entry = tk.Entry(self)
        self.state_entry.pack(side=tk.RIGHT, padx=10, pady=5)

        self.country_entry = tk.Entry(self)
        self.country_entry.pack(side=tk.RIGHT, padx=10, pady=5)

        self.zip_code_entry = tk.Entry(self)
        self.zip_code_entry.pack(side=tk.RIGHT, padx=10, pady=5)

        self.email_entry = tk.Entry(self)
        self.email_entry.pack(side=tk.RIGHT, padx=10, pady=5)

        self.phone_number_entry = tk.Entry(self)
        self.phone_number_entry.pack(side=tk.RIGHT, padx=10, pady=5)
        # Dark mode toggle button
        self.toggle_button = tk.Button(self, text="Toggle Mode", command=parent.toggle_mode)
        self.toggle_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.load_button = tk.Button(self, text="Load Data", command=self.load_data)
        self.load_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.save_button = tk.Button(self, text="Save Data", command=self.save_data)
        self.save_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.update_button = tk.Button(self, text="Update Data", command=self.update_data)
        self.update_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.delete_button = tk.Button(self, text="Delete Data", command=self.delete_data)
        self.delete_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.add_button = tk.Button(self, text="Add Data", command=self.add_data)
        self.add_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.search_button = tk.Button(self, text="Search Data", command=self.search_data)
        self.search_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.search_entry = tk.Entry(self)
        self.search_entry.pack(side=tk.RIGHT, padx=10, pady=5)

    def load_data(self):
        """Loads data from the database and displays it in the table."""
        rows = db_helper.read_dataframe(db_path, "data")

        # Insert data into the table
        for row in rows:
            self.tree.insert("", "end", values=row)

    def save_data(self):
        """Saves data from the table to the database."""
        # Get the data from the table
        data = self.get_data()

        # Save  data to the database
        db_helper.insert_data(db_path, "data", data)        

    def get_data(self):
        """Gets the data from the table and returns it as a list of tuples."""
        data = []

        # Get the selected rows
        selected_rows = self.tree.selection()

        # Iterate over the selected rows
        for row in selected_rows:
            # Get the values of the selected row
            values = self.tree.item(row)['values']

            # Append the values to the data list
            data.append(values)            

        return data
    def delete_data(self):
        """Deletes the selected data from the table."""
        # Get the selected rows
        selected_rows = self.tree.selection()

        # Iterate over the selected rows
        for row in selected_rows:
            # Delete the selected row
            self.tree.delete(row)

        # Save the data to the database
        db_helper.delete_data(db_path, "data", self.get_data())
    def update_data(self):        
        # Get the selected rows
        selected_rows = self.tree.selection()

        # Iterate over the selected rows
        for row in selected_rows:
            # Get the values of the selected row
            values = self.tree.item(row)['values']

            # Update the values in the database
            db_helper.update_data(db_path, "data", self.get_data())

            # Update the values in the table
            self.tree.item(row, values=values)
    def add_data(self):
        """Adds new data to the table."""
        # Get the data from the entry fields
        name = self.name_entry.get()
        age = self.age_entry.get()
        gender = self.gender_entry.get()
        city = self.city_entry.get()
        state = self.state_entry.get()
        country = self.country_entry.get()
        zip_code = self.zip_code_entry.get()
        email = self.email_entry.get()
        phone_number = self.phone_number_entry.get()

        # Add the data to the table
        self.tree.insert("", "end", values=[name, age, gender, city, state, country, zip_code, email, phone_number])

        # Save the data to the database
        db_helper.insert_data(db_path, "data", [(name, age, gender, city, state, country, zip_code, email, phone_number)])  

    def search_data(self):
        """Searches for data in the table based on the search criteria and displays the results."""
        # Get the search criteria
        search_criteria = self.search_entry.get()

        # Search for the data in the table
        self.tree.delete(*self.tree.get_children())
        rows = db_helper.read_dataframe(db_path, "data")

        for row in rows:
            if search_criteria in row:
                self.tree.insert("", "end", values=row)

    def apply_style(self, style):
        self.configure(bg=style['bg'])
        self.load_button.configure(bg=style['btn_bg'], fg=style['btn_fg'])
        self.save_button.configure(bg=style['btn_bg'], fg=style['btn_fg'])
        self.update_button.configure(bg=style['btn_bg'], fg=style['btn_fg'])
        self.delete_button.configure(bg=style['btn_bg'], fg=style['btn_fg'])
        self.add_button.configure(bg=style['btn_bg'], fg=style['btn_fg'])
        self.search_button.configure(bg=style['btn_bg'], fg=style['btn_fg'])
        self.search_entry.configure(bg=style['bg'], fg=style['fg'], insertbackground=style['fg'])       
        self.toggle_button.configure(bg=style['btn_bg'], fg=style['btn_fg'])
        self.name_entry.configure(bg=style['bg'], fg=style['fg'], insertbackground=style['fg'])
        self.age_entry.configure(bg=style['bg'], fg=style['fg'], insertbackground=style['fg'])        
        self.gender_entry.configure(bg=style['bg'], fg=style['fg'], insertbackground=style['fg'])
        self.city_entry.configure(bg=style['bg'], fg=style['fg'], insertbackground=style['fg'])
        self.state_entry.configure(bg=style['bg'], fg=style['fg'], insertbackground=style['fg'])
        self.country_entry.configure(bg=style['bg'], fg=style['fg'], insertbackground=style['fg'])
        self.zip_code_entry.configure(bg=style['bg'], fg=style['fg'], insertbackground=style['fg'])
        self.email_entry.configure(bg=style['bg'], fg=style['fg'], insertbackground=style['fg'])
        self.phone_number_entry.configure(bg=style['bg'], fg=style['fg'], insertbackground=style['fg']) 
# DataView Component (Scrollable Table Area)
class DataView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)

        # Create Treeview (table) widget    
        self.tree = ttk.Treeview(self, columns=("column1", "column2", "column3"), show='headings')
        self.tree.heading("column1", text="ID")
        self.tree.heading("column2", text="Name")
        self.tree.heading("column3", text="Age")

        # Create vertical scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Pack treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def apply_style(self, style):
        self.configure(bg=style['bg'])
        self.tree.tag_configure("row", background=style['bg'], foreground=style['fg'])

# BottomBar Component (Buttons at the bottom)
class BottomBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(side=tk.BOTTOM, fill=tk.X)

        self.button1 = tk.Button(self, text="Button 1")
        self.button1.pack(side=tk.LEFT, padx=5, pady=5)

        self.button2 = tk.Button(self, text="Button 2")
        self.button2.pack(side=tk.LEFT, padx=5, pady=5)

        self.button3 = tk.Button(self, text="Button 3")
        self.button3.pack(side=tk.LEFT, padx=5, pady=5)




    def load_data(self):
        """Loads data from the database and displays it in the table."""
        rows = db_helper.read_dataframe(db_path, "data")

        # Insert data into the table
        for row in rows:
            self.tree.insert("", "end", values=row)

    def save_data(self):
        """Saves data from the table to the database."""
        # Get the data from the table
        data = self.get_data()

        # Save  data to the database
        db_helper.insert_data(db_path, "data", data)

    def get_data(self):
        """Gets the data from the table and returns it as a list of tuples."""
        data = []

        # Get the selected rows
        selected_rows = self.tree.selection()

        # Iterate over the selected rows
        for row in selected_rows:
            # Get the values of the selected row
            values = self.tree.item(row)['values']

            # Append the values to the data list
            data.append(values)            

        return data
    def delete_data(self):
        """Deletes the selected data from the table."""
        # Get the selected rows
        selected_rows = self.tree.selection()

        # Iterate over the selected rows
        for row in selected_rows:
            # Delete the selected row
            self.tree.delete(row)

        # Save the data to the database
        db_helper.delete_data(db_path, "data", self.get_data())
    def update_data(self):
        """Updates the selected data in the table."""
        # Get the selected rows
        selected_rows = self.tree.selection()

        # Iterate over the selected rows
        for row in selected_rows:
            # Get the values of the selected row
            values = self.tree.item(row)['values']

            # Update the values in the database
            db_helper.update_data(db_path, "data", self.get_data())

            # Update the values in the table
            self.tree.item(row, values=values)
    def add_data(self):
        """Adds new data to the table."""
        # Get the data from the entry fields
        name = self.name_entry.get()
        age = self.age_entry.get()
        gender = self.gender_entry.get()
        city = self.city_entry.get()
        state = self.state_entry.get()
        country = self.country_entry.get()
        zip_code = self.zip_code_entry.get()
        email = self.email_entry.get()
        phone_number = self.phone_number_entry.get()

        # Add the data to the table
        self.tree.insert("", "end", values=[name, age, gender, city, state, country, zip_code, email, phone_number])

        # Save the data to the database
        db_helper.insert_data(db_path, "data", [(name, age, gender, city, state, country, zip_code, email, phone_number)])

    def search_data(self):
        """Searches for data in the table based on the search criteria and displays the results."""
    def search_data(self):
        """Searches for data in the table based on the search criteria."""
        # Get the search criteria
        search_criteria = self.search_entry.get()

        # Search for the data in the table
        self.tree.delete(*self.tree.get_children())
        rows = db_helper.read_dataframe(db_path, "data")

        for row in rows:
            if search_criteria in row:
                self.tree.insert("", "end", values=row)
    def apply_style(self, style):
        self.configure(bg=style['bg'])

# Run the application
if __name__ == "__main__":

    # Create an instance of the App class
    app = App()

    # Run the mainloop of the application
    app.mainloop()

    # Log the application exit

