from PIL import Image, ImageFilter

a = Image.open("D:\\Workspace\\envi\\120-53\\clip\\rgb\\20170502.tif").convert(mode="RGB", colors=256)

a = a.filter(ImageFilter.GaussianBlur(5))
a.show()
