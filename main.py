"""Entry point module for the app"""

from capture import DataCapture


def main():
    """
    Just a small demo of the app
    """
    capture = DataCapture()
    capture.add(3)
    capture.add(9)
    capture.add(3)
    capture.add(4)
    capture.add(6)

    print(f"Capturing: {capture}")

    stats = capture.build_stats()
    print(f"{stats.less(4)=}")
    print(f"{stats.between(3, 6)=}")
    print(f"{stats.greater(4)=}")


if __name__ == "__main__":
    main()
