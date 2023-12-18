#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
m3us=''
m3u='#EXTINF:-1 tvg-id="%s" tvg-name="%s"  group-title="%s",%s\n%s\n'

page=re.sub('[\n]{1,}','\n',requests.get('https://jihulab.com/wekh/tvshow/-/raw/main/APTV.txt').text)
titles=re.findall('(.*,#genre#)',page)
txt=re.split(".*#genre#",page)
for i,title in enumerate(titles):
    t=title.split(',')[0]
    lines=txt[i+1].splitlines()[1:]
    for line in lines:
        l=line.split(',')
        m3us+=m3u % (l[0],l[0],t,l[0],l[1])

print('#EXTM3U\n'+m3us)