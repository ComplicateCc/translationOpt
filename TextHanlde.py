# -*- coding: utf-8 -*-

def remove_consecutive_blank_lines(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 去除连续的换行符
    cleaned_lines = []
    previous_line_blank = False
    for line in lines:
        if line.strip() == "":
            if not previous_line_blank:
                cleaned_lines.append(line)
            previous_line_blank = True
        else:
            cleaned_lines.append(line)
            previous_line_blank = False

    # 将处理后的内容写回文件
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(cleaned_lines)

if __name__ == "__main__":
    file_path = "result_backup_new.txt"
    remove_consecutive_blank_lines(file_path)