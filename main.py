from Scheduler import Scheduler
from algorithms.FCFS import FCFS
from Process import Process

def main():
    processes = [
        Process(1, 3, 6, 0, 0, 0),
        Process(2, 1, 7, 0, 0, 0),
        Process(3, 1, 8, 0, 0, 0),
        Process(4, 2, 3, 0, 0, 0)
    ]
    scheduler = Scheduler(FCFS(), processes)
    scheduler.schedule()

if __name__ == "__main__":
    main()