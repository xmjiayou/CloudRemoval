from cloud_removal import main
from cloud_removal.core import model
from cloud_removal.core import processor
from cloud_removal.core import image_utils
import profile

primary_image = "20170315.jpg"
fill_image = "20170126.jpg"
tr = model.SimpleTargetRegion(150, 349, 100, 299)
tr2 = model.SlcOffTargetRegion(500, 500, 0.5, -200.0, 10.0, 40.0)
tr3 = model.SimpleTargetRegion(150, 249, 100, 199)


def test_simulate_missing():
    img = main.simulate_missing(primary_image, tr2)
    return img


def test_multi_temporal_dr():
    img = main.process_by_multi_temporal(primary_image, fill_image, tr, processor.DrProcessor)
    return img


def test_multi_temporal_llhm():
    img = main.process_by_multi_temporal(primary_image, fill_image, tr2, processor.LlhmProcessor)
    return img


def test_multi_temporal_wlr():
    img = main.process_by_multi_temporal(primary_image, fill_image, tr3)
    return img


def test_statistics():
    img_o = image_utils.open_image("D:\\test\\new\\"+primary_image)
    img_r = test_multi_temporal_llhm()
    result = main.result_statistics(img_o, img_r, tr2)
    return result


def test_speed():
    image_utils.show_image(test_multi_temporal_dr())


if __name__ == '__main__':
    # image_utils.show_image(test_multi_temporal_dr())
    # image_utils.show_image(test_multi_temporal_llhm())
    # image_utils.show_image(test_multi_temporal_wlr())
    profile.run("test_speed()")
