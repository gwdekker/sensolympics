import json
from threading import Thread
from time import sleep

from flask import Flask, render_template


from disrupting_vang.streamlistener import StreamListener

# initialize app
from disrupting_vang.task import Task

app = Flask(__name__)

stream_listener = StreamListener()

current_task_id = 0

tasks = {0: Task(stream_listener, sensor_name_user="First sensor"),
         1: Task(stream_listener, sensor_name_user="Second sensor"),
         2: Task(stream_listener, sensor_name_user="Third sensor"),
         3: None}

# set up routes
@app.route('/')
def main():
    global current_task_id
    return render_template('index.html', text=str(tasks[current_task_id]))


def doStuff(args):
    while True:
        sleep(0.5)  # give controll to app.run
        global current_task_id

        current_task = tasks[current_task_id]
        if not current_task.is_initialized:
            current_task.initialize()

        if current_task.check_solution():
            print(f"Solved task {current_task_id}!")
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
