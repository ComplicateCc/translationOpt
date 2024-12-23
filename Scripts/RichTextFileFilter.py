# -*- coding: utf-8 -*-

import os
import re
import shutil
import chardet
from tqdm import tqdm

directory_path = r'G:\Project\TranslationOptimization\Files\客户端独有INI'
new_directory_path = os.path.join(directory_path, 'NewFiles')

# 创建 NewFiles 文件夹，如果不存在
if not os.path.exists(new_directory_path):
    os.makedirs(new_directory_path)

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    return result['encoding']

def is_rich_text_file(file_path):
    encoding = detect_encoding(file_path)
    with open(file_path, 'r', encoding=encoding, errors='ignore') as file:
        for line in file:
            if re.search(r'<col.*?>', line) or \
               re.search(r'\[Antialias.*?\]', line) or \
               re.search(r'\[#\d+.*?\]', line) or \
               re.search(r'\[/0x.*?\]', line):
                return True
    return False

def copy_rich_text_files(directory_path, new_directory_path):
    all_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            all_files.append(os.path.join(root, file))

    for file_path in tqdm(all_files, desc="Processing files"):
        if is_rich_text_file(file_path):
            shutil.copy(file_path, new_directory_path)
            print(f"Copied: {file_path}")

# 遍历路径下的所有文件并复制富文本文件
copy_rich_text_files(directory_path, new_directory_path)