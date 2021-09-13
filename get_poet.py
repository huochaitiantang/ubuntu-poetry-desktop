# -*- coding: utf-8 -*-
import os
import cv2
import sys
import time
import json
import string
import random

from PIL import Image, ImageDraw, ImageFont

sys.path.append('./tools')
from langconv import *


def simple(txt):
  return Converter('zh-hans').convert(txt)


def random_poet(poet_dir, seed):
  poets = []
  for f in os.listdir(poet_dir):
    if f.startswith('poet.'):
      poets.append(f)
  random.seed(seed)
  ind = random.randint(0, len(poets) - 1)
  is_tang = poets[ind].startswith('poet.tang')
  poets_path = poet_dir + '/' + poets[ind]
  #print(poets_path)

  with open(poets_path) as f:
    poets_dict = json.load(f)
    ind = random.randint(0, len(poets_dict) - 1)
    poet = poets_dict[ind]

  poet['author'] = simple(poet['author'])
  poet['title'] = simple(poet['title'])
  # u'strains', u'paragraphs', u'title', u'author'
  poet[u'dynasty'] = u'（唐）' if is_tang else u'（宋）'
  return poet


def add_poet(img_path, poet):
  img = Image.open(img_path)
  draw = ImageDraw.Draw(img)

  title = poet['title']
  author = poet['dynasty'] + poet['author']
  para = poet['paragraphs']
  para_cnt = len(para)
  para_max = 0
  for ind in range(para_cnt):
    para[ind] = simple(para[ind])
    para_len = len(para[ind])
    if para_len > para_max:
      para_max = para_len
  
  W = 1000.
  H = 600.
  mid_h = 400
  mid_w = 1420
  GAP = 8
  # Text size
  font_mid = int(W / (para_max + 10))

  # Too high
  while ((font_mid + GAP)*(para_cnt + 2)) > H:
    font_mid -= 1
  
  # Title, author size
  font_big = font_mid + GAP
  font_sml = font_mid - GAP

  # Title too long
  while (font_big * len(title)) > W:
    font_big -= 1

  # Title location
  vertical = mid_h - (font_mid + GAP)*(para_cnt + 2)/2
  horizont = mid_w - font_big * len(title) / 2

  # Write Title
  font = ImageFont.truetype("font/simhei.ttf", font_big, encoding="utf-8")
  draw.text((horizont, vertical), title, (0, 0, 0), font=font)

  # Author location
  vertical = vertical + font_big + GAP
  horizont = mid_w - font_sml * len(author) / 2

  # Write Author
  font = ImageFont.truetype("font/simhei.ttf", font_sml, encoding="utf-8")
  draw.text((horizont, vertical), author, (0, 0, 0), font=font)
  
  # Para location
  vertical = vertical + font_sml + GAP
  horizont = mid_w - font_mid * para_max / 2 + font_mid

  # Write Paragraphs
  font = ImageFont.truetype("font/simhei.ttf", font_mid, encoding="utf-8")
  for p in para:
    draw.text((horizont, vertical), p, (0, 0, 0), font=font)
    vertical = vertical + font_mid + GAP

  return img