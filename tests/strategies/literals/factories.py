from typing import (Optional,
                    Tuple)

from hypothesis import strategies
from hypothesis.searchstrategy import SearchStrategy

from tests.utils import Domain

to_characters = strategies.characters
to_byte_strings = strategies.binary
to_homogeneous_frozensets = strategies.frozensets
to_homogeneous_lists = strategies.lists


def to_homogeneous_tuples(elements: Optional[SearchStrategy[Domain]] = None,
                          *,
                          min_size: int = 0,
                          max_size: Optional[int] = None
                          ) -> SearchStrategy[Tuple[Domain, ...]]:
    return (to_homogeneous_lists(elements,
                                 min_size=min_size,
                                 max_size=max_size)
            .map(tuple))


to_strings = strategies.text
