import json
import os
import shutil
import tkinter as tk
from tkinter import messagebox, font, filedialog

import ttkbootstrap as ttk

# The directory path from where we want to clean up.
# Dictionary used for storing extension types.
with open('file_extensions.json', 'r') as file:
    file_extensions = json.load(file)

showed_dictionary = 0


def organize_files():
    """
    Function to organize the files found in a directory
    :return:
    """
    folder_path = folder_entry.get()
    if not folder_path:
        messagebox.showwarning("Warning", "Please select the directory path where you want to organize your files")
        return

    for root, _, files in os.walk(folder_path):  # Iterate through each file in the folder
        if files:
            for file in files:
                create_folder(file, root)
                source_path = os.path.join(root, file)
                destination_folder = search_for_specific_key(file_extensions, os.path.splitext(file)[1])[1]
                destination_path = os.path.join(root, destination_folder)
                shutil.move(source_path, destination_path)
            show_success_message()
        else:
            show_no_files_found()
        break


def search_for_specific_key(values, extension_type):
    """
    Search the extension name in the dictionary and return a specific key
    :param values: file_extensions (dictionary)
    :param extension_type: extension name
    :returns: True and the key associated with the found value
    """
    for key, exts in values.items():
        if extension_type in exts:
            return True, key
    return False, 'Unknown'


def create_folder(file_name, root_input):
    """
    Check if folder exists in directory; if not, create it.
    :param file_name: File from the directory
    :param root_input: Root of the specific file
    """
    folder_path = folder_entry.get()
    extension = os.path.splitext(file_name)[1]
    key = search_for_specific_key(file_extensions, extension)[1]

    folder_to_create = os.path.join(root_input, key)
    if not os.path.exists(folder_to_create):
        os.mkdir(folder_to_create)


def show_success_message():
    messagebox.showinfo("Success", "The files are now organized")


def show_no_files_found():
    messagebox.showinfo("Success", "No unorganized files were found in the specified directory")


def insert_path():
    folder_path = filedialog.askdirectory()
    folder_entry.config(state=tk.NORMAL)
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)
    folder_entry.config(state=tk.DISABLED)


def prepare_dictionary_for_treeview():
    global showed_dictionary
    if not showed_dictionary:
        for key, values in file_extensions.items():
            parent_key = extensions_treeview.insert("", tk.END, text=key)
            for value in values:
                extensions_treeview.insert(parent_key, tk.END, text=value)
        showed_dictionary = 1


# Function to get the full path of the selected item
def get_selected_item_path(event):
    selected_item = extensions_treeview.selection()[0]  # Get the selected item
    item_path = []  # List to store the item path

    # Traverse up the hierarchy to build the path
    while selected_item:
        item = extensions_treeview.item(selected_item)
        item_name = item['text']
        item_path.insert(0, item_name)  # Insert at the beginning of the path
        selected_item = extensions_treeview.parent(selected_item)  # Get the parent item

    full_path = "/".join(item_path)  # Join the path using a separator (e.g., '/')
    print("Selected Item Path:", full_path)


# Create the app's main window
root = ttk.Window(themename="darkly")
root.title("File Organization")
root.iconbitmap('images/plan_organizing_schedule_agenda_managing_planning_icon_230470.ico')
root.geometry("600x600")
root.resizable(False, False)

# Title Section
title_frame = tk.Frame(root)
title_frame.pack(fill=tk.X, anchor='center', padx=30, pady=10)
title_label = ttk.Label(title_frame, text="TrashFile", font=font.Font(family="Helvetica", size=20, weight="bold"))
title_label.pack(pady="10", side="top")
title_frame.update_idletasks()
canvas = tk.Canvas(title_frame, height=2, bg="black", highlightthickness=0)
canvas.pack(fill=tk.X, pady=(15, 10))
canvas.create_line(0, 0, title_frame.winfo_width(), 0, fill="grey")

# Actions Section
actions_frame = ttk.LabelFrame(root, text="Actions", width=250, height=250)
actions_frame.pack(expand=True, side="left", anchor="nw", padx="25")
actions_frame.pack_propagate(False)
ttk.Button(actions_frame, text="Organize your files", width=20, command=organize_files).pack(pady=5, side='top')
ttk.Button(actions_frame, text="Show Extensions", width=20, command=prepare_dictionary_for_treeview).pack(pady=5,
                                                                                                          side='top')
ttk.Label(actions_frame, text="Select Folder:").pack(pady=5, side='top')
folder_entry = ttk.Entry(actions_frame, width=25)
folder_entry.pack(pady=5, side='top')
ttk.Button(actions_frame, text="Browse", command=insert_path).pack(pady=5, side='top')

# Extensions Section
extensions_frame = ttk.LabelFrame(root, text="Extensions", height=150, width=200)
extensions_frame.pack(side='top', fill="both", padx=25, expand=True)

extension_button_frame = ttk.LabelFrame(extensions_frame, text="Actions")
extension_button_frame.pack(side='top', fill="both")

delete_extension_button = ttk.Button(extension_button_frame, text="Add", )
delete_extension_button.pack(side='left', padx=15)

add_extension_button = ttk.Button(extension_button_frame, text="Remove")
add_extension_button.pack(side='right', padx=15)

extensions_treeview = ttk.Treeview(extensions_frame)
extensions_treeview.pack()

# Bind the Treeview to a function that will get the selected item's name
extensions_treeview.bind('<<TreeviewSelect>>', get_selected_item_path)
root.mainloop()
