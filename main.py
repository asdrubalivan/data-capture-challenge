from capture import DataCapture


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
