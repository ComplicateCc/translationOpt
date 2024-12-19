import difflib
from collections import defaultdict
import re

# 示例字符串字典，按照字符串长度分组
translation_data_by_numbers = {
    3: ['cat', 'bat', 'sat'],
    4: ['ball', 'call', 'mall', 'tall'],
    5: ['apple', 'maple', 'grape', 'caper'],
    6: ['banana', 'cabana', 'bandana'],
    7: ['elephant', 'relevant', 'levant'],
}

def find_similar_groups(data, threshold=0.8):
    similar_groups = []
    checked_strings = set()  # 存储已比较过的字符串

    # 遍历长度区间
    for length in range(min(data.keys()), max(data.keys()) + 1):
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

# # 获取相似字符串组
# similar_groups = find_similar_groups(translation_data_by_numbers)

# # 打印结果
# for group in similar_groups:
#     print(group)

def remove_punctuation_at_beginning_and_end(text):
    # 定义中英文标点符号的正则表达式模式
    punctuation_pattern = r'^[^\w\s]+|[^\w\s]+$'
    return re.sub(punctuation_pattern, '', text)


# 示例用法
text = "!@#。这是一段测试文本。,.,"
new_text = remove_punctuation_at_beginning_and_end(text)
print(new_text)