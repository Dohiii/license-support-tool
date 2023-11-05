import requests
import re


push_tool_quicktext = "\nLicense Push Tool:\n"\
       "\nUtilize this tool to push one license file to a Mersive Pod running Solstice version 5.5.3 or higher.\n"\
       "\nPlease enter the Pod IP address in the IP address input field.\n"\
       "\nYou can locate the specific license file by pressing the Browse button and selecting the appropriate .bin license file.\n"\
       "\nIf an administrator password is configured on the Pod, please enter it in the Pod admin password field.\n"\
       "\nPress the Push License button to push the license file to the Pod. The Pod will reboot in order to apply the new license.\n"\

# Push a new license file to a pod. Since license files are pod specific, this option works with 1 pod at a time.
def push_license(ip, admin_password, path):
    url = f"https://{ip}/Config/service/uploadLicense"
    license_file = {"LICENSE_pkg": open(path, "rb")}
    response = requests.post(
        url, files=license_file, verify=False, auth=admin_password)
    return response


# Function to validate an IPv4 address, accepts input from the Device IP fuild
def validate_ipv4_input(input_ip_value):
    # Allow empty input
    if input_ip_value == "":
        return True
    # Check if the input matches the IPv4 pattern
    ip_pattern = r'^(\d{0,3}\.){0,3}\d{0,3}$'
    return re.match(ip_pattern, input_ip_value) is not None


