import datetime
import numpy as np
import pandas as pd

return_time_fmt = time_fmt = "%Y-%m-%dT%H:%M:%S.%fZ"


class Task:
    def __init__(self, stream_listener, sensor_name_user):
        self.welcome_text = f"Please find sensor {sensor_name_user} and touch sensor."
        self.task_description = "Press button once within 5 seconds."
        self.task_completed_text = "Congratulations, task completed! Touch sensor to continue."
        self.is_initialized = False
        self.is_finished = False
        self.is_solved = False

        self.time_task_is_started = None
        self.time_task_is_finished = None
        self.my_sensor = "Sens-O-lympics Touch"
        self.stream_listener = stream_listener

    def initialize(self):
        init_time = None
        t1 = datetime.datetime.utcnow()
        while not init_time:
            json_data = self.stream_listener.get_sensor_events(self.my_sensor, t1)
            try:
                init_time = json_data[0]["touch"]["updateTime"]
                init_time = pd.to_datetime(np.datetime64(init_time))
                if not init_time >= t1:
                    init_time = None
            except TypeError:
                continue
            except IndexError:
                continue

        self.time_task_is_started = init_time
        print("Tas")
        self.is_initialized = True

    def finish(self):
        init_time = None
        t1 = datetime.datetime.utcnow()
        while not init_time:
            json_data = self.stream_listener.get_sensor_events(self.my_sensor, t1)
            json_data = sorted(json_data, key=lambda x: x["touch"]["updateTime"])
            try:
                init_time = json_data[-1]["touch"]["updateTime"]
                init_time = pd.to_datetime(np.datetime64(init_time))
                if not init_time >= t1:
                    init_time = None
            except TypeError:
                continue
            except IndexError:
                continue

        self.time_task_is_finished = pd.to_datetime(np.datetime64(init_time))
        self.is_finished = True

    def get_data(self):
        return self.stream_listener.get_sensor_events(self.my_sensor, self.time_task_is_started)

    def check_solution(self):
        sensor_data = self.get_data()
        # solution_data = sorted(solution_data, key=lambda x: x["touch"]["updateTime"])
        solution_data = []
        for s in sensor_data:
            if pd.to_datetime(np.datetime64(s["touch"]["updateTime"])) > self.time_task_is_started:
                solution_data.append(s)
        solution_data = sorted(solution_data, key=lambda x: x["touch"]["updateTime"])
        if len(solution_data) == 1:  # Initial touch is included
            self.is_solved = True


    def __str__(self):
        if not self.is_initialized:
            return self.welcome_text
        if not self.is_solved:
            return self.task_description
        if self.is_solved:
            return self.task_completed_text