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