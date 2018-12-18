import datetime
import os
import requests

from flask import render_template, redirect, url_for

from app import app

from app import globals


@app.route("/restart")
def restart():
    globals.initialize()
    return redirect(url_for("/"))


@app.route("/get-all-sensors")
def all_sensors():
    username = os.environ["SERVICE_ACCOUNT_KEY"]
    password = os.environ["SERVICE_ACCOUNT_SECRET"]
    project_id = os.environ["PROJECT_ID"]

    api_url_base = "https://api.disruptive-technologies.com/v2"
    devices_list_url = f"{api_url_base}/projects/{project_id}/devices"

    # Get list of Devices in Project via API
    device_listing = requests.get(devices_list_url, auth=(username, password))

    # Print list of Devices
    devices = device_listing.json()["devices"]
    return str(devices)


# set up routes
@app.route("/")
def main():
    try:
        return render_template(
            "index.html", text=str(globals.tasks[globals.current_task_id])
        )
    except KeyError:
        if not globals.total_time:
            globals.total_time = datetime.datetime.now() - globals.t_start
        return render_template(
            "index.html",
            text=f"Game over. Go team or go home! You used {globals.total_time} ",
        )
