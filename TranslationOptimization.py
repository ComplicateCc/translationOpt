# -*- coding: utf-8 -*-
from difflib import SequenceMatcher  #比较库
from tqdm import tqdm  #进度条library


#用于整理原数据
str_data = {}

#用于存放处理后的数据
data_map = {}

#结果数据
result_data = {}

#占位符替换
def get_different_with_placeholder(str1, str2, ratio=0.8, threshold=5):
    len_diff = abs(len(str1) - len(str2))
    if len_diff > threshold:
        return False, str1
    
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
    
def init_str_data():
    str_data = {}
    # 读取本地文件 TestFile.txt
    with open("TestFile.txt", "r", encoding="utf-8") as f:
        data = f.readlines()
    
    # 将文件内容转换为字典，并显示进度条
    for line in tqdm(data, desc="初始化文本数据"):
        line = line.strip()
        try:
            key, value = line.split("=", 1)  # 只分割一次，避免多余的 `=` 影响
        except ValueError:
            key = line
            value = line
        
        # 如果 value 已存在，则不添加
        if contains_value(str_data, value):
            continue
        else:
            str_data[key] = value
    
    return str_data

def contains_value(dictionary, value):
    return value in dictionary.values()

def main():
    #初始化数据
    str_data = init_str_data()

    # 处理数据
    for newData in tqdm(str_data.values(), desc="处理文本数据"):
        is_same = False
        for key in data_map.keys():
            is_same, result = get_different_with_placeholder(newData, key)
            if is_same:
                # 如果返回的模板为空，则直接添加到datas中
                if data_map[key]["template"] == "":
                    data_map[key]["template"] = result
                    data_map[key]["datas"].append(newData)
                else:
                    # 如果返回的模板相同，则直接添加到datas中
                    if data_map[key]["template"] == result:
                        data_map[key]["datas"].append(newData)
                    else:
                        data_map[key]["need_check"] = True
                        data_map[key]["datas"].append(newData)
                break
        # 如果没有找到相同的模板，则将newData插入到data_map中
        if not is_same:
            data_map[newData] = {
                "template": "",
                "datas": [newData],
                "need_check": False
            }
            
    # 输出结果 保存data_map中的数据存到txt文件中
    with open("result.txt", "w", encoding="utf-8") as f:
        for key in data_map.keys():
            if data_map[key]['need_check']:
                f.write(f"是否需要人工检查: {data_map[key]['need_check']}\n")
            if data_map[key]['template']:
                f.write(f"模板: {data_map[key]['template']}\n")
                f.write(f"数据: {data_map[key]['datas']}\n")
            else:
                f.write(f"{key}\n")
            f.write("\n")

if __name__ == "__main__":
    main()