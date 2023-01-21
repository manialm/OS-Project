# NOTE: `algorithm` has a `select()` method
# NOTE: assuming first job has arrival time of 0
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
        self.ready_queue: PriorityQueue[Process] = PriorityQueue()
        self.scheduling_info = {}
        for process in processes:
            self.ready_queue.put((process.arrival_time, process))

            self.scheduling_info[process] = SchedulingInfo(
                process.cpu_burst_time_1,
                process.io_time,
                process.cpu_burst_time_2)

    def schedule_cpu(self):
        first_process_arrival_time, _ = self.ready_queue.queue[0]
        if self.time < first_process_arrival_time:
            self.time = first_process_arrival_time
        
        next_process, service_time = self.algorithm.choose_next(
            self.scheduling_info, self.ready_queue)

        print(f"P{next_process.process_id}: ({self.time}, {self.time + service_time})")

        self.advance_time(service_time)

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
        while self.ready_queue.qsize() > 0:
            self.schedule_cpu()

    def schedule_io(self, process):
        io_time = self.scheduling_info[process].io_remaining_time
        self.ready_queue.put((self.time + io_time, process))

    def advance_time(self, service_time: int):
        self.time += service_time

    def update_ready_queue(self):
        for process in self.processes:
                if self.last_time < process.arrival_time <= self.time:
                    self.ready_queue.put((process.arrival_time, process))
            