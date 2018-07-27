from .model import *
from .image_utils import *
import progressbar
from concurrent.futures import ProcessPoolExecutor


class SimulatedProcessor(object):
    """
    The processor that simulates image data missing
    """
    def __init__(self, img_path, target_region):
        self.img = open_image(img_path)
        if not isinstance(target_region, TargetRegion):
            raise TypeError("target_region must be TargetRegion")
        self.target_region = target_region

    def _process(self, image, value):
        simple_img = SimpleImage(image)
        for x in range(simple_img.width):
            for y in range(simple_img.height):
                if self.target_region.is_target(x, y):
                    simple_img.set_value(x, y, value)
        img = array_to_image(simple_img.get_image_array())
        return img

    def process(self, rgb=(0, 0, 0)):
        img = self.img.split()
        img_new = [self._process(img[i], rgb[i]) for i in range(0, len(img))]
        return merge_images(img_new)


class MultiTemporalProcessor(metaclass=abc.ABCMeta):
    """
    An abstract class
    """
    def __init__(self, primary_img_path, fill_img_path, target_region):
        self.primary = [SimpleImage(img) for img in split_image(open_image(primary_img_path))]
        self.fill = [SimpleImage(img) for img in split_image(open_image(fill_img_path))]
        if not isinstance(target_region, TargetRegion):
            raise TypeError("target_region must be TargetRegion")
        self.target_region = target_region
        self.band_num = len(self.primary)

    @abc.abstractmethod
    def _process(self, point):
        """
        To override
        process the pixel of primary in (x,y)
        :param point: point of x,y
        """
        pass

    def process(self):
        print("Start: MultiTemporalProcessor")
        print("Total band number is %s." % self.band_num)
        img_width = self.primary[0].width
        img_height = self.primary[0].height
        target_points = [SimplePoint(x, y)
                         for x in range(0, img_width)
                         for y in range(0, img_height)
                         if self.target_region.is_target(x, y)]
        pb = progressbar.ProgressBar()
        pb.start(len(target_points))
        pb_c = 0
        points_result = set()
        for point in target_points:
            points_result.add(self._process(point))
            pb_c = pb_c + 1
            pb.update(pb_c)
        pb.finish()
        # with ProcessPoolExecutor() as executor:
        #     points_result = list(executor.map(self._process, target_points))
        for result in points_result:
            x = result.x
            y = result.y
            for i in range(self.band_num):
                self.primary[i].set_value(x, y, result.get_result(i))
        img_new = [array_to_image(p.get_image_array()) for p in self.primary]
        return merge_images(img_new)


class DrProcessor(MultiTemporalProcessor):
    """
    Direct replacement method.
    """
    def _process(self, point):
        x = point.x
        y = point.y
        result = [self.fill[i].get_value(x, y) for i in range(self.band_num)]
        return PointResult(x, y, result)


class LlhmProcessor(MultiTemporalProcessor):
    """
    Local linear histogram matching method.
    """
    WINDOW_SIZE = 21

    def _process(self, point):
        x = point.x
        y = point.y
        result = []
        for i in range(self.band_num):
            primary = self.primary[i]
            fill = self.fill[i]
            moving_window = SimpleWindow(x, y, self.WINDOW_SIZE, (primary.width, primary.height))
            valid_points = self._search_valid_points(primary, fill, moving_window)
            result.append(self._estimate_result(valid_points, fill.get_value(x, y)))
        return PointResult(x, y, result)

    def _search_valid_points(self, primary, fill, window):
        """
        search valid points in window
        :param primary: primary SimpleImage
        :param fill: fill SimpleImage
        :param window: moving window (SimpleWindow)
        :return: list of SimilarPixelPair
        """
        valid_points = [SimilarPixelPair(x, y, primary.get_value(x, y), fill.get_value(x, y))
                        for x in range(window.x0, window.x0+window.width)
                        for y in range(window.y0, window.y0+window.height)
                        if not self.target_region.is_target(x, y)]
        return valid_points

    def _estimate_result(self, valid_points, fill_value):
        """
        get the estimated result
        :param valid_points: list of SimilarPixelPair
        :param fill_value: the value of fill img in target pixel
        :return: result (float)
        """
        # p_array = numpy.array([valid_point.value_p for valid_point in valid_points])
        # f_array = numpy.array([valid_point.value_f for valid_point in valid_points])
        p_array = [valid_point.value_p for valid_point in valid_points]
        f_array = [valid_point.value_f for valid_point in valid_points]
        variance_p = numpy.var(p_array)
        mean_p = numpy.mean(p_array)
        variance_f = numpy.var(f_array)
        mean_f = numpy.mean(f_array)
        a = variance_p/variance_f
        b = mean_p-a*mean_f
        result = a*fill_value+b
        return int(result)


