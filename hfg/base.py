from threading import Thread
from abc import ABC, abstractmethod
from functools import wraps


def threaded(func):
    @wraps(func)
    def wrapper(*args, **kwargs) -> Thread:
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()

        return thread

    return wrapper


class ThreadStorage(dict, ABC):
    def store(self, name: str, thread: Thread):
        self[name] = thread

    def running(self):
        for value in self.values():
            if value is not None:
                if value.is_alive():
                    return value.is_alive()

        return False
