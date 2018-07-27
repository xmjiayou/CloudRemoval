from cloud_removal.core import *

IMAGE_PATH = "D:\\test\\new\\out7\\"


def simulate_missing(img_name, target_region):
    """
    simulate data missing in an image
    :param img_name: image name in IMAGE_PATH
    :param target_region: model.TargetRegion
    :return: a new image formatted by Image.Image
    """
    image_full_path = IMAGE_PATH + img_name
    p = processor.SimulatedProcessor(image_full_path, target_region)
    return p.process()


def process_by_multi_temporal(primary_img_name, fill_img_name, target_region, p=processor.WlrProcessor):
    """
    reconstruct the missing date of primary image with fill image in target region by p
    :param primary_img_name: image name in IMAGE_PATH
    :param fill_img_name: image name in IMAGE_PATH
    :param target_region: model.TargetRegion
    :param p: class of MultiTemporalProcessor
    :return: a new Image.Image
    """
    p_path = IMAGE_PATH + primary_img_name
    f_path = IMAGE_PATH + fill_img_name
    if issubclass(processor.MultiTemporalProcessor, p):
        raise TypeError("p must be MultiTemporalProcessor")
    instance_p = p(p_path, f_path, target_region)
    return instance_p.process()


def result_statistics(original_img, reconstructed_img, target_region):
    """
    compute the statistics result(r, are, uiqi, msa)
    :param original_img: the image with missing data
    :param reconstructed_img: the reconstructed image
    :param target_region:
    :return: StatisticsResult
    """
    p = statistics.StatisticProcessor(original_img, reconstructed_img, target_region)
    result = p.process()
    return result


def show_image(image):
    image_utils.show_image(image)
