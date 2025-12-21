import math


def is_almost_integral(value: float, tolerance: float = 0.01):
    """Check if value is within tolerance of the nearest integer"""
    nearest_integral = round(value)
    return math.isclose(value, nearest_integral, abs_tol=tolerance)
