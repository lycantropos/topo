from tests.utils import implication
from topo.continuous import Interval


def test_reflexivity(interval: Interval) -> None:
    assert interval.merges_with_interval(interval)


def test_symmetry(interval: Interval, other_interval: Interval) -> None:
    assert implication(interval.merges_with_interval(other_interval),
                       other_interval.merges_with_interval(interval))


def test_intersecting_intervals(interval: Interval,
                                other_interval: Interval) -> None:
    assert implication(interval.intersects_with_interval(other_interval),
                       interval.merges_with_interval(other_interval))
