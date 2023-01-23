from queue import SimpleQueue

from algorithms.Algorithm import Algorithm
from process.Process import Process
from process.SchedulingInfo import SchedulingInfo


class SchedulerBase:
    def __init__(self, algorithm: Algorithm, processes: list[Process]):
        self.time = 0
        self.algorithm = algorithm

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

    def schedule_cpu(self):
        first_process_arrival_time, _ = min(self.ready_list)
        if self.time < first_process_arrival_time:
            self.time = first_process_arrival_time

        arrival_time, next_process, service_time = self.algorithm.choose_next(
            self.scheduling_info, self.ready_list, self.time
        )

        self.intervals.append(
            (next_process, self.time, self.time + service_time)
        )

        self.time += service_time

        scheduling_info = self.scheduling_info[next_process]

        # First CPU burst
        if scheduling_info.cpu_remaining_time_1 > 0:
            scheduling_info.cpu_remaining_time_1 -= service_time

            # IO Burst
            if scheduling_info.cpu_remaining_time_1 == 0:
                self.first_burst_end[next_process] = self.time
                if scheduling_info.io_remaining_time > 0:
                    self.schedule_io(next_process)

        else:
            # Second CPU burst
            scheduling_info.cpu_remaining_time_2 -= service_time

        # If the process's CPU burst is done, remove it from the ready list
        if self.burst_finished(next_process):
            self.ready_list.remove((arrival_time, next_process))

    def schedule(self):
        while len(self.ready_list) > 0:
            self.schedule_cpu()

    def schedule_io(self, process):
        io_time = self.scheduling_info[process].io_remaining_time
        self.ready_list.append((self.time + io_time, process))

    def burst_finished(self, process: Process):
        first_burst_finished = (self.scheduling_info[process].cpu_remaining_time_1 == 0 and
                                self.scheduling_info[process].cpu_remaining_time_2 == process.cpu_burst_time_2)

        second_burst_finished = (self.scheduling_info[process].cpu_remaining_time_1 == 0 and
                                 self.scheduling_info[process].cpu_remaining_time_2 == 0)

        return first_burst_finished or second_burst_finished

    def remaining_time(self, process: Process):
        info = self.scheduling_info[process]
        if info.cpu_remaining_time_1 > 0:
            return info.cpu_remaining_time_1
        else:
            return info.cpu_remaining_time_2

    def print_intervals(self):
        for process, burst_start, burst_end in self.intervals:
            print(f"P{process.process_id}: ({burst_start}, {burst_end})")

    def get_service_time(self, process: Process):
        return process.cpu_burst_time_1 + process.cpu_burst_time_2

    def get_start_time(self, process: Process):
        return process.arrival_time

    def get_end_time(self, process: Process):
        _, _, end_time = max(
            (process_, burst_start, burst_end)
            for (process_, burst_start, burst_end) in self.intervals
            if process_ == process
        )

        return end_time

    def get_waiting_time(self, process: Process):
        return self.get_end_time(process) - self.get_start_time(process)

    def get_turnaround_time(self, process: Process):
        return self.get_waiting_time(process) - self.get_service_time(process)

    def get_response_time(self, process: Process):
        return self.first_burst_end[process] - process.arrival_time

    def average_waiting_time(self):
        return sum(
            self.get_waiting_time(process)
            for process in self.processes
        ) / len(self.processes)

    def average_turnaround_time(self):
        return sum(
            self.get_turnaround_time(process)
            for process in self.processes
        ) / len(self.processes)

    def average_response_time(self):
        return sum(
            self.get_response_time(process)
            for process in self.processes
        ) / len(self.processes)

    def total_time(self):
        # When the last burst ends
        return self.intervals[-1][-1]

    def total_cpu_time(self):
        return sum(
            self.get_service_time(process)
            for process in self.processes
        )

    def cpu_utilization(self):
        return self.total_cpu_time() / self.total_time()

    def thoroughput(self):
        return len(self.processes) / self.total_time()

    def idle_time(self):
        return self.total_time() - self.cpu_time()

    def print_analysis(self):
        print()
        for process in self.processes:
            print(f'P{process.process_id}:')
            print(
                f'Start and End time: ({self.get_start_time(process)}, {self.get_end_time(process)})')
            print(f'Turnaround Time: {self.get_turnaround_time(process)}')
            print(f'Response Time: {self.get_response_time(process)}')
            print(f'Waiting Time: {self.get_waiting_time(process)}')

            print()
        print()

        print(f'Total time: {self.total_time()}')
        print(f'Average turnaround time: {self.average_turnaround_time()}')
        print(f'Average response time: {self.average_response_time()}')
        print(f'Average waiting time: {self.average_waiting_time()}')
        print(f'CPU Utilization: {100*self.cpu_utilization():.2f}%')
        print(f'Thoroughput: {self.thoroughput():.2f}')

    def save_chart(self):
        import matplotlib.pyplot as plt

        print(f"Gantt chart for {self.get_algorithm_name()} saved!")
        # Declaring a figure "gnt"
        fig, gnt = plt.subplots()

        # Setting Y-axis limits
        gnt.set_ylim(0, 80)

        # Setting X-axis limits
        gnt.set_xlim(0, 60, 1)

        # Setting labels for x-axis and y-axis
        gnt.set_xlabel('Time')
        gnt.set_ylabel('Processes')

        # Setting ticks on y-axis
        gnt.set_yticks([10, 25, 40, 55, 70])
        # Labelling tickes of y-axis
        gnt.set_yticklabels(['P1', 'P2', 'P3', 'P4', 'P5'])

        # Setting graph attribute
        gnt.grid(True)
        
        # Get each process cpu burst tuples
        myData1 = []
        myData2 = []
        myData3 = []
        myData4 = []
        myData5 = []
        for process, burst_start, burst_end in self.intervals:
            if process.process_id == 1:
                myData1.append((burst_start, burst_end - burst_start))
            elif process.process_id == 2:
                myData2.append((burst_start, burst_end - burst_start))
            elif process.process_id == 3:
                myData3.append((burst_start, burst_end - burst_start))
            elif process.process_id == 4:
                myData4.append((burst_start, burst_end - burst_start))
            elif process.process_id == 5:
                myData5.append((burst_start, burst_end - burst_start))
                
        # Process 1
        gnt.broken_barh(myData1, (10, 9), facecolors ='tab:blue')
        
        # Process 2
        gnt.broken_barh(myData2, (25, 9), facecolors =('tab:red'))
        
        # Process 3
        gnt.broken_barh(myData3, (40, 9), facecolors =('tab:orange'))
        
        # Process 4
        gnt.broken_barh(myData4, (55, 9),facecolors =('tab:green'))
                
        # Process 5
        gnt.broken_barh(myData5, (70, 9),facecolors =('tab:pink'))        

        plt.savefig(f"gantt/gantt_{self.get_algorithm_name()}.png")
