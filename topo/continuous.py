import math
from decimal import Decimal
from functools import (partial,
                       reduce)
from itertools import (chain,
                       repeat)
from numbers import (Complex,
                     Number)
from operator import (le,
                      lt,
                      or_)
from typing import (Any,
                    Callable,
                    SupportsFloat,
                    Tuple,
                    cast)

from .base import (EMPTY_SET,
                   EMPTY_SET_STRING,
                   Set,
                   Union)
from .discrete import DiscreteSet
from .utils import generate_repr


class Interval(Set[SupportsFloat]):
    operators_by_inclusion = {False: lt,
                              True: le}

    def __new__(cls,
                left_end: SupportsFloat,
                right_end: SupportsFloat,
                *,
                left_end_inclusive: bool = True,
                right_end_inclusive: bool = True):
        inclusion = left_end_inclusive and right_end_inclusive
        operator = cls.operators_by_inclusion[inclusion]
        if not operator(left_end, right_end):
            return EMPTY_SET
        if inclusion and left_end == right_end:
            return DiscreteSet(left_end)
        return super().__new__(cls)

    def __init__(self,
                 left_end: SupportsFloat,
                 right_end: SupportsFloat,
                 *,
                 left_end_inclusive: bool = True,
                 right_end_inclusive: bool = True) -> None:
        self.left_end = left_end
        self.right_end = right_end
        self.left_end_inclusive = left_end_inclusive
        self.right_end_inclusive = right_end_inclusive

    def __bool__(self) -> bool:
        inclusion = self.left_end_inclusive and self.right_end_inclusive
        operator = self.operators_by_inclusion[inclusion]
        return operator(self.left_end, self.right_end)

    def __hash__(self) -> int:
        return hash((self.left_end,
                     self.right_end,
                     self.left_end_inclusive,
                     self.right_end_inclusive))

    __repr__ = generate_repr(__init__)

    def __str__(self) -> str:
        if not self:
            return EMPTY_SET_STRING
        left_bracket = '[' if self.left_end_inclusive else '('
        right_bracket = ']' if self.right_end_inclusive else ')'
        return (left_bracket
                + str(self.left_end) + ', ' + str(self.right_end)
                + right_bracket)

    def __and__(self, other: Set) -> Set:
        if not isinstance(other, Set):
            return NotImplemented

        if not isinstance(other, Interval):
            return other & self

        if not self.intersects_with_interval(other):
            return EMPTY_SET

        if self.left_end < other.left_end:
            left_end = other.left_end
            left_end_inclusive = other.left_end_inclusive
        elif self.left_end == other.left_end:
            left_end = self.left_end
            left_end_inclusive = min(self.left_end_inclusive,
                                     other.left_end_inclusive)
        else:
            left_end = self.left_end
            left_end_inclusive = self.left_end_inclusive

        if self.right_end < other.right_end:
            right_end = self.right_end
            right_end_inclusive = self.right_end_inclusive
        elif self.right_end == other.right_end:
            right_end = self.right_end
            right_end_inclusive = min(self.right_end_inclusive,
                                      other.right_end_inclusive)
        else:
            right_end = other.right_end
            right_end_inclusive = other.right_end_inclusive

        return Interval(left_end, right_end,
                        left_end_inclusive=left_end_inclusive,
                        right_end_inclusive=right_end_inclusive)

    def __contains__(self, object_: Any) -> bool:
        if not isinstance(object_, Number):
            return False
        if isinstance(object_, Complex):
            if object_.imag:
                return False
            object_ = object_.real
        if math.isnan(object_):
            return False
        left_operator = self.operators_by_inclusion[self.left_end_inclusive]
        right_operator = self.operators_by_inclusion[self.right_end_inclusive]
        left_comparison = left_operator(self.left_end, object_)
        right_comparison = right_operator(object_, self.right_end)
        return left_comparison and right_comparison

    def __eq__(self, other: Set) -> bool:
        if not isinstance(other, Set):
            return NotImplemented
        if isinstance(other, DiscreteSet):
            return False
        if not isinstance(other, Interval):
            return other == self
        return (self.left_end == other.left_end
                and self.left_end_inclusive == other.left_end_inclusive
                and self.right_end == other.right_end
                and self.right_end_inclusive == other.right_end_inclusive)

    def __or__(self, other: Set) -> Set:
        if not isinstance(other, Set):
            return NotImplemented
        if not isinstance(other, Interval):
            return other | self

        if not self.intersects_with_interval(other):
            return Union(self, other)

        def by_left_end_sorting_key(interval: Interval
                                    ) -> Tuple[SupportsFloat, bool]:
            return interval.left_end, not interval.left_end_inclusive

        def by_right_end_sorting_key(interval: Interval
                                     ) -> Tuple[SupportsFloat, bool]:
            return interval.right_end, interval.right_end_inclusive

        left_interval = min(self, other,
                            key=by_left_end_sorting_key)
        right_interval = max(self, other,
                             key=by_right_end_sorting_key)
        return Interval(left_interval.left_end, right_interval.right_end,
                        left_end_inclusive=left_interval.left_end_inclusive,
                        right_end_inclusive=right_interval.right_end_inclusive)

    def __sub__(self, other: Set) -> Set:
        if not isinstance(other, Set):
            return NotImplemented
        if isinstance(other, DiscreteSet):
            def to_real_part(number: Number) -> SupportsFloat:
                if not isinstance(number, Complex):
                    return number
                return number.real

            break_points = sorted(map(to_real_part, filter(self.__contains__,
                                                           other.points)))
            if not break_points:
                return self
            first_excluded_number = break_points[0]
            left_end = self.left_end
            right_end = self.right_end
            left_end_inclusive = self.left_end_inclusive
            if first_excluded_number == left_end:
                left_end_inclusive = False
                break_points.pop(0)
            right_end_inclusive = self.right_end_inclusive
            try:
                last_excluded_number = break_points[-1]
            except IndexError:
                pass
            else:
                if last_excluded_number == right_end:
                    right_end_inclusive = False
                    break_points.pop(-1)
            left_ends = chain([left_end], break_points)
            right_ends = chain(break_points, [right_end])
            left_ends_inclusion = chain([left_end_inclusive],
                                        repeat(False,
                                               times=len(break_points)))
            right_ends_inclusion = chain(repeat(False,
                                                times=len(break_points)),
                                         [right_end_inclusive])
            parts = (Interval(left_end, right_end,
                              left_end_inclusive=left_end_inclusive,
                              right_end_inclusive=right_end_inclusive)
                     for (left_end, right_end,
                          left_end_inclusive,
                          right_end_inclusive) in zip(left_ends, right_ends,
                                                      left_ends_inclusion,
                                                      right_ends_inclusion))
            return Union(*parts)
        if not isinstance(other, Interval):
            return other.__rsub__(self)

        if not self.intersects_with_interval(other):
            return self

        return Union(
                Interval(self.left_end, other.left_end,
                         left_end_inclusive=self.left_end_inclusive,
                         right_end_inclusive=not other.left_end_inclusive),
                Interval(other.right_end, self.right_end,
                         left_end_inclusive=not other.right_end_inclusive,
                         right_end_inclusive=self.right_end_inclusive))

    def intersects_with_interval(self, other: 'Interval') -> bool:
        if self.left_end < other.left_end:
            operator = self.operators_by_inclusion[self.right_end_inclusive]
            return operator(other.left_end, self.right_end)
        elif self.left_end > other.left_end:
            operator = self.operators_by_inclusion[self.left_end_inclusive]
            return operator(self.left_end, other.right_end)
        return True


OpenInterval = cast(Callable[[SupportsFloat, SupportsFloat], Interval],
                    partial(Interval,
                            left_end_inclusive=False,
                            right_end_inclusive=False))
real_line = OpenInterval(Decimal('-inf'), Decimal('inf'))
real_line_extended = Interval(Decimal('-inf'), Decimal('inf'))
