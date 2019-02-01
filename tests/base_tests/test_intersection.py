from topo.base import (EMPTY_SET,
                       Set)


def test_absorption_identity(set_: Set, other_set: Set) -> None:
    result = set_ & (set_ | other_set)

    assert result == set_


def test_associativity(set_: Set, other_set: Set, another_set: Set) -> None:
    result = (set_ & other_set) & another_set

    assert result == set_ & (other_set & another_set)


def test_commutativity(set_: Set, other_set: Set) -> None:
    result = set_ & other_set

    assert result == other_set & set_


def test_difference_operand(set_: Set,
                            other_set: Set,
                            another_set: Set) -> None:
    result = (set_ - other_set) & another_set

    assert result == (set_ & another_set) - other_set


def test_distribution_over_union(set_: Set,
                                 other_set: Set,
                                 another_set: Set) -> None:
    result = set_ & (other_set | another_set)

    assert result == (set_ & other_set) | (set_ & another_set)


def test_idempotence(set_: Set) -> None:
    result = set_ & set_

    assert result == set_


def test_left_absorbing_element(set_: Set) -> None:
    result = EMPTY_SET & set_

    assert not result


def test_right_absorbing_element(set_: Set) -> None:
    result = set_ & EMPTY_SET

    assert not result