class WlrProcessor(MultiTemporalProcessor):
    """
    Weighted linear regression
    """
    ALPHA = 1
    UMBER_OF_REFERENCE_VALUE = 90
    INIT_WINDOW_SIZE = 21
    MAX_WINDOW_SIZE = 300
    WINDOW_STEP = 10

    def _process(self, point):
        x = point.x
        y = point.y
        result = []
        for i in range(self.band_num):
            primary = self.primary[i]
            fill = self.fill[i]
            similar_points = self._get_similar_points(primary, fill, x, y)
            if len(similar_points) == 0:
                print("can not find similar pixels in （"+x+","+y+")")
            result.append(self._estimate_result(fill.get_value(x, y), x, y, similar_points))
        return PointResult(x, y, result)

    def _get_similar_points(self, primary, fill, x, y):
        """
        get the similar points pair of target pixel
        :param primary: primary img
        :param fill: fill img
        :param x: x of target pixel
        :param y: y of target pixel
        :return: list of SimilarPixelPair
        """
        similar_points = []
        window_size = self.INIT_WINDOW_SIZE
        while (len(similar_points) < self.UMBER_OF_REFERENCE_VALUE) and (window_size < self.MAX_WINDOW_SIZE):
            moving_window = SimpleWindow(x, y, window_size, (primary.width, primary.height))
            similar_points = self._search_window(primary, fill, moving_window)
            window_size = window_size + self.WINDOW_STEP
        return similar_points

    def _search_window(self, primary, fill, window):
        """
        search similar points pair in window
        :param primary:
        :param fill:
        :param window:
        :return:
        """
        similar_points = []
        fill_target_value = fill.get_value(window.x, window.y)
        threshold = numpy.std(fill.get_image_array())
        for xx in range(window.x0, window.x0+window.width):
            for yy in range(window.y0, window.y0+window.height):
                if abs(fill_target_value-fill.get_value(xx, yy)) <= threshold:
                    if not self.target_region.is_target(xx, yy):
                        similar_point = SimilarPixelPair(xx, yy, primary.get_value(xx, yy), fill.get_value(xx, yy))
                        similar_points.append(similar_point)
        return similar_points

    def _estimate_result(self, fill_value, x, y, similar_points):
        """
        get result
        :param fill_value:
        :param x:
        :param y:
        :param similar_points:
        :return:
        """
        total_num = len(similar_points)
        primary_value_sum = 0
        fill_value_sum = 0
        d_sum = 0
        for point in similar_points:
            primary_value_sum = primary_value_sum + point.value_p
            fill_value_sum = fill_value_sum + point.value_f
            d = (abs(point.value_f-fill_value)+self.ALPHA)*(((point.x-x)**2)+((point.y-y)**2))
            point.d = d
            d_sum = d_sum + d
        primary_value_mean = primary_value_sum/total_num
        fill_value_mean = fill_value_sum/total_num
        if total_num > 2:
            temp_up = 0
            temp_down = 0
            for point in similar_points:
                weight = (1/point.d)/d_sum
                temp_up = temp_up + weight*(point.value_p-primary_value_mean)*(point.value_f-fill_value_mean)
                temp_down = temp_down + ((point.value_f-fill_value_mean)**2)
            a = temp_up/temp_down
            b = primary_value_mean - a*fill_value_mean
        else:
            a = primary_value_mean/fill_value_mean
            b = 0
        result = a * fill_value + b
        return result
