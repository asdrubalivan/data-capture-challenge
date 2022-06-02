"""
This is the module that implements all the captures and stats operations
"""

from collections import defaultdict
from typing import DefaultDict, Optional, Generator, Tuple, Dict

__all__ = ["DataCapture", "Stats"]


class DataCapture:
    """
    This is the DataCapture class, used to read integers
    """

    def __init__(self):
        self.dict_mapping: DefaultDict[int, int] = defaultdict(int)
        """Dict that is going to capture values
        """
        #: Minimum value captured
        self.min: Optional[int] = None
        #: Maximum value captured
        self.max: Optional[int] = None

    def __len__(self) -> int:
        return sum(self.dict_mapping.values())

    def __repr__(self):  # pragma: no cover
        return f"DataCapture(min:{self.min}, max:{self.max}, elements:{len(self)})"

    def add(self, value: int) -> None:
        """
        Adds a new value to the capture
        Args:
            value: The value to add, it should be an integer
        """
        self.dict_mapping[value] += 1
        if self.min is None or self.min > value:
            self.min = value

        if self.max is None or self.max < value:
            self.max = value

    def _mapping_generator(self) -> Generator[Tuple[int, int], None, None]:
        """
        This is a convenience function that creates a generator
        to iterate all the captured elements
        Yields:
            A tuple of two elements with an index and the number
            of elements that have been captured for that index
        """
        r = range(self.min - 1, self.max + 1)
        for index in r:
            yield index, self.dict_mapping[index]

    def build_stats(self) -> "Stats":
        """
        This is the method that builds stats from the captured
        values.

        It runs in O(n) time

        Returns:
            A new Stats object
        Raises:
            ValueError if there are no values captured
        """
        if self.min is None or self.max is None:
            raise ValueError(f"Invalid values of {self.min=} and {self.max=}")

        accumulated_stats = dict()
        counter = 0
        for index, value in self._mapping_generator():
            counter += value
            accumulated_stats[index] = counter

        return Stats(self, accumulated_stats)


class Stats:
    """
    This is the Stats class that we use to
    read all the data from a DataCapture instance
    """

    def __init__(self, data: "DataCapture", accumulated_stats: Dict[int, int]):
        #: This is a DataCapture instance
        self.data = data
        #: This is a dictionary with accumulated values.
        #: They are cached here so lookups are fast
        self.accumulated_stats = accumulated_stats

    def __repr__(self):  # pragma: no cover
        return f"Stats(({self.data.min=}, {self.data.max=}),{self.accumulated_stats=})"

    def _clamp(self, val):
        return max(self.data.min, min(val, self.data.max))

    def less(self, value: int) -> int:
        """
        Args:
            value: an int
        Returns:
            The number of values captured lesser than value
        """
        if self.data.min <= value <= self.data.max:
            return self.accumulated_stats[value - 1]
        elif value > self.data.max:
            return self.accumulated_stats[self.data.max]
        else:
            return 0

    def between(self, begin: int, end: int) -> int:
        """
        Args:
            begin: Start point
            end: End point
        Returns:
            The number of values that are between "begin" and "end"
        """
        min_ = self.data.min
        max_ = self.data.max

        if (begin < min_ and end < min_) or (begin > max_ and end > max_):
            return 0

        # Avoid flipped args
        new_begin = min(begin, end)
        new_end = max(begin, end)

        clamped_begin = self._clamp(new_begin)
        clamped_end = self._clamp(new_end)

        less_than_begin_elements = self.accumulated_stats[clamped_begin - 1]
        less_than_end_elements = self.accumulated_stats[clamped_end]

        return less_than_end_elements - less_than_begin_elements

    def greater(self, value):
        """
        Args:
            value: an int
        Returns:
            The number of values captured greater than value
        """
        if self.data.min <= value <= self.data.max:
            return self.accumulated_stats[self.data.max] - self.accumulated_stats[value]
        elif value > self.data.max:
            return 0
        else:
            return self.accumulated_stats[self.data.max]
