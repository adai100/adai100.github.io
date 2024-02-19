#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import sleep
from sys import exit
import yaml
import requests
import re,json
import os

# content = ""
# subject = ""
# err=''
alishares=[]
# 检查alishare_list分享的有效性
fname=os.path.join(os.path.dirname(__file__), 'alishare_list.txt')
outputfname=os.path.join(os.path.dirname(__file__), 'alisharelist.txt')
print(fname)
with open(fname,'r') as f:
    temp=f.readlines()

for tmp in temp:
    if tmp.strip():
        alishares.append(tmp.strip())

output_txt=''
for row in alishares:
    line = row.split()
    if line:
        url = (
            "https://api.aliyundrive.com/adrive/v3/share_link/get_share_by_anonymous?share_id="
            + line[1]
        )
    else:
        continue
    req = requests.post(url, json={"share_id": line[1]}).json()
    if "message" not in req:
        if len(line) == 3:
            output_txt += f"{line[0]} {line[1]} {line[2]}\n"
        else:
            output_txt += f"{line[0]} {line[1]}\n"
        print(output_txt)
    sleep(1)
with open(outputfname, "w", encoding="utf-8") as f:
    f.write(output_txt)
