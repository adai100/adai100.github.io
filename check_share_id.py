#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import sleep
from sys import exit
import shutil
import requests
import re, json
import os


def get_list_by_share(share_id, parent_file_id, share_pwd=""):
    if share_pwd == "wumima":
        share_pwd = ""
    share_token = requests.post(
        url="https://api.aliyundrive.com/v2/share_link/get_share_token",
        headers={"Content-Type": "application/json"},
        json={"share_id": share_id, "share_pwd": share_pwd},
    ).json()["share_token"]
    print(share_token)
    url = "https://api.aliyundrive.com/adrive/v2/file/list_by_share"
    headers = {"x-share-token": share_token}
    json1 = {
        "share_id": share_id,
        "parent_file_id": parent_file_id,
        "limit": 200,
        "image_thumbnail_process": "image/resize,w_256/format,jpeg",
        "image_url_process": "image/resize,w_1920/format,jpeg/interlace,1",
        "video_thumbnail_process": "video/snapshot,t_1000,f_jpg,ar_auto,w_256",
        "order_by": "name",
        "order_direction": "ASC",
    }
    json2=requests.post(url, headers=headers, json=json1).json()
    print(json2)
    return json2["items"]


alishares = []
# 检查alishare_list分享的有效性
tempdir = os.path.join(os.path.dirname(__file__), "temp")
shutil.rmtree(tempdir)
fname = os.path.join(os.path.dirname(__file__), "alishare_list.txt")
outputtxtfname = os.path.join(os.path.dirname(__file__), "alisharelist.txt")
outputjsonfname = os.path.join(os.path.dirname(__file__), "alisharelist.json")
print(fname)
with open(fname, "r") as f:
    temp = f.readlines()

for tmp in temp:
    if tmp.strip():
        alishares.append(tmp.strip())

output_txt = ""
output_json = []
for row in alishares:
    line = row.split()
    mount_path = line[0].strip("/")
    # os.makedirs(os.path.join(tempdir,mount_path))
    # break
    if line:
        url = (
            "https://api.aliyundrive.com/adrive/v3/share_link/get_share_by_anonymous?share_id="
            + line[1]
        )
    else:
        continue
    req = requests.post(url, json={"share_id": line[1]}).json()
    if "message" not in req:
        if len(line) == 4:
            item = {
                "mount_path": mount_path,
                "share_id": line[1],
                "parent_file_id": line[2],
                "share_pwd": line[3],
            }
            output_json.append(item)
            output_txt += f"{mount_path} {line[1]} {line[2]} {line[3]}\n"
        elif len(line) == 3:
            item = {
                "mount_path": mount_path,
                "share_id": line[1],
                "parent_file_id": line[2],
                "share_pwd": "wumima",
            }

            output_json.append(item)
            output_txt += f"{mount_path} {line[1]} {line[2]}\n"
        elif len(line) == 2:
            item = {
                "mount_path": mount_path,
                "share_id": line[1],
                "parent_file_id": "root",
                "share_pwd": "wumima",
            }
            output_json.append(item)
            output_txt += f"{mount_path} {line[1]}\n"
        if not os.path.exists(os.path.join(tempdir, mount_path)):
            os.makedirs(os.path.join(tempdir, mount_path))
        json1 = get_list_by_share(
            item["share_id"], item["parent_file_id"], item["share_pwd"]
        )
        with open(os.path.join(tempdir, mount_path, "index.json"), "w") as f:
            json.dump(json1, f)

        print(line[0])
    sleep(1)
# with open(outputtxtfname, "w", encoding="utf-8") as f:
#     f.write(output_txt)
# with open(outputjsonfname, "w", encoding="utf-8") as f:
#     json.dump(output_json, f)
