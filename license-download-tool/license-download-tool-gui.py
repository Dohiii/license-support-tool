from utils import pattern, LicenseUtil, ToolTip, download_tool_quicktext
import customtkinter
import tkinter as tk
from datetime import datetime
from tkinter import filedialog
import os

'''
Utils and constants section
'''
# gui window size
window_width = 600
window_height= 480

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("green")
loading = False
# colors
RED= "#FF0000"
GREEN = "#00FF00"
BLACK = "#000000"

success = []
license_json = {}
license = LicenseUtil()

# time now
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
current_date = now.strftime("%m/%d/%Y")

# the same folder as the compiled app.
default_folder = os.getcwd()

# Global variable to store the selected folder
selected_folder = ""

'''
Helper functions section
'''
def start_loading_animation():
    global loading
    loading = True
    animate_loading()


def animate_loading():
    if loading:
        push_button.configure(text="Loading...")
        root.after(500, lambda: animate_loading())
        push_button.update_idletasks()  # Update the push_button display
    else:
        push_button.configure(text="Download licenses")


def stop_loading_animation():
    global loading
    loading = False
    push_button.configure(text="Download licenses")


# Function to reset all input fuilds to its initial states
def reset_fields_default():
    id_entry.delete(0, tk.END)

# Update widget with information
def update_text_widget(text, is_success=True):
    text_widget.config(state=tk.NORMAL)  # Enable text widget for editing

    if is_success:
        text_widget.tag_config("success", foreground=BLACK)
        text_widget.insert("1.0", f" {text}", "success")
    else:
        text_widget.tag_config("error", foreground=RED)
        text_widget.insert("1.0", f" {text}", "error")

    text_widget.config(state=tk.DISABLED)  # Disable text widget for editing

# Functions to set the default value for folder_entry
def browse_folder_func():
    global selected_folder

    # If a folder was previously selected, use it as the initial directory
    initial_directory = selected_folder if selected_folder else default_folder

    folder_path = filedialog.askdirectory(initialdir=initial_directory)
    if folder_path:
        selected_folder = folder_path  # Store the selected folder
        folder_entry.delete(0, tk.END)  # Clear any existing text
        folder_entry.insert(0, selected_folder)

def set_default_folder():
    default_folder = os.getcwd()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, default_folder)


'''
Main function that handles downloading license file and error handling
'''
def main_func():
    global success
    global license_json
    ids_string = id_entry.get()
    values_arr = pattern.split(ids_string)
    license_path = folder_entry.get()
    start_loading_animation()

    for pod_id in values_arr:
        # Check if pod_id starts with "MPOD"
        if pod_id.startswith("MPOD") | pod_id.startswith("mpod") :
            license_json = {"serialId": pod_id.upper()}
        else:
            license_json = {"keplerId": pod_id.lower()}
        
        # if no license provided skip iteration and do nothing
        if pod_id == '':
            continue

        try:
            response, pod_id = license.pull_license(license_json, pod_id)
        
            license.save_license(response, pod_id, license_path)
            success.append(pod_id)
            update_text_widget(f"License created - {pod_id} \n")
        except Exception as error:
            str_error = str(error).split(":")[0].strip()
            update_text_widget(f"{str_error} \n", False)
            update_text_widget(f"license not created for - {pod_id} \n", False)

    stop_loading_animation()
    reset_fields_default()
    update_text_widget(f"\n {current_time} {current_date} --- Run results --- \n Created - {len(success)} license{'s' if len(success)>1 else ''} \n")
    success = []


'''
GUI logic starts here
'''
root = customtkinter.CTk()
root.title("License Download Tool")

# Window logic section

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x}+{y}")



'''
ID input section
'''
id_label = customtkinter.CTkLabel(root, text="Pod Serial Numbers or Device IDs:")
id_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

# Add a tooltip to the label
tooltip_text = "Device ID can be retrieved: \n\n - Solstice Dashboard under the Licensing tab > Device Info.\n - Solstice Cloud under Monitor > Deployment.\n - Directly from the Pod’s “Update and Licensing” configuration settings tab \n"
tooltip = ToolTip(id_label, tooltip_text)

# Make id_entry span columns 1 and 2 to take up more space
id_entry = customtkinter.CTkEntry(root)
id_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

'''
Folder select section
'''
# File Entry on the right
folder_label = customtkinter.CTkLabel(root, text="Path to save license files:")
folder_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

folder_entry = customtkinter.CTkEntry(root)
folder_entry.grid(row=1, column=1, columnspan=1, padx=10, pady=5, sticky="ew")

# Browse Button under the file input field on the right
browse_button = customtkinter.CTkButton(
    root, text="Browse", command=browse_folder_func)
browse_button.grid(row=1, column=2, padx=10, pady=5, sticky="w")

# Set the default value for folder_entry
set_default_folder()

'''
Download button section
'''
# Push License button in the middle
button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0, columnspan=4, pady=20)

push_button = customtkinter.CTkButton(
    button_frame, text="Download licenses", command=main_func)
push_button.pack()

'''
Text widget section
'''
# Text Field below the "Push License" button that stretches horizontally
text_widget = tk.Text(root, height=3, wrap=tk.WORD)
text_widget.config
text_widget.grid(row=3, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")
text_widget.insert(tk.END, download_tool_quicktext)
text_widget.config(state=tk.DISABLED)  # Disable text widget for editing

# Create a scrollbar
scrollbar = tk.Scrollbar(root)
scrollbar.grid(row=3, column=4, sticky="ns")

# Attach the scrollbar to the text_widget
text_widget.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_widget.yview)


'''
GRID section and main loop start.
'''
# Make the text field stretch horizontally and vertically
root.grid_rowconfigure(3, weight=5)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=5)

root.mainloop()