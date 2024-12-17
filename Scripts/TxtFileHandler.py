# -*- coding: utf-8 -*-

import re
import csv

class DataStructure:
    def __init__(self, origin_string_data, clean_string_data, placeholder):
        self.origin_string_data = origin_string_data
        self.clean_string_data = clean_string_data
        self.placeholder = set(placeholder)

    def __repr__(self):
        return f"DataStructure(origin_string_data={self.origin_string_data}, clean_string_data={self.clean_string_data}, placeholder={self.placeholder})"

def contains_chinese(text):
    # Check if the text contains any Chinese characters
    return any('\u4e00' <= char <= '\u9fff' for char in text)

input_file_path = r'G:\Project\TranslationOptimization\Files\客户端独有INI\MagicChildType.txt'
output_csv_path = r'G:\Project\TranslationOptimization\Files\客户端独有INI\MagicChildType_new.csv'

seen_lines = set()
data_structures = []

with open(input_file_path, 'r', encoding='utf-8') as infile:
    for line in infile:
        elements = line.split()
        chinese_elements = [element for element in elements if contains_chinese(element)]
        if chinese_elements:
            chinese_line = ' '.join(chinese_elements)
            if chinese_line not in seen_lines:
                data_structure = DataStructure(origin_string_data=line.strip(), clean_string_data=chinese_line, placeholder="")
                data_structures.append(data_structure)
                seen_lines.add(chinese_line)

# Save to CSV
with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['origin_string_data', 'clean_string_data', 'placeholder']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for data in data_structures:
        writer.writerow({
            'origin_string_data': data.origin_string_data,
            'clean_string_data': data.clean_string_data,
            'placeholder': ','.join(data.placeholder)
        })