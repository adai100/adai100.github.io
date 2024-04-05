#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import sleep
from sys import exit
import shutil
import requests
import re, json
import os
from retry import retry


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
    ret = []
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
    for i in json2['items']:
        ret.append(i)

    while json2["next_marker"] != "":
        sleep(1)
        json1["marker"] = json2["next_marker"]
        json2 = requests.post(url, headers=headers, json=json1).json()
        if json2["items"]:
            for i in json2['items']:
                ret.append(i)

    return ret
# share_token = get_share_token("3eKuM6Nm8ac")
# j = get_list_by_share(
#     "3eKuM6Nm8ac", "65a25a761193d0222c96494f9cceacd10591628f", share_token
# )
# print(j)
z = {}
share_token = get_share_token("3eKuM6Nm8ac")
j = get_list_by_share(
    "3eKuM6Nm8ac", "65a25a761193d0222c96494f9cceacd10591628f", share_token
)
z["阿三劳动法就"] = j
with open("/dev/shm/t.json", "w", encoding="utf-8") as f:
    json.dump(z, f)

# req = requests.post(
#     url="https://v1.api.production.link3.cc:5678/api/no_auth/user",
#     headers={
#         "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
#         "Accept": "application/json, text/plain, */*",
#         "Accept-Language": "zh,zh-CN;q=0.8,en;q=0.5,en-US;q=0.3",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Content-Type": "application/json",
#         "Origin": "https://link3.cc",
#         "Connection": "keep-alive",
#         "Referer": "https://link3.cc/",
#         "Sec-Fetch-Dest": "empty",
#         "Sec-Fetch-Mode": "cors",
#         "Sec-Fetch-Site": "same-site",
#     },
#     json={"username": "alipan"},
# ).json()["data"]["links"]
# for i in json.loads(req):
#     if (
#         "icon_url" in i["typeValue"]
#         and i["typeValue"]["icon_url"]
#         == "user_create_images/module_urls/img.alicdn.com"
#     ):

#         share_id = i["typeValue"]["nav_url"].split("/")[4]
#         share_token = get_share_token(share_id)
#         parent_file_id = get_list_by_share(share_id, "root", share_token)[0]["file_id"]
#         print(i["typeValue"]["title"], " ", share_id, " ", parent_file_id)
#         sleep(1)
#     else:
#         continue


# alishares = []
# items=[]
# # 检查alishare_list分享的有效性

# fname = os.path.join(os.path.dirname(__file__), "alishare_list.txt")

# print(fname)
# with open(fname, "r") as f:
#     temp = f.readlines()

# for tmp in temp:
#     if tmp.strip():
#         alishares.append(tmp.strip())
# print(alishares)

# output_txt = ""
# output_json = []
# for row in alishares:
#     line = row.split()
#     mount_path = line[0].strip("/")
#     if line:
#         url = (
#             "https://api.aliyundrive.com/adrive/v3/share_link/get_share_by_anonymous?share_id="
#             + line[1]
#         )
#     else:
#         continue
#     req = requests.post(url, json={"share_id": line[1]}).json()
#     print(req)
#     if "message" not in req and req["file_infos"]:
#         if len(line) == 4:
#             item = {
#                 "mount_path": mount_path,
#                 "share_id": line[1],
#                 "parent_file_id": line[2],
#                 "share_pwd": line[3],
#             }
#             output_json.append(item)
#             output_txt += f"{mount_path} {line[1]} {line[2]} {line[3]}\n"
#         elif len(line) == 3:
#             item = {
#                 "mount_path": mount_path,
#                 "share_id": line[1],
#                 "parent_file_id": line[2],
#                 "share_pwd": "wumima",
#             }

#             output_json.append(item)
#             output_txt += f"{mount_path} {line[1]} {line[2]}\n"
#         elif len(line) == 2:
#             item = {
#                 "mount_path": mount_path,
#                 "share_id": line[1],
#                 "parent_file_id": "root",
#                 "share_pwd": "wumima",
#             }
#             output_json.append(item)
#             output_txt += f"{mount_path} {line[1]}\n"
#         if not os.path.exists(os.path.join(tempdir, mount_path)):
#             os.makedirs(os.path.join(tempdir, mount_path))
#         print(item)
#         json1 = get_list_by_share(
#             item["share_id"], item["parent_file_id"], item["share_pwd"]
#         )
#         with open(os.path.join(tempdir, mount_path, "index.json"), "w") as f:
#             json.dump(json1, f)

#         print(line[0])

#     sleep(2)
# with open(outputtxtfname, "w", encoding="utf-8") as f:
#     f.write(output_txt)
# with open(outputjsonfname, "w", encoding="utf-8") as f:
#     json.dump(output_json, f)
