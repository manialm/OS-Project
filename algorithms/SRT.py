from algorithms.Algorithm import Algorithm
from Process import Process
from SchedulingInfo import SchedulingInfo


class SRT(Algorithm):

    def choose_next(self, scheduling_info: dict[Process, SchedulingInfo]):
        next_process = min(
            scheduling_infos, key=lambda k: scheduling_infos[k].cpu_remaining_time_1)
        service_time = min(
            scheduling_infos[next_process].cpu_remaining_time_1,
            next_arrival_time)

        return next_process, service_time
