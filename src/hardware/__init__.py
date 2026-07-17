"""Hardware-run support: chain selection, readout mitigation, ZNE extrapolation.

Pure-computation helpers for the Month-5/6 hardware scaling pipeline
(experiments/hardware_scaling.py). Nothing here talks to IBM — these functions
take calibration numbers / counts and return numbers, so they are unit-testable
offline (tests/test_hardware_mitigation.py).
"""
