#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from time import sleep
import os

items = {}
outputjsonfname = os.path.join(os.path.dirname(__file__), "alisharelist.json")


def get_share_token(share_id, share_pwd=""):
    if share_pwd == "wumima":
        share_pwd = ""
    share_token = requests.post(
        url="https://api.aliyundrive.com/v2/share_link/get_share_token",
        headers={
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
            "x-canary": "client=web,app=share,version=v2.3.1",
            "x-device-id": "2nZcHZsF5AoBASQIgnCfKv7S",
            "Content-Type": "application/json",
        },
        json={"share_id": share_id, "share_pwd": share_pwd},
    ).json()["share_token"]
    return share_token


def get_list_by_share(share_id, parent_file_id, share_token, share_pwd=""):
    if share_pwd == "wumima":
        share_pwd = ""

    url = "https://api.aliyundrive.com/adrive/v2/file/list_by_share"
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        "x-canary": "client=web,app=share,version=v2.3.1",
        "x-device-id": "2nZcHZsF5AoBASQIgnCfKv7S",
        "x-share-token": share_token,
    }
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
    json2 = requests.post(url, headers=headers, json=json1).json()
    # print(json2)
    return json2["items"]


req = requests.post(
    url="https://v1.api.production.link3.cc:5678/api/no_auth/user",
    headers={"Content-Type": "application/json"},
    json={"username": "alipan"},
).json()["data"]["links"]
for i in json.loads(req):
    if (
        "icon_url" in i["typeValue"]
        and i["typeValue"]["icon_url"]
        == "user_create_images/module_urls/img.alicdn.com"
    ):

        print(i["typeValue"]["title"])
        share_id = i["typeValue"]["nav_url"].split("/")[4]
        share_token = get_share_token(share_id)
        parent_file_id = get_list_by_share(share_id, "root", share_token)[0]["file_id"]

        items[i["typeValue"]["title"]] = get_list_by_share(
            share_id, parent_file_id, share_token
        )
        sleep(1)

alishares = []
fname = os.path.join(os.path.dirname(__file__), "alishare_list.txt")
with open(fname, "r") as f:
    temp = f.readlines()
for tmp in temp:
    if tmp.strip():
        alishares.append(tmp.strip())


for row in alishares:
    line = row.split()
    mount_path = line[0].strip("/")
    if line:
        url = (
            "https://api.aliyundrive.com/adrive/v3/share_link/get_share_by_anonymous?share_id="
            + line[1]
        )
    else:
        continue
    req = requests.post(url, json={"share_id": line[1]}).json()
    print(req)
    if "message" not in req and req["file_infos"]:
        share_token = get_share_token(line[1])
        items[line[0].strip("/").replace('/','_')] = get_list_by_share(line[1], line[2], share_token)
    sleep(1)
    
with open(outputjsonfname, "w", encoding="utf-8") as f:
    json.dump(items, f)
