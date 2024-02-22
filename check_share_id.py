#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import sleep
from sys import exit
import shutil
import requests
import re, json
import os

# content = ""
# subject = ""
# err=''
alishares = []
# 检查alishare_list分享的有效性
tempdir = os.path.join(os.path.dirname(__file__), "temp")
# os.makedirs(tempdir)
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
        if not os.path.exists(os.path.join(tempdir,mount_path)):
            os.makedirs(os.path.join(tempdir,mount_path))
        with open(os.path.join(tempdir, mount_path, "index.json"), "w") as f:
            json.dump(item, f)
        print(line[0].strip("/").replace("/", "|"))
    sleep(1)
# with open(outputtxtfname, "w", encoding="utf-8") as f:
#     f.write(output_txt)
# with open(outputjsonfname, "w", encoding="utf-8") as f:
#     json.dump(output_json, f)
