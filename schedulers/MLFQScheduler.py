from queue import PriorityQueue

from process.Process import Process
from process.SchedulingInfo import SchedulingInfo
from schedulers.SchedulerBase import SchedulerBase


class MLFQScheduler(SchedulerBase):

    def __init__(self, processes: list[Process]):
        # NOTE: passing None as algorithm
        super().__init__(None, processes)

        self.queues = [PriorityQueue() for _ in range(3)]

        self.scheduling_info = {}
        for process in processes:
            self.queues[0].put((process.arrival_time, process))

            self.scheduling_info[process] = SchedulingInfo(
                process.cpu_burst_time_1,
                process.io_time,
                process.cpu_burst_time_2)

        self.counts = [3, 2, 1]
        self.time_quantums = [4, 16, float('inf')]
        self.turn = 0
        self.intervals: list[tuple[Process, int, int]] = []
        self.mlfq_intervals: list[tuple[int, Process, int, int]] = []
        self.first_burst_end: dict[Process] = {}
        self.time = 0

    def schedule_cpu(self):
        for _ in range(self.counts[self.turn]):
            if (self.queues[self.turn].empty()):
                break

            arrival_time, next_process = self.queues[self.turn].get()
            if arrival_time > self.time:
                self.time = arrival_time

            remaining_time = self.remaining_time(next_process)
            service_time = min(self.time_quantums[self.turn], remaining_time)

            self.intervals.append(
                (next_process, self.time, self.time + service_time)
            )
            self.mlfq_intervals.append(
                (self.turn, next_process, self.time, self.time + service_time)
            )
            self.time += service_time

            # If the process still needs the CPU, put it back in the (future) queue
            remaining_time -= service_time
            if remaining_time > 0:
                self.queues[(self.turn + 1) % 3].put((self.time, next_process))

            scheduling_info=self.scheduling_info[next_process]

            # First CPU burst
            if scheduling_info.cpu_remaining_time_1 > 0:
                scheduling_info.cpu_remaining_time_1 -= service_time

                # IO Burst
                if scheduling_info.cpu_remaining_time_1 == 0:
                    self.first_burst_end[next_process]=self.time
                    if scheduling_info.io_remaining_time > 0:
                        self.schedule_io(next_process)

            else:
                # Second CPU burst
                scheduling_info.cpu_remaining_time_2 -= service_time

        self.turn=(self.turn + 1) % 3

    def schedule(self):
        while not all(q.empty() for q in self.queues):
            self.schedule_cpu()

    def schedule_io(self, process: Process):
        io_time=self.scheduling_info[process].io_remaining_time
        self.queues[0].put((self.time + io_time, process))

    def print_intervals(self):
        for queue_number, process, burst_start, burst_end in self.mlfq_intervals:
            print(
                f"P{process.process_id}: [{queue_number}] ({burst_start}, {burst_end})")

    def get_algorithm_name(self):
        return 'MLFQ'