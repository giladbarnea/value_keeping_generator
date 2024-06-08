import sys

from value_keeping_generator import value_keeping_generator


def generator():
    yield 1
    yield 2
    yield 3


class TestFunctional:
    def test_sanity_can_iterate_over_values(self):
        gen = value_keeping_generator(generator())
        assert list(gen)  #  == [1, 2, 3]
        gen = value_keeping_generator(generator())
        expected = 1
        for i in gen:
            assert i == expected
            expected += 1

    def test_sanity_yield_from(self):
        def yields_from():
            yield from generator()

        g = value_keeping_generator(yields_from())
        assert list(g)  #  == [1, 2, 3]
        g = value_keeping_generator(yields_from())
        expected = 1
        for i in g:
            assert i == expected
            expected += 1

    def test_value_kept_after_exhausting(self):
        gen = value_keeping_generator(generator())
        list(gen)
        assert gen.value == 3

    def test_value_EMPTY_before_iterating(self):
        gen = value_keeping_generator(generator())
        assert gen.value is value_keeping_generator.EMPTY

    def test_value_EMPTY_after_exhausting_empty_generator(self):
        gen = value_keeping_generator(iter([]))
        list(gen)
        assert gen.value is value_keeping_generator.EMPTY

        def empty():
            for i in range(0):
                yield i
        gen = value_keeping_generator(empty())
        list(gen)
        assert gen.value is value_keeping_generator.EMPTY

    def test_value_returns_with_yield_from(self):
        def yields_from():
            value = yield from value_keeping_generator(generator())
            assert value == 3

        iter(yields_from())

    def test_respects_passed_generator_custom_return_value(self):
        def generator():
            yield 1
            yield 2
            return 42

        gen = value_keeping_generator(generator())
        assert list(gen)  #  == [1, 2]
        assert gen.value == 42

    def test_respects_passed_generator_custom_return_value_yield_from(self):
        def generator():
            yield 1
            yield 2
            return 42

        def yields_from():
            value = yield from value_keeping_generator(generator())
            assert value == 42

        iter(yields_from())

class TestDecorator:
    def test_sanity_can_iterate_over_values(self):
        # @value_keeping_generator
        def gen():
            yield 1
            yield 2
            yield 3

        # g1 = value_keeping_generator(iter([]))
        # g1 = value_keeping_generator(gen())
        g2 = value_keeping_generator(gen)
        assert list(g1)  #  == [1, 2, 3]

"""
gen()
print(inspect.isgenerator(generator))  #  True
print(inspect.isfunction(generator))  #   False
print(inspect.isgeneratorfunction(generator))  #  False
print(inspect.isroutine(generator))  #    False

gen
print(inspect.isgenerator(generator))  #  False
print(inspect.isfunction(generator))  #   True
print(inspect.isgeneratorfunction(generator))  #  True
print(inspect.isroutine(generator))  #    True

iter([])
print(inspect.isgenerator(generator))  #  False
print(inspect.isfunction(generator))  #   True
print(inspect.isgeneratorfunction(generator))  #  True
print(inspect.isroutine(generator))  #    True
"""
