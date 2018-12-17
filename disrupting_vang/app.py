import json
import sys
from threading import Thread
from time import sleep

from flask import Flask, render_template


from disrupting_vang.streamlistener import StreamListener, devices

# initialize app
from disrupting_vang.task import Task

app = Flask(__name__)

# stream_listener = StreamListener()

current_task_id = 0


device_list = list(set(devices.keys()))
tasks = {}
for i, device in enumerate(device_list):
    tasks[i] = Task(StreamListener(), sensor_name_user=device_list[i])

# set up routes
@app.route('/')
def main():
    global current_task_id
    try:
        return render_template('index.html', text=str(tasks[current_task_id]))
    # return render_template('index.html', text=str(tasks[current_task_id]))
    except KeyError:
        return render_template('index.html', text="Game over. Go team or go home!")

def doStuff(args):
    while True:
        sleep(0.5)  # give controll to app.run
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


if __name__ == "__main__":
    thread = Thread(target=doStuff, args=(10,))
    thread.start()
    app.run()
