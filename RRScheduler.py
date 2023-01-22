from queue import PriorityQueue
from Process import Process
from SchedulingInfo import SchedulingInfo
from collections import defaultdict

class RRScheduler:

    def __init__(self, time_quantum: int, processes: list[Process]):
        self.time_quantum = time_quantum
        self.processes = processes
        self.queue = PriorityQueue()

        self.scheduling_info = {}
        for process in processes:
            self.queue.put((process.arrival_time, process))

            self.scheduling_info[process] = SchedulingInfo(
                process.cpu_burst_time_1,
                process.io_time,
                process.cpu_burst_time_2)

        self.intervals: list[tuple[Process, int, int]] = []
        self.first_burst_end: dict[Process] = {}
        self.time = 0

    def schedule_cpu(self):
        arrival_time, next_process = self.queue.get()
        if arrival_time > self.time:
            self.time = arrival_time

        remaining_time = self.remaining_time(next_process)
        service_time = min(self.time_quantum, remaining_time)

        self.intervals.append((next_process, self.time, self.time + service_time))
        self.time += service_time

        # If the process still needs the CPU, put it back in the (future) queue
        remaining_time -= service_time
        if remaining_time > 0:
            self.queue.put((self.time, next_process))

        scheduling_info = self.scheduling_info[next_process]

        # First CPU burst
        if scheduling_info.cpu_remaining_time_1 > 0:
            scheduling_info.cpu_remaining_time_1 -= service_time

            # IO Burst
            if scheduling_info.cpu_remaining_time_1 == 0:
                self.first_burst_end[next_process] = self.time
                if scheduling_info.io_remaining_time > 0:
                    self.schedule_io(next_process)

        else:
            # Second CPU burst
            scheduling_info.cpu_remaining_time_2 -= service_time

    def schedule(self):
        while not self.queue.empty():
            self.schedule_cpu()

    def schedule_io(self, process: Process):
        io_time = self.scheduling_info[process].io_remaining_time
        self.queue.put((self.time + io_time, process))

    def remaining_time(self, process: Process):
        info = self.scheduling_info[process]
        if info.cpu_remaining_time_1 > 0:
            return info.cpu_remaining_time_1
        else:
            return info.cpu_remaining_time_2

    def burst_finished(self, process: Process):
        first_burst_finished = (self.scheduling_info[process].cpu_remaining_time_1 == 0 and
                                self.scheduling_info[process].cpu_remaining_time_2 == process.cpu_burst_time_2)

        second_burst_finished = (self.scheduling_info[process].cpu_remaining_time_1 == 0 and
                                 self.scheduling_info[process].cpu_remaining_time_2 == 0)

        return first_burst_finished or second_burst_finished

    def print_intervals(self):
        for process, burst_start, burst_end in self.intervals:
            print(f"P{process.process_id}: ({burst_start}, {burst_end})")