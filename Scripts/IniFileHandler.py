# -*- coding: utf-8 -*-

import hashlib
import itertools
import json
import os
import csv
import re
import sqlite3
import uuid
import pandas as pd
import DataStructure
from DataCollection import clean_and_extract_text
from difflib import SequenceMatcher  #比较库
from tqdm import tqdm  #进度条library

from SQLDataBase import create_connection, create_table
from TranslationTemplateData import CleanStrData, TranslationTemplateData 

# 每个文件提取的词
extracted_words = set()

def contains_chinese(text):
    # Check if the text contains any Chinese characters
    return any('\u4e00' <= char <= '\u9fff' for char in text)

def check_if_line_is_invalid(line):
    return line.startswith('//') or line.startswith('；') or line.startswith(';')

def generate_guid(origin_string_data, clean_string_data, source_file):
    # 使用 origin_string_data, clean_string_data 和 source_file 生成唯一且一致的哈希值
    unique_string = origin_string_data + clean_string_data + source_file
    hash_object = hashlib.md5(unique_string.encode())
    return str(uuid.UUID(hash_object.hexdigest()))

def get_data_structure(ori_text, cur_text, file_name):
    ori_string_data = ori_text
    clean_string_data = clean_and_extract_text(cur_text, extracted_words)
    #打印extracted_words
    if extracted_words:
        print(extracted_words)
    guid = generate_guid(ori_string_data, clean_string_data, file_name)
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
            #如果 clean_string_data 不为空则添加到data_structures
            if data_structure.clean_string_data:
                data_structures.append(data_structure)
        #打印data_structures数量大于1的情况
        # if len(data_structures) > 1:
        #     print(f"========输出了多行待翻译的中文数据: {ori_line}")
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
template_datas = {}

#结果数据
result_data = {}

def extract_numbers(text):
    # 提取所有数字
    return re.findall(r'\d+', text)

def replace_numbers_with_placeholder(text, num_dict):
    # 将所有数字替换为占位符
    def replacer(match):
        num = match.group(0)
        return num_dict[num]
    
    return re.sub(r'\d+', replacer, text)

def get_different_with_placeholder(str1, str2, ratio=0.8, ignore_similar=False):
    # 提取字符串1和字符串2中的所有数字
    nums1 = extract_numbers(str1)
    nums2 = extract_numbers(str2)
    
    # 创建字典，将字符串1中的数字替换为从01开始的递增数字
    num_dict1 = {num: f'{i:02}' for i, num in enumerate(nums1, start=1)}
    # 创建字典，如果num_dict1中不存在，则将字符串2中的数字替换为从99开始的递减数字 添加到num_dict1中
    num_dict2 = {num: f'{99 - i:02}' for i, num in enumerate(nums2, start=1) if num not in num_dict1}
    
    # 整合两个字典
    num_dict1.update(num_dict2)
    
    # 替换数字为占位符
    str1_placeholder = replace_numbers_with_placeholder(str1, num_dict1)
    str2_placeholder = replace_numbers_with_placeholder(str2, num_dict1)
    
    if not ignore_similar:
        s = SequenceMatcher(None, str1_placeholder, str2_placeholder)
        if s.ratio() < ratio:
            return False, str1, [], []

    parts = []
    ori_parts1 = []
    ori_parts2 = []
    holder_index = 0

    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == 'equal':
            parts.append(str2_placeholder[j1:j2])
        else:
            placeholder = "{" + str(holder_index) + "}"
            holder_index += 1
            parts.append(placeholder)
            ori_parts1.append(str1_placeholder[i1:i2])
            ori_parts2.append(str2_placeholder[j1:j2])
    
    # 将占位符替换回原始数字
    result = "".join(parts)
    for num, placeholder in num_dict1.items():
        result = result.replace(placeholder, num)
    for num, placeholder in num_dict2.items():
        result = result.replace(placeholder, num)
        
    # 移除ori_parts1 ori_parts2中的纯数字
    ori_parts1 = [part for part in ori_parts1 if not part.isdigit()]
    ori_parts2 = [part for part in ori_parts2 if not part.isdigit()]
    
    # print(result)
    # print(ori_parts1)
    # print(ori_parts2)    
    
    return True, result, ori_parts1, ori_parts2

def contains_value(dictionary, value):
    return value in dictionary.values()

# 计算字符串相似度
def is_similar(a, b, ratiothresh=0.8):
    return SequenceMatcher(None, a, b).ratio() > ratiothresh

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
                    # "methods": set()
                }
            translation_data[data.clean_string_data]["guids"].add(data.guid)
            translation_data[data.clean_string_data]["source_files"].add(data.source_file)
            # translation_data[data.clean_string_data]["methods"].add("None")
    return translation_data

def init_translation_datas_by_keylength(translation_data):
    translation_data_by_numbers = {}
    key_length_list = []
    # 按照 translation_data key 的字数进行分类，将整个数据结构添加到 translation_data_by_numbers 中
    for key, value in translation_data.items():
        key_length = len(key)
        if key_length not in translation_data_by_numbers:
            translation_data_by_numbers[key_length] = {}
            key_length_list.append(key_length)
        translation_data_by_numbers[key_length][key] = value
    return translation_data_by_numbers, key_length_list

