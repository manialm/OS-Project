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

        # If the process's CPU burst is done, remove it from the ready list
        if (self.scheduling_info[next_process].cpu_remaining_time_1 == 0 or
                self.scheduling_info[next_process].cpu_remaining_time_2 == 0):
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

    def merge_intervals(self):
        first, *rest = self.intervals
        merged_intervals = [first]

        for process, burst_start, burst_end in rest:
            last_process, last_burst_start, last_burst_end = merged_intervals[-1]
            if last_process == process and last_burst_end == burst_start:
                merged_intervals[-1] = (process, last_burst_start, burst_end)
            else:
                merged_intervals.append((process, burst_start, burst_end))

        self.intervals = merged_intervals
