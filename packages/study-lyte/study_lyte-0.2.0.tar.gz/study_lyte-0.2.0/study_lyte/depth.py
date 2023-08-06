import numpy as np


def get_depth_from_acceleration(acceleration, dt=None, series_time=None):
    """
    acceleration indexed by time or dt is provided
    Assuming the starting velocity is 0, then calculate the
    travel
    """
    if dt is not None:
        series_time = np.array([dt]*len(acceleration))

    delta_x = 0.5 * acceleration * series_time**2
    return delta_x.cumsum()