
import os
import requests

from app import utils

time_fmt = "%Y-%m-%dT%H:%M:%SZ"

devices = {
    "Sens-O-lympics Prox 0" : "bdoktct7rihjbm0408n0",
    "Sens-O-lympics Touch" : "bdoktct7rihjbm0408o0",
    "Sens-O-lympics Prox 1" : "bdoktc57rihjbm0400o0",
    "Sens-O-lympics Temp 0" : "bdoktbt7rihjbm03vtng",
    "Sens-O-lympics Temp 1" : "bchoqbl7rihkg465932g"
}


class StreamListener:

    def get_sensor_events(self, sensor_name, time_from=None):
        # print(f"StreamListener sees {sensor_name}, {time_from}")

        device_id = devices.get(sensor_name)

        utils.load_dotenv()

        username = os.environ["SERVICE_ACCOUNT_KEY"]
        password = os.environ["SERVICE_ACCOUNT_SECRET"]
        project_id = os.environ["PROJECT_ID"]

        api_url_base = "https://api.disruptive-technologies.com/v2"
        url = f"{api_url_base}/projects/{project_id}/devices/{device_id}/events?"
        url += f"event_types=touch&event_types=temperature&event_types=objectPresent&"

        if time_from:
            time_url_format = time_from.strftime(time_fmt)
            url += f"start_time={time_url_format}"

        response = requests.get(
            url,
            auth=(username, password),
            headers={"accept" : "application/json"},
        )
        try:
            event_list = [e['data'] for e in response.json()['events']]
        except KeyError:
            event_list = []

        return event_list


