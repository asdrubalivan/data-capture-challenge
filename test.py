"""
Module for app tests
"""

import pytest
import json
from capture import DataCapture


@pytest.fixture
def capture() -> DataCapture:
    """
    Fixture with already captured values

    Returns:
        DataCapture with captured values
    """
    capture = DataCapture()
    capture.add(3)
    capture.add(9)
    capture.add(3)
    capture.add(4)
    capture.add(6)

    return capture


@pytest.fixture
def empty_capture() -> DataCapture:
    """
    Empty capture fixture

    Returns:
        Empty DataCapture
    """
    return DataCapture()


@pytest.fixture
def big_capture() -> DataCapture:
    """
    This is a fixture to test a capture
    with a lot of values

    Returns:
        A DataCapture with 600 objects
    """
    json_data = json.load(open("fixtures/data.json", "r"))
    capture = DataCapture()
    capture_add = capture.add  # We cache the method here

    for val in json_data:
        capture_add(val)

    return capture


def test_capture(capture: DataCapture):
    """
    Tests capture methods
    """
    assert len(capture) == 5
    assert capture.max == 9
    assert capture.min == 3


def test_big_capture(big_capture: DataCapture):
    """
    Tests a big capture object
    """
    assert len(big_capture) == 600
    assert big_capture.min == 0
    assert big_capture.max == 999

    stats = big_capture.build_stats()

    assert stats.greater(868) == 84
    assert stats.greater(998) == 2

    assert stats.less(500) == 293
    assert stats.less(2) == 1

    assert stats.between(2, 100) == 50
    assert stats.between(0, 1000) == 600
    assert stats.between(800, 1200) == 125


def test_stats(capture: DataCapture):
    """
    Tests that stats work correctly
    """
    stats = capture.build_stats()

    # should return 2 (only two values 3, 3 are less than 4)
    assert stats.less(4) == 2

    assert stats.less(20) == 5
    assert stats.less(1) == 0
    assert (
        stats.greater(4) == 2
    )  # should return 2 (6 and 9 are the only two values greater than 4)
    assert stats.greater(5) == 2  # Fixing another bug
    assert stats.greater(69) == 0
    assert stats.greater(0) == 5
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


def test_empty_capture(empty_capture: DataCapture):
    """
    Tests that default behavior for captures
    work correctly
    """
    assert len(empty_capture) == 0
    assert empty_capture.min is None
    assert empty_capture.max is None

    with pytest.raises(ValueError):
        empty_capture.build_stats()
