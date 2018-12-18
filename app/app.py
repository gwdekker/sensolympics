import sys
from time import sleep

from flask import render_template

from app import app

from app.streamlistener import StreamListener, devices

# initialize app
from app.task import Task

# stream_listener = StreamListener()

current_task_id = 0


device_list = list(set(devices.keys()))
tasks = {}
for i, device in enumerate(device_list):
    tasks[i] = Task(StreamListener(), sensor_name_user=device_list[i])


@app.route("/restart")
def restart():
    global current_task_id
    current_task_id = 0


# set up routes
@app.route("/")
def main():
    global current_task_id
    try:
        return render_template("index.html", text=str(tasks[current_task_id]))
    # return render_template('index.html', text=str(tasks[current_task_id]))
    except KeyError:
        return render_template("index.html", text="Game over. Go team or go home!")


def doStuff(args):
    while True:
        sleep(0.001)  # give controll to app.run
        global current_task_id
        print(current_task_id)
        try:
            current_task = tasks[current_task_id]
        except KeyError:
            sys.exit(1)
        if not current_task.is_initialized:
            current_task.initialize()

        if current_task.is_initialized:
            current_task.check_solution()

        if current_task.is_solved and not current_task.is_finished:
            current_task.finish()
        if current_task.is_finished:
            current_task_id += 1

        # task_id = 0
        # task = tasks[task_id]
        # while True :
        #     while not task.is_started :
        #         task.start()
        #         continue
        #     print(f"Assignment {task_id} is started!")
        #     while not task.is_solved(data_in) :
        #         continue
        #     print(f"Assignment {task_id} is solved!")
        #     task_id += 1
        #     task = tasks.get(task_id)
        #     if task is None :
        #         print('Finished')
