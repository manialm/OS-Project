import csv

from process.Process import Process

class CSVReader:

    def __init__(self, csv_file: str):
        self.csv_file = csv_file

    def get_processes(self):
        processes = []

        with open(self.csv_file, 'r') as f:
            reader = csv.reader(f)
            first, *rest = reader
            for row in rest:
                process = self.create_process(first, row)
                processes.append(process)

        return processes

    def create_process(self, props, values):
        process = Process()
        for i, prop in enumerate(props):
            self.set_value(process, prop, values[i])

        return process

    def set_value(self, process: Process, prop: str, value: str):
        value = int(value)

        if prop == 'process_id':
            process.process_id = value
        elif prop == 'arrival_time':
            process.arrival_time = value
        elif prop == 'cpu_time1':
            process.cpu_burst_time_1 = value
        elif prop == 'io_time':
            process.io_time = value
        elif prop == 'cpu_time2':
            process.cpu_burst_time_2 = value

        return process


if __name__ == '__main__':
    csv_file = 'csv/input_file.csv'
    for process in CSVReader(csv_file).get_processes():
        print(process)
    