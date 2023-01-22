from algorithms.Algorithm import Algorithm
from Process import Process
from SchedulingInfo import SchedulingInfo
from queue import PriorityQueue

class FCFS(Algorithm):

    def choose_next(self, scheduling_info: dict[Process, SchedulingInfo],
    ready_queue: PriorityQueue[Process]) -> tuple[Process, int]:

        _, next_process = ready_queue.get()

        service_time = scheduling_info[next_process].cpu_remaining_time_1
        if service_time == 0:
            service_time = scheduling_info[next_process].cpu_remaining_time_2

        return next_process, service_time
