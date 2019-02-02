from tests.utils import implication
from topo.continuous import Interval


def test_reflexivity(interval: Interval) -> None:
    result = interval.intersects_with_interval(interval)

    assert result


def test_symmetry(interval: Interval, other_interval: Interval) -> None:
    result = interval.intersects_with_interval(other_interval)

    assert implication(result,
                       other_interval.intersects_with_interval(interval))
