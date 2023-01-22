from algorithms.Algorithm import Algorithm
from Process import Process
from SchedulingInfo import SchedulingInfo
from queue import PriorityQueue
from heapq import heapify


class SJF(Algorithm):

    def choose_next(self, scheduling_info: dict[Process, SchedulingInfo],
    ready_list: list[tuple[int, Process]], time: int) -> tuple[Process, int]:

        ready_list = [(arrival_time, process) for arrival_time, process in ready_list
                     if arrival_time <= time]

        # ready_list elements are tuples of (arrival_time, process)
        # so the minimum element has the earliest arrival time
        arrival_time, next_process = min(
            ready_list,
            key=lambda k: self.remaining_time(scheduling_info[process := k[1]])
        )

        service_time = self.remaining_time(scheduling_info[next_process])
        return arrival_time, next_process, service_time

    def remaining_time(self, info: SchedulingInfo):
        if info.cpu_remaining_time_1 > 0:
            return info.cpu_remaining_time_1
        else:
            return info.cpu_remaining_time_2