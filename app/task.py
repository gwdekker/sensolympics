import datetime
import numpy as np
import pandas as pd

return_time_fmt = time_fmt = "%Y-%m-%dT%H:%M:%S.%fZ"


def sort_function(x):
            try:
                return x["touch"]["updateTime"]
            except KeyError:
                return x["temperature"]["updateTime"]


class Task:
    def __init__(self, stream_listener, sensor_name_user):
        self.stream_listener = stream_listener
        self.my_sensor = sensor_name_user

        self.welcome_text = f"Please find sensor {self.my_sensor} and touch sensor."
        self.task_description = "Press button once within 5 seconds."
        self.task_completed_text = "Congratulations, task completed! Touch sensor to continue."
        self.is_initialized = False
        self.is_finished = False
        self.is_solved = False

        self.time_task_is_started = None
        self.time_task_is_finished = None

    def initialize(self):
        init_time = None
        t1 = datetime.datetime.utcnow()
        while not init_time:
            json_data = self.stream_listener.get_sensor_events(self.my_sensor, t1)
            try:
                # Index = 0 since we need first touch
                init_time = self.get_init_time(json_data, t1, 0)
            except TypeError:
                continue
            except IndexError:
                continue

        self.time_task_is_started = init_time
        print("Tas")
        self.is_initialized = True

    @staticmethod
    def get_init_time(json_data, t1, index):
        try:
            init_time = json_data[index]["touch"]["updateTime"]
            init_time = pd.to_datetime(np.datetime64(init_time))
            if not init_time > t1:
                init_time = None
        except KeyError:
            try:
                init_time = json_data[index]["temperature"]["updateTime"]
            except KeyError:
                init_time = json_data[index]["objectPresent"]["updateTime"]

            init_time = pd.to_datetime(np.datetime64(init_time))
            if not init_time > t1:
                init_time = None
        return init_time

    def finish(self):
        init_time = None
        t1 = datetime.datetime.utcnow()
        while not init_time:
            json_data = self.stream_listener.get_sensor_events(self.my_sensor, t1)
            json_data = sorted(json_data, key=sort_function)
            try:
                # Index = -1 since we need last touch
                init_time = self.get_init_time(json_data, t1, -1)
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
        timestamps = []
        for s in sensor_data:
            try:
                t = pd.to_datetime(np.datetime64(s["touch"]["updateTime"]))
                if t > self.time_task_is_started and t not in timestamps:
                    timestamps.append(t)
                    solution_data.append(s)
            except KeyError:
                t = pd.to_datetime(np.datetime64(s["temperature"]["updateTime"]))
                if  t > self.time_task_is_started and t not in timestamps:
                    timestamps.append(t)
                    solution_data.append(s)

        solution_data = sorted(solution_data, key=sort_function)
        if len(timestamps) == 1:  # Initial touch is included
            self.is_solved = True

    def __str__(self):
        if not self.is_initialized:
            return self.welcome_text
        if not self.is_solved:
            return self.task_description
        if self.is_solved:
            return self.task_completed_text


class TempTask(Task):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.welcome_text = f"Please find sensor {self.my_sensor} and touch sensor. It is located at the table"
        self.task_description = "It's god damn cold here!"
        self.task_completed_text = "Congratulations, task completed! Touch sensor to continue."

        self.temp_lim = None

    def check_solution(self):
        sensor_data = self.get_data()
        # solution_data = sorted(solution_data, key=lambda x: x["touch"]["updateTime"])
        solution_data = []
        timestamps = []
        temp_values = []
        for s in sensor_data:
            try:
                t = pd.to_datetime(np.datetime64(s["temperature"]["updateTime"]))
                value = s["temperature"]["value"]
                if not self.temp_lim:
                    self.temp_lim = value + 2.0
                if t > self.time_task_is_started and t not in timestamps:
                    timestamps.append(t)
                    temp_values.append(value)
                    solution_data.append(s)
            except KeyError:
                continue
        temp_values.sort(reverse=True)
        try:
            if max(temp_values) >= self.temp_lim:  # Initial touch is included
                self.is_solved = True
        except ValueError:
            pass


class ProxTask(Task):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.welcome_text = f"Please find sensor {self.my_sensor} and touch sensor. It is located at the table"
        self.task_description = "Press and hold sensor for 3*pi seconds (+- 10%)"
        self.task_completed_text = "Congratulations, task completed! Touch sensor to continue."

        self.target_time = 3*np.pi

    def check_solution(self):
        sensor_data = self.get_data()
        solution_data = []
        timestamps = []
        not_present_times = [s['objectPresent']['updateTime']
                             for s in sensor_data
                             if ("objectPresent" in s.keys() and
                                 s['objectPresent'].get('state') == 'NOT_PRESENT') ]
        present_times = [s['objectPresent']['updateTime']
                             for s in sensor_data
                             if ("objectPresent" in s.keys() and s['objectPresent'].get('state') == 'PRESENT') ]
        if len(present_times) > len(not_present_times):
            present_times = present_times[1:]
        if len(not_present_times) == 0:
            return False

        press_duration_s = (pd.to_datetime(not_present_times[0]) - pd.to_datetime(present_times[0])).total_seconds()

        self.task_description = f"Press and hold sensor for 3π seconds (+- 10%). " \
            f"Last registered press: {press_duration_s:.2f} seconds"

        if abs(press_duration_s - self.target_time)/self.target_time <= 0.1:
            self.is_solved = True
            self.task_completed_text = f"Congratulations, task completed! \n" \
                f"You pressed for {press_duration_s / np.pi:.2f} π seconds. \n Touch sensor to continue."
