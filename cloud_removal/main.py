from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from core import processor
from core import model

IMAGE_PATH = "D:\\test\\new\\"


def image_to_array(image):
    return np.array(image)


def array_to_image(array):
    return Image.fromarray(array).convert("L")


def open_image(name):
    file_path = IMAGE_PATH+name
    return Image.open(file_path).convert("RGB")


def show_image(image):
    plt.figure("main")
    plt.axis("off")
    plt.imshow(image)
    plt.show()


if __name__ == "__main__":
    target_region = model.SimpleTargetRegion(150, 350, 100, 300)
    p1 = processor.SimulatedProcessor("D:\\test\\new\\20170315.jpg", target_region)
    img_new = p1.process()
    show_image(img_new)
    # image1 = open_image("20170315.jpg")
    # image2 = open_image("20170126.jpg")
    # r, g, b = image1.split()
    # array1 = image_to_array(r)
    # array2 = image_to_array(image2)
    # print(image1.width)
    # print(type(image1))
    # print(type(array1))
    # print(array1.ndim)
    # print(array1.shape)
    # print(r.size)
    # count = 0
    # for y in range(100, 300):
    #     for x in range(150, 350):
    #         array1[x][y] = array2[x][y]
    #         count = count + 1
    # print(count)
    # image_new = Image.fromarray(array1)
    # show_image(image_new)
