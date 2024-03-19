from value_keeping_generator import value_keeping_generator


def generator():
    yield 1
    yield 2
    yield 3


def test_sanity_can_iterate_over_values():
    gen = value_keeping_generator(generator())
    assert list(gen) == [1, 2, 3]
    gen = value_keeping_generator(generator())
    expected = 1
    for i in gen:
        assert i == expected
        expected += 1


def test_sanity_yield_from():
    def yields_from():
        yield from generator()

    g = value_keeping_generator(yields_from())
    assert list(g) == [1, 2, 3]
    g = value_keeping_generator(yields_from())
    expected = 1
    for i in g:
        assert i == expected
        expected += 1


def test_last_value_kept_after_exhausting():
    gen = value_keeping_generator(generator())
    list(gen)
    assert gen.value == 3


def test_last_value_EMPTY_before_iterating():
    gen = value_keeping_generator(generator())
    assert gen.value is value_keeping_generator.EMPTY


def test_value_EMPTY_after_exhausting_empty_generator():
    gen = value_keeping_generator(iter([]))
    list(gen)
    assert gen.value is value_keeping_generator.EMPTY


def test_last_value_returns_with_yield_from():
    def yields_from():
        last_value = yield from value_keeping_generator(generator())
        assert last_value == 3

    iter(yields_from())


def test_respects_passed_generator_custom_return_value():
    def generator():
        yield 1
        yield 2
        return 42

    gen = value_keeping_generator(generator())
    assert list(gen) == [1, 2]
    assert gen.value == 42
