import datetime

from app.streamlistener import StreamListener, devices
from app.task import Task, MaxTempTask, MinTempTask, ProxTask, TouchTask


def initialize():
    global current_task_id
    current_task_id = 0

    global device_list
    device_list = list(set(devices.keys()))

    global tasks
    tasks = {}
    for i, device in enumerate(device_list):
        task_cls = Task
        if device_list[i] == "Sens-O-lympics Temp 0":
            task_cls = MaxTempTask
        elif device_list[i] == "Sens-O-lympics Temp 1":
            task_cls = MinTempTask
        elif "Prox" in device_list[i]:
            task_cls = ProxTask
        elif device_list[i] == "Sens-O-lympics Touch":
            task_cls = TouchTask
        tasks[i] = task_cls(StreamListener(), sensor_name_user=device_list[i])

    global t_start
    t_start = datetime.datetime.now()

    global  total_time
    total_time = None