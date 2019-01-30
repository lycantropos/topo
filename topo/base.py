from abc import (ABC,
                 abstractmethod)
from functools import reduce
from itertools import repeat
from operator import (and_,
                      or_,
                      sub)
from typing import (Generic,
                    Iterable)

from .functional import flatmap
from .hints import Domain
from .utils import generate_repr


class Set(ABC, Generic[Domain]):
    @abstractmethod
    def __bool__(self) -> bool:
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __and__(self, other: 'Set') -> 'Set':
        pass

    @abstractmethod
    def __contains__(self, object_: Domain) -> bool:
        pass

    @abstractmethod
    def __or__(self, other: 'Set') -> 'Set':
        pass

    @abstractmethod
    def __sub__(self, other: 'Set') -> 'Set':
        pass

    def __eq__(self, other: 'Set') -> bool:
        return not (self - other) and not (other - self)

    def __rsub__(self, other: 'Set') -> 'Set':
        return NotImplemented

    def __xor__(self, other: 'Set') -> 'Set':
        return (self | other) - (self & other)


class DiscreteSet(Set[Domain]):
    def __init__(self, *points: Domain) -> None:
        self.points = frozenset(points)

    def __bool__(self) -> bool:
        return bool(self.points)

    def __hash__(self) -> int:
        return hash(self.points)

    __repr__ = generate_repr(__init__)

    def __str__(self) -> str:
        return '{' + ', '.join(map(str, self.points)) + '}'

    def __and__(self, other: Set) -> Set:
        if not isinstance(other, Set):
            return NotImplemented
        common_points = (point
                         for point in self.points
                         if point in other)
        return DiscreteSet(*common_points)

    def __contains__(self, object_: Domain) -> bool:
        return object_ in self.points

    def __eq__(self, other: Set) -> bool:
        if not isinstance(other, Set):
            return NotImplemented
        if not isinstance(other, DiscreteSet):
            return super().__eq__(other)
        return self.points == other.points

    def __or__(self, other: Set) -> Set:
        if not isinstance(other, Set):
            return NotImplemented
        if not isinstance(other, DiscreteSet):
            extra_points = [point
                            for point in self.points
                            if point not in other]
            if not extra_points:
                return other
            return Union(DiscreteSet(*extra_points),
                         other)
        return DiscreteSet(*self.points, *other.points)

    def __sub__(self, other: Set) -> Set:
        if not isinstance(other, Set):
            return NotImplemented
        remaining_points = (point
                            for point in self.points
                            if point not in other)
        return DiscreteSet(*remaining_points)


EMPTY_SET = DiscreteSet()
EMPTY_SET_STRING = str(EMPTY_SET)


class Union(Set[Domain]):
    def __init__(self, *subsets: Set) -> None:
        def flatten_set(set_: Set) -> Iterable[Set]:
            if isinstance(set_, Union):
                yield from flatmap(flatten_set, set_.subsets)
            else:
                yield set_

        self.subsets = tuple(filter(None, flatmap(flatten_set, subsets)))

    def __bool__(self) -> bool:
        return any(map(bool, self.subsets))

    def __hash__(self) -> int:
        return hash(self.subsets)

    __repr__ = generate_repr(__init__)

    def __str__(self) -> str:
        if not self:
            return EMPTY_SET_STRING
        return ' or '.join(map(str, self.subsets))

    def __eq__(self, other: Set) -> bool:
        if not isinstance(other, Set):
            return NotImplemented
        if not isinstance(other, Union):
            return super().__eq__(other)
        return self.subsets == other.subsets

    def __and__(self, other: Set) -> Set:
        if not isinstance(other, Set):
            return NotImplemented
        if not other:
            return EMPTY_SET
        intersections = map(and_, self.subsets, repeat(other))
        return reduce(or_, intersections)

    def __or__(self, other: Set) -> Set:
        if not isinstance(other, Set):
            return NotImplemented
        if not other:
            return self
        operands = map(or_, self.subsets, repeat(other))
        return reduce(or_, operands)

    def __contains__(self, object_: Domain) -> bool:
        return any(object_ in subset
                   for subset in self.subsets)

    def __rsub__(self, other: Set) -> Set:
        if not isinstance(other, Set):
            return NotImplemented
        operands = map(sub, repeat(other), self.subsets)
        return reduce(and_, operands)

    def __sub__(self, other: Set) -> Set:
        if not isinstance(other, Set):
            return NotImplemented
        operands = map(sub, self.subsets, repeat(other))
        return reduce(or_, operands)
