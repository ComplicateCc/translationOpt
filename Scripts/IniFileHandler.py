# -*- coding: utf-8 -*-

import os
import csv
import pandas as pd
from DataStructure import DataStructure
from DataCollection import clean_and_extract_text

# 每个文件提取的词
extracted_words = set()

def contains_chinese(text):
    # Check if the text contains any Chinese characters
    return any('\u4e00' <= char <= '\u9fff' for char in text)

def process_ini_file(file_path):
    data_structures = []
    with open(file_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            line = line.strip()
            if line.startswith('//') or line.startswith('；')or line.startswith(';'):
                continue
            if contains_chinese(line):
                clean_string_data = clean_and_extract_text(line, extracted_words)
                data_structure = DataStructure(origin_string_data=line, clean_string_data=clean_string_data, placeholder="")
                data_structures.append(data_structure)
    return data_structures

def process_directory(directory_path):
    all_data = {}
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.ini'):
                file_path = os.path.join(root, file)
                data_structures = process_ini_file(file_path)
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
                
def save_to_csv(all_data, output_excel_path):
    with pd.ExcelWriter(output_excel_path, engine='xlsxwriter') as writer:
        for file_name, data_structures in all_data.items():
            data = {
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
save_to_csv(all_data, output_excel_path)