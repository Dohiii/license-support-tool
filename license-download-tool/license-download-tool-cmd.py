import requests
import argparse

#test
#test
URL = "https://kepler-backend.mersive.com:443/licensing/v1"
header = {
    "Content-Type": "application/json",
    "accept": "application/json"
    }

def pull_license(license_json):
    """Pulls the license from MCL. """
    response = requests.post(url=URL + "/license/license", headers=header, json=license_json)
    response.raise_for_status()
    save_license(response, pod_id)

def save_license(r, pod_id):
    "Saving license to a file (pod_id.bin) in the same folder as the script."
    with open(f"mcl_{pod_id}.bin", "w") as lic_file:
        lic_file.write(r.text)
    print(f"License was saved as mcl_{pod_id}.bin")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This tool allows downloading licenses from MCL prod. environ. for"
                                                 "support purposes.")
    parser.add_argument("--podID", required=True, nargs="+", help="Specify pod IDs.")

    args = parser.parse_args()

# Create a list of pod IDs and get license.
for pod_id in args.podID:
    license_json = {"keplerId": pod_id}
    pull_license(license_json)

