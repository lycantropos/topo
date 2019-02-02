import math
from functools import partial
from operator import lt
from typing import SupportsFloat

from hypothesis import strategies
from hypothesis.searchstrategy import SearchStrategy

from tests.utils import Domain
from topo.continuous import Interval
from topo.hints import Map
from .literals.base import (booleans,
                            real_numbers)


@strategies.composite
def to_intervals(draw: Map[SearchStrategy[Domain], Domain],
                 ends: SearchStrategy[SupportsFloat],
                 inclusions: SearchStrategy[bool] = booleans) -> Interval:
    left_end = draw(ends.filter(math.isfinite))
    right_end = draw(ends.filter(partial(lt, left_end)))
    left_end_inclusive = draw(inclusions)
    right_end_inclusive = draw(inclusions)
    return Interval(left_end,
                    right_end,
                    left_end_inclusive=left_end_inclusive,
                    right_end_inclusive=right_end_inclusive)


intervals = to_intervals(real_numbers)
