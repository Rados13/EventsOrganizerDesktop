import abc


class ConflictChecker(metaclass=abc.ABC):

    @abc.abstractmethod
    def solve(self):
        pass

    @abc.abstractmethod
    def get_conflicts(self):
        pass
