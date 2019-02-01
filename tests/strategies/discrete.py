from typing import (Iterable,
                    Optional)

from hypothesis.searchstrategy import SearchStrategy

from tests.utils import Domain
from topo.discrete import DiscreteSet
from .literals.factories import to_homogeneous_tuples


def to_discrete_sets(elements: SearchStrategy[Domain],
                     *,
                     min_size: int = 0,
                     max_size: Optional[int] = None
                     ) -> SearchStrategy[DiscreteSet[Domain]]:
    def discrete_set_from_points(points: Iterable[Domain]) -> DiscreteSet:
        return DiscreteSet(*points)

    return (to_homogeneous_tuples(elements,
                                  min_size=min_size,
                                  max_size=max_size)
            .map(discrete_set_from_points))
