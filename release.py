#!/usr/bin/env python3
"""
    功能：自动生成 Markdown 文件的各种信息，最后复制到目录。
    使用方法 python3 release.py file1.md file2.md ...
"""
import os
import argparse
import re
import datetime
from time import gmtime, strftime
from lib import meta_util, escape_util, slug_util, translate_util, pangu_markdown, md_util
from shutil import copyfile


def main():

    print("当前时区为：%s" % strftime("%z", gmtime()))

    # default_config = {
    #     'output_dir': "C:/doc/Projects/cv/content/zh/posts",
    #     'escape': True,
    #     'authors': ['Pluveto']
    # }

    options = load_options()

    for filename in options['file']:
        process_post(filename, options)

    exit(0)


def load_options():
    example_text = '''示例:\n
    python release.py -o "./test" -a Pluveto -e 测试文件.md'''

    parser = argparse.ArgumentParser(
        description='将 typora 风格的 markdown 文件转换为 hugo 支持的风格',
        epilog=example_text)
    parser.add_argument('-o', '--output', dest="output_dir", help='输出文件夹')
    parser.add_argument('-a', '--authors', dest="authors",
                        required=True, help='作者', nargs="+")
    parser.add_argument(
        '-e', '--escape', action=argparse.BooleanOptionalAction, help='数学转义')
    parser.add_argument('file', nargs='+')
    args = parser.parse_args()
    if not os.path.isdir(args.output_dir):
        print("无效的目录：%s." % args.output_dir)
        exit(1)
    return vars(args)


def process_post(doc_path, config):
    """处理单篇博文

    Args:
        doc_path (string): 路径
        config (dict): 程序配置信息
    Return:
        返回一个消息，用于显示给用户
    """
    raw_content = open(doc_path, 'r', encoding='utf-8').read()
    filename = os.path.splitext(os.path.basename(doc_path))[0]  # 无扩展名

    if(filename.startswith('_')):
        # _ 开头的文件直接复制
        out_path = os.path.join(config['output_dir'], os.path.basename(doc_path))
        copyfile(doc_path, out_path)
        return ""

    old_meta = meta_util.read_meta(doc_path)
    user_meta = meta_util.fill_meta(old_meta)

    slug = None
    if("slug" in user_meta.keys()):
        # 首选使用用户提供的 slug
        slug = user_meta["slug"]

    gen_meta = auto_meta(filename, doc_path, config['authors'], slug)

    meta = meta_util.merge_meta(gen_meta, user_meta)

    if(config['escape']):
        content = escape_util.escape_math(raw_content)
    # content = md_util.remove_title(content)
    content = md_util.hide(content)
    out_path = os.path.join(config['output_dir'], meta['slug'] + ".md")

    content = meta_util.strip_meta(content)
    content = meta_util.insert_meta_str(meta, content)
    content = pangu_markdown.spacing_md(content)
    # 输出到静态博客的源博文目录
    open(out_path, 'w', encoding='utf-8').write(content)
    # print("\tok: " + out_path)
    writeback(doc_path, old_meta, meta, raw_content)
    if(("](C:\\Users") in raw_content):
        return "文件可能含有未上传的图片：" + os.path.abspath(doc_path)
    return ""


def writeback(doc_path, old_meta, meta, raw_content):
    """写回到文档于用户手中的位置

    Args:
        doc_path (dict): 写回路径
        old_meta (dict): 旧有元数据
        meta (新元数据): [description]
        raw_content (string): 写回的内容，不含头部 meta
    """
    new_meta = meta.copy()
    if 'lastmod' in new_meta.keys():
        del new_meta['lastmod']
    # 避免多余的 IO
    if(old_meta != new_meta):
        print("\twritten: " + doc_path)
        content = meta_util.insert_meta_str(
            new_meta, meta_util.strip_meta(raw_content))
        open(doc_path, 'w', encoding='utf-8').write(content)
    else:
        # print("\tignored.")
        return


def auto_meta(filename, path, authors, slug=None):
    """生成 meta

    Args:
        filename (str): 文件名（无扩展名）
        path (str): 文件路径（用于获取创建时间等）
        authors (list): 作者列表

    Returns:
        dict: meta 字典
    """
    if(slug == None):
        print('translating...')
        slug = slug_util.slugify(translate_util.ch_to_en(filename))

    dict = {
        'title': filename,
        'toc': True,
        'authors': authors,
        'date': datetime.datetime.fromtimestamp(os.path.getctime(path)).astimezone().isoformat(),
        'lastmod': datetime.datetime.fromtimestamp(os.path.getmtime(path)).astimezone().isoformat(),
        'draft': False,
        'slug': slug
    }
    m = re.search(r"^ch-(\d+)", slug)
    if m:
        dict['weight'] = int(m.group(1))
    return dict


if __name__ == "__main__":
    main()
