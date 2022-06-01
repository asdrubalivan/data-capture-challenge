from collections import defaultdict

__all__ = ["DataCapture", "Stats"]


class DataCapture:
    def __init__(self):
        self._dict_mapping = defaultdict(int)
        self.min = None
        self.max = None

    def __len__(self):
        return sum(self._dict_mapping.values())

    def __repr__(self):  # pragma: no cover
        return f"DataCapture(min:{self.min}, max:{self.max}, elements:{len(self)})"

    def add(self, value):
        self._dict_mapping[value] += 1
        if self.min is None or self.min > value:
            self.min = value

        if self.max is None or self.max < value:
            self.max = value

    def _mapping_generator(self):
        r = range(self.min - 1, self.max + 1)
        for index in r:
            yield index, self._dict_mapping[index]

    def build_stats(self):
        if self.min is None or self.max is None:
            raise ValueError(f"Invalid values of {self.min=} and {self.max=}")

        accumulated_stats = dict()
        counter = 0
        for index, value in self._mapping_generator():
            counter += value
            accumulated_stats[index] = counter

        return Stats(self, accumulated_stats)


class Stats:
    def __init__(self, data, accumulated_stats):
        self.data = data
        self.accumulated_stats = accumulated_stats

    def __repr__(self):  # pragma: no cover
        return f"Stats(({self.data.min=}, {self.data.max=}),{self.accumulated_stats=})"

    def _clamp(self, val):
        return max(self.data.min, min(val, self.data.max))

    def less(self, value):
        if self.data.min <= value <= self.data.max:
            return self.accumulated_stats[value - 1]
        elif value > self.data.max:
            return self.accumulated_stats[self.data.max]
        else:
            return 0

    def between(self, begin, end):
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
        if self.data.min <= value <= self.data.max:
            return self.accumulated_stats[self.data.max] - self.accumulated_stats[value]
        elif number > self.data.max:
            return 0
        else:
            return self.accumulated_stats[self.data.max]
