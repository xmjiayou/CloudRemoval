from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

img1 = Image.open("111.png").convert("RGB")
img2 = Image.open("222.jpg")
img3 = Image.open("444.jpeg")

if __name__ == "__main__":
    r, g, b = img1.split()
    print(isinstance(img1,Image.Image))
    img11 = Image.merge("RGB", (g, b, r))
    plt.figure("test")
    plt.axis("off")
    plt.imshow(img11)
    plt.show()
