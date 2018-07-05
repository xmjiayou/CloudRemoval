import logging
from PIL import Image
import logging
from .target_region import TargetRegion

logger = logging.getLogger(__name__)


class AbstractProcessor(object):

    def __init__(self, primary_img, fill_img, target_region, band_num):
        self.primary_img = primary_img
        self.fill_img = fill_img
        self.target_region = target_region
        self.band_num = band_num

    def _process(self):
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

    """
    def __init__(self, img_path, target_region):
        self.img = Image.open(img_path).convert("RGB")
        if not isinstance(target_region, TargetRegion):
            raise TypeError("target_region must be TargetRegion")
        self.target_region = target_region

    def _process(self, r=0, g=0, b=0):
        logger.info("------ start:simulated processor ------")

        logger.info("------ end:simulated processor ------")
