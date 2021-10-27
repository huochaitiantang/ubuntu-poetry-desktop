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


def random_tang300_poet(poet_dir, seed):
  random.seed(seed)
  is_tang = True
  poets_path = poet_dir + '/唐诗三百首.json'

  with open(poets_path) as f:
    poets_dict = json.load(f)
    ind = random.randint(0, len(poets_dict) - 1)
    poet = poets_dict[ind]

  poet['author'] = simple(poet['author'])
  poet['title'] = simple(poet['title'])
  # u'strains', u'paragraphs', u'title', u'author'
  poet[u'dynasty'] = u'（唐）' if is_tang else u'（宋）'
  return poet


def add_poet(img_path, poet, img_info=""):
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

  fill_color = (255, 255, 255)
  stroke_color = (0, 0, 0)
  stroke_width = 3

  # Title location
  vertical = mid_h - (font_mid + GAP)*(para_cnt + 2)/2
  horizont = mid_w - font_big * len(title) / 2

  # Write Title
  font = ImageFont.truetype("font/simhei.ttf", font_big, encoding="utf-8")
  draw.text((horizont, vertical), title, fill=fill_color, font=font, stroke_fill=stroke_color, stroke_width=stroke_width)

  # Author location
  vertical = vertical + font_big + GAP
  horizont = mid_w - font_sml * len(author) / 2

  # Write Author
  font = ImageFont.truetype("font/simhei.ttf", font_sml, encoding="utf-8")
  draw.text((horizont, vertical), author, fill=fill_color, font=font, stroke_fill=stroke_color, stroke_width=stroke_width)

  # Para location
  vertical = vertical + font_sml + GAP
  horizont = mid_w - font_mid * para_max / 2 + font_mid

  # Write Paragraphs
  font = ImageFont.truetype("font/simhei.ttf", font_mid, encoding="utf-8")
  for p in para:
    draw.text((horizont, vertical), p, fill=fill_color, font=font, stroke_fill=stroke_color, stroke_width=stroke_width)
    vertical = vertical + font_mid + GAP

  # write the img info
  if img_info != "":
    idx = img_info.find('(')
    if idx >= 1:
      img_name = img_info[:idx-1]
      img_author = img_info[idx:]
      w, h = img.size
      font = ImageFont.truetype("font/simhei.ttf", 20, encoding="utf-8")
      draw.text((w - (21 * len(img_name) + 20), h - 50), img_name, fill=fill_color, font=font, stroke_fill=stroke_color, stroke_width=1)
      #draw.text((w - (21 * len(img_name) + 20), h - 25), img_author, fill=fill_color, font=font, stroke_fill=stroke_color, stroke_width=1)

  return img