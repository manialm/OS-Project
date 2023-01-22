from queue import PriorityQueue
from Process import Process
from SchedulingInfo import SchedulingInfo

class RRScheduler:

    def __init__(self, time_quantum: int, processes: list[Process]):
        self.time_quantum = time_quantum
        self.processes = processes
        self.queue = PriorityQueue()

        self.ready_list: list[Process] = []
        self.scheduling_info = {}
        for process in processes:
            self.ready_list.append((process.arrival_time, process))

            self.scheduling_info[process] = SchedulingInfo(
                process.cpu_burst_time_1,
                process.io_time,
                process.cpu_burst_time_2)

        self.intervals: list[tuple[Process, int, int]] = []
        self.first_burst_end: dict[Process] = {}
        self.time = 1

    def schedule_cpu(self):
        # NOTE: how to advance time when queue is empty
        if self.queue.empty():
            self.time, _ = min(self.ready_list)

        for (arrival_time, process) in self.ready_list:
            if arrival_time <= self.time:
                self.queue.put((arrival_time, process))

        _, next_process = self.queue.get()
        print(next_process.process_id, self.ready_list)
        service_time = min(self.time_quantum, self.remaining_time(next_process))
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
            self.scheduling_info[next_process].cpu_remaining_time_2 -= service_time

        # If the process's CPU burst is done, remove it from the ready list
        if self.burst_finished(next_process):
            self.ready_list.remove((arrival_time, next_process))

    def schedule(self):
        while len(self.ready_list) > 0:
            self.schedule_cpu()

    def schedule_io(self, process: Process):
        io_time = self.scheduling_info[process].io_remaining_time
        self.ready_list.append((self.time + io_time, process))

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