import pytest

from tests import strategies
from tests.utils import find
from topo.continuous import Interval


@pytest.fixture(scope='function')
def interval() -> Interval:
    return find(strategies.intervals)


@pytest.fixture(scope='function')
def other_interval() -> Interval:
    return find(strategies.intervals)


@pytest.fixture(scope='function')
def another_interval() -> Interval:
    return find(strategies.intervals)
