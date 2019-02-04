from tests.utils import (equivalence,
                         implication)
from topo.base import (EMPTY_SET,
                       Set)


def test_antisymmetry(set_: Set, other_set: Set) -> None:
    assert implication(set_ >= other_set >= set_, set_ == other_set)


def test_connection_with_intersection(set_: Set, other_set: Set) -> None:
    assert equivalence(set_ >= other_set, set_ & other_set == other_set)


def test_connection_with_union(set_: Set, other_set: Set) -> None:
    assert equivalence(set_ >= other_set, set_ | other_set == set_)


def test_greatest_element(set_: Set) -> None:
    assert set_ >= EMPTY_SET


def test_maximal_element(set_: Set) -> None:
    assert implication(EMPTY_SET >= set_, not set_)


def test_reflexivity(set_: Set) -> None:
    assert set_ >= set_


def test_transitivity(set_: Set, other_set: Set, another_set: Set) -> None:
    assert implication(set_ >= other_set >= another_set, set_ >= another_set)
