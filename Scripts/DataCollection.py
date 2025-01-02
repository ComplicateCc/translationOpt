# -*- coding: utf-8 -*-
import os
import pandas as pd
import re

def contains_chinese(text):
    """检查字符串中是否包含中文字符"""
    return re.search(r'[\u4e00-\u9fff]', str(text)) is not None

def clean_and_extract_text(text, extracted_words):
    """删除富文本格式和换行符等符号，并提取富文本包住的词"""
    # text = re.sub(r'\[.*?\]', '[]', text)
    # text = re.sub(r'<.*?>', '<>', text)
    
    # 删除开头  数字= 如：21845004=
    # text = re.sub(r'\d+=', '', text)
    
    # 删除所有 <col XXXXXX> 之类的字符串
    # text = re.sub(r'<col.*?>', '', text)
    # 删除所有 [Antialias 开头 ] 结尾的字符串
    # text = re.sub(r'\[Antialias.*?\]', '', text)
    # 删除所有 [#数字 开头 ] 结尾的字符串
    # text = re.sub(r'\[#\d+.*?\]', '', text)
    # 删除所有 [/0x 开头 ] 结尾的字符串
    # text = re.sub(r'\[/0x.*?\]', '', text)
    # 删除所有换行符 \n 和制表符 \t
    # text = text.replace(r'\n', '')
    # text = text.replace(r'\t', '')
    
    # 提取富文本包住的词
    # matches = re.findall(r'\[\/\$\$\$.*?\$\$\$\](.*?)\[\/\$\$\$.*?\$\$\$\]', text)
    # for match in matches:
    #     cleaned_match = match.strip()
    #     if cleaned_match and cleaned_match not in extracted_words:
    #         extracted_words.add(cleaned_match)
    # 删除所有富文本格式、换行符和 [=$$$=] 等符号
    # text = re.sub(r'\[\/\$\$\$.*?\$\$\$\]', '', text)
    # text = re.sub(r'\[\/\$\$\$.*?\]', '', text)  # 删除类似 [/$$$xFFFFFF] 的标签
    # text = re.sub(r'\[=\$\$\$=\]', '', text)  # 删除 [=$$$=] 符号
    # text = re.sub(r'\n+', ' ', text)  # 删除所有换行符并替换为一个空格
    
    # 删除 <> [] {}
    # text = re.sub(r"<.*?>|\[.*?\]|\{.*?\}", "", text)
    
    # 删除结尾的 "#数字" 格式的字符串
    # text = re.sub(r'#\d+$', '', text)
    
    # 正则匹配删除 数字=如：21845004=
    # text = re.sub(r'\d+=', '', text)
    
    
    # 正则匹配删除 <interval=30> 格式的字符串
    # text = re.sub(r'<interval=\d+>', '', text)
    
    # 正则匹配删除 {#0xXXXXX#}  XXXXX为任意长度字符
    # text = re.sub(r'{#0x.*?#}', '', text)
    
    # 删除结尾为  多个|d的字符串 如|75|215|1
    # text = re.sub(r'\|\d+(?:\|\d+)*$', '', text)
    
    # 删除开头为 多个[*d,d*]的字符串 如[*1,-5*][*21,-5*]
    # text = re.sub(r'^\[\*\d+,-?\d+\*\](?:\[\*\d+,-?\d+\*\])*', '', text)
    
    # 删除开头和结尾的中英文标点符号
    # text = re.sub(r'^[^\w\s]+|[^\w\s]+$', '', text)
    
    return text.strip()  # 删除开头和结尾的空格

def process_xlsx_files(directory):
    resource_data_dir = os.path.join(directory, "resource_data")
    os.makedirs(resource_data_dir, exist_ok=True)  # 创建 resource_data 文件夹
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".xlsx"):
                # 每个文件提取的词
                extracted_words = set()
                
                file_path = os.path.join(root, filename)
                # 读取整个 .xlsx 文件
                df = pd.read_excel(file_path, skiprows=1)
                print(f"Processing file: {filename}")
                print("Columns:", df.columns.tolist())  # 打印列名
                # 检查是否有至少两列
                if df.shape[1] < 2:
                    print(f"File {filename} does not have a second column.")
                    continue
                # 选择第二列
                second_col = df.iloc[:, 1]
                # 删除所有富文本格式和换行符，并删除所有开头的空格和不包含中文字符的行
                second_col = second_col.astype(str).apply(lambda x: clean_and_extract_text(x, extracted_words))
                second_col = second_col[second_col.apply(contains_chinese)]
                # 将输出的结果保存成同名的 .txt 文件
                output_file = os.path.join(resource_data_dir, os.path.splitext(filename)[0] + ".txt")
                with open(output_file, "w", encoding="utf-8") as f:
                    for line in second_col:
                        f.write(line + "\n")
                    for word in extracted_words:
                        f.write(word + "\n")

def remove_duplicate_lines(directory):
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".txt"):
                file_path = os.path.join(root, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                # 删除所有完全相同的元素
                unique_lines = list(set(lines))
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(unique_lines)

if __name__ == "__main__":
    # target_directory = r"G:\Project\translationOpt\Files"
    # process_xlsx_files(target_directory)
    # resource_data_directory = os.path.join(target_directory, "resource_data")
    # remove_duplicate_lines(resource_data_directory)
    str = r'2111245=<col FF$$$>主幻兽类型要求[ABC]：<col FFFFFF>\n紫霞仙子/青霞仙子\n<col FF$$$>副幻兽类型要求：<col FFFFFF>\n任意全能宠（限$$$年前推出的全能宠，不包括紫霞仙子/青霞仙子本身）'
    print(clean_and_extract_text(str, set()))