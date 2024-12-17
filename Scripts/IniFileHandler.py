# -*- coding: utf-8 -*-

import os
import csv
import re
import uuid
import pandas as pd
import DataStructure
from DataCollection import clean_and_extract_text
from difflib import SequenceMatcher  #比较库
from tqdm import tqdm  #进度条library

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
    #打印extracted_words
    if extracted_words:
        print(extracted_words)
    guid = str(uuid.uuid1())
    return DataStructure.DataStructure(origin_string_data=ori_string_data, guid=guid, clean_string_data=clean_string_data, placeholder=extracted_words, source_file=file_name)

def handle_space_split(ori_line, line, file_name):
    #尝试用空格划分句子
    elements = line.split()
    #提取包含中文信息的元素
    chinese_elements = [element for element in elements if contains_chinese(element)]
    if chinese_elements:
        data_structures = []
        for element in chinese_elements:
            data_structure = get_data_structure(ori_line, element, file_name)
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
                data_structures = handle_space_split(line, elements[1], file_name)
            else:
                data_structures.append(get_data_structure(line, line_new, file_name))
        elif len(elements) > 2:
            # print(f"========multiple elements: {line}")
            # isUnknownFormat = True
            data_structures.append(get_data_structure(line, line_new, file_name))
        else:
            data_structures = handle_space_split(line, line_new, file_name)
        return data_structures
    return None

# def process_ini_file(file_path):
#     data_structures = []
#     with open(file_path, 'r', encoding='utf-8') as infile:
#         for line in infile:
#             line = line.strip()
#             if check_if_line_is_invalid(line):
#                 continue
#             if contains_chinese(line):
#                 clean_string_data = clean_and_extract_text(line, extracted_words)
#                 data_structure = DataStructure.DataStructure(origin_string_data=line, clean_string_data=clean_string_data, placeholder="")
#                 data_structures.append(data_structure)
#     return data_structures


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
                #遍历result集合 添加到data_structures
                for ds in result:
                    data_structures.append(ds)
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
            if not data_structures:
                print(f"Warning: No data structures found for file {file_name}. Skipping.")
                continue

            guids = []
            origin_string_data = []
            clean_string_data = []
            placeholders = []

            for ds in data_structures:
                if hasattr(ds, 'guid'):
                    guids.append(ds.guid)
                else:
                    print(f"Error: DataStructure object in file {ds} is missing 'guid' attribute.")
                    guids.append('')  # Append an empty string or handle as needed

                origin_string_data.append(ds.origin_string_data)
                clean_string_data.append(ds.clean_string_data)
                placeholders.append(','.join(ds.placeholder))

            data = {
                'guid': guids,
                'origin_string_data': origin_string_data,
                'clean_string_data': clean_string_data,
                'placeholder': placeholders
            }

            df = pd.DataFrame(data)
            df.to_excel(writer, sheet_name=file_name, index=False)

#用于整理原数据
str_data = {}

#用于存放处理后的数据
data_map = {}

#结果数据
result_data = {}

#占位符替换
def get_different_with_placeholder(str1, str2, ratio=0.8, threshold=5):
    # len_diff = abs(len(str1) - len(str2))
    # if len_diff > threshold:
    #     return False, str1
    
    s = SequenceMatcher(None, str1, str2)
    if s.ratio() < ratio:
        return False, str1
    
    parts = []
    last_j = 0
    holder_index = 0
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == 'equal':
            parts.append(str2[j1:j2])
        else:
            placeholder = "{" + str(holder_index) + "}"
            holder_index += 1
            parts.append(placeholder)
    return True,"".join(parts)

def contains_value(dictionary, value):
    return value in dictionary.values()

# 初始化translation_data 字典型
# translation_str 翻译数据 key
# guids 标识符集合 value    
def init_translation_datas(all_data):
    translation_data = {}
    for file_name, data_structures in all_data.items():
        for data in data_structures:
            if data.clean_string_data not in translation_data:
                translation_data[data.clean_string_data] = {
                    "guids": set(),
                    "source_files": set()
                }
            translation_data[data.clean_string_data]["guids"].add(data.guid)
            translation_data[data.clean_string_data]["source_files"].add(data.source_file)
    return translation_data

def init_translation_datas_by_numbers(translation_data):
    translation_data_by_numbers = {}
    # 按照 translation_data key 的字数进行分类，将整个数据结构添加到 translation_data_by_numbers 中
    for key, value in translation_data.items():
        key_length = len(key)
        if key_length not in translation_data_by_numbers:
            translation_data_by_numbers[key_length] = {}
        translation_data_by_numbers[key_length][key] = value
    return translation_data_by_numbers

# def handle_data(all_data):
    #遍历all_data 以clean_string_data为目标字符串

# Define the directory path and output CSV path
directory_path = r'G:\Project\TranslationOptimization\Files'
output_csv_path = r'G:\Project\TranslationOptimization\Files\all_ini_files.csv'
output_excel_path = r'G:\Project\TranslationOptimization\Files\all_ini_files.xlsx'

length_threshold = 5

def main():
    # Process the directory and save to CSV
    all_data = process_directory(directory_path)
    save_to_excel(all_data, output_excel_path)
    translation_data = init_translation_datas(all_data)
    translation_data_by_numbers = init_translation_datas_by_numbers(translation_data)
    str_data = translation_data.keys()
    
    # 处理数据
    for newData in tqdm(str_data, desc="处理文本数据"):
        length = len(newData)
        is_similar = False
        # 遍历 translation_data_by_numbers 长度为 length +- length_threshold 的数据
        for i in range(length - length_threshold, length + length_threshold + 1):
            if i in translation_data_by_numbers:
                for key in translation_data_by_numbers[i].keys():
                    is_similar, result = get_different_with_placeholder(newData, key)
                    if is_similar:
                        # 如果 data_map 没有 key 则添加 key
                        if key not in data_map:
                            data_map[key] = {
                                "template": result,
                                "datas": [newData],
                                "need_check": False,
                                "source_files": set(translation_data_by_numbers[i][key].get("source_files", set()))
                            }
                        else:
                            # 如果返回的模板为空，则直接添加到 datas 中
                            if data_map[key]["template"] == "":
                                data_map[key]["template"] = result
                            elif data_map[key]["template"] != result:
                                data_map[key]["need_check"] = True
        
                            data_map[key]["datas"].append(newData)
                            data_map[key]["source_files"].update(translation_data_by_numbers[i][key].get("source_files", set()))
                        break
        
        # 如果没有找到相同的模板，则将 newData 插入到 data_map 中
        if not is_similar:
            data_map[newData] = {
                "template": "",
                "datas": [newData],
                "need_check": False,
                "source_files": set()
            }
        
        # 输出结果 保存 data_map 中的数据存到 txt 文件中
        with open("result.txt", "w", encoding="utf-8") as f:
            for key in data_map.keys():
                if data_map[key]['need_check']:
                    f.write(f"是否需要人工检查: {data_map[key]['need_check']}\n")
                if data_map[key]['template']:
                    f.write(f"模板: {data_map[key]['template']}\n")
                    f.write(f"数据: {data_map[key]['datas']}\n")
                    #如果source_files数量大于一则打印
                    if len(data_map[key]['source_files']) > 1:
                        f.write(f"文件名: {data_map[key]['source_files']}\n")
            # else:
                #不打印没有模板的数据
                # f.write(f"{key}\n")
            # f.write("\n")

if __name__ == "__main__":
    main()