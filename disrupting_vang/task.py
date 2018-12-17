import datetime
import numpy as np
import pandas as pd

return_time_fmt = time_fmt = "%Y-%m-%dT%H:%M:%S.%fZ"

class Task:
    def __init__(self, stream_listener, sensor_name_user):
        self.welcome_text = f"Please find sensor {sensor_name_user} and touch sensor."
        self.task_description = "Press button twice within 10 seconds."
        self.task_completed_text = "Congratulations. Task completed!"
        self.is_initialized = False
        self.is_solved = False

        self.time_task_is_started = None
        self.my_sensor = "Sens-O-lympics Touch"
        self.stream_listener = stream_listener

    def initialize(self):
        init_time = None
        t1 = datetime.datetime.utcnow()
        while not init_time:
            json_data = self.stream_listener.get_sensor_events(self.my_sensor, t1)
            try:
                init_time = json_data[0]["touch"]["updateTime"]
            except TypeError:
                continue
            except IndexError:
                continue

        self.time_task_is_started = pd.to_datetime(np.datetime64(init_time))
        self.is_initialized = True

    def get_data(self):
        return self.stream_listener.get_sensor_events(self.my_sensor, self.time_task_is_started)

    def check_solution(self):
        if len(self.get_data()) > 0:
            self.is_solved = True
        return self.is_solved

    def __str__(self):
        if not self.is_initialized:
            return self.welcome_text
        if not self.is_solved:
            return self.task_description
        if self.is_solved:
            return self.task_completed_text