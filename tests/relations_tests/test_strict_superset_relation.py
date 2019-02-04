from tests.utils import implication
from topo.base import Set


def test_asymmetry(set_: Set, other_set: Set) -> None:
    assert implication(set_ > other_set, not other_set > set_)


def test_connection_with_superset_relation(set_: Set, other_set: Set) -> None:
    assert implication(set_ > other_set, set_ >= other_set)


def test_irreflexivity(set_: Set) -> None:
    assert not set_ > set_


def test_transitivity(set_: Set, other_set: Set, another_set: Set) -> None:
    assert implication(set_ > other_set > another_set, set_ > another_set)
