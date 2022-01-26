"""
    功能：读取 Markdown 文件的 meta 信息
"""

import os
import sys
import yaml
import datetime
from dateutil import parser
import copy


def read_meta(path):
    """读取 Markdown 元数据

    Args:
        path (str): 文件路径

    Returns:
        dict: 元数据
    """
    with open(path, 'r', encoding='utf-8') as file:
        status = 0  # 0 for init, 1 for start, 2 for end
        builder = []
        while True:
            line = file.readline()
            if len(line) == 0:
                break
            if len(line.strip()) == 0:
                continue
            if status == 0 and not line.strip().startswith("---"):
                break;
            if line.strip() == "---":
                status += 1
                continue
            if(status == 0):
                continue
            if(status == 1):
                builder.append(line)
                continue
            if(status == 2):
                break
        yaml_str = ''.join(builder)
        dict = yaml.load(yaml_str, Loader=yaml.SafeLoader)
        return dict


def insert_meta_str(meta, content):
    meta_str = yaml.dump(meta, allow_unicode=True)
    return "---\n%s---\n%s" % (meta_str, content)

def fill_meta(meta):
    """补全 meta 中的信息

    Args:
        meta (dict): meta dict
    """
    # print(meta)
    if(meta == None or meta == ""):
        meta = {}
    new_meta = copy.deepcopy(meta)
    if "date" in new_meta.keys():
        new_meta["date"] = parser.parse(new_meta["date"]).astimezone().isoformat()
    if "lastmod" in new_meta.keys():
        new_meta["lastmod"] = parser.parse(new_meta["date"]).astimezone().isoformat()
    return new_meta    

def strip_meta(content):
    """移除文档中的 meta 部分

    Args:
        content (str): 完整的 md 文档
    """
    status = 0 # stauts = 1 代表处于 meta 区域
    builder = []
    reading_body = False
    for line in content.split('\n'):
        if reading_body:
            builder.append(line)
            continue
        if line.strip() == "---":
            status += 1

        if status == 2:
            status = 3
            reading_body = True
            continue
        if status == 0 or status > 2:
            builder.append(line)
            continue
        if status == 1:
            continue
    md_str = '\n'.join(builder)
    return md_str

def merge_meta(gen_meta, user_meta):    
    return {**gen_meta, **user_meta}