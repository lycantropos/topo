from typing import (Iterable,
                    Optional)

from hypothesis import strategies
from hypothesis.searchstrategy import SearchStrategy

from tests.utils import Domain
from topo.base import (EMPTY_SET,
                       Set,
                       Union)
from .literals.factories import to_homogeneous_tuples


def to_unions(elements: SearchStrategy[Set[Domain]],
              *,
              min_size: int = 0,
              max_size: Optional[int] = None) -> SearchStrategy[Set[Domain]]:
    def union_from_sets(sets: Iterable[Set]) -> Set:
        union = Union(*sets)
        if isinstance(union, Union) and len(union.subsets) == 1:
            return list(union.subsets)[0]
        return union

    return (to_homogeneous_tuples(elements,
                                  min_size=min_size,
                                  max_size=max_size)
            .map(union_from_sets))


empty_sets = strategies.just(EMPTY_SET)
