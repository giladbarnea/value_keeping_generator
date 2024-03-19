import typing
from collections.abc import Generator
import inspect

T = typing.TypeVar('T')


class value_keeping_generator(typing.Generic[T]):
    """Keeps the last value yielded."""

    EMPTY = object()
    def __init__(self, generator: Generator[T, None, None]):
        self.value = value_keeping_generator.EMPTY
        self._generator = generator

    def __call__(self, generator: Generator[T, None, None]):
        self._generator = generator
        return self

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
