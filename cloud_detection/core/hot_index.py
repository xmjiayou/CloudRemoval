from PIL import Image, ImageDraw
import numpy as np

image_type = ".tif"
image_path = "D:\\Workspace\\envi\\120-53\\clip\\rgb\\"
primary_image_name = "20160312"
auxiliary_image_name_list = ["20170907",
                             "20170502",
                             # "20161123",
                             "20160718",
                             "20160616",
                             "20160429",
                             "20160413",
                             # "20160312",
                             "20160225"]


def open_image(name):
    file_path = image_path + name + image_type
    return Image.open(file_path).convert("RGB", colors=256)


def hot_index(image, a, b):
    pass


if __name__ == '__main__':
    print("")
