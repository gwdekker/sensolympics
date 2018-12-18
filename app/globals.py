from app.streamlistener import StreamListener, devices
from app.task import Task


def initialize():
    global current_task_id
    current_task_id = 0

    global device_list
    device_list = list(set(devices.keys()))

    global tasks
    tasks = {}
    for i, device in enumerate(device_list):
        tasks[i] = Task(StreamListener(), sensor_name_user=device_list[i])


