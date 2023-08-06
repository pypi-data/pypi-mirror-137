from abc import abstractmethod, ABC

from taskimporter import Task


class BaseTaskManager(ABC):
    name: str

    @staticmethod
    @abstractmethod
    def add_task(task: Task, project: str) -> None:
        pass
