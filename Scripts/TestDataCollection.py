import os
import pandas as pd
import re
import IniFileHandler


def should_skip_line(line):
    """
    判断是否应跳过某一行数据
    :param line: 待判断的行数据
    :return: True 表示应跳过，False 表示不应跳过
    """
    line = line.strip()
    if not line:
        return True
    if line.startswith('//') or line.startswith('；') or line.startswith(';'):
        return True
    if not re.search('[\u4e00-\u9fff]', line):
        return True
    return False


def read_txt_file(file_path, result_set):
    """
    读取txt文件内容并处理
    :param file_path: txt文件路径
    :param result_set: 存储结果的集合
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f.readlines():
            if not should_skip_line(line) and line not in result_set:
                result_set.add(line)


def read_xlsx_file(file_path, result_set):
    """
    读取xlsx文件内容并处理
    :param file_path: xlsx文件路径
    :param result_set: 存储结果的集合
    """
    try:
        df = pd.read_excel(file_path)
        for col in df.columns:
            for value in df[col].dropna():
                value = str(value).strip()
                if not should_skip_line(value) and value not in result_set:
                    result_set.add(value)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")


def read_ini_file(file_path, result_set):
    """
    读取ini文件内容并处理
    :param file_path: ini文件路径
    :param result_set: 存储结果的集合
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f.readlines():
            if not should_skip_line(line) and line not in result_set:
                result_set.add(line)


def read_files(directory):
    """
    读取指定目录下所有txt、xlsx、ini文件内容
    :param directory: 目标目录
    :return: 处理后的结果集合
    """
    result_set = set()
    file_extensions = ('.txt', '.xlsx', '.ini')
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(file_extensions):
                file_path = os.path.join(root, file)
                if file.endswith('.txt'):
                    read_txt_file(file_path, result_set)
                elif file.endswith('.xlsx'):
                    read_xlsx_file(file_path, result_set)
                elif file.endswith('.ini'):
                    read_ini_file(file_path, result_set)
    return result_set


def save_to_excel(data_set, output_path):
    """
    将集合数据保存到Excel文件
    :param data_set: 包含数据的集合
    :param output_path: 输出Excel文件路径
    """
    df = pd.DataFrame(list(data_set), columns=['待翻译文本'])
    df.to_excel(output_path, index=False)


if __name__ == "__main__":
    target_directory = r'G:\Project\TranslationOptimization\OriginalFiles'
    output_excel_path =r'G:\Project\TranslationOptimization\output222.xlsx'
    data = read_files(target_directory)
    save_to_excel(data, output_excel_path)
    
    # result_set = set()
    # read_xlsx_file(r'D:\Program Files (x86)\Netdragon\imData\im\100127@nd\RecvFile\本地化翻译需求沟通_4954399830900250\目前\目前\itemtype-名称.xlsx', result_set)
    # print(result_set)
