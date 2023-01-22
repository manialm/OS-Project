import abc
from queue import PriorityQueue

from Process import Process
from SchedulingInfo import SchedulingInfo
class Algorithm(abc.ABC):
    @abc.abstractmethod
    def choose_next(self, scheduling_info: dict[Process, SchedulingInfo],
    ready_list: list[tuple[int, Process]], time: int) -> tuple[Process, int]:
        raise NotImplementedError