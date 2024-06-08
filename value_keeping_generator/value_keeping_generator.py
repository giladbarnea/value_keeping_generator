import typing
from collections.abc import Generator
import inspect
import inspect
from icecream import ic


def generator():
    yield 1
    yield 2
    yield 3


ic(inspect.isgenerator(generator))  # False
ic(inspect.isfunction(generator))  # True
ic(inspect.isgeneratorfunction(generator))  # True
ic(inspect.isroutine(generator))  # True

ic(inspect.isgenerator(generator()))  # True
ic(inspect.isfunction(generator()))  # False
ic(inspect.isgeneratorfunction(generator()))  # False
ic(inspect.isroutine(generator()))  # False

ic(inspect.isgenerator((x for x in range(5))))  # True
ic(inspect.isfunction((x for x in range(5))))  # False
ic(inspect.isgeneratorfunction((x for x in range(5))))  # False
ic(inspect.isroutine((x for x in range(5))))  # False


# import sys
#
# sys.exit(0)
T = typing.TypeVar("T")


class value_keeping_generator(typing.Generic[T]):
    """Keeps the last value yielded."""

    EMPTY = object()

    def __init__(self, generator: Generator[T, None, None]):
        self.value = value_keeping_generator.EMPTY
        self._generator = generator

    def __iter__(self):
        if inspect.isgenerator(self._generator):
            return self._exhaust_generator(self._generator)
        else:
            return self._exhaust_iterator(self._generator)

    def _exhaust_generator(self, gen):
        value = self._generator.send(None)
        self.value = value
        yield value
        while True:
            try:
                self.value = self._generator.send(None)
                yield self.value
            except StopIteration as e:
                if e.value is not None:
                    self.value = e.value
                return self.value

    def _exhaust_iterator(self, gen):
        for value in self._generator:
            self.value = value
            yield value
