from time import sleep
import sys

from app import globals


# noinspection PyUnresolvedReferences
def main_logic(args):
    while True:
        sleep(0.001)  # give controll to app.run
        print(globals.current_task_id)
        try:
            current_task = globals.tasks[globals.current_task_id]
        except KeyError:
            sys.exit(1)
        if not current_task.is_initialized:
            current_task.initialize()

        if current_task.is_initialized:
            current_task.check_solution()

        if current_task.is_solved and not current_task.is_finished:
            current_task.finish()
        if current_task.is_finished:
            globals.current_task_id += 1
