from .image_utils import *
from . import model
import math


class BandStatisticsResult(object):
    def __init__(self, original_values, reconstructed_values, r, are, uiqi):
        self._original_values = original_values
        self._reconstructed_values = reconstructed_values
        self._r = r
        self._are = are
        self._uiqi = uiqi

    @property
    def original_values(self):
        return self._original_values

    @property
    def reconstructed_values(self):
        return self._reconstructed_values

    @property
    def r(self):
        """the Pearson correlation coefficient"""
        return self._r

    @property
    def are(self):
        """the average relative error"""
        return self._are

    @property
    def uiqi(self):
        """the universal image quality index"""
        return self._uiqi


class StatisticsResult(object):
    def __init__(self, msa, band_results):
        self._msa = msa
        self._band_statistics_result = [result for result in band_results if isinstance(result, BandStatisticsResult)]

    @property
    def msa(self):
        """mean spectral angle"""
        return self._msa

    @property
    def band_results(self):
        """list of all single band result"""
        return self._band_statistics_result

    def __str__(self):
        s = "Band statistic result is:\n"
        n = 0
        for result in self._band_statistics_result:
            n = n+1
            s = s + ("Band %s(R:%s; ARE:%s; UIQI:%s)\n" % (n, result.r, result.are, result.uiqi))
        s = s + ("MSA:%s" % self._msa)
        return s


class StatisticProcessor(object):
    def __init__(self, original_img, reconstructed_img, target_region, band_num=3):
        for img in (original_img, reconstructed_img):
            if not isinstance(img, Image.Image):
                raise TypeError("img must be Image")
        self._original_img = split_image(original_img)
        self._reconstructed_img = split_image(reconstructed_img)
        if not isinstance(target_region, model.TargetRegion):
            raise TypeError("target_region must be TargetRegion")
        self._target_region = target_region
        self._band_num = band_num

    def process(self):
        band_results = []
        for i in range(0, self._band_num):
            band_results.append(self._compute_band_results(i))
        msa = self._compute_msa(band_results)
        return StatisticsResult(msa, band_results)

    def _compute_band_results(self, band):
        """
        r, are, uiqi of each band
        :return: list of BandStatisticsResult
        """
        width = self._original_img[band].width
        height = self._original_img[band].height
        or_img_array = image_to_array(self._original_img[band])
        re_img_array = image_to_array(self._reconstructed_img[band])
        or_values = [int(or_img_array[x][y]) for x in range(0, width)
                     for y in range(0, height)
                     if self._target_region.is_target(x, y)]
        re_values = [int(re_img_array[x][y]) for x in range(0, width)
                     for y in range(0, height)
                     if self._target_region.is_target(x, y)]
        # for x in range(0, width):
        #     for y in range(0, height):
        #         if self._target_region.is_target(x, y):
        #             or_values.append(or_img_array[x][y])
        #             re_values.append(re_img_array[x][y])
        total_num = len(or_values)
        # or_array = numpy.array(or_values)
        # re_array = numpy.array(re_values)
        r_up, r_down_o, r_down_r, are_up = 0, 0, 0, 0
        or_mean = numpy.mean(or_values)
        re_mean = numpy.mean(re_values)
        for i in range(0, total_num):
            or_value = or_values[i]
            re_value = re_values[i]
            r_up = r_up + (or_value-or_mean)*(re_value-re_mean)
            r_down_o = r_down_o + (or_value-or_mean)**2
            r_down_r = r_down_r + (re_value-re_mean)**2
            if or_value == 0:
                or_value = 1
            are_up = are_up + abs(or_value-re_value)/or_value
        r = r_up/((r_down_o*r_down_r)**(1/2))
        are = (are_up/total_num)*100
        std_o = (r_down_o/total_num)**(1/2)
        std_r = (r_down_r/total_num)**(1/2)
        cov_or = r_up/total_num
        uiqi = (cov_or/(std_o*std_r)) *\
               ((2*or_mean*re_mean)/(or_mean**2+re_mean**2)) *\
               ((2*std_o*std_r)/(std_o**2+std_r**2))
        return BandStatisticsResult(or_values, re_values, r, are, uiqi)

    def _compute_msa(self, band_results):
        """
        msa of all bands
        :return:
        """
        total_num = len(band_results[0].original_values)
        msa_up = 0.0
        for i in range(0, total_num):
            msa_up_up = 1
            msa_up_down_left = 1
            msa_up_down_right = 1
            for b in range(0, self._band_num):
                msa_up_up = msa_up_up + band_results[b].original_values[i]*band_results[b].reconstructed_values[i]
                msa_up_down_left = msa_up_down_left + (band_results[b].original_values[i]**2)
                msa_up_down_right = msa_up_down_right + (band_results[b].reconstructed_values[i]**2)
            msa_up = msa_up + math.acos(msa_up_up/((msa_up_down_left*msa_up_down_right)**(1/2)))
        msa = msa_up/total_num
        return msa
