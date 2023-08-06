import numpy as np


def uniform(distance: float, width: float, parameter: float) -> float:
    """
    Uniform distribution for density profiles
    :param distance: Distance from flight path
    :param width: Swath width
    :param parameter: Free parameter to be fitted
    :return:
    """
    es_dentro = np.abs(distance) < width / 2
    return np.double(es_dentro) * parameter


def triangular(distance: float, width: float, parameter: float) -> float:
    """
    Triangular distribution for density profiles
    :param distance: Distance from flight path
    :param width: Swath width
    :param parameter: Free parameter to be fitted
    :return:
    """
    slope = -2 * parameter / width
    es_dentro = np.abs(distance) < width / 2  # pragma: no mutate
    return (slope * np.abs(distance) + parameter) * np.double(es_dentro)


def normal(distance: float, width: float, parameter: float) -> float:
    """
    Normal distribution for density profiles
    :param distance: Distance from flight path
    :param width: Swath width
    :param parameter: Free parameter to be fitted
    :return:
    """
    standard_deviation = width / 4
    return (
        parameter
        / np.sqrt(2 * np.pi * standard_deviation**2)
        * np.exp(-(distance**2) / (2 * standard_deviation**2))
    )
