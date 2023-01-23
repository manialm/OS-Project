from algorithms.Algorithm import Algorithm
from process.Process import Process
from process.SchedulingInfo import SchedulingInfo
import heapq

class SRT(Algorithm):

    def __init__(self):
        self.name = 'SRT'

    def choose_next(self, scheduling_info: dict[Process, SchedulingInfo],
    ready_list: list[tuple[int, Process]], time: int) -> tuple[Process, int]:

        ready_list_orig = ready_list.copy()
        ready_list = [(arrival_time, process) for arrival_time, process in ready_list
                     if arrival_time <= time]

        # Similar to SJF        
        arrival_time, next_process = min(
            ready_list,
            key=lambda k: self.remaining_time(scheduling_info[process := k[1]])
        )

        # Difference to SJF
        remaining_time = self.remaining_time(scheduling_info[next_process])
        next_arrival_time = heapq.nsmallest(2, set(arrival_time for arrival_time, _ in ready_list_orig))[-1]
        
        if next_arrival_time <= time:
            service_time = remaining_time
        else:
            service_time = min(remaining_time, next_arrival_time - time)

        return arrival_time, next_process, service_time

    def remaining_time(self, info: SchedulingInfo):
        if info.cpu_remaining_time_1 > 0:
            return info.cpu_remaining_time_1
        else:
            return info.cpu_remaining_time_2