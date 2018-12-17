import json
import pprint
import os

import requests
import sseclient

from disrupting_vang import utils

utils.load_dotenv()

username = os.environ["SERVICE_ACCOUNT_KEY"]
password = os.environ["SERVICE_ACCOUNT_SECRET"]
project_id = os.environ["PROJECT_ID"]

api_url_base = "https://api.disruptive-technologies.com/v2"
devices_list_url = f"{api_url_base}/projects/{project_id}/devices"
devices_stream_url = f"{api_url_base}/projects/{project_id}/devices:stream"

# Get list of Devices in Project via API
device_listing = requests.get(devices_list_url, auth=(username, password))

# Print list of Devices
devices = device_listing.json()["devices"]
print(f"The Inventory Project contains {len(devices)} device(s):")
for v in devices:
    print(v["name"])
print()

# Listen to all events from all Devices in Project via API
print("Listening for events... (press CTRL-C to abort)")
response = requests.get(
    devices_stream_url,
    auth=(username, password),
    headers={"accept": "text/event-stream"},
    stream=True,
)
client = sseclient.SSEClient(response)
for event in client.events():
    pprint.pprint(json.loads(event.data))
