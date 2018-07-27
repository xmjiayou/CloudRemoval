from cloud_removal import main
from cloud_removal.core import model
from cloud_removal.core import processor
from cloud_removal.core import image_utils


primary_image = "20170315.jpg"
fill_image = "20170126.jpg"

tr = model.SimpleTargetRegion(150, 349, 100, 299)
# tr2 = model.SlcOffTargetRegion(500, 500, 0.5, -200.0, 10.0, 40.0)

# img_new = main.simulate_missing(primary_image, tr2)
# img_new = main.process_by_multi_temporal(primary_image, fill_image, tr2, processor.LlhmProcessor)
# img_new = main.process_by_multi_temporal(primary_image, fill_image, tr, processor.WlrProcessor)

# main.show_image(img_new)

img_old = image_utils.open_image("D:\\test\\new\\20170315.jpg")
img_new = image_utils.open_image("D:\\test\\new\\20170315.jpg")

result = main.result_statistics(img_old, img_new, tr)
print(result)