def create_data_structure(conn, data_structures):
    sql_check = ''' SELECT 1 FROM data_structures WHERE guid = ? '''
    sql_insert = ''' INSERT INTO data_structures(origin_string_data, guid, clean_string_data, placeholder, source_file)
                     VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    
    # Filter out duplicates
    filtered_data_structures = []
    for data in tqdm(data_structures, desc="查询数据库"):
        cur.execute(sql_check, (data[1],))  # Check if guid exists
        if not cur.fetchone():
            filtered_data_structures.append(data)
    
    # Batch insert all data structures
    cur.executemany(sql_insert, filtered_data_structures)
    conn.commit()

def save_to_sql(all_data):
    database = r"original_data.db"

    # create a database connection
    conn = sqlite3.connect(database)
    with conn:
        create_table_sql = """ CREATE TABLE IF NOT EXISTS data_structures (
                                    id integer PRIMARY KEY,
                                    origin_string_data text NOT NULL,
                                    guid text NOT NULL,
                                    clean_string_data text,
                                    placeholder text,
                                    source_file text
                                ); """
        create_table(conn, create_table_sql)

        data_structures = []
        for file_name, data_list in tqdm(all_data.items(), desc="Processing files"):
            for data in data_list:
                data_structure = (data.origin_string_data, data.guid, data.clean_string_data, ','.join(data.placeholder), data.source_file)
                data_structures.append(data_structure)

        # Batch insert all data structures
        create_data_structure(conn, data_structures)
    conn.close()
    
def hanlde_translationTemplateDatas(all_data):
    translation_data = init_translation_datas(all_data)
    translation_data_by_numbers = init_translation_datas_by_keylength(translation_data)
    data_pairs = translation_data.items()
    
    # 处理数据
    for data_pair_key, data_pair_value in tqdm(data_pairs, desc="处理文本数据"):
        length = len(data_pair_key)
        is_similar = False
        # 遍历 translation_data_by_numbers 长度为 length +- length_threshold 的数据
        for i in range(length - length_threshold, length + length_threshold + 1):
            if i in translation_data_by_numbers:
                for key in translation_data_by_numbers[i].keys():
                    # 完全相同则跳过
                    if key == data_pair_key:
                        continue
                                        
                    is_similar, result, placeholder1, placeholder2 = get_different_with_placeholder(data_pair_key, key)
                    if is_similar:
                        # 如果 template_datas 没有 key 则添加 key
                        if key not in template_datas:
                            clean_str_datas = []
                            # clean_str_datas 清洗后的字符串数据的集合
                            #     每个集合元素
                            #     clean_str_data 清洗后的字符串数据
                            #     guids 对应的唯一标识
                            # 添加clean_str_data  guid 
                            clean_str_data1 = data_pair_key
                            guids1 = data_pair_value["guids"]
                            clean_str_datas.append(CleanStrData(clean_str_data1, guids1))
                            
                            clean_str_data2 = key
                            guids2 = translation_data_by_numbers[i][key].get("guids", set())
                            # 添加clean_str_data1 guids1作为key value数据 添加到clean_str_datas中
                            clean_str_datas.append(CleanStrData(clean_str_data2, guids2))
                            
                            
                            placeholders = {}
                            # placeholders 占位符集合
                            #     每个集合元素
                            #     placeholder 占位符
                            #     guids 对应的唯一标识
                            # 添加placeholder  guid
                            # 将placeholder1 placeholder2中的内容和guids 添加到placeholders中，如果不存在placeholder key
                            for placeholder in placeholder1:
                                if placeholder not in placeholders:
                                    placeholders[placeholder] = set()
                                placeholders[placeholder].update(guids1)
                            for placeholder in placeholder2:
                                if placeholder not in placeholders:
                                    placeholders[placeholder] = set()
                                placeholders[placeholder].update(guids2)
                            
                            template_data = TranslationTemplateData(result, clean_str_datas, placeholders)
                            template_datas[key] = template_data
                        else:
                            # 如果返回的模板为空，则直接添加到 datas 中
                            if template_datas[key].template == "":
                                template_datas[key].template = result
                            elif template_datas[key].template != result:
                                template_datas[key].need_check = True
                            
                            template_datas[key].clean_str_datas.extend(clean_str_datas)
                            for placeholder in placeholders:
                                if placeholder not in template_datas[key].placeholders:
                                    template_datas[key].placeholders[placeholder] = set()
                                template_datas[key].placeholders[placeholder].update(placeholders[placeholder])
        # 将template_datas 存储到 txt文件中
        with open("result_1219_old.txt", "w", encoding="utf-8") as f:
            for key in template_datas.keys():
                if template_datas[key].need_check:
                    f.write(f"是否需要人工检查: {template_datas[key].need_check}\n")
                if template_datas[key].template:
                    f.write(f"模板: {template_datas[key].template}\n")
                    f.write(f"数据: {template_datas[key].clean_str_datas}\n")
                    f.write(f"占位符: {template_datas[key].placeholders}\n")
            # else:
                #不打印没有模板的数据
                # f.write(f"{key}\n")
            # f.write("\n")                        

import difflib
from tqdm import tqdm

def find_similar_groups(data, threshold=0.8):
    similar_groups = []
    checked_strings = set()  # 存储已比较过的字符串

    # 遍历长度区间
    for length in tqdm(range(min(data.keys()), max(data.keys()) + 1), desc="相似度查询中"):
        if length not in data:
            continue
        
        current_group = []  # 当前长度下的字符串组
        current_group.extend(data[length])
        
        # 处理长度插值在5以内的字符串
        for diff in range(1, 6):
            if length + diff in data:
                current_group.extend(data[length + diff])
            if length - diff in data:
                current_group.extend(data[length - diff])
                
        # 去除重复字符串
        current_group = list(set(current_group))

        # 对当前组的字符串进行两两比较
        for i in range(len(current_group)):
            str1 = current_group[i]
            if str1 in checked_strings:
                continue
            new_group = [str1]
            for j in range(i + 1, len(current_group)):
                str2 = current_group[j]
                if difflib.SequenceMatcher(None, str1, str2).ratio() >= threshold:
                    new_group.append(str2)
            if len(new_group) > 1:  # 只保存包含多个字符串的组
                similar_groups.append(set(new_group))
            checked_strings.update(new_group)  # 更新已比较的字符串

    return similar_groups

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, CleanStrData):
            return {
                'clean_str_data': obj.clean_str_data,
                'guids': list(obj.guids)
            }
        if isinstance(obj, TranslationTemplateData):
            return {
                'template': obj.template,
                'clean_str_datas': [self.default(data) for data in obj.clean_str_datas],
                'placeholders': list(obj.placeholders)
            }
        return json.JSONEncoder.default(self, obj)

def hanlde_translationTemplateDatas_new(all_data):
    translation_data = init_translation_datas(all_data)
    translation_data_by_numbers, key_length_list = init_translation_datas_by_keylength(translation_data)
    
    translation_data_pair_list = {}

    # 对key_length_list进行排序
    key_length_list.sort()

    # 将 translation_data_by_numbers 转换为 find_similar_groups 所需的格式
    data = {}
    for length in key_length_list:
        data[length] = list(translation_data_by_numbers[length].keys())

    # 找到相似的组
    similar_groups = find_similar_groups(data)

    # 处理相似的组
    for group in similar_groups:
        group = list(group)
        key1 = group[0]
        if key1 not in translation_data_pair_list:
            translation_data_pair_list[key1] = []
            translation_data_pair_list[key1].append(CleanStrData(key1, translation_data_by_numbers[len(key1)][key1].get("guids", set())))
        for key2 in group[1:]:
            translation_data_pair_list[key1].append(CleanStrData(key2, translation_data_by_numbers[len(key2)][key2].get("guids", set())))

    template_datas = {}

    # 处理占位符数据
    for key in translation_data_pair_list.keys():
        placeholders = {}
        # 用get_different_with_placeholder 比较translation_data_pair_list[key]前两个元素
        is_similar, result, placeholder1, placeholder2 = get_different_with_placeholder(translation_data_pair_list[key][0].clean_str_data, translation_data_pair_list[key][1].clean_str_data)
        if result not in template_datas:
            clean_str_datas = translation_data_pair_list[key]
            
            template_data = TranslationTemplateData(result, clean_str_datas, placeholders)
            template_datas[result] = template_data

    # 用Json的格式保存结果
    with open("result_1219_222.txt", "w", encoding="utf-8") as f:
        json.dump(template_datas, f, cls=CustomEncoder, ensure_ascii=False, indent=4)
                      

# def handle_data(all_data):
    #遍历all_data 以clean_string_data为目标字符串

# Define the directory path and output CSV path
directory_path = r'G:\Project\TranslationOptimization\Files'
output_csv_path = r'G:\Project\TranslationOptimization\Files\all_ini_files.csv'
output_excel_path = r'G:\Project\TranslationOptimization\Files\all_ini_files.xlsx'

length_threshold = 5

def main():
    all_data = process_directory(directory_path)
    save_to_excel(all_data, output_excel_path)
    save_to_sql(all_data)
    # hanlde_translationTemplateDatas(all_data)
    hanlde_translationTemplateDatas_new(all_data)
    # get_different_with_placeholder('1111012,3,106,0,300000,1350,0,10,100,"1048185,1","1092174,129,1","增加伤害法宝[*-13,112*]3[*-4,-1*][~SQCZ_BBBSIcon~]",65,3783,0,12,1,"1037231|1037232|1037233|1111010|1111110|1111210|1110010|1110110|1110210||1048400|1111011|1111111|1111211|1092174|1092015",3,"3276', 
    #                                '1111012,3,107,0,360000,1450,0,10,100,"1048185,1","1092174,189,1","增加伤害法宝[*-13,112*]3[*-4,-1*][~SQCZ_BBBSIcon~]",65,3783,0,12,1,"1037231|1037232|1037233|1111010|1111110|1111210|1110010|1110110|1110210||1048400|1111011|1111111|1111211|1092174|1092015",3,"3276')
    return
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