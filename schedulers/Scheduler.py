"""
self.scheduling_info = {
    Process1: SchedulingInfo(cpu_remaining_time_1, io_left_time, cpu_remaining_time_2),
    Process2: SchedulingInfo(cpu_remaining_time_1, io_left_time, cpu_remaining_time_2),
    ...
}
"""
from queue import SimpleQueue

from algorithms.Algorithm import Algorithm
from process.Process import Process
from schedulers.SchedulerBase import SchedulerBase
from process.SchedulingInfo import SchedulingInfo


class Scheduler(SchedulerBase):

    def __init__(self, algorithm: Algorithm, processes: list[Process]):
        super().__init__(algorithm, processes)

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