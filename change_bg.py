# -*- coding: utf-8 -*-
import os
import cv2
import time
import random

from PIL import Image, ImageDraw, ImageFont

def add_text(img_path, txt):
  #img = cv2.imread(img_path)
  img = Image.open(img_path)

  draw = ImageDraw.Draw(img)
  font = ImageFont.truetype("font/simhei.ttf", 50, encoding="utf-8")
  draw.text((800, 150), u'诗词标题', (0, 0, 0), font=font)

  new_path = os.getcwd() + '/tmp.jpg'
  img.save(new_path)
  return new_path

def change_bg(bgdir):
  imgs = os.listdir(bgdir)
  ind = random.randint(0, len(imgs) - 1)
  img_path = '{}/{}'.format(bgdir, imgs[ind])
  img_path = add_text(img_path, 'Hello World!醉翁亭记')

  c_path = '"file://' + img_path + '"'
  print("Change Background with {}...".format(c_path))
  os.system('gsettings set org.gnome.desktop.background picture-uri ' + c_path)

def main():
  interval = 5
  bgdir = os.getcwd() + '/img'
  while True:
    change_bg(bgdir)
    time.sleep (interval)

if __name__ == '__main__':
  main()
