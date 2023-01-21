# NOTE: `algorithm` has a `select()` method

"""
self.scheduling_infos = {
    Process1: SchedulingInfo(cpu_remaining_time_1, io_left_time, cpu_remaining_time_2),
    Process2: SchedulingInfo(cpu_remaining_time_1, io_left_time, cpu_remaining_time_2),
    ...
}
"""
from queue import SimpleQueue
from SchedulingInfo import SchedulingInfo

class Scheduler:

    def __init__(self, algorithm, processes):
        self.algorithm = algorithm
        self.process = processes

        self.ready_queue = SimpleQueue()
        self.scheduling_infos = {}
        for process in processes:
            self.ready_queue.put((process.arrival_time, process))
            
            self.scheduling_infos[process] = SchedulingInfo(
                process.arrival_time,
                process.cpu_burst_time_1,
                process.io_time,
                process.cpu_burst_time_2)

    def schedule_next(self):
        next_process, service_time = self.algorithm.choose_next(
            self.scheduling_infos, self.ready_queue)

        print(next_process, service_time)

        remaining_time = self.scheduling_infos[next_process].cpu_remaining_time_1
        if remaining_time > 0:
            self.scheduling_infos[next_process].cpu_remaining_time_1 -= service_time
        else:
            self.scheduling_infos[next_process].cpu_remaining_time_2 -= service_time

    def schedule(self):
        while self.ready_queue.qsize() > 0:
            self.schedule_next()
