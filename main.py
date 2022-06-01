from collections import defaultdict


class DataCapture:
    def __init__(self):
        self._dict_mapping = defaultdict(int)
        self.min = None
        self.max = None

    def __len__(self):
        return sum(self._dict_mapping.values())

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

    def __repr__(self):
        return f"Stats(({self.data.min=}, {self.data.max=}),{self.accumulated_stats=})"

    def _clamp(self, val):
        return max(self.data.min, min(val, self.data.max))

    def less(self, value):
        if self.data.min <= value <= self.data.max:
            return self.accumulated_stats[value - 1]
        elif number > self.data.max:
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


def test_data():
    capture = DataCapture()
    capture.add(3)
    capture.add(9)
    capture.add(3)
    capture.add(4)
    capture.add(6)

    assert len(capture) == 5
    assert capture.max == 9
    assert capture.min == 3

    stats = capture.build_stats()
    assert stats.less(4) == 2  # should return 2 (only two values 3, 3 are less than 4)
    assert (
        stats.greater(4) == 2
    )  # should return 2 (6 and 9 are the only two values greater than 4)
    assert stats.greater(5) == 2  # Fixing another bug
    assert (
        stats.between(3, 6) == 4
    )  # should return 4 (3, 3, 4 and 6 are between 3 and 6)
    assert stats.between(1, 2) == 0
    assert stats.between(10, 100) == 0
    assert stats.between(3, 9) == 5
    assert stats.between(1, 20) == 5
    assert stats.between(7, 8) == 0
    assert stats.between(9, 3) == 5
    assert stats.between(5, 12) == 2


if __name__ == "__main__":
    test_data()
