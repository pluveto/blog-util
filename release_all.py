"""
    release_all.py 是对 release 的封装，用于根据用户提供的配置文件批量、分目录进行 release 操作。
"""

import yaml
import os
from release import process_post
from lib import meta_util

def get_files(dir_name):
    _, _, filenames = next(os.walk(dir_name))
    ret = []
    for name in filenames:
        if not name.endswith(".md"):
            continue
        ret.append(os.path.join(dir_name, name))
    return ret

def main():
    """读取配置文件，并且加载文件列表，处理每一个文件
    """
    config_file_path  = "config.yaml"

    config = yaml.load(open(config_file_path, encoding="utf-8", mode="r"), Loader=yaml.SafeLoader)

    list_file_path = "file_list.yaml"

    file_list = yaml.load(open(list_file_path, encoding="utf-8", mode="r"), Loader=yaml.SafeLoader)

    ret_msgs = []

    for output_dir, files in file_list.items():
        #print(output_dir)
        
        if not os.path.isdir(output_dir):
            init_docs_dir(output_dir)

        for name in files:
            # print("name", name)
            if os.path.isdir(name):
                #print("Dir")
                files.extend(get_files(name))
                del name
                continue
            if not name.endswith(".md"):
                continue
            #print("\t" + name)
            dir_config = config.copy()
            dir_config['output_dir'] = output_dir
            ret_msg = process_post(name, dir_config)
            if(len(ret_msg) > 0):
                ret_msgs.append(ret_msg)
    
    for msg in ret_msgs:        
        print(msg)

def init_docs_dir(output_dir):
    os.mkdir(output_dir)
    docs_title = os.path.basename(output_dir)
    docs_meta_path = output_dir + "/_index.md"
    content = meta_util.insert_meta_str({'title': docs_title}, '')
    open(docs_meta_path, encoding="utf-8", mode="w").write(content)
    
if __name__ == "__main__":
    main()
