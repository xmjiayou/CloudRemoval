import abc
import logging
import numpy

logger = logging.getLogger(__name__)


class TargetRegion(metaclass=abc.ABCMeta):
    """
    This is an abstract class.
    The target region going to be processed
    """
    @abc.abstractmethod
    def is_target(self, x, y):
        """
        To overwrite
        Determine (x,y) whether or not it is in the target region.
        :param x: x
        :param y: y
        :return: boolean
        """
        return False


class SimpleTargetRegion(TargetRegion):
    """
    Rectangle target region
    """
    def __init__(self, x_min, x_max, y_min, y_max):
        if not _is_int(x_min, x_max, y_min, y_max):
            raise TypeError("extends must be int")
        self._x_min = x_min
        self._x_max = x_max
        self._y_min = y_min
        self._y_max = y_max

    def is_target(self, x, y):
        return self._x_min <= x <= self._x_max and self._y_min <= y <= self._y_max


class SlcOffTargetRegion(TargetRegion):
    """
    The region that simulate slc-off
    """
    TARGET_VALUE = 0
    N0_TARGET_VALUE = 1

    def __init__(self, height, width, a, b0, interval_b, interval_y):
        if not _is_int(height, width):
            raise TypeError("height or width must be int")
        if not _is_float(a, b0, interval_b, interval_y):
            raise TypeError("a, b0, interval_b, interval_y must be float")
        self.height = height
        self.width = width
        self.mask = numpy.ones([width, height])
        shadow_num = int((height-b0)/(interval_b+interval_y))
        for y in range(0, height):
            for x in range(0, width):
                for i in range(0, shadow_num):
                    b = b0 + i * (interval_b + interval_y)
                    y1 = a * x + b
                    y2 = a * x + b + interval_b
                    if y1 < y < y2:
                        self.mask[y][x] = self.TARGET_VALUE

    def is_target(self, x, y):
        if not _is_int(x, y):
            raise TypeError("x,y must be int")
        if x < 0 or x > self.width:
            raise ValueError("x is out of range")
        if y < 0 or y > self.height:
            raise ValueError("y is out of range")
        result = self.mask[y][x]
        return result == self.TARGET_VALUE


def _is_int(*args):
    for a in args:
        if not isinstance(a, int):
            return False
    return True


def _is_float(*args):
    for a in args:
        if not isinstance(a, float):
            return False
    return True
