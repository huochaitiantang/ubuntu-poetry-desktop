# -*- coding: utf-8 -*-
import urllib.request
import requests
import os
import re
import time
from get_poet import random_poet, add_poet, random_tang300_poet
import json


def get_img_url(date=None):
    img_url = ""
    img_info = ""
    try:
        cur_date = time.strftime("%Y-%m-%d", time.localtime())
        cur_second = int(time.mktime(time.strptime(cur_date,"%Y-%m-%d")))
        date = cur_date if date is None else date
        second = int(time.mktime(time.strptime(date,"%Y-%m-%d")))
        last_id = (cur_second - second) // (60 * 60 * 24)
        url = "https://www.bing.com/HPImageArchive.aspx?format=js&idx={}&n=1&mkt=zh-CN".format(last_id)
        r = requests.get(url)
        status = r.status_code
        if status == 200:
            img = r.json()['images'][0]
            if img['enddate'] != date.replace('-', ''):
                raise Exception("Not equal date: {} vs {}".format(date, img['enddate']))
            img_url = "https://cn.bing.com/" + img['url']
            img_info = img['copyright']
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


def process_date(img_dir, date):
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    second = int(time.mktime(time.strptime(date,"%Y-%m-%d")))
    bing_img_path = os.path.join(img_dir, "{}.jpg".format(date))
    poet_img_path = os.path.join(img_dir, "{}-poet.jpg".format(date))
    json_path = os.path.join(img_dir, "{}.json".format(date))

    if  (not os.path.exists(bing_img_path)) or \
        (not os.path.exists(poet_img_path)) or \
        (not os.path.exists(json_path)):

        img_url, img_info = get_img_url(date)
        if img_url != "":
            print("Bing img: {}, {}".format(img_url, img_info))
            save_img(img_url, bing_img_path)

            # poet = random_poet("./chinese-poetry/json", second)
            poet = random_tang300_poet("./chinese-poetry/json", second)
            img = add_poet(bing_img_path, poet, img_info=img_info)
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


def main():
    while True:
        date = time.strftime("%Y-%m-%d", time.localtime())
        process_date("./img", date)
        time.sleep(1800)


def test():
    # only latest 7 days are valid
    process_date("./img", "2021-09-05")
    process_date("./img", "2021-09-06")
    process_date("./img", "2021-09-07")
    process_date("./img", "2021-09-08")
    process_date("./img", "2021-09-09")
    process_date("./img", "2021-09-10")
    process_date("./img", "2021-09-11")
    process_date("./img", "2021-09-12")
    process_date("./img", "2021-09-13")
    process_date("./img", "2021-09-14")


if __name__ == "__main__":
    #test()
    main()