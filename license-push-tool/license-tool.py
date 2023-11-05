import requests
import urllib3
import argparse


# Description for argparse help.
tool_description = "This tool allows sending Solstice license files to Pods. To receive your license file please " \
                   "contact Mersive support support@mersive.com."

if __name__ == "__main__":
    # Create command line arguments parser.
    parser = argparse.ArgumentParser(add_help=True, description=tool_description,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--ip", required=True, nargs=1, type=str, metavar="ip.add.re.ss",
                        help="Specify Pod's IP address separated by coma")
    parser.add_argument("--license", required=True, nargs=1, type=str, metavar="c:\path_to\mcl_<pod_id>.bin",
                        help="Uploads licence file to Pod. Specify path and file name after argument. If the license is"
                             "valid the pod will reboot automatically to apply it.")
    parser.add_argument("--pwd", nargs=1, help="For Pods that use admin password, please specify the password after the"
                                               " argument.")
    parser.add_argument("-v", "--version", action="version", version="1.0.0")
    args = parser.parse_args()

# Check if an IP address/es is provided and add them to a list.
if args.ip:
    pods = args.ip[0].split(",")

if args.pwd:
    auth = ('admin', args.pwd[0])
else:
    auth = ('admin', '')

# Ignoring unsigned certificates.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Push a new license file to a pod. Since license files are pod specific, this option works with 1 pod at a time.
if args.license:
    print("Sending license file to Pod. The Pod will reboot after the license is applied.")
    url = f"https://{args.ip[0]}/Config/service/uploadLicense"
    license_file = {"LICENSE_pkg": open(args.license[0], "rb")}
    try:
        response = requests.post(url, files=license_file, verify=False, auth=auth)
        response_formatted = response.text.split('"')
        response.raise_for_status()
        print(response_formatted[-2])

    except Exception as error:
        if str(error).split("'")[1] == "Connection aborted.":
            print("License uploaded and the pod is rebooting to apply the new license.")
        else:
            print(error)
            print("Could not connect to pod.")



