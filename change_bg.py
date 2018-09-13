# -*- coding: utf-8 -*-
import os
import cv2
import sys
import time
import json
import random

from PIL import Image, ImageDraw, ImageFont

sys.path.append('./tools')
from langconv import *

def add_text(img_path, txt):
  img = Image.open(img_path)
  draw = ImageDraw.Draw(img)
  font = ImageFont.truetype("font/simhei.ttf", 50, encoding="utf-8")
  draw.text((800, 150), txt, (0, 0, 0), font=font)

  new_path = os.getcwd() + '/tmp.jpg'
  img.save(new_path)
  return new_path


def simple(txt):
  return Converter('zh-hans').convert(txt)


def add_poet(img_path, poet):
  txt = simple(poet['title']) + '\n'
  txt = txt + poet['dynasty']
  txt = txt + simple(poet['author']) + '\n'
  for p in poet['paragraphs']:
    txt = txt + simple(p) + '\n'

  img = Image.open(img_path)
  draw = ImageDraw.Draw(img)
  font = ImageFont.truetype("font/simhei.ttf", 50, encoding="utf-8")
  draw.text((800, 150), txt, (0, 0, 0), font=font)

  new_path = os.getcwd() + '/tmp.jpg'
  img.save(new_path)
  return new_path
  

def random_poet(poet_dir):
  poets = []
  for f in os.listdir(poet_dir):
    if f.startswith('poet.'):
      poets.append(f)
  ind = random.randint(0, len(poets) - 1)
  is_tang = poets[ind].startswith('poet.tang')
  poets_path = poet_dir + '/' + poets[ind]
  print(poets_path)

  with open(poets_path) as f:
    poets_dict = json.load(f)
    ind = random.randint(0, len(poets_dict) - 1)
    poet = poets_dict[ind]

  # u'strains', u'paragraphs', u'title', u'author'
  poet[u'dynasty'] = u'（唐）' if is_tang else u'（宋）'
  print(poet.keys())
  return poet


def change_bg(bgdir, poetdir):
  imgs = os.listdir(bgdir)
  ind = random.randint(0, len(imgs) - 1)
  img_path = '{}/{}'.format(bgdir, imgs[ind])
  #img_path = add_text(img_path, u'Hello World!醉翁亭记')
  poet = random_poet(poetdir)
  img_path = add_poet(img_path, poet)

  c_path = '"file://' + img_path + '"'
  print("Change Background with {}...".format(c_path))
  os.system('gsettings set org.gnome.desktop.background picture-uri ' + c_path)


def main():
  interval = 5
  bgdir = os.getcwd() + '/img'
  while True:
    change_bg(bgdir, './chinese-poetry/json')
    time.sleep(interval)

if __name__ == '__main__':
  main()
