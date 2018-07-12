import logging
import abc
from . import model
from .image_utils import *

logger = logging.getLogger(__name__)


class AbstractProcessor(metaclass=abc.ABCMeta):

    def __init__(self, primary_img_path, fill_img_path, target_region):
        self.primary_img = primary_img
        self.fill_img = fill_img
        self.target_region = target_region
        self.band_num = band_num

    @abc.abstractmethod
    def _process(self, img, value):
        """
        To override
        """
        return None

    def process(self):
        logging.INFO("------开始处理------")
        for i in self.band_num:
            n = i+1
            logging.INFO("处理波段"+n)
            try:
                return self._process()
            except Exception as e:
                logging.ERROR(e)

        logging.INFO("------结束处理------")


class SimulatedProcessor(object):
    """
    The processor that simulates image data missing
    """
    def __init__(self, img_path, target_region):
        self.img = Image.open(img_path).convert("RGB")
        if not isinstance(target_region, model.TargetRegion):
            raise TypeError("target_region must be TargetRegion")
        self.target_region = target_region

    def _process(self, image, value):
        simple_img = model.SimpleImage(image)
        for x in range(simple_img.width):
            for y in range(simple_img.height):
                if self.target_region.is_target(x, y):
                    simple_img.set_value(x, y, value)
        img = Image.fromarray(simple_img.get_image_array())
        return img

    def process(self, r=0, g=0, b=0):
        logger.info("------ start:simulated processor ------")
        img_r, img_g, img_b = self.img.split()
        img_new = []
        for img in (img_r, img_g, img_b):
            img_new.append(self._process(img, 0))
        img_new = Image.merge("RGB", img_new)
        logger.info("------ end:simulated processor ------")
        return img_new
