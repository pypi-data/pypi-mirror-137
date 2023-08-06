from study_lyte.depth import get_depth_from_acceleration
import pytest
import numpy as np

@pytest.mark.parametrize("accel, dt, expected_depth", [
    ([1,1, 1], 1, [0.5, 1. , 1.5])
])
def test_get_depth_from_acceleration(accel, dt, expected_depth):
    """
    Test our ability to extract position of the probe from acceleration
    """

    depth = get_depth_from_acceleration(np.array(accel), dt=dt)
    np.testing.assert_equal(depth, expected_depth)