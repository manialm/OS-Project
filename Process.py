from dataclasses import dataclass

# NOTE: unsafe_hash=True, so make sure to not mutate process in dict
@dataclass(unsafe_hash=True, order=True, eq=True)
class Process:
    process_id: int = 0
    arrival_time: int = 0
    cpu_burst_time_1: int = 0
    io_time: int = 0
    cpu_burst_time_2: int = 0
    finish_time: int = 0