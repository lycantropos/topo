from hypothesis import strategies

from .factories import (to_byte_strings,
                        to_characters,
                        to_homogeneous_frozensets,
                        to_homogeneous_tuples,
                        to_strings)

booleans = strategies.booleans()
integers = (booleans
            | strategies.integers())
real_numbers = (integers
                | strategies.floats(allow_nan=False,
                                    allow_infinity=True)
                | strategies.decimals(allow_nan=False,
                                      allow_infinity=True))
numbers = (real_numbers
           | strategies.complex_numbers(allow_nan=False,
                                        allow_infinity=True))
scalars = (strategies.none()
           | numbers
           | strategies.just(NotImplemented)
           | strategies.just(Ellipsis))
byte_strings = to_byte_strings()
strings = to_strings(to_characters())
deferred_hashables = strategies.deferred(lambda: hashables)
hashables = (scalars
             | byte_strings
             | strings
             | to_homogeneous_frozensets(deferred_hashables)
             | to_homogeneous_tuples(deferred_hashables))
