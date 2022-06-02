Module test
===========
Module for app tests

Functions
---------

    
`big_capture() ‑> capture.DataCapture`
:   This is a fixture to test a capture
    with a lot of values
    
    Returns:
        A DataCapture with 600 objects

    
`capture() ‑> capture.DataCapture`
:   Fixture with already captured values
    
    Returns:
        DataCapture with captured values

    
`empty_capture() ‑> capture.DataCapture`
:   Empty capture fixture
    
    Returns:
        Empty DataCapture

    
`test_big_capture(big_capture: capture.DataCapture)`
:   Tests a big capture object

    
`test_capture(capture: capture.DataCapture)`
:   Tests capture methods

    
`test_empty_capture(empty_capture: capture.DataCapture)`
:   Tests that default behavior for captures
    work correctly

    
`test_stats(capture: capture.DataCapture)`
:   Tests that stats work correctly