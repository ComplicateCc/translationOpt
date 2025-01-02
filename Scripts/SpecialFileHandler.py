# -*- coding: utf-8 -*-

# 用于处理特殊格式文件的类
# 这样就不会在提取文件时添加很多额外恶心的逻辑代码   不需要全局考虑特殊情况

import os
import re

class SpecialFileHandler:
    # def __init__(self, directory):
    #     self.directory = directory
    #     self.seen_lines = set()
    def __init__(self, directory, new_directory):
        self.directory = directory
        self.new_directory = new_directory
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

    # def process_directory(self):
    #     for root, _, files in os.walk(self.directory):
    #         for file in files:
    #             file_path = os.path.join(root, file)
    #             self.process_file(file_path)
                
    # def handle_file_taskevent(self, file_path):
    #     new_lines = []
    #     with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
    #         for line in file:
    #             if not self.contains_chinese(line):
    #                 continue
    #             if line.startswith(';'):
    #                 continue
    #             if line in self.seen_lines:
    #                 continue
                
    #             value = line
                
    #             elemnts = line.split('=')
    #             if len(elemnts) == 2:
    #                 value = elemnts[1].strip()
    #                 # 正则匹配 删除 [*] *为任意长度的任意字符re.sub(r'\[.*?\]', '', text)
    #                 value = re.sub(r'\[.*?\]', '', value)
    #                 # 尝试删除"："后面的内容
    #                 value = re.sub(r':.*', '', value)                    
    #             else:
    #                 #打印错误行
    #                 print(f"Error line: {line}")
                
    #             # 如果非重复 则加入
    #             new_lines.append(value)

    #     # 保存数据到新文件
    #     with open(new_taskevent_directory, 'w', encoding='utf-8', errors='ignore') as file:
    #         file.writelines(new_lines)

    def handle_file_taskevent(self, file_path):
        new_lines = []
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                if not self.contains_chinese(line):
                    continue
                if line.startswith(';'):
                    continue
                if line in self.seen_lines:
                    continue
                
                value = line.strip()
                
                elements = line.split('=')
                if len(elements) == 2:
                    value = elements[1].strip()
                    # 正则匹配 删除 [*] *为任意长度的任意字符
                    value = re.sub(r'\[.*?\]', '', value)
                else:
                    # 打印错误行
                    print(f"Error line: {line}")
                
                # 尝试删除：后面的所有内容
                value = re.sub(r'：.*', '', value)
                
                # 如果非重复 则加入
                new_lines.append(value + '\n')

        # 删除new_lines中的重复行
        new_lines = list(set(new_lines))

        # 保存数据到新文件
        # new_file_path = os.path.join(self.new_directory, os.path.basename(file_path))
        with open(new_taskevent_directory, 'w', encoding='utf-8', errors='ignore') as file:
            file.writelines(new_lines)

    # def process_directory(self):
    #     for root, _, files in os.walk(self.directory):
    #         for file in files:
    #             file_path = os.path.join(root, file)
    #             self.handle_file_taskevent(file_path)

files_directory = r'G:\Project\TranslationOptimization\Files\客户端独有INI\generator'
taskevent_directory = r'G:\Project\TranslationOptimization\Files\客户端独有INI\TaskEvent.ini'
new_taskevent_directory = r'G:\Project\TranslationOptimization\Files\客户端独有INI\NewTaskEvent.ini'
old_gem_directory = r'G:\Project\TranslationOptimization\Files\客户端独有INI\NewGemTip.ini'
new_gem_directory = r'G:\Project\TranslationOptimization\Files\客户端独有INI\NewGem.ini'
# handler = SpecialFileHandler(files_directory)
# handler.process_directory()
# handler = SpecialFileHandler(taskevent_directory, new_taskevent_directory)
# handler.handle_file_taskevent(taskevent_directory)


