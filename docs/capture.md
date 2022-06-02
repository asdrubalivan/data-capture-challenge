Module capture
==============
This is the module that implements all the captures and stats operations

Classes
-------

`DataCapture()`
:   This is the DataCapture class, used to read integers

    ### Instance variables

    `dict_mapping`
    :   Dict that is going to capture values

    `max`
    :   Maximum value captured

    `min`
    :   Minimum value captured

    ### Methods

    `add(self, value: int) ‑> None`
    :   Adds a new value to the capture
        Args:
            value: The value to add, it should be an integer

    `build_stats(self) ‑> capture.Stats`
    :   This is the method that builds stats from the captured
        values.
        
        It runs in O(n) time
        
        Returns:
            A new Stats object
        Raises:
            ValueError if there are no values captured

`Stats(data: DataCapture, accumulated_stats: Dict[int, int])`
:   This is the Stats class that we use to
    read all the data from a DataCapture instance

    ### Instance variables

    `accumulated_stats`
    :   This is a dictionary with accumulated values.
        They are cached here so lookups are fast

    `data`
    :   This is a DataCapture instance

    ### Methods

    `between(self, begin: int, end: int) ‑> int`
    :   Args:
            begin: Start point
            end: End point
        Returns:
            The number of values that are between "begin" and "end"

    `greater(self, value)`
    :   Args:
            value: an int
        Returns:
            The number of values captured greater than value

    `less(self, value: int) ‑> int`
    :   Args:
            value: an int
        Returns:
            The number of values captured lesser than value