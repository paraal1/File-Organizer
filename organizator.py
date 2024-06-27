import json
import os
import shutil
import tkinter as tk
from tkinter import messagebox, font, filedialog

import ttkbootstrap as ttk

# Icon file https://icon-icons.com/icon/plan-organizing-schedule-agenda-managing-planning/230470

# The directory path from where we want to clean up.
# Dictionary used for storing extension types.
with open('file_extensions.json', 'r') as file:
    file_extensions = json.load(file)


def organize_files():
    """
    Function to organize the files found in a directory
    :return:
    """
    folder_path = folder_entry.get()
    if folder_path is None or folder_path == "":
        messagebox.showwarning("Warning", "Please select the directory path where you want to organize your files")
    else:
        for root, directory, files in os.walk(folder_path):  # Iterate trought each file from /Downloads folder
            for file in files:
                create_folder(folder_path, root)
                source_path = os.path.join(root, folder_path)
                destination_path = os.path.join(root,
                                                search_for_specific_key(file_extensions, os.path.splitext(file)[1])[1])
                shutil.move(source_path, destination_path)
            if len(files) == 0:
                show_no_files_found()
            else:
                show_success_message()
            break


def search_for_specific_key(values, extension_type):
    """
    Function that search the extension name in the dictionary and return specific key
    :param values: file_extensions(dictionary)
    :param extension_type: extension name
    :returns: True and the key associated with the found value
    """
    for key in values:
        for value in values[key]:
            if extension_type in value:
                return True, key
    return False


def create_folder(file_input, root_input):
    """
    Function to check if folder exist in directory, if exists pass, if not creates it.
    :param file_input: File from the directory
    :param root_input: Root of the specific file
    :return:
    """
    folder_path = folder_entry.get()
    extension = os.path.splitext(file_input)
    if search_for_specific_key(file_extensions, extension[1]):
        check_key = search_for_specific_key(file_extensions, extension[1])[1]
        path = os.path.join(root_input, check_key)
        if os.path.exists(path):
            pass
        else:
            path = os.path.join(folder_path, check_key)
            os.mkdir(path)
    else:
        file_extensions['Unknown'].append(extension)
        create_folder(file, root)


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
    return folder_path


# Create the app's main window
root = ttk.Window(themename="darkly")
root.title("File Organization")
root.iconbitmap('images/plan_organizing_schedule_agenda_managing_planning_icon_230470.ico')
root.geometry("1280x800")

root.resizable(False, False)

# Create the frame for the title
title_frame = tk.Frame(root)
title_frame.pack(fill=tk.X, anchor='center', padx=30, pady=10)

title_h1 = font.Font(family="Helvetica", size=20, weight="bold")

# Create title label
title_label = ttk.Label(title_frame, text="TrashFile", font=title_h1)
title_label.pack(pady="10", anchor="w")

# Get the width of the frame
title_frame.update_idletasks()
frame_width = title_frame.winfo_width()

# Create the canvas for the underline
canvas = tk.Canvas(title_frame, height=2, bg="black", highlightthickness=0)
canvas.pack(fill=tk.X, pady=(15, 10))

# Draw the underline
canvas.create_line(0, 0, frame_width, 0, fill="grey")

# Create and add the actions label
actions_frame = ttk.LabelFrame(root, text="Actions", width=250, height=800)
actions_frame.pack(expand=True, anchor="e", pady=5, padx=30)
actions_frame.pack_propagate(False)

# Create folder selection
folder_label = ttk.Label(actions_frame, text="Select Folder:")
folder_label.pack(pady=5, side='top')
folder_entry = ttk.Entry(actions_frame, width=50)
folder_entry.pack(pady=5, side='top')
browse_button = ttk.Button(actions_frame, text="Browse", command=insert_path)
browse_button.pack(pady=5, side='top')

# Create and add the buttons for actions
organize_button = ttk.Button(actions_frame, text="Organize your files", width=20, command=organize_files)
organize_button.pack(pady=5, side='top')

# Create and add the button to show json data
show_json_button = ttk.Button(actions_frame, text="Show Extensions", width=20)
show_json_button.pack(pady=5, side='top')

root.mainloop()
