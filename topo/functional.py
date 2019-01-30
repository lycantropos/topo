from itertools import chain
from typing import Iterable

from .hints import (Domain,
                    Map,
                    Range)

flatten = chain.from_iterable


def flatmap(function: Map[Domain, Iterable[Range]],
            *iterables: Iterable[Domain]) -> Iterable[Range]:
    yield from flatten(map(function, *iterables))
