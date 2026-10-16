"""Simulated GPS hardware service."""


class GPSSignalLostError(Exception):
    """Custom exception raised when the GPS device loses its signal."""


def get_current_location():
    """Return the simulated phone GPS coordinates."""
    return (10.0, 105.0)
