from PIL import Image
import numpy
import matplotlib.pyplot as plt


def open_image(image_path, mode="RGB"):
    """
    open an image in rgb model
    :param image_path: image file path
    :param mode: open mode
    :return: PIL.Image.Image
    """
    print("Opening image file in '%s'." % image_path)
    return Image.open(image_path).convert(mode)


def save_image(image, output_path):
    if not isinstance(image, Image.Image):
        raise TypeError("image must be PIL.Image.Image")
    image.save(output_path)


def image_to_array(image):
    if not image.mode == "L":
        raise ValueError("image must be L mode")
    return numpy.array(image, dtype=int)


def array_to_image(array):
    return Image.fromarray(array).convert("L")


def split_image(image):
    if not isinstance(image, Image.Image):
        raise TypeError("image must be Image.Image")
    return image.split()


def merge_images(images, mode="RGB"):
    return Image.merge(mode, images)


def show_image(image):
    plt.figure("main")
    plt.axis("off")
    plt.imshow(image)
    plt.show()
