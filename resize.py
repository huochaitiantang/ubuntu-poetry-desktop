import os
import cv2

minH = 1080
minW = 1920

cnt = 1

for img_name in os.listdir('./img'):
  img = cv2.imread('./img/{}'.format(img_name))
  h, w, c = img.shape

  upH = ((minH + 0.5) / float(h))
  upW = ((minW + 0.5) / float(w))
  up = max(upH, upW)

  if up > 1.0:
    newH = int(h * up)
    newW = int(w * up)
    img = cv2.resize(img, (newW, newH), interpolation=cv2.INTER_CUBIC)
    h, w, c = img.shape

  print(h, w, c)
  assert(h >= minH)
  assert(w >= minW)

  startH = (h - minH) / 2
  startW = (w - minW) / 2
  endH = startH + minH
  endW = startW + minW

  #cv2.imwrite('./img/{}.jpg'.format(cnt), img[startH:endH, startW:endW, :])
  cnt = cnt + 1


