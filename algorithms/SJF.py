from algorithms.Algorithm import Algorithm
from Process import Process
from SchedulingInfo import SchedulingInfo
from queue import PriorityQueue
from heapq import heapify

class SJF(Algorithm):

    def choose_next(self, scheduling_info: dict[Process, SchedulingInfo],
    ready_queue: PriorityQueue[Process]) -> tuple[Process, int]:

        # NOTE: apparently popping from PriorityQueue().queue is safe?
        # NOTE: needs refactor to become simpler
        self.ready_queue = ready_queue

        queue = ready_queue.queue
        next_process_idx = min(range(len(queue)),
            key=lambda idx: self.remaining_time(scheduling_info[queue[idx][1]])
        )

        next_process = queue[next_process_idx][1]
        queue.pop(next_process_idx)
        self.stabilize_queue()

        service_time = self.remaining_time(scheduling_info[next_process])
        return next_process, service_time

    def remaining_time(self, info: SchedulingInfo):
        if info.cpu_remaining_time_1 > 0:
            return info.cpu_remaining_time_1
        else:
            return info.cpu_remaining_time_2

    def stabilize_queue(self):
        """Restore the Priority Queue invariant"""
        # NOTE: this method will probably raise eyebrows

        heapify(self.ready_queue.queue)