# ori_str = r'[]50%[]概率失败，销毁[]1[]个材料器灵或销毁[]2[]个材料器灵并获得[]1[]个[]【1级器灵】[]；\n·[]50%[]概率成功，随机获得[]【4级器灵】、 【5级器灵】、【8级器灵】[]中的一种。\n\n·游戏中的“概率”均是在[]大数据样本（大量用户）统计下的数值，并非单个玩家每次获得的概率[]（例如在概率为50%的情况下，并非玩家参与2次，就会有1次成功）。'
# 将ori_str 里面所有 [x] 替换为 []
# new_str = re.sub(r'\[.*?\]', '[]', ori_str)
# print(new_str)



        
def extract_chinese(text):
    # 提取中文部分
    chinese_text = re.findall(r'[\u4e00-\u9fff]+', text)
    return ''.join(chinese_text) if chinese_text else None

def split_and_extract_chinese(input_str):
    parts = input_str.split('\\n')
    result = []
    for part in parts:
        chinese_text = extract_chinese(part)
        if chinese_text:
            result.append(chinese_text)
    return result

def GemFileHandler(file_path, new_gem_directory):
    new_lines = set()  # 使用集合来去重
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            # 提取中文部分
            chinese_texts = split_and_extract_chinese(line)
            for chinese_text in chinese_texts:
                new_lines.add(chinese_text + '\n')
    if not os.path.exists(new_gem_directory):
        os.makedirs(new_gem_directory)
    with open(new_gem_directory, 'w', encoding='utf-8', errors='ignore') as file:
        file.writelines(new_lines)


# GemFileHandler(old_gem_directory, new_gem_directory)

NewGemStoneTip_path = r'G:\Project\TranslationOptimization\Files\客户端独有INI\NewGemStoneTip.ini'

def extract_data_from_file(file_path, target_key):
    data_list = []
    with open(file_path, 'r', encoding='utf - 8') as f:
        content = f.read()
        blocks = content.split('\n\n')
        for block in blocks:
            if block.strip():
                lines = block.split('\n')
                current_data = {}
                for line in lines:
                    if '=' in line:
                        key, value = line.split('=', 1)
                        current_data[key.strip()] = value.strip()
                if target_key in current_data:
                    data_list.append(current_data[target_key])
    return data_list


# # 提取所有Title1的数据
# title1_data = extract_data_from_file(NewGemStoneTip_path, 'Title1')
# print("Title1的数据:", title1_data)
# # 提取所有Desc1的数据
# desc1_data = extract_data_from_file(NewGemStoneTip_path, 'Desc1')
# print("Desc1的数据:", desc1_data)

import pandas as pd

import pandas as pd

# 读取Excel文件
file_path = r'G:\Project\TranslationOptimization\Files\Test\all_ini_files.xlsx'
new_file_path = r'G:\Project\TranslationOptimization\Files\Test\all_ini_files_processed.xlsx'

import pandas as pd
import os

def process_excel(file_path, new_file_path):
    try:
        # 读取Excel文件，sheet_name=None表示读取所有页签
        excel_data = pd.read_excel(file_path, sheet_name=None)
        writer = pd.ExcelWriter(new_file_path, engine='openpyxl')
        for sheet_name, df in excel_data.items():
            if df.shape[1] >= 2:  # 确保有至少两列
                second_col_name = df.columns[1]
                # 清空除第二列外的其他列
                for col in df.columns:
                    if col != second_col_name:
                        df[col] = ''
                # 将第二列数据移动到第一列
                df['guid'] = df[second_col_name]
                df = df.drop(columns=[second_col_name])
                # 将处理后的数据写回到Excel文件的对应页签
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        writer.close()
        print(f"处理完成，已保存为 '{new_file_path}'")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

if __name__ == "__main__":
    file_path = r'G:\Project\TranslationOptimization\Files\Test\all_ini_files.xlsx'
    new_file_path = r'G:\Project\TranslationOptimization\Files\Test\all_ini_files_processed.xlsx'
    process_excel(file_path, new_file_path)

