from schedulers.Scheduler import Scheduler
from algorithms.FCFS import FCFS
from algorithms.SJF import SJF
from algorithms.SRT import SRT
from schedulers.RRScheduler import RRScheduler
from process.Process import Process
from CSVReader import CSVReader

CSV_FILE = 'csv/input_file.csv'

def test_fcfs(processes: list[Process]):
    print('\nFCFS:')
    scheduler = Scheduler(FCFS(), processes)
    scheduler.schedule()
    scheduler.print_intervals()
    scheduler.print_analysis()

def test_sjf(processes: list[Process]):
    print('\nSJF:')
    scheduler = Scheduler(SJF(), processes)
    scheduler.schedule()
    scheduler.print_intervals()
    scheduler.print_analysis()

def test_srt(processes: list[Process]):
    print('\nSRT:')
    scheduler = Scheduler(SRT(), processes)
    scheduler.schedule()
    scheduler.merge_intervals()
    scheduler.print_intervals()
    scheduler.print_analysis()

def test_rr(processes: list[Process]):
    print('\nRR:')
    time_quantum = 3
    scheduler = RRScheduler(time_quantum, processes)
    scheduler.schedule()
    scheduler.print_intervals()
    scheduler.print_analysis()

def main():
    # processes = [
    #     Process(1, 3, 6, 0, 0, 0),
    #     Process(2, 1, 7, 0, 0, 0),
    #     Process(3, 1, 8, 0, 0, 0),
    #     Process(4, 2, 3, 0, 0, 0)
    # ]

    processes = CSVReader(CSV_FILE).get_processes()
    test_fcfs(processes)
    test_sjf(processes)
    test_srt(processes)
    test_rr(processes)

if __name__ == "__main__":
    main()