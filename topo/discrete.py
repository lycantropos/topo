from .base import (Set,
                   Union)
from .hints import Domain
from .utils import generate_repr


class DiscreteSet(Set[Domain]):
    def __init__(self, *points: Domain) -> None:
        self.points = frozenset(points)

    def __bool__(self) -> bool:
        return bool(self.points)

    def __hash__(self) -> int:
        return hash(self.points)

    __repr__ = generate_repr(__init__)

    def __str__(self) -> str:
        return '{' + ', '.join(map(repr, self.points)) + '}'

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
            return Union(DiscreteSet(*extra_points), other)
        return DiscreteSet(*self.points, *other.points)

    def __sub__(self, other: Set) -> Set:
        if not isinstance(other, Set):
            return NotImplemented
        remaining_points = (point
                            for point in self.points
                            if point not in other)
        return DiscreteSet(*remaining_points)
