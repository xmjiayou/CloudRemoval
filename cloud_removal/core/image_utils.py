from PIL import Image
import numpy
import matplotlib.pyplot as plt


def open_image(image_path):
    """
    open an image in rgb model
    :param image_path: image file path
    :return: PIL.Image.Image
    """
    return Image.open(image_path).convert("RGB")


def image_to_array(image):
    return numpy.array(image)


def array_to_image(array):
    return Image.fromarray(array).convert("L")


def merge_images(*images):
    return Image.merge("RGB", images)


def show_image(image):
    plt.figure("main")
    plt.axis("off")
    plt.imshow(image)
    plt.show()