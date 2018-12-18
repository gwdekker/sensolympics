from app.streamlistener import StreamListener, devices
from app.task import Task, TempTask


def initialize():
    global current_task_id
    current_task_id = 0

    global device_list
    device_list = list(set(devices.keys()))

    global tasks
    tasks = {}
    for i, device in enumerate(device_list):
        task_cls = Task
        if "Temp" in device_list[i]:
            task_cls = TempTask
        tasks[i] = task_cls(StreamListener(), sensor_name_user=device_list[i])
