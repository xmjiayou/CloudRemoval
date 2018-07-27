from cloud_removal import main
from cloud_removal.core import model
from cloud_removal.core import processor
from cloud_removal.core import image_utils


def test_simulate_missing(primary_image, target_region):
    img = main.simulate_missing(primary_image, target_region)
    return img


def test_multi_temporal_dr(primary_image, fill_image, target_region):
    img = main.process_by_multi_temporal(primary_image, fill_image, target_region, processor.DrProcessor)
    return img


def test_multi_temporal_llhm(primary_image, fill_image, target_region):
    img = main.process_by_multi_temporal(primary_image, fill_image, target_region, processor.LlhmProcessor)
    return img


def test_multi_temporal_wlr(primary_image, fill_image, target_region):
    img = main.process_by_multi_temporal(primary_image, fill_image, target_region)
    return img


def test_statistics(img_o, img_r, target_region):
    img_o = image_utils.open_image("D:\\test\\new\\out7\\"+img_o)
    result = main.result_statistics(img_o, img_r, target_region)
    return result


if __name__ == '__main__':
    original_img = "20170315.jpg"
    primary_img = "20170315_cover.jpg"
    fill_img = "20170126.jpg"
    tr = model.SimpleTargetRegion(150, 349, 100, 299)
    tr2 = model.SlcOffTargetRegion(500, 500, 0.5, -200.0, 10.0, 40.0)
    tr3 = model.SimpleTargetRegion(150, 249, 100, 199)
    tr4 = model.SimpleTargetRegion(200, 225, 100, 125)

    # image = test_simulate_missing(primary_image, tr3)
    # image = test_multi_temporal_dr(tr)
    # image = test_multi_temporal_llhm(primary_img, fill_img, tr2)
    image = test_multi_temporal_wlr(primary_img, fill_img, tr3)
    print(test_statistics(original_img, image, tr3))
    image_utils.save_image(image, "D:\\test\\new\\out7\\20170315_cover_by_0126.jpg")
    image_utils.show_image(image)

