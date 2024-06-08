# value_keeping_generator

`value_keeping_generator` plainly wraps Python generators, allowing you to keep track of the last value yielded. 
This need has been coming up a lot when working with LLM streams.
The alternatives are either `return`ing after everything has been yielded, and abusing the `last_value = yield from my_generator` syntax; or iterating through a shifted copy of the generator at the same time as the original generator, which is bad for latency and memory consumption.

## Usage

```python
from value_keeping_generator import value_keeping_generator

@value_keeping_generator
def my_generator():
    yield 1
    yield 2
    yield 3

gen = my_generator()

for value in gen:
    print(value)  # Outputs: 1, 2, 3

print(gen.value)  # Outputs: 3, the last value yielded
```
