# -*- coding: utf-8 -*-


def handle_data():
    # 读取本地文件 result_backup.txt
    with open("result_backup.txt", "r", encoding="utf-8") as f:
        data = f.readlines()
    
    # 筛选以“数据”开头的数据
    extracted_data = []
    for line in data:
        line = line.strip()
        if line.startswith("数据:"):
            # 提取出数据部分
            data_str = line[len("数据:"):].strip()
            # 将字符串转换为列表
            data_list = eval(data_str)
            # 将列表中的每个元素添加到提取的数据中
            extracted_data.extend(data_list)
            #以换行符分隔
            extracted_data.append("\n")
    
    # 将数据保存到新文件中
    with open("result_backup_new.txt", "w", encoding="utf-8") as f:
        for line in extracted_data:
            f.write(line + "\n")

if __name__ == "__main__":
    handle_data()
