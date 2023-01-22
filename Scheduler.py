"""
self.scheduling_info = {
    Process1: SchedulingInfo(cpu_remaining_time_1, io_left_time, cpu_remaining_time_2),
    Process2: SchedulingInfo(cpu_remaining_time_1, io_left_time, cpu_remaining_time_2),
    ...
}
"""
from queue import PriorityQueue
from SchedulingInfo import SchedulingInfo
from Process import Process


class Scheduler:

    def __init__(self, algorithm, processes: list[Process]):
        self.last_time = -1
        self.time = 0
        self.algorithm = algorithm

        self.processes = processes
        self.ready_list: list[tuple[int, Process]] = []
        self.scheduling_info = {}
        for process in processes:
            self.ready_list.append((process.arrival_time, process))

            self.scheduling_info[process] = SchedulingInfo(
                process.cpu_burst_time_1,
                process.io_time,
                process.cpu_burst_time_2)

        # 3-Tuples of (process, burst start, burst end)
        self.intervals: list[tuple[Process, int, int]] = []

    def schedule_cpu(self):
        first_process_arrival_time, _ = min(self.ready_list)
        if self.time < first_process_arrival_time:
            self.time = first_process_arrival_time

        ready_now = [(arrival_time, process) for arrival_time, process in self.ready_list
                     if arrival_time <= self.time]
        arrival_time, next_process, service_time = self.algorithm.choose_next(
            self.scheduling_info, ready_now
        )
        self.ready_list.remove((arrival_time, next_process))

        self.intervals.append(
            (next_process, self.time, self.time + service_time)
        )

        self.time += service_time

        scheduling_info = self.scheduling_info[next_process]

        # First CPU burst
        if scheduling_info.cpu_remaining_time_1 > 0:
            scheduling_info.cpu_remaining_time_1 -= service_time

            # IO Burst
            if scheduling_info.cpu_remaining_time_1 == 0:
                if scheduling_info.io_remaining_time > 0:
                    self.schedule_io(next_process)

        else:
            # Second CPU burst
            self.scheduling_info[next_process].cpu_remaining_time_2 -= service_time

    def schedule(self):
        while len(self.ready_list) > 0:
            self.schedule_cpu()

    def schedule_io(self, process):
        io_time = self.scheduling_info[process].io_remaining_time
        self.ready_list.append((self.time + io_time, process))

    def print_intervals(self):
        for process, burst_start, burst_end in self.intervals:
            print(f"P{process.process_id}: ({burst_start}, {burst_end})")
