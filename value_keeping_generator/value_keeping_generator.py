import typing
from collections.abc import Generator

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
        for chunk in self._generator:
            self.value = chunk
            yield chunk
        return self.value
