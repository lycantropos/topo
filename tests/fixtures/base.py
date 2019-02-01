from functools import partial
from typing import Optional

import pytest
from hypothesis.searchstrategy import SearchStrategy

from tests import strategies
from tests.utils import find
from topo.base import Set


@pytest.fixture(scope='session')
def min_set_size() -> int:
    return 0


@pytest.fixture(scope='session')
def max_set_size() -> Optional[int]:
    return 2


@pytest.fixture(scope='function')
def sets_strategy(min_set_size: int,
                  max_set_size: Optional[int]) -> SearchStrategy[Set]:
    limit_size = partial(partial,
                         min_size=min_set_size,
                         max_size=max_set_size)
    plain_sets = (strategies.empty_sets
                  | limit_size(strategies.discrete.to_discrete_sets)
                  (strategies.hashables)
                  | strategies.intervals)
    return plain_sets | limit_size(strategies.to_unions)(plain_sets)


@pytest.fixture(scope='function')
def set_(sets_strategy: SearchStrategy[Set]) -> Set:
    return find(sets_strategy)


@pytest.fixture(scope='function')
def other_set(sets_strategy: SearchStrategy[Set]) -> Set:
    return find(sets_strategy)


@pytest.fixture(scope='function')
def another_set(sets_strategy: SearchStrategy[Set]) -> Set:
    return find(sets_strategy)
