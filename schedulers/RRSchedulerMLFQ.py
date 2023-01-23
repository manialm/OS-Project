from process.Process import Process

class RRSchedulerMLFQ(RRScheduler):
    
    def __init__(self, time_quantum: int, processes: list[Process]):
        super().__init__(time_quantum, processes)

    def add_to_queue(self, arrival_time: int, process: list[Process]):
        self.queue.put((arrival_time, process))