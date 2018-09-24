import os
import cv2

img_names = ["2", "3", "4", "6", "8"]

for img_name in img_names:
  img_path = "./img/{}.jpg".format(img_name)
  assert(os.path.exists(img_path))
  img = cv2.imread(img_path)
  img = cv2.flip(img, 1)
  cv2.imwrite('./img/new_{}.jpg'.format(img_name), img)

