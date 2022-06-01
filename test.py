import pytest
from capture import DataCapture


@pytest.fixture
def capture():
    capture = DataCapture()
    capture.add(3)
    capture.add(9)
    capture.add(3)
    capture.add(4)
    capture.add(6)

    return capture


@pytest.fixture
def empty_capture():
    return DataCapture()


def test_capture(capture):
    assert len(capture) == 5
    assert capture.max == 9
    assert capture.min == 3


def test_stats(capture):
    stats = capture.build_stats()
    assert stats.less(4) == 2  # should return 2 (only two values 3, 3 are less than 4)
    assert stats.less(20) == 5
    assert stats.less(1) == 0
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


def test_empty_capture(empty_capture):
    assert len(empty_capture) == 0
    assert empty_capture.min is None
    assert empty_capture.max is None

    with pytest.raises(ValueError):
        empty_capture.build_stats()
