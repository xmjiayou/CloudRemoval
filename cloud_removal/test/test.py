from cloud_removal.core import image_utils
from PIL import ImageDraw
import cloud_removal.core.image_utils


if __name__ == "__main__":
    image = image_utils.open_image("D:\\test\\new\\20170315.jpg")
    image2 = image_utils.open_image("D:\\test\\new\\20170315.jpg")
    print(type(image.getpixel((0, 0))[0]))
    # draw = ImageDraw.Draw(image)
    # for x in range(100, 200):
    #     for y in range(100, 200):
    #         draw.point((x, y), (0, 0, 0))
    # cloud_removal.core.image_utils.show_image(image)
