# -*- coding: utf-8 -*-

import re

def contains_chinese(text):
    # 检查文本是否包含中文字符
    return any('\u4e00' <= char <= '\u9fff' for char in text)

def clean_file(file_path):
    new_lines = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            # 删除每行开头的'"'  '“'  '”'字符
            line = line.lstrip('"').lstrip('“').lstrip('”')
            # 如果不包含中文则删除整行
            if not contains_chinese(line):
                continue
            new_lines.append(line)
    
    # 保存数据到原文件
    with open(file_path, 'w', encoding='utf-8', errors='ignore') as file:
        file.writelines(new_lines)

# 示例用法
file_path = r'G:\Project\TranslationOptimization\Test\Test.ini'
clean_file(file_path)