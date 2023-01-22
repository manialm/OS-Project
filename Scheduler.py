"""
self.scheduling_info = {
    Process1: SchedulingInfo(cpu_remaining_time_1, io_left_time, cpu_remaining_time_2),
    Process2: SchedulingInfo(cpu_remaining_time_1, io_left_time, cpu_remaining_time_2),
    ...
}
"""
from queue import SimpleQueue
from SchedulingInfo import SchedulingInfo
from Process import Process
from algorithms.Algorithm import Algorithm


class Scheduler:

    def __init__(self, algorithm: Algorithm, processes: list[Process]):
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

        self.first_burst_end = {}

    def schedule_cpu(self):
        first_process_arrival_time, _ = min(self.ready_list)
        if self.time < first_process_arrival_time:
            self.time = first_process_arrival_time

        arrival_time, next_process, service_time = self.algorithm.choose_next(
            self.scheduling_info, self.ready_list, self.time
        )

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
                self.first_burst_end[next_process] = self.time
                if scheduling_info.io_remaining_time > 0:
                    self.schedule_io(next_process)

        else:
            # Second CPU burst
            scheduling_info.cpu_remaining_time_2 -= service_time

        # If the process's CPU burst is done, remove it from the ready list
        if self.burst_finished(next_process):
            self.ready_list.remove((arrival_time, next_process))

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

    def burst_finished(self, process: Process):
        first_burst_finished = (self.scheduling_info[process].cpu_remaining_time_1 == 0 and
                                self.scheduling_info[process].cpu_remaining_time_2 == process.cpu_burst_time_2)

        second_burst_finished = (self.scheduling_info[process].cpu_remaining_time_1 == 0 and
                                 self.scheduling_info[process].cpu_remaining_time_2 == 0)

        return first_burst_finished or second_burst_finished

    # For debug purposes
    def print_list(self):
        print([(arrival_time, process.process_id)
              for arrival_time, process in self.ready_list])

    def get_service_time(self, process: Process):
        return process.cpu_burst_time_1 + process.cpu_burst_time_2

    def get_start_time(self, process: Process):
        return process.arrival_time

    def get_end_time(self, process: Process):
        _, _, end_time = max(
            (process_, burst_start, burst_end)
            for (process_, burst_start, burst_end) in self.intervals
            if process_ == process
        )

        return end_time

    def get_waiting_time(self, process: Process):
        return self.get_end_time(process) - self.get_start_time(process)

    def get_turnaround_time(self, process: Process):
        return self.get_waiting_time(process) - self.get_service_time(process)

    def get_response_time(self, process: Process):
        return self.first_burst_end[process] - process.arrival_time

    def average_waiting_time(self):
        return sum(
            self.get_waiting_time(process)
            for process in self.processes
        ) / len(self.processes)

    def average_turnaround_time(self):
        return sum(
            self.get_turnaround_time(process)
            for process in self.processes
        ) / len(self.processes)

    def average_response_time(self):
        return sum(
            self.get_response_time(process)
            for process in self.processes
        ) / len(self.processes)

    def total_time(self):
        # When the last burst ends
        return self.intervals[-1][-1]

    def total_cpu_time(self):
        return sum(
            self.get_service_time(process)
            for process in self.processes
        )

    def cpu_utilization(self):
        return self.total_cpu_time() / self.total_time()

    def thoroughput(self):
        return len(self.processes) / self.total_time()

    def idle_time(self):
        return self.total_time() - self.cpu_time()

    def print_analysis(self):
        print()
        for process in self.processes:
            print(f'P{process.process_id}:')
            print(
                f'Start and End time: ({self.get_start_time(process)}, {self.get_end_time(process)})')
            print(f'Turnaround Time: {self.get_turnaround_time(process)}')
            print(f'Response Time: {self.get_response_time(process)}')
            print(f'Waiting Time: {self.get_waiting_time(process)}')

            print()
        print()

        print(f'Total time: {self.total_time()}')
        print(f'Average turnaround time: {self.average_turnaround_time()}')
        print(f'Average response time: {self.average_response_time()}')
        print(f'Average waiting time: {self.average_waiting_time()}')
        print(f'CPU Utilization: {100*self.cpu_utilization():.2f}%')
        print(f'Thoroughput: {self.thoroughput():.2f}')
        

