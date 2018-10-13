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


primary_image = open_image(primary_image_name)
auxiliary_images = [open_image(name) for name in auxiliary_image_name_list]
height = primary_image.height
width = primary_image.width


def search_seeds():
    seeds = np.zeros((width, height))
    for x in range(width):
        for y in range(height):
            n = 0
            rbg_p = primary_image.getpixel((x, y))
            for a_img in auxiliary_images:
                if is_seed(rbg_p, a_img.getpixel((x, y))):
                    n = n + 1
            if n >= 4:
                seeds[x][y] = 1
    return seeds


def is_seed(rgb_p, rgb_a):
    n = 0
    for i in range(3):
        if (rgb_p[i] - rgb_a[i]) > 170:
            n = n + 1
    return n == 3


def region_growing(seeds):
    mask = np.zeros((width, height))
    for x in range(width):
        for y in range(height):
            if seeds[x][y] == 1:
                mask = mark_cloud((x, y), mask)
    return mask


def mark_cloud(xy, mask):
    x, y = xy
    mask[x][y] = 1
    neighbor_points = get_neighbors((x, y))
    valid_points = check_neighbors(neighbor_points, mask)
    while valid_points is not None and len(valid_points) > 0:
        for point in valid_points:
            p_x, p_y = point
            mask[p_x][p_y] = 1
        temp_points = []
        for point in valid_points:
            neighbors = check_neighbors(get_neighbors(point), mask)
            if len(neighbors) > 0:
                temp_points.extend(neighbors)
        valid_points = set(temp_points)
    # for point in neighbor_points:
    #     if is_cloud(point):
    #         mask = mark_cloud(image, point, mask)
    return mask


def get_neighbors(point):
    x, y = point
    neighbor_points = [(x-1, y-1), (x, y-1), (x+1, y-1),
                       (x-1, y), (x+1, y),
                       (x-1, y+1), (x, y+1), (x+1, y+1)]
    return neighbor_points


def check_neighbors(neighbors, mask):
    valid_points = []
    for point in neighbors:
        x, y = point
        if is_cloud(point) and mask[x][y] != 1:
            valid_points.append(point)
    return valid_points


def is_cloud(point):
    x, y = point
    if x < 0 or y < 0 or x >= width or y >= height:
        return False
    rgb = primary_image.getpixel(point)
    n = 0
    for i in range(3):
        if 150 <= rgb[i] <= 255:
            n = n + 1
    return n == 3


if __name__ == "__main__":
    seeds_ = search_seeds()
    mask_ = region_growing(seeds_)
    image_draw = ImageDraw.Draw(primary_image)
    for xx in range(width):
        for yy in range(height):
            if seeds_[xx][yy] == 1:
                image_draw.point((xx, yy), fill=(0, 0, 255))
            else:
                if mask_[xx][yy] == 1:
                    image_draw.point((xx, yy), fill=(255, 0, 0))
    primary_image.show()
