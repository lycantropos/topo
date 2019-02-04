from tests.utils import implication
from topo.continuous import Interval


def test_antisymmetry(interval: Interval, other_interval: Interval) -> None:
    assert implication(interval.overlaps_interval(other_interval)
                       and other_interval.overlaps_interval(interval),
                       interval == other_interval)


def test_reflexivity(interval: Interval) -> None:
    assert interval.overlaps_interval(interval)


def test_transitivity(interval: Interval,
                      other_interval: Interval,
                      another_interval: Interval) -> None:
    assert implication(interval.overlaps_interval(other_interval)
                       and other_interval.overlaps_interval(another_interval),
                       interval.overlaps_interval(another_interval))
