# NOTE: `algorithm` has a `select()` method

"""
self.scheduling_infos = {
    Process1: SchedulingInfo(cpu_remaining_time_1, io_left_time, cpu_remaining_time_2),
    Process2: SchedulingInfo(cpu_remaining_time_1, io_left_time, cpu_remaining_time_2),
    ...
}
"""


class Scheduler:

    def __init__(self, algorithm, processes):
        self.algorithm = algorithm
        self.process = processes

        self.scheduling_infos = {}
        for process in processes:
            self.scheduling_infos[process] = SchedulingInfo(
                process.arrival_time,
                process.cpu_burst_time_1, process.io_time, process.cpu_burst_time_2)

    def schedule(self, process):
        next_process, service_time = self.algorithm.choose_next(
            self.scheduling_infos)

        remaining_time = self.scheduling_infos[next_process].cpu_remaining_time_1
        if remaining_time > 0:
            self.scheduling_infos[next_process].cpu_remaining_time_1 -= service_time
        else:
            self.scheduling_infos[next_process].cpu_remaining_time_2 -= service_time
