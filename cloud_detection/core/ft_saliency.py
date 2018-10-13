from PIL import Image, ImageFilter
import numpy as np
from cloud_detection.core import CIELab_utils as Lab
from cloud_removal.core import model


img = Image.open("D:\\Workspace\\envi\\120-53\\clip\\rgb\\20170502.tif").convert(mode="RGB", colors=256)
img = img.filter(ImageFilter.GaussianBlur(5))

img_width = img.width
img_height = img.height

l_ = np.zeros((img_width, img_height), dtype=np.float64)
a_ = np.zeros((img_width, img_height), dtype=np.float64)
b_ = np.zeros((img_width, img_height), dtype=np.float64)


for x in range(img_width):
    for y in range(img_height):
        l_[x][y], a_[x][y], b_[x][y] = Lab.rgb_to_lab(img.getpixel((x, y)))

l_mean = np.mean(l_)
a_mean = np.mean(a_)
b_mean = np.mean(b_)

s = np.zeros((img_width, img_height), dtype=np.float64)

for x in range(img_width):
    for y in range(img_height):
        s[x][y] = ((l_[x][y]-l_mean)**2 + (a_[x][y]-a_mean)**2 + (b_[x][y]-b_mean)**2)**(1/2)

c = np.zeros((img_width, img_height), dtype=np.float64)
std = np.std(s)

for x in range(img_width):
    for y in range(img_height):
        if s[x][y] < std:
            s_t = s[x][y]
        else:
            window = model.SimpleWindow(x,y,3,(img_width,img_height))
            w = [s[i][j]
                 for i in range(window.x0, window.x0+window.width)
                 for j in range(window.y0, window.y0+window.height)]
            v = np.var(w)
            s_t = s[x][y]**v
        if s_t > 255:
            s_t = 255
        c[x][y] = s_t - s[x][y]

c = np.transpose(c)
img_new = Image.fromarray(c)
img_new.filter(ImageFilter.MedianFilter)
img_new.show()
