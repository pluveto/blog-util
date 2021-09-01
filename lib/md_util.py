import re

def remove_title(content):    
    '''
    此处会误伤 # 开头的代码
    建议使用 hugo 的 startLevel: 2 解决
    '''
    return re.sub(r'(---\n+)# .*\n?', r'\1', content)
    return re.sub(r'(?m)^# .*\n?', '', content)

def hide(content):
    return re.sub(r'<!--hide-->.*\n?', '', content)