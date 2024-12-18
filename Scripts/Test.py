import re
from collections import OrderedDict

def extract_chinese_and_remove_duplicates(file_path):
    chinese_texts = OrderedDict()
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        # 用于分割每行数据的正则表达式，保留引号内的逗号
        split_pattern = re.compile(r'(?:[^,"]|"(?:\\.|[^"])*")+')
        # 匹配中文的正则表达式，可匹配包含中文的任意字符串
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]+.*[\u4e00-\u9fff]+')
        for line in lines:
            # 按保留引号内逗号的方式分割行数据
            columns = split_pattern.findall(line)
            for column in columns:
                match = re.search(chinese_pattern, column)
                if match:
                    text = match.group()
                    # 移除富文本格式 [/0xXXXXX]
                    text = re.sub(r'\[/0x.*?\]', '', text)
                    # 去除换行符和空格
                    text = text.replace('\n', '').replace(' ', '')
                    chinese_texts[text] = None
    return list(chinese_texts.keys())

file_path = 'G:\Project\TranslationOptimization\Files\客户端独有INI\generator\cq_artifact_affix_type.txt'
result = extract_chinese_and_remove_duplicates(file_path)
for text in result:
    print(text)