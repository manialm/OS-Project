import abc

class Algorithm(abc.ABC):
    @abc.abstractmethod
    def choose_next(self, scheduling_infos, ready_queue):
        raise NotImplementedError