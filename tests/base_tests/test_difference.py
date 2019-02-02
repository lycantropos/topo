from topo.base import (EMPTY_SET,
                       Set)


def test_difference_subtrahend(set_: Set,
                               other_set: Set,
                               another_set: Set) -> None:
    result = set_ - (other_set - another_set)

    assert result == (set_ - other_set) | (set_ & another_set)


def test_empty_set_minuend(set_: Set) -> None:
    result = EMPTY_SET - set_

    assert not result


def test_empty_set_subtrahend(set_: Set) -> None:
    result = set_ - EMPTY_SET

    assert result == set_


def test_expressing_intersection_as_difference(set_: Set,
                                               other_set: Set) -> None:
    result = set_ - (set_ - other_set)

    assert result == set_ & other_set


def test_intersection_minuend(set_: Set,
                              other_set: Set,
                              another_set: Set) -> None:
    result = (set_ & other_set) - another_set

    assert result == set_ & (other_set - another_set)


def test_intersection_subtrahend(set_: Set,
                                 other_set: Set,
                                 another_set: Set) -> None:
    result = set_ - (other_set & another_set)

    assert result == (set_ - other_set) | (set_ - another_set)


def test_union_subtrahend(set_: Set,
                          other_set: Set,
                          another_set: Set) -> None:
    result = set_ - (other_set | another_set)

    assert result == (set_ - other_set) & (set_ - another_set)


def test_self_difference(set_: Set) -> None:
    result = set_ - set_

    assert not result
