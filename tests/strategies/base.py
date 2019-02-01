from typing import (Iterable,
                    Optional,
                    Set)

from hypothesis import strategies
from hypothesis.searchstrategy import SearchStrategy

from tests.utils import Domain
from topo.base import (EMPTY_SET,
                       Union)
from .literals.factories import to_homogeneous_tuples


def to_unions(elements: SearchStrategy[Set[Domain]],
              *,
              min_size: int = 0,
              max_size: Optional[int] = None) -> SearchStrategy[Union[Domain]]:
    def union_from_sets(sets: Iterable[Set]) -> Union:
        return Union(*sets)

    return (to_homogeneous_tuples(elements,
                                  min_size=min_size,
                                  max_size=max_size)
            .map(union_from_sets))


empty_sets = strategies.just(EMPTY_SET)
