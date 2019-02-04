from tests.utils import implication
from topo.continuous import Interval


def test_reflexivity(interval: Interval) -> None:
    assert interval.intersects_with_interval(interval)


def test_symmetry(interval: Interval, other_interval: Interval) -> None:
    assert implication(interval.intersects_with_interval(other_interval),
                       other_interval.intersects_with_interval(interval))


def test_overlapping_intervals(interval: Interval,
                               other_interval: Interval) -> None:
    assert implication(interval.overlaps_interval(other_interval),
                       interval.intersects_with_interval(other_interval))
