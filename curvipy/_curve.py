from abc import ABC as _ABC
from abc import abstractmethod as _abstractmethod

from typing import Callable as _Callable
from typing import Union as _Union

from ._interval import Interval as _Interval

_TNumber = _Union[int, float]
_TVector = tuple[_TNumber, _TNumber]


class Curve(_ABC):
    """Base class for all two-dimensional curves."""

    @_abstractmethod
    def points(self, interval: _Interval) -> list[_TNumber]:
        """Returns the curve point for each value in the given interval.

        Parameters
        ----------
        interval : Interval
            The interval from which the curve will be plotted.

        Returns
        -------
        list[int or float]
            A list of curve points.
        """
        pass


class Function(Curve):
    """Function that given a real number returns another real number `y = f(x)`.

    Parameters
    ----------
    function : Callable[[int or float], int or float]
        Function that given an integer or float returns another integer or float.
    """

    def __init__(self, function: _Callable[[_TNumber], _TNumber]):
        self.function = function

    def points(self, interval: _Interval) -> list[_TNumber]:
        """Returns the function point for each value in the given interval.

        Parameters
        ----------
        interval : Interval
            The interval from which the function will be plotted.

        Returns
        -------
        list[int or float]
            A list of function points.
        """
        return [(x, self.function(x)) for x in interval]


class ParametricFunction(Curve):
    """Function that given a real number returns a 2-dimensional vector `f(t) = <x(t), y(t)>`.

    Parameters
    ----------
    function : Callable[[int or float], tuple[int or float, int or float]]
                Function that given an integer or float returns a tuple containing two \
                integers or floats.
    """

    def __init__(self, parametric_function: _Callable[[_TNumber], _TVector]):
        self.parametric_function = parametric_function

    def points(self, interval: _Interval) -> list[_TNumber]:
        """Returns the parametric function point for each value in the given interval.

        Parameters
        ----------
        interval : Interval
            The interval from which the parametric function will be plotted.

        Returns
        -------
        list[int or float]
            A list of parametric function points.
        """
        return [self.parametric_function(t) for t in interval]


class TransformedCurve(Curve):
    """Applies a linear transformation (defined as a 2x2 matrix) to the given curve.

    Parameters
    ----------
    matrix : tuple[\
            tuple[int or float, int or float],\
            tuple[int or float, int or float]\
            ]
        Linear transformation represented as a 2x2 matrix.
        
    curve : Curve
        Curve to be transformed.
    """

    def __init__(
        self,
        matrix: tuple[
            tuple[_TNumber, _TNumber],
            tuple[_TNumber, _TNumber],
        ],
        curve: Curve,
    ):
        self.__curve = curve
        self.__matrix = matrix

    def points(self, interval: _Interval) -> list[_TNumber]:
        """Returns the curve point for each value in the given interval.

        Parameters
        ----------
        interval : Interval
            The interval from which the transformed curve will be plotted.

        Returns
        -------
        list[int or float]
            A list of transformed curve points.
        """
        points = []
        for point in self.__curve.points(interval):
            points.append(
                [
                    point[0] * self.__matrix[0][0] + point[1] * self.__matrix[0][1],
                    point[0] * self.__matrix[1][0] + point[1] * self.__matrix[1][1],
                ]
            )
        return points
