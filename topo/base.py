from abc import (ABC,
                 abstractmethod)
from functools import reduce
from itertools import repeat
from operator import (and_,
                      sub)
from typing import (FrozenSet,
                    Generic,
                    Iterable)

from reprit.base import generate_repr

from .functional import flatmap
from .hints import Domain


class Set(ABC, Generic[Domain]):
    @abstractmethod
    def __bool__(self) -> bool:
        """
        Evaluates to ``True`` if set is not empty and ``False`` otherwise.
        """
        pass

    @abstractmethod
    def __hash__(self) -> int:
        """
        All sets considered hashable (e.g. for using as ``dict`` keys)
        and as a consequence should not be mutated after creation.
        """
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __and__(self, other: 'Set') -> 'Set':
        """
        Intersects with given set.
        """
        pass

    @abstractmethod
    def __contains__(self, object_: Domain) -> bool:
        """
        Checks membership of given object.
        """
        pass

    @abstractmethod
    def __or__(self, other: 'Set') -> 'Set':
        """
        Unites with given set.
        """
        pass

    @abstractmethod
    def __sub__(self, other: 'Set') -> 'Set':
        """
        Subtracts given set.
        """
        pass

    def __eq__(self, other: 'Set') -> bool:
        """
        Checks equality with given set.
        """
        if not isinstance(other, Set):
            return NotImplemented
        if not self:
            return not other
        return not (self - other) and not (other - self)

    def __ge__(self, other: 'Set') -> bool:
        """
        Checks if set is superset of given set.
        """
        if not isinstance(other, Set):
            return NotImplemented
        return self & other == other

    def __gt__(self, other: 'Set') -> bool:
        """
        Checks if set is strict superset of given set.
        """
        if not isinstance(other, Set):
            return NotImplemented
        return self >= other and self != other

    def __le__(self, other: 'Set') -> bool:
        """
        Checks if set is subset of given set.
        """
        if not isinstance(other, Set):
            return NotImplemented
        return self & other == self

    def __lt__(self, other: 'Set') -> bool:
        """
        Checks if set is strict subset of given set.
        """
        if not isinstance(other, Set):
            return NotImplemented
        return self <= other and self != other

    def __rsub__(self, other: 'Set') -> 'Set':
        return NotImplemented

    def __xor__(self, other: 'Set') -> 'Set':
        """
        Symmetrically subtracts given set.
        """
        return (self | other) - (self & other)

    def unfold(self) -> Iterable['Set']:
        """
        Returns disjunctive subsets.
        """
        yield self


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

    def __ge__(self, other: Set) -> bool:
        if not isinstance(other, Set):
            return NotImplemented
        return not other

    def __gt__(self, other: Set) -> bool:
        if not isinstance(other, Set):
            return NotImplemented
        return False

    def __le__(self, other: Set) -> bool:
        if not isinstance(other, Set):
            return NotImplemented
        return True

    def __lt__(self, other: Set) -> bool:
        if not isinstance(other, Set):
            return NotImplemented
        return bool(other)

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
        self._subsets = frozenset(filter(None, flatmap(Set.unfold, subsets)))

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

    def __and__(self, other: Set) -> Set:
        if not isinstance(other, Set):
            return NotImplemented
        if not (self or other):
            return EMPTY_SET
        return (Union(*map(and_, self.subsets, repeat(other)))
                .fold())

    def __eq__(self, other: Set) -> bool:
        if not isinstance(other, Union):
            return super().__eq__(other)
        return self.subsets == other.subsets

    def __ge__(self, other: Set) -> bool:
        if not self:
            return not other
        if not isinstance(other, Union):
            return any(subset >= other
                       for subset in self.subsets)
        return all(self >= subset
                   for subset in other.subsets)

    def __le__(self, other: Set) -> bool:
        return all(subset <= other
                   for subset in self.subsets)

    def __or__(self, other: Set) -> Set:
        if not isinstance(other, Set):
            return NotImplemented
        if not other:
            return self
        return (Union(*self.subsets, other)
                .fold())

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
        return (Union(*map(sub, self.subsets, repeat(other)))
                .fold())

    def fold(self) -> Set:
        """
        Flattens union if possible.
        """
        subsets = self.subsets
        if not subsets:
            return EMPTY_SET
        if len(subsets) == 1:
            return list(subsets)[0]
        return self

    def unfold(self) -> Iterable[Set]:
        yield from flatmap(Set.unfold, self.subsets)


def compress(sets: Iterable[Set]) -> Iterable[Set]:
    sets = list(flatmap(Set.unfold, sets))
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
            yield from set_.unfold()
