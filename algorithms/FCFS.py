from algorithms.Algorithm import Algorithm
from process.Process import Process
from process.SchedulingInfo import SchedulingInfo
from queue import PriorityQueue

class FCFS(Algorithm):

    def choose_next(self, scheduling_info: dict[Process, SchedulingInfo],
    ready_list: list[tuple[int, Process]], time: int) -> tuple[Process, int]:

        ready_list = [(arrival_time, process) for arrival_time, process in ready_list
                     if arrival_time <= time]
        # ready_list elements are tuples of (arrival_time, process)
        # so the minimum element has the earliest arrival time
        arrival_time, next_process = min(ready_list)

        service_time = scheduling_info[next_process].cpu_remaining_time_1
        if service_time == 0:
            service_time = scheduling_info[next_process].cpu_remaining_time_2

        return arrival_time, next_process, service_time


    # @staticmethod
    # def pop_min(arr: list):
    #     """Return the minimum element of arr and remove it from arr"""
    #     val, idx = min((val, idx) for idx, val in enumerate(arr))
    #     arr.pop(idx)
    #     return val