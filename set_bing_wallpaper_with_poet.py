# -*- coding: utf-8 -*-
import urllib.request
import requests
import os
import re
import time
from get_poet import random_poet, add_poet
import json


def get_img_url(url="https://cn.bing.com/"):
    img_url = ""
    img_info = ""
    try:
        r = requests.get(url)
        status = r.status_code
        if status == 200:

            #<a href="/th?id=OHR.VeniceBeach_ZH-CN9971532384_1920x1200.jpg&amp;rf=LaDigue_1920x1200.jpg" data-h="ID=HpApp,44580.1" class="downloadLink
            res = re.search(r"<a href=\"\/th.*downloadLink", r.text)
            res = res.group()
            res = re.split(r"\"", res)[1]
            img_url = url + res

            # class="title">威尼斯海滩滑板公园鸟瞰图，洛杉矶</a><div><div class="copyright" id="copyright">
            res = re.search(r"class=\"title\">.*id=\"copyright\">", r.text)
            res = res.group()
            img_info = re.split(r"[<>]", res)[1]
        else:
            print("Error status code: {}!".format(status))
    except Exception as e:
        print("Error: {}!".format(e))
    return img_url, img_info


def save_img(img_url, img_path):
    try:
        urllib.request.urlretrieve(img_url, img_path)
        print("Local Img {} Saved".format(img_path))
    except Exception as e:
        print ("Error: {}".format(e))
    return


def set_wallpaper(img_path):
  c_path = '"file://' + os.path.abspath(img_path) + '"'
  print("Set Wallpaper {}".format(c_path))
  os.system('gsettings set org.gnome.desktop.background picture-uri ' + c_path)
  return


def main():
    img_dir = "./img"
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    while True:
        date = time.strftime("%Y-%m-%d", time.localtime())
        second = int(time.mktime(time.strptime(date,"%Y-%m-%d")))

        bing_img_path = os.path.join(img_dir, "{}.jpg".format(date))
        poet_img_path = os.path.join(img_dir, "{}-poet.jpg".format(date))
        json_path = os.path.join(img_dir, "{}.json".format(date))

        if  (not os.path.exists(bing_img_path)) or \
            (not os.path.exists(poet_img_path)) or \
            (not os.path.exists(json_path)):

            img_url, img_info = get_img_url()
            print("Bing img: {}, {}".format(img_url, img_info))
            save_img(img_url, bing_img_path)

            poet = random_poet("./chinese-poetry/json", second)
            img = add_poet(bing_img_path, poet)
            print("Poet: {}".format(poet))
            img.save(poet_img_path)

            data = {
                "date": date,
                "second": second,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "bing_img_url:": img_url,
                "bing_img_info": img_info,
                "poet": poet,
                "bing_img_path": bing_img_path,
                "poet_img_path": poet_img_path,
            }
            json.dump(data, open(json_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

            set_wallpaper(poet_img_path)

        time.sleep(1800)


if __name__ == "__main__":
    main()