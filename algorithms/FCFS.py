from typing import Dict
from Process import Process
from SchedulingInfo import SchedulingInfo
from queue import PriorityQueue

class FCFS:

    def choose_next(self, scheduling_infos: Dict[Process, SchedulingInfo],
    ready_queue: PriorityQueue):
        next_process = ready_queue.get()
        service_time = scheduling_infos[next_process].cpu_remaining_time_1

        return next_process, service_time
