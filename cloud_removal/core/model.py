import abc
from .image_utils import *
from collections import namedtuple


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
                        self.mask[x][y] = self.TARGET_VALUE

    def is_target(self, x, y):
        return self.mask[x][y] == self.TARGET_VALUE


SimplePoint = namedtuple("SimplePoint", ["x", "y"])


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


class SimpleWindow(object):
    """
    Moving window
    """
    def __init__(self, x, y, size, img_size):
        if not size % 2 == 1:
            raise ValueError("window size must be odd")
        self._x = x
        self._y = y

        half_size = (size-1)/2
        max_x = img_size[0]-1
        max_y = img_size[1]-1

        # window can not over the extend of image
        if x-half_size < 0:
            self._x0 = 0
            self._width = x+half_size
        elif x+half_size > max_x:
            self._x0 = x-half_size
            self._width = max_x-self._x0+1
        else:
            self._x0 = x - half_size
            self._width = size
        if y-half_size < 0:
            self._y0 = 0
            self._height = y+half_size
        elif y+half_size > max_y:
            self._y0 = y-half_size
            self._height = max_y-self._y0+1
        else:
            self._y0 = y - half_size
            self._height = size

    @property
    def x(self):
        return int(self._x)

    @property
    def y(self):
        return int(self._y)

    @property
    def x0(self):
        return int(self._x0)

    @property
    def y0(self):
        return int(self._y0)

    @property
    def width(self):
        return int(self._width)

    @property
    def height(self):
        return int(self._height)


# SimilarPixelPair = namedtuple("SimilarPixelPair", ["x", "y", "value_p", "value_f"])
class SimilarPixelPair(object):
    """
    similar pixel pair
    to record the value of primary and fill image in pixel(x,y)
    """
    def __init__(self, x, y, p, f):
        self._x = x
        self._y = y
        self._f = f
        self._p = p

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def value_p(self):
        return self._p

    @property
    def value_f(self):
        return self._f


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
