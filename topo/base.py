from abc import (ABC,
                 abstractmethod)
from functools import reduce
from itertools import repeat
from operator import (and_,
                      sub)
from typing import (FrozenSet,
                    Generic,
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
        if not self:
            return not other
        return not (self - other) and not (other - self)

    def __rsub__(self, other: 'Set') -> 'Set':
        return NotImplemented

    def __xor__(self, other: 'Set') -> 'Set':
        return (self | other) - (self & other)


EMPTY_SET_STRING = '{}'


class EmptySet(Set[Domain]):
    def __init__(self) -> None:
        pass

    def __bool__(self) -> bool:
        return False

    def __hash__(self) -> int:
        return 0

    __repr__ = generate_repr(__init__)

    def __str__(self) -> str:
        return EMPTY_SET_STRING

    def __and__(self, other: Set) -> Set:
        return self

    def __contains__(self, object_: Domain) -> bool:
        return False

    def __eq__(self, other: Set) -> bool:
        if not isinstance(other, Set):
            return NotImplemented
        return not other

    def __or__(self, other: Set) -> Set:
        if not isinstance(other, Set):
            return NotImplemented
        return other

    def __rsub__(self, other: Set) -> Set:
        return other

    def __sub__(self, other: Set) -> Set:
        return self


EMPTY_SET = EmptySet()


class Union(Set[Domain]):
    def __init__(self, *subsets: Set) -> None:
        self._disperse = True
        self._subsets = frozenset(filter(None, flatmap(flatten_set, subsets)))

    @property
    def subsets(self) -> FrozenSet[Set]:
        if self._disperse:
            self._subsets = frozenset(compress(self._subsets))
            self._disperse = False
        return self._subsets

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
        if not (self or other):
            return EMPTY_SET
        return Union(*map(and_, self.subsets, repeat(other)))

    def __or__(self, other: Set) -> Set:
        if not isinstance(other, Set):
            return NotImplemented
        if not other:
            return self
        return Union(*self.subsets, other)

    def __contains__(self, object_: Domain) -> bool:
        return any(object_ in subset
                   for subset in self.subsets)

    def __rsub__(self, other: Set) -> Set:
        if not isinstance(other, Set):
            return NotImplemented
        if not self:
            return other
        if not other:
            return EMPTY_SET
        operands = map(sub, repeat(other), self.subsets)
        return reduce(and_, operands)

    def __sub__(self, other: Set) -> Set:
        if not isinstance(other, Set):
            return NotImplemented
        return Union(*map(sub, self.subsets, repeat(other)))


def compress(sets: Iterable[Set]) -> Iterable[Set]:
    sets = list(flatmap(flatten_set, sets))
    while True:
        try:
            set_ = sets.pop()
        except IndexError:
            break
        for index, rest_set in enumerate(sets):
            union = set_ | rest_set
            if (isinstance(union, Union)
                    and set_ in union._subsets
                    and rest_set in union._subsets):
                continue
            else:
                sets[index] = union
                break
        else:
            yield from flatten_set(set_)


def flatten_set(set_: Set) -> Iterable[Set]:
    if isinstance(set_, Union):
        yield from flatmap(flatten_set, set_.subsets)
    else:
        yield set_
