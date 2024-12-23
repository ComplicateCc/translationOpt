# -*- coding: utf-8 -*-

# 用于处理特殊格式文件的类
# 这样就不会在提取文件时添加很多额外恶心的逻辑代码   不需要全局考虑特殊情况

import os
import re

class SpecialFileHandler:
    def __init__(self, directory):
        self.directory = directory
        self.seen_lines = set()

    def contains_chinese(self, text):
        # 检查文本是否包含中文字符
        return any('\u4e00' <= char <= '\u9fff' for char in text)

    def process_file(self, file_path):
        new_lines = []
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                if not self.contains_chinese(line):
                    continue
                if line in self.seen_lines:
                    continue
                self.seen_lines.add(line)
                new_lines.append(line)

        # 保存数据到源文件
        with open(file_path, 'w', encoding='utf-8', errors='ignore') as file:
            file.writelines(new_lines)

    def process_directory(self):
        for root, _, files in os.walk(self.directory):
            for file in files:
                file_path = os.path.join(root, file)
                self.process_file(file_path)

# 示例用法
files_directory = r'G:\Project\TranslationOptimization\Files\客户端独有INI\generator'
handler = SpecialFileHandler(files_directory)
handler.process_directory()