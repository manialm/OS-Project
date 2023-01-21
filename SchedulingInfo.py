from dataclasses import dataclass

@dataclass
class SchedulingInfo:
    cpu_remaining_time_1: int
    io_remaining_time: int
    cpu_remaining_time_2: int