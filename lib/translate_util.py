import requests

import json
import re

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def ch_to_en(query):    
    if(is_ascii(query)):
        query = re.sub(r"^Chapter {0,1}(\d+)[ -]{0,1}", r"ch-\g<1>", query)
        return query
    
    query = re.sub(r"^第 {0,1}(\d+) {0,1}章", r"ch-\g<1>", query)
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    data = {
        "i": query,
        "from": "zh-CHS",
        "to": "en",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": "16081210430989",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "lan-select"
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        + ' AppleWebKit/537.36 (KHTML, like Gecko) Ch'
        + 'rome/90.0.4430.72 Safari/537.36 Edg/90.0.818.39'
    }
    response = requests.post(url, data=data, headers=headers)
    html = response.content.decode('utf-8')
    result = json.loads(html)['translateResult'][0][0]['tgt']
    return result
