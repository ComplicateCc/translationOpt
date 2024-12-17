# -*- coding: utf-8 -*-

import os
import csv
import re
import uuid
import pandas as pd
import DataStructure
from DataCollection import clean_and_extract_text

# 每个文件提取的词
extracted_words = set()

def contains_chinese(text):
    # Check if the text contains any Chinese characters
    return any('\u4e00' <= char <= '\u9fff' for char in text)

def check_if_line_is_invalid(line):
    return line.startswith('//') or line.startswith('；') or line.startswith(';')

def get_data_structure(ori_text, cur_text, file_name):
    ori_string_data = ori_text
    clean_string_data = clean_and_extract_text(cur_text, extracted_words)
    guid = str(uuid.uuid4())
    return DataStructure.DataStructure(origin_string_data=ori_string_data, guid=guid, clean_string_data=clean_string_data, placeholder=extracted_words, source_file=file_name)

def handle_space_split(line, file_name):
    elements = line.split()
    chinese_elements = [element for element in elements if contains_chinese(element)]
    if chinese_elements:
        data_structures = []
        for element in chinese_elements:
            data_structure = get_data_structure(line, element, file_name)
            data_structures.append(data_structure)
        return data_structures
    return None

def handle_single_line(line, file_name=""):
    # 创建一组 data_structure 对象
    data_structures = []
    
    if contains_chinese(line):
        #删除所有格式为 [=x=]的字符串 x为任意数字
        line_new = re.sub(r'\[=\d+=\]', '', line)
        #删除Link=x x为任意数字
        line_new = re.sub(r'Link=\d+', '', line_new)
        
        # isUnknownFormat = False
        
        #尝试以等号分割句子
        elements = line_new.split('=')
        if len(elements) == 2 :
            if not contains_chinese(elements[0]) and contains_chinese(elements[1]):
                # return elements[1]
                data_structure = get_data_structure(line, elements[1], file_name)
            else:
                # print(f"========Invalid line: {line}")
                # isUnknownFormat = True
                data_structure = get_data_structure(line, line, file_name)
        elif len(elements) > 2:
            # print(f"========multiple elements: {line}")
            # isUnknownFormat = True
            data_structure = get_data_structure(line, line, file_name)
        else:
            #尝试用空格划分句子
            elements = line_new.split()
            #提取包含中文信息的元素
            chinese_elements = [element for element in elements if contains_chinese(element)]
            if chinese_elements:
                # return ' '.join(chinese_elements)
                # 打印所有元素
                # print(f"========chinese_elements line: {line}")
                # 为所有元素创建data_structure对象
                for element in chinese_elements:
                    data_structure = get_data_structure(line, element, file_name)
                    data_structures.append(data_structure)
            else:
                # print(f"========no chinese_elements line: {line}")
                # isUnknownFormat = True
                data_structure = get_data_structure(line, line, file_name)
        # if isUnknownFormat:
        #     return False
        return data_structure
    return None

def process_ini_file(file_path):
    data_structures = []
    with open(file_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            line = line.strip()
            if check_if_line_is_invalid(line):
                continue
            if contains_chinese(line):
                clean_string_data = clean_and_extract_text(line, extracted_words)
                data_structure = DataStructure.DataStructure(origin_string_data=line, clean_string_data=clean_string_data, placeholder="")
                data_structures.append(data_structure)
    return data_structures


# 遍历单行 测试模板格式是否包含全情况
def process_ini_single_line(file_path):
    #DataStruture集合
    data_structures = []
    with open(file_path, "r", encoding="utf-8") as infile:
        file_name = os.path.basename(file_path)
        for line in infile:
            line = line.strip()
            if check_if_line_is_invalid(line):
                continue
            result = handle_single_line(line, file_name)
            if result:
                data_structures.append(result)
    return data_structures

def test_process_all_single_line(directory_path):
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                process_ini_single_line(file_path)


def process_directory(directory_path):
    all_data = {}
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.ini'):
                file_path = os.path.join(root, file)
                data_structures = process_ini_single_line(file_path)
                all_data[file] = data_structures
    return all_data

def save_to_csv_old(all_data, output_csv_path):
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['file_name', 'origin_string_data', 'clean_string_data', 'placeholder']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for file_name, data_structures in all_data.items():
            for data in data_structures:
                writer.writerow({
                    'file_name': file_name,
                    'origin_string_data': data.origin_string_data,
                    'clean_string_data': data.clean_string_data,
                    'placeholder': ','.join(data.placeholder)
                })

def save_to_excel(all_data, output_excel_path):
    with pd.ExcelWriter(output_excel_path, engine='xlsxwriter') as writer:
        for file_name, data_structures in all_data.items():
            data = {
                'guid': [ds.guid for ds in data_structures],
                'origin_string_data': [ds.origin_string_data for ds in data_structures],
                'clean_string_data': [ds.clean_string_data for ds in data_structures],
                'placeholder': [','.join(ds.placeholder) for ds in data_structures]
            }
            df = pd.DataFrame(data)
            df.to_excel(writer, sheet_name=file_name, index=False)


# Define the directory path and output CSV path
directory_path = r'G:\Project\TranslationOptimization\Files'
output_csv_path = r'G:\Project\TranslationOptimization\Files\all_ini_files.csv'
output_excel_path = r'G:\Project\TranslationOptimization\Files\all_ini_files.xlsx'

# Process the directory and save to CSV
all_data = process_directory(directory_path)
save_to_excel(all_data, output_excel_path)
# test_process_all_single_line(directory_path)
