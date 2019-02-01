from hypothesis import strategies

from topo.continuous import Interval
from .literals.base import (booleans,
                            real_numbers)

intervals = strategies.builds(Interval,
                              real_numbers,
                              real_numbers,
                              left_end_inclusive=booleans,
                              right_end_inclusive=booleans)
