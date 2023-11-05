import re
import requests
import os
from tkinter import *
import tkinter as tk

# utils
pattern = re.compile(r'[ ,.!;]+')

download_tool_quicktext = "\nLicense Download Tool:\n"\
       "\nUtilize this tool to download one or multiple license files for Mersive Pods running Solstice version 5.5.3 or higher.\n"\
       "\nPlease enter the Pod Device IDs or Serial Numbers in the input field. You can separate multiple entries using spaces, commas, or semicolons.\n"\
       "\nYou can choose to save the license files to the root of a FAT32 formatted USB flash drive in order to force load them onto the Pods.\n"\
       "\nOnce saved, insert the drive into the Pod's USB port to force-load the license.\n"\
       "\nIf multiple Pods are being updated, you can save multiple license files to the same USB drive.\n"\
       "\nThe USB flash drive MUST be inserted into an already fully powered up Pod.\n"\
       "\nIf booting up the Pod, DO NOT have the flash drive in it. Wait until you see the standard Pod Welcome screen background."

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None

        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip_window, text=self.text, background="lightyellow", relief="solid", borderwidth=1, justify="left", padx=10, pady=5)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class LicenseUtil:
    URL = "https://kepler-backend.mersive.com:443/licensing/v1"
    header = {
    "Content-Type": "application/json",
    "accept": "application/json"
    }

    def pull_license(self, license_json, pod_id):
        """Pulls the license from MCL. """
        response = requests.post(url=self.URL + "/license/license",
                                    headers=self.header, json=license_json)
        response.raise_for_status()
        return response, pod_id
        # self.save_license(response, pod_id)

    def save_license(self, response, pod_id, path=None):
        """
        Saving the license to a file (pod_id.bin) in the specified directory (or the script's directory if path is not provided).
        
        :param response: The license data to save.
        :param pod_id: The Pod ID used in the filename.
        :param path: The directory where the file should be saved (optional).
        """
        if path is not None:
            file_path = os.path.join(path, f"mcl_{pod_id}.bin")
        else:
            file_path = f"mcl_{pod_id}.bin"

        with open(file_path, "w") as lic_file:
            lic_file.write(response.text)


