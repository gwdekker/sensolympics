import datetime
import os
import requests

from flask import render_template, redirect, url_for

from app import app
from app.streamlistener import StreamListener, devices
from app.task import Task, MaxTempTask, MinTempTask, ProxTask, ProxTask1, TouchTask

from app import globals


@app.route("/restart")
def restart():
    globals.current_task_id = 0

    globals.device_list = list(set(devices.keys()))

    globals.tasks = {}
    for i, device in enumerate(globals.device_list):
        task_cls = Task
        if globals.device_list[i] == "Sens-O-lympics Temp 0":
            task_cls = MaxTempTask
        elif globals.device_list[i] == "Sens-O-lympics Temp 1":
            task_cls = MinTempTask
        elif globals.device_list[i] == "Sens-O-lympics Prox 0":
            task_cls = ProxTask
        elif globals.device_list[i] == "Sens-O-lympics Prox 1":
            task_cls = ProxTask1
        elif globals.device_list[i] == "Sens-O-lympics Touch":
            task_cls = TouchTask
        globals.tasks[i] = task_cls(
            StreamListener(), sensor_name_user=globals.device_list[i]
        )

    globals.t_start = datetime.datetime.now()

    globals.total_time = None
    return redirect(url_for("main"))


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
