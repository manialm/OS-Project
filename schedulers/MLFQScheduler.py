from schedulers.SchedulerBase import SchedulerBase  

class MLFQScheduler(BaseScheduler):

    def __init__(self, processes: list[Process]):
        self.processes = processes
        self.ready_list: list[tuple[int, Process]] = []
        self.scheduling_info = {}
        for process in processes:
            self.ready_list.append((process.arrival_time, process))

            self.scheduling_info[process] = SchedulingInfo(
                process.cpu_burst_time_1,
                process.io_time,
                process.cpu_burst_time_2)

        # 3-Tuples of (process, burst start, burst end)
        self.intervals: list[tuple[Process, int, int]] = []

        self.first_burst_end = {}