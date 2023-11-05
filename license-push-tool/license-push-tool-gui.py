import customtkinter
from tkinter import filedialog
import tkinter as tk
from utils import push_license, validate_ipv4_input, push_tool_quicktext
from datetime import datetime

'''
Utils and constants section
'''
# gui window size
window_width = 650
window_height= 480

# colors
RED= "#FF0000"
GREEN = "#00FF00"
BLACK = "#000000"

# Utils and constants
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("green")
loading = False

# time now
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
current_date = now.strftime("%m/%d/%Y")
run_result = f'{current_date} --- Run results --- \n'

# Global variable to store the selected file
selected_file = ""

'''
Helper functions section
'''
# helper functions to animate start and end of the main button animation
def start_loading_animation():
    global loading
    loading = True
    animate_loading()

# helper functions to animate start and end of the main button animation
def animate_loading():
    if loading:
        push_button.configure(text="Loading...")
        root.after(500, lambda: animate_loading())
        push_button.update_idletasks()  # Update the push_button display
    else:
        push_button.configure(text="Push license")

# helper functions to animate start and end of the main button animation
def stop_loading_animation():
    global loading
    loading = False
    push_button.configure(text="Push license")


# Function to reset all input fuilds to its initial states
def reset_fields_default():
    ip_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    file_entry.delete(0, tk.END)


# Function to set the default value for file_entry
def set_default_file():
    global selected_file  # Declare the global variable
    default_file = ""  # You can set a default file if needed

    # Use the selected file as the default if available
    initial_file = selected_file if selected_file else default_file

    file_entry.delete(0, tk.END)
    file_entry.insert(0, initial_file)

# Browse File button function
def browse_file_func():
    global selected_file  # Declare the global variable
    file_path = filedialog.askopenfilename(
        filetypes=[("BIN Files", "*.bin")], initialdir=selected_file, title="Select a .bin file")
    if file_path:
        selected_file = file_path  # Store the selected file
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)


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


'''
Main function for push license to the Pod and error handling
'''
# Function to start the license push process
def push_license_button_clicked():
    # getting data from the GUI input fields (strings)
    ip_address = ip_entry.get()
    password = password_entry.get()
    file_path = file_entry.get()

    # check if nessesery fulds are filled. (required)
    if file_path == "":
            update_text_widget("Please select license file \n")

    if ip_address == "":
            update_text_widget("Please provide Pods IP address \n")

    #check if password was provided, if not password filed will stay empty (not required)
    if password:
        auth = ('admin', password)
    else:
        auth = ('admin', '')

    try:
        start_loading_animation()
        response = push_license(ip=ip_address, admin_password=auth, path=file_path)
        response_formatted = response.text.split('"')
        response.raise_for_status()
        
        if response_formatted[-2] == 'passwordRequired':
            update_text_widget("Pod password required\n", False)
        elif response_formatted[-2] == 'Unable to apply license file change':
            update_text_widget(
                    f"{response_formatted[-2]}, please make sure you are selecting the correct license file for this specific Pod  \n", False)
        stop_loading_animation()

    except Exception as error:
        if str(error).split("'")[1] == "Connection aborted.":
            update_text_widget(
                " License uploaded and the Pod is rebooting to apply the new license.\n ")
            
            stop_loading_animation()
            reset_fields_default()
        else:
            stop_loading_animation()
            update_text_widget(error)
            update_text_widget("Could not connect to the Pod. \n", False)
    update_text_widget(run_result)

'''
GUI logic section
'''
root = customtkinter.CTk()
root.title("License Push Tool")

# Window logic section
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

'''
IP input section
'''
# IP Address Entry with validation
ip_label = customtkinter.CTkLabel(root, text="Pod IP address:")
ip_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

# Validation function to allow only valid IPv4 addresses
validate_ipv4_func = root.register(validate_ipv4_input)
ip_entry = customtkinter.CTkEntry(
    root, validate="key", validatecommand=(validate_ipv4_func, "%P"))
ip_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

'''
Pssword input section
'''
# Password Entry
password_label = customtkinter.CTkLabel(root, text="Pod admin password:")
password_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

password_entry = customtkinter.CTkEntry(root, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

'''
Browse button section
'''

# Set the default file when the app starts

# File Entry on the right
file_label = customtkinter.CTkLabel(root, text="Path to .bin license file:")
file_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")

file_entry = customtkinter.CTkEntry(root)
file_entry.grid(row=0, column=3, padx=10, pady=5, sticky="w")

set_default_file()


# Browse Button under the file input field on the right
browse_button = customtkinter.CTkButton(
    root, text="Browse", command=browse_file_func)
browse_button.grid(row=1, column=3, padx=10, pady=5, sticky="w")

'''
Push button section
'''
# Push License button in the middle
button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0, columnspan=4, pady=20)

push_button = customtkinter.CTkButton(
    button_frame, text="Push License", command=push_license_button_clicked)
push_button.pack()

'''
Text widget section
'''
# Text Field below the "Push License" button that stretches horizontally
text_widget = tk.Text(root, height=3, wrap=tk.WORD)
text_widget.config
text_widget.grid(row=3, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")
text_widget.insert(tk.END, push_tool_quicktext)
text_widget.config(state=tk.DISABLED)  # Disable text widget for editing

# Create a scrollbar
scrollbar = tk.Scrollbar(root)
scrollbar.grid(row=3, column=4, sticky="ns")

# Attach the scrollbar to the text_widget
text_widget.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_widget.yview)

'''
Grid section and start of GUI mainloop
'''
# Make the text field stretch horizontally and vertically
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)

root.mainloop()
