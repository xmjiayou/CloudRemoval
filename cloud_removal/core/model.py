import abc
from .image_utils import *


class TargetRegion(metaclass=abc.ABCMeta):
    """
    This is an abstract class.
    The target region going to be processed
    """
    @abc.abstractmethod
    def is_target(self, x, y):
        """
        To override
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
        """
        Constructor of SimpleTargetRegion
        :param x_min: minimum coordinate of X axis
        :param x_max: maximum coordinate of X axis
        :param y_min: minimum coordinate of Y axis
        :param y_max: maximum coordinate of Y axis
        """
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
        """
        Constructor of SlcOffTargetRegion
        :param height: height of image
        :param width: width of image
        :param a: slope of a strip
        :param b0: intercept of the starting strip
        :param interval_b: interval of strip
        :param interval_y: interval between strips
        """
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


class SimpleImage(object):
    """
    single band image
    """
    def __init__(self, pil_img):
        if not isinstance(pil_img, Image.Image):
            raise TypeError("pil_img must be PIL.Image.Image")
        self._height = pil_img.height
        self._width = pil_img.width
        self._values = image_to_array(pil_img)

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    def get_value(self, x, y):
        return self._values[x][y]

    def set_value(self, x, y, v):
        self._values[x][y] = v

    def get_image_array(self):
        return self._values


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
