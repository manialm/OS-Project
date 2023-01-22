from algorithms.Algorithm import Algorithm
from Process import Process
from SchedulingInfo import SchedulingInfo


class SRT(Algorithm):

    def choose_next(self, scheduling_info: dict[Process, SchedulingInfo],
    ready_list: list[tuple[int, Process]]) -> tuple[Process, int]:

        # Similar to SJF        
        arrival_time, next_process = min(
            ready_list,
            key=lambda k: self.remaining_time(scheduling_info[process := k[1]])
        )

        # Difference to SJF
        remaining_time = self.remaining_time(scheduling_info[next_process])
        next_arrival_time = min(arrival_time for arrival_time, _ in ready_list)
        service_time = min(remaining_time, next_arrival_time)

        return arrival_time, next_process, service_time

    def remaining_time(self, info: SchedulingInfo):
        if info.cpu_remaining_time_1 > 0:
            return info.cpu_remaining_time_1
        else:
            return info.cpu_remaining_time_2